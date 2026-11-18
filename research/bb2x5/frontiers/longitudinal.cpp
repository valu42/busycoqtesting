// Transform finite boundary-call streams through cells of a two-state TM.
// longitudinal.py checks the first-return contract and the left-half driver.
#include <algorithm>
#include <gmpxx.h>
#include <array>
#include <charconv>
#include <cstdint>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Count = std::uint64_t;
constexpr unsigned halt_state = 10;
constexpr unsigned cycle_state = 11;
Count bit_limit;
struct WordLimit : std::runtime_error { WordLimit() : std::runtime_error("materialized word budget") {} };
Count parse(const char *str) {
    Count value;
    auto end = str + std::char_traits<char>::length(str);
    auto r = std::from_chars(str, end, value);
    if (r.ec != std::errc{} || r.ptr != end) throw std::runtime_error("invalid unsigned integer");
    return value;
}

// LSB first. Outer language is prefix + period^copies + suffix. Only distinct
// materialized pieces occupy storage. Equal letters remain A=0 and B=1.
struct Word {
    Count size = 0;
    std::vector<Count> data;
    Count at(Count pos, unsigned n) const {
        unsigned shift = pos % 64;
        Count v = data[pos/64] >> shift;
        if (n > 64-shift) v |= data[pos/64+1] << (64-shift);
        return n == 64 ? v : v & ((Count(1) << n)-1);
    }
    void push(Count bits, unsigned n, Count limit=bit_limit) {
        if (!n) return;
        if (n > limit || size > limit-n) throw WordLimit{};
        auto shift = unsigned(size % 64);
        if (!shift) data.push_back(bits);
        else {
            data.back() |= bits << shift;
            if (n > 64-shift) data.push_back(bits >> (64-shift));
        }
        size += n;
    }
    void append(const Word &other, Count limit=bit_limit) {
        for (Count i=0; i<other.size; i+=64)
            push(other.data[i/64], unsigned(std::min<Count>(64,other.size-i)), limit);
    }
};
Word letters(const std::string &s) {
    Word w;
    for (char c : s) w.push(c=='B',1);
    return w;
}
struct Stream {
    Word prefix, period, suffix;
    mpz_class copies = 0;
    mpz_class size() const { return prefix.size + copies*period.size + suffix.size; }
    std::string first_letters(Count limit) const {
        std::string result;
        auto take=[&](const Word& w) {
            for (Count i=0; i<w.size && result.size()<limit; ++i)
                result.push_back(w.at(i,1) ? 'B' : 'A');
        };
        take(prefix);
        for (Count k=0; period.size && result.size()<limit && k<copies; ++k) take(period);
        take(suffix);
        return result;
    }
};
struct Output { unsigned state = 0, length = 0; Count bits = 0; };
class Transducer {
    std::array<std::array<Output, 2>, 10> cell{};
    std::array<std::vector<Output>, 10> packets;
    unsigned packet_bits = 8;
    static Output single(const std::string &machine, unsigned usual,
                         const std::string &first, unsigned state, unsigned input) {
        unsigned symbol = state/2;
        bool virgin_child = state%2;
        std::array<bool,20> visited{};
        Output out;
        for (;;) {
            auto key = (2*symbol+input)*2+virgin_child;
            if (visited[key]) { out.state=cycle_state; return out; }
            visited[key]=true;
            const char *rule = machine.data()+16*input+3*symbol;
            if (*rule == '-') { out.state=halt_state; return out; }
            symbol=unsigned(rule[0]-'0'); input=unsigned(rule[2]-'A');
            if (rule[1]=='L') { out.state=2*symbol+virgin_child; return out; }
            out.bits |= Count(input) << out.length++;
            input = virgin_child ? unsigned(first[input]-'A') : usual;
            virgin_child=false;
        }
    }
public:
    Transducer(const std::string &machine, unsigned usual, const std::string &first) {
        unsigned longest=1;
        for (unsigned s=0; s<10; ++s) for (unsigned i=0; i<2; ++i) {
            cell[s][i]=single(machine,usual,first,s,i);
            longest=std::max(longest, cell[s][i].length);
        }
        packet_bits=std::min(packet_bits, 63/longest);
        const unsigned count=1U << packet_bits;
        for (unsigned s=0; s<10; ++s) {
            packets[s].resize(count);
            for (unsigned bits=0; bits<count; ++bits) {
                Output out{s,0,0};
                for (unsigned i=0; i<packet_bits && out.state<halt_state; ++i) {
                    auto part=cell[out.state][(bits >> i) & 1];
                    out.bits |= part.bits << out.length;
                    out.length+=part.length; out.state=part.state;
                }
                packets[s][bits]=out;
            }
        }
    }
    void transform(const Word &w, unsigned &state, Word &out, Count limit) const {
        auto emit=[&](const Output& a) {
            // A local halt can depend on an outstanding child call. The caller
            // resolves a candidate using the physical order of instructions.
            if (a.state==halt_state) throw std::runtime_error("candidate undefined instruction");
            if (a.state==cycle_state) throw std::runtime_error("unresolved local call cycle");
            out.push(a.bits,a.length,limit);
            state=a.state;
        };
        Count i=0;
        if (packet_bits==8) {
            for (Count j=0; j<w.size/8; ++j) {
                unsigned bits=(w.data[j/8]>>(8*(j%8)))&255;
                emit(packets[state][bits]);
            }
            i=w.size-w.size%8;
        }
        for (; i<w.size;) {
            bool packet = w.size-i >= packet_bits;
            auto n = packet ? packet_bits : 1U;
            auto bits = w.at(i,n);
            emit(packet ? packets[state][bits] : cell[state][bits]);
            i+=n;
        }
    }
    Word image(const Word &w, unsigned &state) const {
        Word out;
        transform(w,state,out,bit_limit);
        return out;
    }
    Stream image(const Stream &in, unsigned &state) const {
        Stream out;
        out.prefix = image(in.prefix,state);
        std::array<int,10> first;
        first.fill(-1);
        std::vector<Word> pieces;
        std::vector<unsigned> starts;
        while (pieces.size()<in.copies && first[state]<0) {
            first[state]=int(pieces.size()); starts.push_back(state);
            pieces.push_back(image(in.period,state));
        }
        if (pieces.size()==in.copies) {
            for (const auto &p: pieces) out.prefix.append(p);
        } else {
            unsigned begin = unsigned(first[state]), cycle = unsigned(pieces.size())-begin;
            for (unsigned j=0; j<begin; ++j) out.prefix.append(pieces[j]);
            for (unsigned j=begin; j<pieces.size(); ++j) out.period.append(pieces[j]);
            out.copies = (in.copies-begin)/cycle;
            unsigned remainder = unsigned(mpz_fdiv_ui(in.copies.get_mpz_t(),cycle));
            remainder = (remainder + cycle - begin%cycle)%cycle;
            for (unsigned j=0; j<remainder; ++j) out.suffix.append(pieces[begin+j]);
            state = starts[begin+remainder];
        }
        auto tail = image(in.suffix,state);
        out.suffix.append(tail);
        return out;
    }
};

