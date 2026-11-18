// Exact finite pulse streams for line 17. Each bit is one input slot, LSB first.
#include <algorithm>
#include <array>
#include <charconv>
#include <cstdint>
#include <gmpxx.h>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Count = std::uint64_t;
constexpr unsigned invalid = 6;
constexpr Count arithmetic_limit = std::numeric_limits<Count>::max()/16;
struct WordLimit {};

Count number(const char* str) {
    Count x;
    auto end = str + std::char_traits<char>::length(str);
    auto v = std::from_chars(str, end, x);
    if (v.ec!=std::errc{} || v.ptr!=end) throw std::runtime_error("invalid integer");
    return x;
}

struct Word {
    Count size = 0;
    std::vector<Count> data;
    Count read(Count pos, unsigned width) const {
        const unsigned off=pos%64;
        Count bits=data[pos/64]>>off;
        if (width>64-off) bits |= data[pos/64+1]<<(64-off);
        return width==64 ? bits : bits & ((Count(1)<<width)-1);
    }
    void push(Count bits, unsigned width, Count limit) {
        if (!width) return;
        if (width>limit || size>limit-width) throw WordLimit{};
        unsigned shift=size%64;
        if (!shift) data.push_back(bits);
        else {
            data.back() |= bits<<shift;
            if (width>64-shift) data.push_back(bits>>(64-shift));
        }
        size+=width;
    }
    void append(const Word& w, Count limit) {
        for (Count i=0; i<w.size; i+=64)
            push(w.data[i/64],static_cast<unsigned>(std::min<Count>(64,w.size-i)),limit);
    }
    void clear() { size=0; data.clear(); }
};

// The mark separation admits only 595 of the 65,536 sixteen-slot words.
// Keep a compact transfer table and retain byte handling for other inputs.
struct SpacedWords {
    static constexpr unsigned missing=std::numeric_limits<std::uint16_t>::max();
    std::array<std::uint16_t,65536> index;
    std::vector<std::uint16_t> words;
    SpacedWords() {
        index.fill(missing);
        for (unsigned w=0;w<index.size();++w) {
            if (w & ((w>>1)|(w>>2))) continue;
            index[w]=static_cast<std::uint16_t>(words.size());
            words.push_back(static_cast<std::uint16_t>(w));
        }
    }
};
const SpacedWords& spaced_words() {
    static const SpacedWords words;
    return words;
}

// Apply every complete transfer and return the remaining bit count (0..7).
// The emitter updates state before the next table lookup.
template<class ByteTable,class WideTable,class Emit>
unsigned apply_chunks(const Word& in,unsigned& state,const ByteTable& table,const WideTable& wide,Emit emit) {
    const auto& indices=spaced_words().index;
    for (Count i=0;i<in.size/16;++i) {
        unsigned word=(in.data[i/4]>>(16*(i%4)))&65535;
        unsigned entry=indices[word];
        if (entry!=SpacedWords::missing) emit(wide[entry][state]);
        else {
            emit(table[state][word&255]);
            emit(table[state][word>>8]);
        }
    }
    unsigned tail=in.size%16;
    if (tail>=8) {
        emit(table[state][in.read(in.size-tail,8)]);
        tail-=8;
    }
    return tail;
}

struct Packet {
    std::uint8_t state=0, width=0, calls=0, interior=0;
    std::uint32_t bits=0;
};
struct Transfer {
    std::array<std::array<Packet,256>,6> table{};
    std::vector<std::array<Packet,6>> wide;
    static Packet compile(unsigned initial, unsigned bits, unsigned width) {
        Packet out;
        unsigned v=initial/2, pending=initial%2;
        for (unsigned i=0;i<width;++i) {
            bool mark=(bits>>i)&1;
            if (pending && mark) { out.state=invalid; return out; }
            if (pending || mark) {
                out.calls+=v ? 3 : 4;
                out.interior+=v==0 ? 2 : (v==1 ? 6 : 4);
                if (v==1) out.bits |= 2U<<out.width;
                out.width+=v ? 2 : 1;
                pending=v!=0;
                v=(v+2)%3;
            } else {
                ++out.calls;
                if (v==2) { ++out.width; out.interior+=2; }
                v=(v+1)%3;
            }
        }
        out.state=2*v+pending;
        return out;
    }
    Transfer() {
        for (unsigned s=0;s<6;++s)
            for (unsigned b=0;b<256;++b) table[s][b]=compile(s,b,8);
        const auto& words=spaced_words().words;
        wide.resize(words.size());
        for (size_t j=0;j<words.size();++j)
            for (unsigned s=0;s<6;++s) wide[j][s]=compile(s,words[j],16);
    }
    void apply(const Word& in, unsigned& state, Word& out,
               Count& calls, Count& interior, Count limit) const {
        auto emit=[&](const Packet& p) {
            if (p.state==invalid) throw std::runtime_error("overlapping marked bursts");
            out.push(p.bits,p.width,limit);
            calls+=p.calls; interior+=p.interior; state=p.state;
        };
        unsigned tail=apply_chunks(in,state,table,wide,emit);
        if (tail) {
            unsigned bits=static_cast<unsigned>(in.read(in.size-tail,tail));
            emit(compile(state,bits,tail));
        }
    }
};

