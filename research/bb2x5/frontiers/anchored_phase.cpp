// Exact first entries and blank checkpoints for formal lines 21 and 22.
// Build: c++ -O3 -std=c++20 anchored_phase.cpp -lgmpxx -lgmp -o anchored_phase
// Usage: anchored_phase LINE PERIODIC_CUT PERIOD_COPIES [CHECKPOINT_INTERVAL]
#include <algorithm>
#include <array>
#include <cstdint>
#include <gmpxx.h>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Bits = std::uint64_t;
using Count = mpz_class;
constexpr int packet_width = 8;
constexpr int group_width = 4;
constexpr int trace_width = 18;
constexpr int virgin = 3;
// Encoded states 0,1,2 are the three mature symbols. 3,4 are the fresh 0,2.
constexpr char digit[] = "34102";

struct Word {
    std::size_t size = 0;
    std::vector<Bits> data{0, 0};

    void reserve_bits(std::size_t bits) {
        auto words = bits / 64 + 3;
        if (data.size() < words) data.resize(words);
    }
    void clear() { size = 0; data[0] = data[1] = 0; }
    Bits at(std::size_t i) const {
        auto p = i / 64, shift = i % 64;
        return shift ? (data[p] >> shift) | (data[p+1] << (64-shift)) : data[p];
    }
    // The caller reserves space and supplies exactly the low n bits.
    void push(Bits bits, unsigned n) {
        if (!n) return;
        auto p = size / 64, shift = size % 64;
        data[p] |= bits << shift;
        data[p+1] = shift ? bits >> (64-shift) : 0;
        size += n;
    }
    void slice(const Word& w, std::size_t begin, std::size_t len) {
        reserve_bits(size + len);
        for (std::size_t i = 0; i < len; i += 64) {
            unsigned n = std::min<std::size_t>(64, len-i);
            Bits bits = w.at(begin+i);
            if (n < 64) bits &= (Bits(1) << n)-1;
            push(bits, n);
        }
    }
    std::string head(std::size_t n) const {
        std::string s;
        for (std::size_t i=0; i<std::min(size,n); ++i) s += at(i)&1 ? 'B' : 'A';
        return s;
    }
};

struct Entry { int next; unsigned bits, length; };
using CellTable = std::array<std::array<Entry,2>,5>;
struct Packet { Bits bits; unsigned length, visits; int next; };
struct FreshHalt { std::size_t coordinate = 0; };

class Engine {
    CellTable cell;
    std::array<std::array<Bits,256>,5> single{};
    std::array<std::array<Bits,256>,81> group{};

