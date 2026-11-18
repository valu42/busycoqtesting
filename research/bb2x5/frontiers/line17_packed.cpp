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

struct Packet {
    std::uint8_t state=0, width=0, calls=0, interior=0;
    std::uint16_t bits=0;
};
struct Transfer {
    std::array<std::array<Packet,256>,6> table{};
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
    }
    void apply(const Word& in, unsigned& state, Word& out,
               Count& calls, Count& interior, Count limit) const {
        auto emit=[&](const Packet& p) {
            if (p.state==invalid) throw std::runtime_error("overlapping marked bursts");
            out.push(p.bits,p.width,limit);
            calls+=p.calls; interior+=p.interior; state=p.state;
        };
        for (Count i=0; i<in.size/8; ++i) {
            unsigned byte=(in.data[i/8]>>(8*(i%8))) & 255;
            emit(table[state][byte]);
        }
        unsigned tail=in.size%8;
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

// Fall back before building a large word. Stream the original input unchanged
// through every remaining digit; word boundaries survive as state, not padding.
void finish(const Transfer& tr, const Stream& in, const std::vector<unsigned>& initial,
            unsigned cut, Count work_limit) {
    if (in.size()>work_limit)
        throw std::runtime_error("finite slot budget at pair "+std::to_string(cut)+
                                 ": need "+in.size().get_str()+", budget "+std::to_string(work_limit));
    std::vector<Digit> digits;
    for (unsigned j=cut;j<initial.size();++j) digits.push_back({initial[j]});
    Word a,b;
    auto feed=[&](const Word& w) {
        for (Count offset=0;offset<w.size;) {
            const Count end=offset+std::min<Count>(65536,w.size-offset);
            for (Count j=offset;j<end;j+=64) {
                auto width=static_cast<unsigned>(std::min<Count>(64,end-j));
                a.push(w.read(j,width),width,65536);
            }
            for (auto& digit:digits) {
                if (!a.size) break;
                if (a.size>arithmetic_limit || digit.calls>arithmetic_limit*8 || digit.interior>arithmetic_limit*8)
                    throw std::runtime_error("finite counter limit");
                tr.apply(a,digit.state,b,digit.calls,digit.interior,Count(1)<<28);
                if (digit.n>arithmetic_limit-b.size) throw std::runtime_error("finite length limit");
                digit.n+=b.size;
                a.clear(); std::swap(a,b);
            }
            a.clear(); offset=end;
        }
    };
    feed(in.prefix);
    if (in.period.size) {
        Count copies=in.copies.get_ui(); // bounded by total size above
        Count block=std::min<Count>(copies,65536/in.period.size);
        if (block>1) {
            Word tile;
            for (Count j=0;j<block;++j) tile.append(in.period,65536);
            for (Count j=0;j<copies/block;++j) feed(tile);
            copies%=block;
        }
        for (Count j=0;j<copies;++j) feed(in.period);
    }
    feed(in.suffix);
    for (const auto& digit:digits) print(digit.state,digit.n,digit.calls,digit.interior);
}

int main(int argc,char** argv) try {
    if (argc!=4) throw std::runtime_error("usage: line17-packed ADDITIONAL_EPOCHS WORD_BITS FINITE_SLOTS < register");
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
    Stream input;
    input.period.push(2,4,limit); input.copies=epochs;
    for (unsigned i=0;i<initial.size();++i) {
        if (input.period.size>65536 && input.size()<=std::min(limit,work_limit)) {
            finish(tr,input,initial,i,work_limit);
            return 0;
        }
        unsigned state=initial[i];
        Totals tally;
        try {
            auto out=lift(tr,input,state,tally,limit);
            print(state,out.size(),tally.calls,tally.interior);
            input=std::move(out);
        } catch (const WordLimit&) {
            finish(tr,input,initial,i,work_limit);
            return 0;
        }
    }
    return 0;
} catch (const std::exception& e) { std::cerr<<e.what()<<'\n'; return 2; }
  catch (const WordLimit&) { std::cerr<<"finite chunk budget exceeded\n"; return 2; }