struct Stream {
    Word prefix, period, suffix;
    mpz_class copies=0;
    mpz_class size() const { return prefix.size+copies*period.size+suffix.size; }
};
#include "line17_rank.hpp"
struct Piece {
    Word word;
    Count calls=0, interior=0;
    unsigned start;
    explicit Piece(unsigned s) : start(s) {}
};
struct Totals { mpz_class calls=0, interior=0; };

// At a period boundary, equal trit AND pending bit mean that the entire next
// copy has the same image and both the same instruction counts. Only copies
// actually present in this finite input may be inspected (including its tail).
Stream lift(const Transfer& tr, const Stream& in, unsigned& state, Totals& tally, Count limit) {
    Stream out;
    Count calls=0, interior=0;
    tr.apply(in.prefix,state,out.prefix,calls,interior,limit);
    std::array<int,6> first; first.fill(-1);
    std::vector<Piece> parts;
    while (parts.size()<in.copies && first[state]<0) {
        first[state]=static_cast<int>(parts.size());
        auto& part=parts.emplace_back(state);
        tr.apply(in.period,state,part.word,part.calls,part.interior,limit);
    }
    unsigned begin=parts.size();
    bool repeats=parts.size()<in.copies;
    if (repeats) begin=static_cast<unsigned>(first[state]);
    for (unsigned j=0;j<begin;++j) {
        out.prefix.append(parts[j].word,limit);
        calls+=parts[j].calls; interior+=parts[j].interior;
    }
    if (repeats) {
        const unsigned cycle=static_cast<unsigned>(parts.size())-begin;
        Count cycle_calls=0,cycle_interior=0;
        for (unsigned j=begin;j<parts.size();++j) {
            out.period.append(parts[j].word,limit);
            cycle_calls+=parts[j].calls; cycle_interior+=parts[j].interior;
        }
        mpz_class remaining=in.copies-begin;
        unsigned tail=mpz_fdiv_q_ui(out.copies.get_mpz_t(),remaining.get_mpz_t(),cycle);
        tally.calls+=out.copies*cycle_calls; tally.interior+=out.copies*cycle_interior;
        for (unsigned j=begin;j<begin+tail;++j) {
            out.suffix.append(parts[j].word,limit);
            calls+=parts[j].calls; interior+=parts[j].interior;
        }
        state=parts[begin+tail].start;
        if (!out.period.size) out.copies=0;
    }
    tr.apply(in.suffix,state,out.suffix,calls,interior,limit);
    tally.calls+=calls; tally.interior+=interior;
    return out;
}

void print(unsigned state,const mpz_class& n,const mpz_class& calls,const mpz_class& interior) {
    std::cout<<state/2<<' '<<state%2<<' '<<n<<' '<<calls<<' '<<interior<<'\n';
}
struct Digit { unsigned state; Count n=0,calls=0,interior=0; };
void check_room(const Digit& digit) {
    // A single bounded chunk can add at most six times its input length.
    if (digit.n>arithmetic_limit || digit.calls>8*arithmetic_limit || digit.interior>8*arithmetic_limit)
        throw std::runtime_error("finite counter limit");
}