    Packet local(int state, Bits bits, unsigned n) const {
        Packet p{0,0,n,state};
        for (unsigned i=0; i<n; ++i) {
            auto e = cell[p.next][(bits>>i)&1];
            if (e.next < 0) return {0,0,0,-1};
            if (p.length+e.length > 63) throw std::runtime_error("packet too large");
            p.bits |= Bits(e.bits) << p.length;
            p.length += e.length;
            p.next = e.next;
        }
        return p;
    }
    Packet four(int state, Bits bits, unsigned n) const {
        unsigned visits = 0;
        int next = 0, place = 1;
        for (int j=0; j<group_width; ++j) {
            auto p = local(state%3,bits,n);
            visits += p.visits; next += place*p.next;
            bits = p.bits; n = p.length; state /= 3; place *= 3;
        }
        return {bits,n,visits,next};
    }
    static Bits pack(Packet p) {
        if (p.next<0) return 255;
        if (p.length>40 || p.visits>255) throw std::runtime_error("packed table overflow");
        return (p.bits<<24) | (Bits(p.visits)<<16) | (p.length<<8) | p.next;
    }
public:
    explicit Engine(int line) {
        cell[0] = {{{1,0,0},{0,2,3}}};  // 3: A is silent, B emits ABA
        cell[1] = {{{0,1,1},{2,0,0}}};  // 4: A emits B
        cell[2] = {{{0,0,1},{1,unsigned(line==21),1}}};
        cell[3] = {{{0,1,2},{4,0,0}}};  // fresh A emits BA
        cell[4] = {{{0,0,0},{-1,0,0}}};
        for (unsigned byte=0; byte<256; ++byte) {
            for (int q=0; q<5; ++q) single[q][byte] = pack(local(q,byte,packet_width));
            for (int q=0; q<81; ++q) group[q][byte] = pack(four(q,byte,packet_width));
        }
    }
    template<bool grouped = false>
    int image(const Word& in, int state, Word& out, std::uint64_t& visits) const {
        out.clear(); out.reserve_bits(in.size+65536);
        std::uint64_t cost = 0;
        auto byte = [&](unsigned b) {
            Bits p = grouped ? group[state][b] : single[state][b];
            state = p&255;
            if (!grouped && state==255) throw FreshHalt{};
            if constexpr (grouped) cost += (p>>16)&255;
            out.push(p>>24,(p>>8)&255);
        };
        std::size_t words=in.size/64;
        for (std::size_t i=0; i<words; ++i) {
            // At most 40 bits per byte, including the four-cell packet.
            if (i%128==0) out.reserve_bits(out.size+128*8*40+64);
            Bits w=in.data[i];
            for (int j=0; j<8; ++j, w>>=8) byte(w&255);
        }
        out.reserve_bits(out.size+512);
        unsigned remaining=in.size%64;
        Bits w=in.data[words];
        while (remaining>=8) { byte(w&255); w>>=8; remaining-=8; }
        if (remaining) {
            auto p = grouped ? four(state,w,remaining) : local(state,w,remaining);
            if (p.next<0) throw FreshHalt{};
            cost += p.visits; state=p.next; out.push(p.bits,p.length);
        }
        visits = grouped ? cost : in.size;
        return state;
    }
};

struct Period {
    Word start, repeat;
    Count before=0, groups=1;
    std::string head() const {
        if (!repeat.size) throw std::runtime_error("empty output period");
        auto s=start.head(trace_width);
        while (s.size()<trace_width) s+=repeat.head(trace_width-s.size());
        return s;
    }
};
struct History {
    Count before, groups;
    std::size_t front_size, period_size;
    int final_state;
    std::string prefix;
};
Period advance(const Period& p, const Engine& engine, std::vector<History>& history) {
    Period out; std::uint64_t unused;
    int state=engine.image(p.start,virgin,out.start,unused);
    std::array<int,5> seen; seen.fill(-1);
    std::vector<Word> pieces;
    while (seen[state]<0) {
        seen[state]=pieces.size(); pieces.emplace_back();
        state=engine.image(p.repeat,state,pieces.back(),unused);
    }
    int first=seen[state];
    history.push_back({p.before,p.groups,p.start.size,p.repeat.size,state,p.head()});
    out.before=p.before+p.groups*first;
    out.groups=p.groups*(pieces.size()-first);
    std::size_t total=0;
    for (std::size_t j=first; j<pieces.size(); ++j) total+=pieces[j].size;
    if (pieces.size()-first==1) out.repeat=std::move(pieces[first]);
    else {
        out.repeat.reserve_bits(total);
        for (std::size_t j=first; j<pieces.size(); ++j) out.repeat.slice(pieces[j],0,pieces[j].size);
    }
    for (int j=0; j<first; ++j) out.start.slice(pieces[j],0,pieces[j].size);
    return out;
}