// The overflowing image has not been committed. Feed the original input through
// the remaining cells in chronological chunks, retaining each cell's symbol
// and its first-child flag across chunk boundaries.
void finish(const Transducer& trans, const Stream& input, const std::string& seed,
            std::string& tape, std::vector<mpz_class>& entries, std::vector<std::string>& prefixes,
            Count trace, Count budget) {
    if (input.size()>budget)
        throw std::runtime_error("finite slot budget at cell "+std::to_string(entries.size())+
                                 ": need "+input.size().get_str()+", budget "+std::to_string(budget));
    const size_t start=entries.size();
    constexpr Count chunk=65536, chunk_limit=Count(1)<<26;
    std::vector<unsigned> states;
    Word a,b;
    auto feed=[&](const Word& part) {
        for (Count base=0; base<part.size; base+=chunk) {
            const Count end=std::min(base+chunk,part.size);
            for (Count j=base; j<end; j+=64) {
                auto width=unsigned(std::min<Count>(64,end-j));
                a.push(part.at(j,width),width,chunk);
            }
            for (size_t i=start; a.size; ++i) {
                if (i>=100000) throw std::runtime_error("cell depth budget");
                if (i==entries.size()) {
                    unsigned symbol=i<seed.size()?unsigned(seed[i]-'0'):0;
                    states.push_back(2*symbol+(i+1>=seed.size()));
                    entries.emplace_back(0);
                    if (trace) prefixes.emplace_back();
                }
                entries[i]+=a.size;
                if (trace) {
                    for (Count j=0; j<a.size && prefixes[i].size()<trace; ++j)
                        prefixes[i].push_back(a.at(j,1)?'B':'A');
                }
                try { trans.transform(a,states[i-start],b,chunk_limit); }
                catch (const std::runtime_error& e) {
                    throw std::runtime_error(std::string(e.what())+" at cell "+std::to_string(i));
                }
                a.size=0; a.data.clear(); std::swap(a,b);
            }
        }
    };
    feed(input.prefix);
    if (input.period.size) {
        Count copies=input.copies.get_ui(); // total slots are bounded above
        const Count block=std::min(copies,chunk/input.period.size);
        if (block>1) {
            Word tile;
            for (Count j=0;j<block;++j) tile.append(input.period,chunk);
            for (Count j=0;j<copies/block;++j) feed(tile);
            copies%=block;
        }
        for (Count j=0;j<copies;++j) feed(input.period);
    }
    feed(input.suffix);
    tape.resize(std::max(tape.size(),entries.size()),'0');
    for (size_t j=0;j<states.size();++j) tape[start+j]=char('0'+states[j]/2);
}