// Compose two adjacent digits. One input slot can at most double at each digit.
struct PairPacket {
    Count bits=0;
    std::uint8_t state=invalid,width=0,middle=0;
    std::uint8_t left_calls=0,left_inner=0,right_calls=0,right_inner=0;
};
struct PairTransfer {
    std::array<std::array<PairPacket,256>,36> table{};
    std::vector<std::array<PairPacket,36>> wide;
    static PairPacket compile(unsigned left,unsigned right,unsigned bits,unsigned width) {
        PairPacket p;
        const Packet a=Transfer::compile(left,bits,width);
        if (a.state==invalid) return p;
        p.left_calls=a.calls; p.left_inner=a.interior; p.middle=a.width;
        for (unsigned offset=0; offset<a.width; offset+=8) {
            auto child=Transfer::compile(right,a.bits>>offset,std::min(8U,a.width-offset));
            if (child.state==invalid) return p;
            right=child.state;
            p.bits|=Count(child.bits)<<p.width;
            p.width+=child.width;
            p.right_calls+=child.calls; p.right_inner+=child.interior;
        }
        p.state=6*a.state+right;
        return p;
    }
    PairPacket combine(unsigned state,unsigned word) const {
        auto p=table[state][word&255];
        if (p.state==invalid) return p;
        const auto& next=table[p.state][word>>8];
        if (next.state==invalid) return next;
        p.state=next.state;
        p.bits|=next.bits<<p.width;
        p.width+=next.width; p.middle+=next.middle;
        p.left_calls+=next.left_calls; p.left_inner+=next.left_inner;
        p.right_calls+=next.right_calls; p.right_inner+=next.right_inner;
        return p;
    }
    PairTransfer() {
        for (unsigned state=0;state<36;++state)
            for (unsigned byte=0;byte<256;++byte)
                table[state][byte]=compile(state/6,state%6,byte,8);
        const auto& words=spaced_words().words;
        wide.resize(words.size());
        for (size_t j=0;j<words.size();++j)
            for (unsigned state=0;state<36;++state) wide[j][state]=combine(state,words[j]);
    }
    void apply(const Word& in,Digit& left,Digit& right,Word& out) const {
        unsigned state=6*left.state+right.state;
        auto take=[&](const PairPacket& p) {
            if (p.state==invalid) throw std::runtime_error("overlapping marked bursts");
            state=p.state;
            left.n+=p.middle; left.calls+=p.left_calls; left.interior+=p.left_inner;
            right.calls+=p.right_calls; right.interior+=p.right_inner;
            out.push(p.bits,p.width,Count(1)<<28);
        };
        unsigned tail=apply_chunks(in,state,table,wide,take);
        if (tail) take(compile(state/6,state%6,in.read(in.size-tail,tail),tail));
        left.state=state/6; right.state=state%6;
        right.n+=out.size;
    }
};

// Replay the selected chunk, counting both outputs when one input emits two.
bool reaches_cut(std::vector<unsigned>& states,size_t digit,unsigned bit,Count& remaining) {
    if (digit==states.size()) return --remaining==0;
    const auto p=Transfer::compile(states[digit],bit,1);
    if (p.state==invalid) throw std::runtime_error("overlapping marked bursts");
    states[digit]=p.state;
    for (unsigned j=0;j<p.width;++j)
        if (reaches_cut(states,digit+1,(p.bits>>j)&1,remaining)) return true;
    return false;
}

// If the periodic word gets too large, stream the input through every remaining
// digit. Partial words carry their ending digit states into the next chunk.
std::optional<Count> finish(const Transfer& tr, const Stream& in, const std::vector<unsigned>& initial,
                            unsigned cut, Count work_limit,const mpz_class& rank,bool report_counts) {
    if (in.size()>work_limit)
        throw std::runtime_error("finite slot budget at pair "+std::to_string(cut)+
                                 ": need "+in.size().get_str()+", budget "+std::to_string(work_limit));
    std::vector<Digit> digits;
    for (unsigned j=cut;j<initial.size();++j) digits.push_back({initial[j]});
    PairTransfer pairs;
    Word a,b;
    bool locate=rank>0;
    std::vector<unsigned> before(locate ? digits.size() : 0);
    Count consumed=0;
    std::optional<Count> match;
    auto feed=[&](const Word& w) {
        for (Count offset=0;offset<w.size;) {
            const Count end=offset+std::min<Count>(65536,w.size-offset);
            for (Count j=offset;j<end;j+=64) {
                auto width=static_cast<unsigned>(std::min<Count>(64,end-j));
                a.push(w.read(j,width),width,65536);
            }
            if (locate)
                for (size_t j=0;j<digits.size();++j) before[j]=digits[j].state;
            Count previous=digits.back().n;
            size_t i=0;
            for (; i+1<digits.size() && a.size; i+=2) {
                check_room(digits[i]);
                check_room(digits[i+1]);
                pairs.apply(a,digits[i],digits[i+1],b);
                a.clear(); std::swap(a,b);
            }
            if (i<digits.size() && a.size) {
                auto& digit=digits[i];
                check_room(digit);
                tr.apply(a,digit.state,b,digit.calls,digit.interior,Count(1)<<28);
                digit.n+=b.size; b.clear();
            }
            if (locate && digits.back().n>=rank) {
                mpz_class ordinal=rank-previous;
                Count remaining=ordinal.get_ui();
                for (Count j=offset;j<end;++j) {
                    if (reaches_cut(before,0,w.read(j,1),remaining)) {
                        match=consumed+j-offset+1;
                        return true;
                    }
                }
                throw std::logic_error("chunk and single-slot reachability differ");
            }
            consumed+=end-offset;
            a.clear(); offset=end;
        }
        return false;
    };
    if (feed(in.prefix)) return match;
    if (in.period.size) {
        Count copies=in.copies.get_ui(); // bounded by total size above
        Count block=std::min<Count>(copies,65536/in.period.size);
        if (block>1) {
            Word tile;
            for (Count j=0;j<block;++j) tile.append(in.period,65536);
            for (Count j=0;j<copies/block;++j) if (feed(tile)) return match;
            copies%=block;
        }
        for (Count j=0;j<copies;++j) if (feed(in.period)) return match;
    }
    if (feed(in.suffix)) return match;
    if (report_counts)
        for (const auto& digit:digits) print(digit.state,digit.n,digit.calls,digit.interior);
    return {};
}

