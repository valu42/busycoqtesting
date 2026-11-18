// Exact periodic transduction for line 17 with packed, file-backed words.
// Build with -O3 -std=c++17 -fopenmp -mssse3 and link with GMP.
#include "line17_pulse.hpp"
#include <array>
#include <gmpxx.h>
#include <iostream>
#include <vector>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <memory>
#include <unistd.h>
#include <sys/mman.h>
#include <fcntl.h>
#ifdef __SSSE3__
#include <tmmintrin.h>
#endif

namespace tiled {
using StateMap = std::array<uint8_t,16>;
struct Tables {
    std::vector<StateMap> maps;
    std::vector<std::array<Packet,6>> chunks;
    Tables(): maps(65536),chunks(65536) {
        for (unsigned w=0;w<65536;++w) {
            maps[w].fill(invalid);
            for (unsigned s=0;s<6;++s) {
                auto p=Packet::compile(s,w,16);
                maps[w][s]=p.state;
                chunks[w][s]=p;
            }
        }
    }
};

// Bits are packed least-significant first. Large words live in an unlinked
// temporary file in the working directory. Only written pages need disk space.
struct Bits {
    Count size=0, capacity=0;
    std::vector<Count> small;
    Count* addr=nullptr;
    int fd=-1;
    explicit Bits(Count bound) {
        capacity=(bound+63)/64+2;
        if (capacity <= 8192) {
            small.assign(capacity,0);
            addr=small.data();
        } else {
            char pattern[]="line17-tiles-XXXXXX";
            fd=mkstemp(pattern);
            if (fd<0) throw std::runtime_error("cannot create temporary word");
            if (unlink(pattern) != 0) {
                close(fd);
                throw std::runtime_error("cannot unlink temporary word");
            }
            if (ftruncate(fd, capacity * sizeof(Count)) != 0) {
                close(fd);
                throw std::runtime_error("cannot size temporary word");
            }
            void* p = mmap(nullptr, capacity * sizeof(Count), PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
            if (p == MAP_FAILED) {
                close(fd);
                throw std::runtime_error("cannot map temporary word");
            }
            addr=static_cast<Count*>(p);
            madvise(p,capacity*sizeof(Count),MADV_SEQUENTIAL);
        }
    }
    ~Bits() {
        if (fd >= 0) {
            munmap(addr, capacity * sizeof(Count));
            close(fd);
        }
    }
    Bits(const Bits&) = delete;
    Bits& operator=(const Bits&) = delete;
    void append(const Count* source, Count n) {
        if (!n) return;
        if ((size+n+63)/64+1>capacity) throw std::runtime_error("output exceeded two slots per input");
        Count* to=addr+size/64;
        unsigned offset=size%64;
        size_t words=(n+63)/64;
        if (!offset) memcpy(to,source,words*sizeof(Count));
        else {
            to[0]|=source[0]<<offset;
            for (size_t i=1;i<words;++i) to[i]=(source[i-1]>>(64-offset))|(source[i]<<offset);
            if (offset+n>64*words) to[words]=source[words-1]>>(64-offset);
        }
        size+=n;
    }
};
using Shared=std::shared_ptr<Bits>;
using Segments=std::vector<Shared>;
Count length(const Segments& segments) {
    Count size = 0;
    for (const auto& part : segments) size += part->size;
    return size;
}
void append(Segments& segments, const Shared& part) {
    if (part && part->size) segments.push_back(part);
}
struct Result { Shared out; Count calls=0,interior=0; unsigned end=0; };
constexpr unsigned tile=65536;
struct Slice {
    StateMap map{};
    std::array<Count,2*tile/64+2> out{};
    Count n=0,calls=0,interior=0;
    unsigned start=0, end=0;
};
// Compose the six possible starting states over this tile. State 6 is an
// absorbing conflict. Composing maps in order is associative, so tiles can
// build their maps independently before their actual entry states are known.
void map_slice(Slice& s,const Count* src,unsigned n,const Tables& t) {
#ifdef __SSSE3__
    __m128i m=_mm_setr_epi8(0,1,2,3,4,5,6,6,6,6,6,6,6,6,6,6);
    for (unsigned i=0;i<n/16;++i) {
        unsigned w=(src[i/4]>>(16*(i%4)))&65535;
        m=_mm_shuffle_epi8(_mm_loadu_si128(reinterpret_cast<const __m128i*>(t.maps[w].data())),m);
    }
    _mm_storeu_si128(reinterpret_cast<__m128i*>(s.map.data()),m);
#else
    s.map = {0,1,2,3,4,5,6};
    for (unsigned i = 0; i < n/16; ++i) {
        unsigned w = (src[i/4] >> (16*(i%4))) & 65535;
        for (unsigned q = 0; q < 6; ++q) s.map[q] = t.maps[w][s.map[q]];
    }
#endif
    if (unsigned tail=n%16) {
        unsigned w=unsigned(src[(n-tail)/64]>>((n-tail)%64))&65535;
        for (unsigned q=0;q<6;++q) if (s.map[q]<6)s.map[q]=Packet::compile(s.map[q],w,tail).state;
    }
}
void emit_slice(Slice& s,const Count* src,unsigned n,const Tables& t) {
    unsigned state=s.start,offset=0,done=0;
    Count acc=0,calls=0,interior=0;
    auto emit=[&](const Packet& p){
        if (p.state == invalid) throw std::runtime_error("overlapping marked bursts");
        state=p.state;
        calls+=p.calls; interior+=p.interior;
        Count data=p.bits;
        acc|=data<<offset;
        offset+=p.width;
        if (offset>=64) {
            s.out[done++]=acc; offset-=64;
            acc=offset ? data>>(p.width-offset):0;
        }
    };
    for (unsigned i=0;i<n/16;++i) {
        unsigned w=(src[i/4]>>(16*(i%4)))&65535;
        emit(t.chunks[w][state]);
    }
    if (unsigned tail=n%16) {
        unsigned w=unsigned(src[(n-tail)/64]>>((n-tail)%64))&65535;
        emit(Packet::compile(state,w,tail));
    }
    s.out[done]=acc;
    s.n=done*64+offset;
    s.calls=calls; s.interior=interior; s.end=state;
}
// Resolve the tile boundaries, then emit in parallel and join in tape order.
// The two lanes of work share the compiled pulse table with the scalar worker.
Result transform(const Segments& input,unsigned state,const Tables& t,Count bits_limit,int workers) {
    Count len=length(input);
    if (len>bits_limit) throw std::runtime_error("word budget exceeded at "+std::to_string(len)+" input bits");
    Result res;
    res.end=state;
    if (!len) return res;
    res.out=std::make_shared<Bits>(2*len);
    int group=std::min<Count>(16u*workers,(len+tile-1)/tile);
    std::vector<Slice> scratch(group);
    for (auto& part:input) {
        for (Count base=0;base<part->size;) {
            int count=std::min<Count>(group,(part->size-base+tile-1)/tile);
            auto width = [&](int j) {
                return unsigned(std::min<Count>(tile, part->size - base - Count(j)*tile));
            };
            auto source = [&](int j) {
                return part->addr + base/64 + Count(j)*(tile/64);
            };
            #pragma omp parallel for if (count>=workers && workers>1) num_threads(workers) schedule(static)
            for (int j=0;j<count;++j) map_slice(scratch[j],source(j),width(j),t);
            for (int j=0;j<count;++j) {
                scratch[j].start=res.end;
                res.end=scratch[j].map[res.end];
                if (res.end==invalid) throw std::runtime_error("overlapping marked bursts");
            }
            #pragma omp parallel for if (count>=workers && workers>1) num_threads(workers) schedule(static)
            for (int j=0;j<count;++j) emit_slice(scratch[j],source(j),width(j),t);
            for (int j=0;j<count;++j) {
                res.out->append(scratch[j].out.data(),scratch[j].n);
                res.calls+=scratch[j].calls; res.interior+=scratch[j].interior;
            }
            base+=Count(count)*tile;
        }
    }
    return res;
}
struct Totals { mpz_class calls=0, interior=0; };
struct Ray {
    Segments prefix, period, suffix;
    mpz_class copies = 0;
    Count period_marks = 0;
};

// When the stopping sweep is chosen later, this record evaluates an entire
// digit exactly at every compatible boundary (origin + k * root_period).
struct Cycle {
    unsigned transient = 0, cycle = 0, state = 0;
    Count prefix_slots = 0, period_slots = 0;
    mpz_class prefix_calls = 0, prefix_inner = 0;
    mpz_class period_calls = 0, period_inner = 0;
    mpz_class origin, root_period;
};

// Equal digit states at a copy boundary give the same word, raw cost and
// final state. Keep the preperiod and remainder in their original order.
Ray lift(unsigned& state,const Ray& in,Totals& totals,const Tables& t,Count limit,int workers,Cycle* summary=nullptr){
    Ray out;
    auto prefix=transform(in.prefix,state,t,limit,workers);
    append(out.prefix,prefix.out);
    state=prefix.end;
    totals.calls+=prefix.calls; totals.interior+=prefix.interior;
    std::array<int,6> first; first.fill(-1);
    std::vector<Result> parts;
    while (parts.size()<in.copies && first[state]<0) {
        first[state]=parts.size();
        parts.push_back(transform(in.period,state,t,limit,workers));
        state=parts.back().end;
    }
    bool cycle=parts.size()<in.copies;
    size_t begin=cycle ? first[state] : parts.size();
    auto add=[&](const Result& p,Segments& target,const mpz_class& copies) {
        append(target,p.out);
        totals.calls+=copies*p.calls; totals.interior+=copies*p.interior;
    };
    for (size_t j=0;j<begin;++j) add(parts[j],out.prefix,1);
    if (cycle) {
        if (summary) {
            summary->transient = begin;
            summary->cycle = parts.size() - begin;
            summary->state = state;
            summary->prefix_slots = length(out.prefix);
            summary->prefix_calls = totals.calls;
            summary->prefix_inner = totals.interior;
            for (size_t j = begin; j < parts.size(); ++j) {
                summary->period_slots += parts[j].out ? parts[j].out->size : 0;
                summary->period_calls += parts[j].calls;
                summary->period_inner += parts[j].interior;
            }
        }
        mpz_class left=in.copies-begin;
        auto rem=mpz_fdiv_q_ui(out.copies.get_mpz_t(),left.get_mpz_t(),parts.size()-begin);
        for (size_t j = begin; j < parts.size(); ++j) {
            const auto& part = parts[j];
            add(part, out.period, out.copies);
            // Each generated mark adds two internal moves beyond two per emitted slot.
            out.period_marks += part.interior/2 - (part.out ? part.out->size : 0);
        }
        for (size_t j=begin;j<begin+rem;++j) {
            add(parts[j],out.suffix,1); state=parts[j].end;
        }
        if (!length(out.period))out.copies=0;
    }
    auto suffix=transform(in.suffix,state,t,limit,workers);
    append(out.suffix,suffix.out);
    totals.calls+=suffix.calls; totals.interior+=suffix.interior; state=suffix.end;
    return out;
}

void write_row(unsigned state, const mpz_class& slots, const mpz_class& calls, const mpz_class& inner, std::ostream& out=std::cout) {
    out << state/2 << ' ' << state%2 << ' ' << slots << ' ' << calls << ' ' << inner << '\n';
}

// Stream a finite suffix once its period would need too much disk. Each digit
// consumes its tiles chronologically, including partial bursts across tiles.
struct TailDigit {
    unsigned state;
    Count slots = 0, calls = 0, interior = 0;
    Slice buffer;
};

void feed_tail(std::vector<TailDigit>& digits, size_t i, const Count* bits,
               Count n, const Tables& tables) {
    if (!n || i == digits.size()) return;
    auto& digit = digits[i];
    while (n) {
        unsigned width = std::min<Count>(tile, n);
        auto& out = digit.buffer;
        out.start = digit.state;
        emit_slice(out, bits, width, tables);
        digit.state = out.end;
        if (digit.slots > UINT64_MAX - out.n || digit.calls > UINT64_MAX - out.calls ||
            digit.interior > UINT64_MAX - out.interior)
            throw std::overflow_error("finite suffix counter overflow");
        digit.slots += out.n;
        digit.calls += out.calls;
        digit.interior += out.interior;
        feed_tail(digits, i+1, out.out.data(), out.n, tables);
        n -= width;
        if (n) bits += width/64;
    }
}

void finish_aligned_tail(const Ray& in, const std::vector<unsigned>& states, size_t cut,
                         const Tables& tables) {
    std::vector<TailDigit> digits(states.size() - cut);
    for (size_t i = cut; i < states.size(); ++i) digits[i-cut].state = states[i];
    auto feed = [&](const Segments& words) {
        for (const auto& part : words) feed_tail(digits, 0, part->addr, part->size, tables);
    };
    feed(in.prefix);
    if (length(in.period)) {
        if (!mpz_fits_ulong_p(in.copies.get_mpz_t()))
            throw std::overflow_error("too many finite copies in tiled suffix");
        auto copies = in.copies.get_ui();
        for (Count k = 0; k < copies; ++k) {
            feed(in.period);
            if (std::getenv("LINE17_TILES_TRACE") && copies <= 100)
                std::cerr << "streamed period " << k+1 << " of " << copies << '\n';
        }
    }
    feed(in.suffix);
    for (const auto& digit : digits)
        write_row(digit.state, digit.slots, digit.calls, digit.interior);
}

// The source phase at each chosen boundary contains a complete number of every
// earlier period. This makes an arbitrary-precision sweep index inexpensive to
// reconstruct even when its decimal representation was unknown during the lift.
void write_aligned_rows(const std::vector<Cycle>& history, const mpz_class& epochs, std::ostream& out=std::cout) {
    out << "epochs " << epochs << '\n';
    for (const auto& c : history) {
        mpz_class delta = epochs - c.origin;
        if (delta < 0 || delta % c.root_period != 0)
            throw std::logic_error("chosen sweep does not align with a preceding cut");
        mpz_class k = delta / c.root_period;
        write_row(c.state, c.prefix_slots + k*c.period_slots,
                  c.prefix_calls + k*c.period_calls, c.prefix_inner + k*c.period_inner,out);
    }
    out.flush();
}
}
#include "line17_coded.hpp"
#include "line17_ternary.hpp"
#include "line17_virtual.hpp"
#include "line17_lift.hpp"
int main(int argc,char** argv) try {
    using namespace tiled;
    if(argc>1 && std::string(argv[1])=="lift")return virtual_lift(argc-1,argv+1);
    if(argc>1 && std::string(argv[1])=="index")return virtual_index(argc-1,argv+1);
    if(argc>1 && std::string(argv[1])=="probe")return virtual_probe(argc-1,argv+1);
    if(argc>1 && std::string(argv[1])=="virtual")return virtual_advance(argc-1,argv+1);
    bool exporting = argc == 6 && std::string(argv[4]) == "export-coded";
    bool coded_mode = exporting || (argc == 5 && std::string(argv[4]) == "coded");
    bool aligned = coded_mode || (argc == 5 && std::string(argv[4]) == "at-least");
    if (argc != 4 && !aligned)
        throw std::runtime_error("usage: line17-tiles ADDITIONAL_EPOCHS WORD_BITS THREADS [at-least|coded] or CUT WORD_BITS THREADS export-coded FILE < register");
    mpz_class epochs(argv[1],10);
    Count limit = number(argv[2]);
    Count requested_workers = number(argv[3]);
    if (epochs < 0 || limit < 16 || limit > (Count(1)<<43) ||
        requested_workers < 1 || requested_workers > 64)
        throw std::runtime_error("invalid budget");
    int workers = static_cast<int>(requested_workers);
    std::string reg;
    std::cin>>reg;
    if (reg.empty() || reg.size()%2 || reg.size()>848) throw std::runtime_error("invalid register length");
    size_t export_cut=0;
    if(exporting) {
        if(epochs<53 || epochs>reg.size()/2) throw std::runtime_error("coded export cut outside the register");
        export_cut=epochs.get_ui();
        mpz_ui_pow_ui(epochs.get_mpz_t(),7,reg.size()/2+1);
    }
    Tables t; Ray stream;
    auto initial=std::make_shared<Bits>(4); initial->addr[0]=2; initial->size=4;
    append(stream.period,initial); stream.copies=epochs;
    unsigned pending = 0;
    std::vector<unsigned> states;
    for (size_t i = 0; i < reg.size(); i+=2) {
        char v = reg[i], flag = reg[i+1];
        if ((v!='0' && v!='1' && v!='2') || (flag!='2' && flag!='3'))
            throw std::runtime_error("invalid register digit");
        states.push_back(2*(v=='1' ? 0 : (v=='0' ? 1 : 2)) + pending);
        pending = flag == '3';
    }
    std::vector<Cycle> history;
    mpz_class origin = 0, root_period = 1;
    for (size_t i = 0; i < states.size(); ++i) {
        unsigned state = states[i];
        Totals totals;
        if (aligned) {
            // Seven copies suffice to find a repeated state among six states.
            // Discard the artificial remainder. Keep the true infinite ray.
            stream.copies = 7;
            auto& summary = history.emplace_back();
            stream = tiled::lift(state, stream, totals, t, limit, workers, &summary);
            if (!summary.cycle) throw std::logic_error("no period in seven copies");
            origin += root_period * summary.transient;
            root_period *= summary.cycle;
            summary.origin = origin;
            summary.root_period = root_period;
            stream.suffix.clear();
            if (std::getenv("LINE17_TILES_TRACE"))
                std::cerr << "cycle " << i+1 << ' ' << origin << ' ' << root_period << ' '
                          << length(stream.prefix) << ' ' << length(stream.period) << ' '
                          << stream.period_marks << '\n';
            if (coded_mode && i+1>=53 && length(stream.prefix)==0 && length(stream.period)>=65536 &&
                length(stream.period)<=limit && origin+root_period<epochs) {
                coded::Alphabet alphabet;
                auto word=coded::from_packed(stream.period,alphabet);
                stream=Ray{};
                coded::run(std::move(word),std::move(history),states,epochs,limit,workers,alphabet,
                           export_cut,exporting ? argv[5] : nullptr);
                return 0;
            }
            bool stream_tail = length(stream.period) > limit/3;
            if (exporting && (stream_tail || i+1>=export_cut))
                throw std::runtime_error("cannot reach a pure coded period at requested cut within budget");
            if (origin + root_period >= epochs || i+1 == states.size() || stream_tail) {
                mpz_class repeats = 0;
                if (epochs > origin) {
                    mpz_class remainder = epochs - origin;
                    mpz_cdiv_q(repeats.get_mpz_t(), remainder.get_mpz_t(), root_period.get_mpz_t());
                }
                const mpz_class actual = origin + repeats*root_period;
                write_aligned_rows(history, actual);
                stream.copies = repeats;
                aligned = false;
                if (stream_tail && i+1 < states.size()) {
                    if (std::getenv("LINE17_TILES_TRACE"))
                        std::cerr << "streaming cut " << i+1 << ": " << repeats << " periods of "
                                  << length(stream.period) << " slots, plus " << length(stream.prefix)
                                  << " leading slots; aligned sweep " << actual << '\n';
                    finish_aligned_tail(stream, states, i+1, t);
                    return 0;
                }
            }
        } else {
            stream = tiled::lift(state, stream, totals, t, limit, workers);
            mpz_class n = length(stream.prefix) + stream.copies*length(stream.period) + length(stream.suffix);
            write_row(state, n, totals.calls, totals.interior);
            std::cout.flush();
        }
        if (!aligned && std::getenv("LINE17_TILES_TRACE"))
            std::cerr << i+1 << ' ' << length(stream.prefix) << ' ' << length(stream.period)
                      << ' ' << stream.copies << ' ' << length(stream.suffix)
                      << ' ' << stream.period_marks << '\n';
    }
    return 0;
} catch (const std::exception& e) { std::cerr<<e.what()<<'\n'; return 2; }