int main(int argc, char **argv) try {
    if (argc<3 || argc>5) throw std::runtime_error("usage: longitudinal PERIOD_GROUPS MAX_BITS [PREFIX_LETTERS [FINITE_SLOTS]] < protocol");
    mpz_class groups(argv[1],10); bit_limit=parse(argv[2]);
    Count trace=argc>=4 ? parse(argv[3]) : 0;
    Count finite_slots=argc==5 ? parse(argv[4]) : 0;
    if (trace>65536) throw std::runtime_error("entry prefix exceeds 65536 letters");
    std::string machine,prefix,period,usual,first,seed;
    if (!(std::cin >> machine >> prefix >> period >> usual >> first >> seed)) throw std::runtime_error("incomplete protocol");
    if (prefix==".") prefix.clear();
    if (prefix.find_first_not_of("AB")!=std::string::npos || groups<=0 || bit_limit<16 || period.empty() || period.find_first_not_of("AB")!=std::string::npos ||
        usual.size()!=1 || first.size()!=2 || (usual+first).find_first_not_of("AB")!=std::string::npos ||
        machine.size()!=31 || machine[15]!='_') throw std::runtime_error("invalid protocol");
    for (unsigned q=0; q<2; ++q) for (unsigned s=0; s<5; ++s) {
        auto ins=machine.substr(16*q+3*s,3);
        if (ins!="---" && (ins[0]<'0' || ins[0]>'4' || (ins[1]!='L' && ins[1]!='R') || (ins[2]!='A' && ins[2]!='B')))
            throw std::runtime_error("invalid machine encoding");
    }
    bool blank = seed==".";
    if (blank) seed.clear();
    else if (seed.find_first_not_of("01234")!=std::string::npos) throw std::runtime_error("invalid positive tape");
    Stream input;
    if (blank) {
        input.prefix=letters("A"+prefix); input.period=letters(period); input.copies=groups-1;
        input.suffix=letters(period.substr(0,period.size()-1));
    } else {
        input.period=letters(period.back()+period.substr(0,period.size()-1)); input.copies=groups;
    }
    Transducer trans(machine,unsigned(usual[0]-'A'),first);
    std::string tape=seed;
    std::vector<mpz_class> entries;
    std::vector<std::string> prefixes;
    for (std::size_t depth=0; input.size(); ++depth) {
        if (depth>=100000) throw std::runtime_error("cell depth budget");
        unsigned symbol=depth<seed.size()?unsigned(seed[depth]-'0'):0U;
        unsigned state=2*symbol + (depth+1 >= seed.size());
        try {
            auto out=trans.image(input,state);
            entries.push_back(input.size());
            if (trace) prefixes.push_back(input.first_letters(trace));
            input=std::move(out);
        }
        catch (const WordLimit& e) {
            if (!finite_slots) throw std::runtime_error(std::string(e.what())+" at cell "+std::to_string(depth));
            finish(trans,input,seed,tape,entries,prefixes,trace,finite_slots);
            break;
        }
        catch(const std::runtime_error &e) { throw std::runtime_error(std::string(e.what())+" at cell "+std::to_string(depth)); }
        if (depth==tape.size()) tape.push_back(char('0'+state/2));
        else tape[depth]=char('0'+state/2);
    }
    std::cout << tape << '\n';
    for (size_t i=0; i<entries.size(); ++i) {
        std::cout << entries[i];
        if (trace) std::cout << ' ' << prefixes[i];
        std::cout << '\n';
    }
    return 0;
} catch (const std::exception &e) { std::cerr << e.what() << '\n'; return 2; }