int main(int argc,char** argv) try {
    mpz_class rank=0; // Zero selects the ordinary complete-sweep clock.
    bool scan=argc==5 && std::string(argv[4])=="scan";
    if (scan || (argc==5 && std::string(argv[4])=="first")) rank=1;
    else if (argc==6 && std::string(argv[4])=="select") {
        rank=mpz_class(argv[5],10);
        if (rank<=0) throw std::runtime_error("the output rank must be positive");
    } else if (argc!=4)
        throw std::runtime_error("usage: line17-packed ADDITIONAL_EPOCHS WORD_BITS FINITE_SLOTS [first | scan | select RANK] < register");
    bool locate=rank>0;
    bool report_counts=!locate || scan;
    mpz_class epochs(argv[1],10);
    Count limit=number(argv[2]), work_limit=number(argv[3]);
    std::string register_word;
    if (!(std::cin>>register_word) || register_word.empty() || register_word.size()%2 || register_word.size()>848 ||
        epochs<0 || limit<16 || limit>(Count(1)<<32) || work_limit>arithmetic_limit)
        throw std::runtime_error("invalid register or budget");
    std::vector<unsigned> initial;
    unsigned pending=0;
    for (size_t i=0;i<register_word.size();i+=2) {
        char v=register_word[i], f=register_word[i+1];
        if ((v!='1' && v!='0' && v!='2') || (f!='2' && f!='3')) throw std::runtime_error("invalid register digit");
        initial.push_back(2*(v=='1'?0:(v=='0'?1:2))+pending); pending=f=='3';
    }
    Transfer tr;
    std::optional<SlotOrigins> origins;
    if (locate) origins.emplace();
    Stream input;
    input.period.push(2,4,limit); input.copies=epochs;
    auto finish_stream=[&](unsigned cut) {
        auto hit=finish(tr,input,initial,cut,work_limit,rank,report_counts);
        if (locate) {
            input=Stream{};
            if (hit) std::cout<<origins->root(tr,mpz_class(*hit))<<'\n';
            else std::cout<<"none\n";
        }
    };
    for (unsigned i=0;i<initial.size();++i) {
        if (input.period.size>65536 && input.size()<=std::min(limit,work_limit)) {
            finish_stream(i);
            return 0;
        }
        unsigned state=initial[i];
        Totals tally;
        try {
            auto out=lift(tr,input,state,tally,limit);
            if (locate) origins->remember(input,initial[i]);
            if (report_counts) print(state,out.size(),tally.calls,tally.interior);
            input=std::move(out);
        } catch (const WordLimit&) {
            finish_stream(i);
            return 0;
        }
    }
    if (locate) {
        bool hit=input.size()>=rank;
        input=Stream{};
        if (hit) std::cout<<origins->root(tr,rank)<<'\n';
        else std::cout<<"none\n";
    }
    return 0;
} catch (const std::exception& e) { std::cerr<<e.what()<<'\n'; return 2; }
  catch (const WordLimit&) { std::cerr<<"finite chunk budget exceeded\n"; return 2; }