struct Cell { int state=virgin; std::string prefix; };
class Tail {
    const Engine& engine;
    const std::size_t cut;
    Word a,b;
public:
    std::vector<Cell> cells;
    Count visits=0;
    Tail(const Engine& e, std::size_t cut) : engine(e), cut(cut) {}
    void consume(const Word& w) {
        constexpr std::size_t block=262144;
        for (std::size_t pos=0; pos<w.size; pos+=block) {
            a.clear(); a.slice(w,pos,std::min(block,w.size-pos));
            for (std::size_t j=0; a.size;) {
                if (cells.size()==j) cells.emplace_back();
                auto& c=cells[j];
                c.prefix+=a.head(trace_width-c.prefix.size());
                std::uint64_t count;
                bool ready=j%group_width==0 && j+group_width<=cells.size() &&
                    std::all_of(cells.begin()+j,cells.begin()+j+group_width,
                                [](const Cell& v){return v.prefix.size()==trace_width && v.state<3;});
                if (ready) {
                    int q=0;
                    for (int k=group_width-1; k>=0; --k) q=3*q+cells[j+k].state;
                    q=engine.image<true>(a,q,b,count);
                    for (int k=0; k<group_width; ++k) {cells[j+k].state=q%3; q/=3;}
                    j+=group_width;
                } else {
                    try {c.state=engine.image(a,c.state,b,count);}
                    catch (const FreshHalt&) { throw FreshHalt{cut+j}; }
                    ++j;
                }
                visits+=count;
                std::swap(a,b);
            }
        }
    }
};

int main(int argc,char** argv) try {
    if (argc!=4 && argc!=5) throw std::runtime_error("usage: anchored_phase LINE PERIODIC_CUT PERIOD_COPIES [CHECKPOINT_INTERVAL]");
    int line=std::stoi(argv[1]), cut=std::stoi(argv[2]);
    auto copies=std::stoull(argv[3]);
    auto interval=argc==5 ? std::stoull(argv[4]) : copies;
    if ((line!=21 && line!=22) || cut<0 || !copies || !interval) throw std::runtime_error("invalid run parameters");
    Engine engine(line); Period p;
    // The initial A followed by (BAABABABAAABA)^infinity, grouped at rank zero.
    for (char letter:std::string("ABAABABABAAAB")) p.repeat.push(letter=='B',1);
    std::vector<History> history;
    for (int j=0; j<cut; ++j) {
        try { p=advance(p,engine,history); }
        catch (const FreshHalt&) { throw FreshHalt{static_cast<std::size_t>(j)}; }
    }
    std::cout<<"cut "<<cut<<" initial_letters "<<p.start.size<<" cycle_letters "<<p.repeat.size
             <<" initial_groups "<<p.before<<" cycle_groups "<<p.groups<<std::endl;
    Tail tail(engine,cut); tail.consume(p.start);
    std::vector<std::string> early_prefixes;
    for (unsigned long long i=1; i<=copies; ++i) {
        tail.consume(p.repeat);
        if (i%interval && i!=copies) continue;
        Count groups=p.before+p.groups*static_cast<unsigned long>(i);
        Count visits=tail.visits;
        std::string tape;
        for (const auto& h:history) {
            Count elapsed=groups-h.before;
            if (elapsed<0 || elapsed%h.groups!=0) throw std::runtime_error("period phase mismatch");
            Count entries=h.front_size+(elapsed/h.groups)*h.period_size;
            visits+=entries;
            if (i==copies) early_prefixes.push_back(entries<trace_width ?
                h.prefix.substr(0,entries.get_ui()) : h.prefix);
            tape+=digit[h.final_state];
        }
        for (const auto& c:tail.cells) tape+=digit[c.state];
        Count steps=52*groups*groups-21*groups+8+2*visits-13*groups;
        std::cout<<"checkpoint "<<i<<" groups "<<groups<<" steps "<<steps
                 <<" tape "<<tape<<std::endl;
    }
    for (std::size_t i=0; i<early_prefixes.size(); ++i) std::cout<<i<<" "<<early_prefixes[i]<<"\n";
    for (std::size_t i=0; i<tail.cells.size(); ++i) std::cout<<cut+i<<" "<<tail.cells[i].prefix<<"\n";
    return 0;
} catch(const FreshHalt& h) {
    std::cout<<"B2 at coordinate "<<h.coordinate<<" on its first two entries BB\n"; return 0;
} catch(const std::exception& e) { std::cerr<<e.what()<<"\n"; return 1; }
