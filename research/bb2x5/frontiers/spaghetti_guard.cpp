// Exact guarded crossing traces for line 19 in either initial state.
// 3 means physical 4 to the left of the head, physical 3 to its right.
#include <algorithm>
#include <array>
#include <charconv>
#include <cstdint>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>

using Count = std::int64_t;
using Word = std::uint32_t;
constexpr int width = 16;
constexpr char machine[] = "1RB2RA3LA---2LB_2LA4RA4RB0RB0LA";
struct Rule { int digit, move, state; };
Rule rules[2][2][4]{};

int digit(Word w,int i) { return (w >> (2*i)) & 3; }
Word write(Word w,int i,int d) {
    int shift = 2*i;
    return (w & ~(Word(3) << shift)) | (Word(d) << shift);
}
struct Exit {
    Word word; int pos, dir, q, steps, low, first_low;
    bool inside, edge, halted;
};

template<class Note>
Exit trace(Word w, int n, int pos, int dir, int q, int budget, Note note) {
    Exit a{w,pos,dir,q,0,pos,0,false,false,false};
    while (a.pos >= 0 && a.pos < n && a.steps < budget) {
        int s = digit(a.word,a.pos);
        // Incoming B on 3 after a right step, or a return on 0,1,2,
        // in both cases with 1 at the cell immediately to the left.
        if ((a.dir == 1 ? (s == 3 && a.q == 1) : s <= 2) &&
                (a.pos == 0 || digit(a.word,a.pos-1) == 1)) {
            if (a.pos == 0) a.edge = true; else a.inside = true;
            note(a,s);
        }
        Rule r = rules[a.dir==1][a.q][s];
        if (!r.move) { a.halted = true; break; }
        a.word = write(a.word,a.pos,r.digit);
        a.pos += r.move; a.dir = r.move; a.q = r.state; ++a.steps;
        if (a.pos<a.low) { a.low=a.pos; a.first_low=a.steps; }
    }
    return a;
}

struct Ignore { void operator()(const Exit &,int) const {} };
struct Slot { std::uint64_t key = UINT64_MAX; Exit value{}; };
std::array<std::vector<Exit>,4> small;
std::vector<Slot> large(1 << 18);

Exit halves(Word word, int dir, int q) {
    int start=dir==1?0:15;
    Exit a{word,start,dir,q,0,start,0,false,false,false};
    for (int i = 0; i < 64; ++i) {
        int offset = a.pos < 8 ? 0 : 8;
        auto part = small[2*a.q+(a.dir==1)][(a.word >> (offset*2)) & 0xffff];
        a.inside |= part.inside || (offset && part.edge && digit(a.word,7)==1);
        a.edge |= !offset && part.edge;
        a.word = offset ? (a.word & 0xffff) | (part.word << 16)
                        : (a.word & 0xffff0000) | part.word;
        a.pos = offset+part.pos; a.dir = part.dir; a.q = part.q;
        if (offset+part.low<a.low) { a.low=offset+part.low; a.first_low=a.steps+part.first_low; }
        a.steps += part.steps; a.halted = part.halted;
        if (part.pos>=0 && part.pos<8) break;
        if (a.pos<0 || a.pos>=width) break;
    }
    return a;
}

Exit lookup(Word w,int dir,int q) {
    std::uint64_t key = (std::uint64_t(w)<<2) + 2*q + (dir==1);
    auto &slot = large[(key*11400714819323198485ULL >> 46) & (large.size()-1)];
    if (slot.key != key) { slot.key=key; slot.value=halves(w,dir,q); }
    return slot.value;
}

struct Guard {
    int first_digit, stage, prefix;
    Count cell, seed;
    std::array<Count,3> returns{};
};
struct Tally {
    Count seeds[4]{}, replies[4][3][2]{};
    Count by_prefix[256][7]{}, fresh_launches[256]{};
    std::map<Count,Guard> open;
    Guard first{}, longest{};
    void record(Count cell,Count t,int dir,int q,int s,int right,int prefix,bool fresh) {
        if (dir==1) {
            if (open.count(cell)) throw std::logic_error("seed overwrites open guard");
            if (fresh) ++fresh_launches[prefix];
            open.emplace(cell,Guard{right,0,prefix,cell,t,{}}); ++seeds[right]; ++by_prefix[prefix][0]; return;
        }
        auto pos=open.find(cell);
        if (pos==open.end() || pos->second.stage!=s)
            throw std::logic_error("return disagrees with guard history");
        Guard &g=pos->second;
        ++replies[g.first_digit][s][q]; ++by_prefix[g.prefix][1+2*s+q]; g.returns[s]=t;
        if (s==2) {
            if (!first.seed) first=g;
            if (!longest.seed || (t-g.returns[1])>(longest.returns[2]-longest.returns[1]))
                longest=g;
        }
        if (q==1 || s==2) open.erase(pos);
        else ++g.stage;
    }
};

int main(int argc,char **argv) try {
    bool profile = argc==4 && std::string(argv[3])=="profile";
    if (argc!=3 && !profile) throw std::runtime_error("usage: spaghetti_guard A|B RAW_TARGET [profile]");
    std::string seed=argv[1], num=argv[2];
    Count target{};
    auto parse=std::from_chars(num.data(),num.data()+num.size(),target);
    if ((seed!="A" && seed!="B") || parse.ec!=std::errc{} || parse.ptr!=num.data()+num.size()
            || target<0 || target>(Count(1)<<60)) throw std::runtime_error("invalid seed or target");
    for (int d=0;d<2;++d) for (int q=0;q<2;++q) for (int s=0;s<4;++s) {
        int actual=(!d && s==3)?4:s;
        const char *r=machine+16*q+3*actual;
        if (*r!='-') rules[d][q][s]={std::min(r[0]-'0',3),r[1]=='R'?1:-1,r[2]-'A'};
    }
    for (int q=0;q<2;++q) for (int dir:{-1,1}) {
        auto &table=small[2*q+(dir==1)];
        table.reserve(65536);
        for (Word i=0;i<65536;++i)
            table.push_back(trace(i,8,dir==1?0:7,dir,q,1024,Ignore{}));
    }

    std::vector<Word> positive,negative;
    auto get=[&](Count b) -> Word {
        const auto &v=b<0?negative:positive;
        auto i=std::size_t(b<0?-1-b:b);
        return i<v.size()?v[i]:0;
    };
    Count head=0, steps=0, calls=0, detailed=0, least=0, first_least=0;
    int dir=1,q=seed[0]-'A';
    Tally tally;
    while (steps<target) {
        Count block=head>=0?head/width:-1-(-1-head)/width;
        int pos=int(head-block*width);
        Word w=get(block);
        bool edge=(dir==1 && pos==0) || (dir==-1 && pos==width-1);
        Exit a=edge?lookup(w,dir,q):trace(w,width,pos,dir,q,1024,Ignore{});
        bool outside=a.edge && digit(get(block-1),15)==1;
        if (a.inside || outside || a.steps>target-steps) {
            int budget=int(std::min<Count>(target-steps,a.steps));
            // go precisely to the summarized stop, also if an inner table
            // exhausted its local budget. The undefined instruction has no cost.
            auto note=[&](const Exit &cur,int s) {
                if (cur.pos==0 && !outside) return;
                int right=cur.pos==15 ? digit(get(block+1),0) : digit(cur.word,cur.pos+1);
                int prefix=0;
                if (profile && cur.dir==1) {
                    for (int j=1;j<=4;++j) {
                        int i=cur.pos+j;
                        int d=i<width ? digit(cur.word,i) : digit(get(block+1),i-width);
                        prefix=4*prefix+d;
                    }
                }
                // The launching A0 scanned cell-1 one instruction earlier.
                // All sites previously visited form an interval containing zero.
                Count low=block*width+cur.low;
                Count first=low<least ? steps+cur.first_low : first_least;
                bool fresh=std::min(low,least)==block*width+cur.pos-1 && first==steps+cur.steps-1;
                tally.record(block*width+cur.pos,steps+cur.steps,cur.dir,cur.q,s,right,prefix,fresh);
            };
            auto exact=trace(w,width,pos,dir,q,budget,note);
            if (exact.steps==a.steps && (exact.word!=a.word || exact.dir!=a.dir ||
                    exact.pos!=a.pos || exact.q!=a.q || exact.low!=a.low ||
                    exact.first_low!=a.first_low)) throw std::logic_error("guard replay mismatch");
            exact.halted=a.halted && exact.steps==a.steps;
            a=exact; ++detailed;
        }
        auto &v=block<0?negative:positive;
        auto i=std::size_t(block<0?-1-block:block);
        if (i>=v.size()) v.resize(i+1);
        v[i]=a.word;
        if (block*width+a.low<least) { least=block*width+a.low; first_least=steps+a.first_low; }
        head=block*width+a.pos; q=a.q; dir=a.dir; steps+=a.steps; ++calls;
        if (a.halted) break;
    }
    std::cout<<steps<<' '<<head<<' '<<q<<' '<<dir<<' '<<calls<<' '<<detailed<<'\n';
    for (int d:{0,2,3}) {
        std::cout<<d<<' '<<tally.seeds[d];
        for(auto &row:tally.replies[d]) for(auto c:row) std::cout<<' '<<c;
        std::cout<<'\n';
    }
    auto show=[&](const Guard &g) {
        std::cout<<g.cell<<' '<<g.seed<<' '<<g.first_digit<<' '<<g.stage;
        for (auto t:g.returns) std::cout<<' '<<t;
        std::cout<<'\n';
    };
    show(tally.first); show(tally.longest);
    std::cout<<tally.open.size()<<'\n';
    for (auto &[_,g]:tally.open) show(g);
    Count left=-Count(negative.size())*width, end=Count(positive.size())*width;
    std::cout<<left<<'\n';
    for (Count x=left; x<end; ++x) {
        Count b=x>=0?x/width:-1-(-1-x)/width;
        int s=digit(get(b),int(x-b*width));
        bool left_side = x<head || (x==head && dir==-1);
        std::cout<<char('0'+(s==3 && left_side?4:s));
    }
    std::cout<<'\n';
    for (int k=0;profile && k<256;++k) if (tally.by_prefix[k][0]) {
        for (int j=3;j>=0;--j) std::cout<<digit(k,j);
        for (auto count:tally.by_prefix[k]) std::cout<<' '<<count;
        std::cout<<' '<<tally.fresh_launches[k]<<'\n';
    }
} catch(const std::exception &e) { std::cerr<<e.what()<<'\n'; return 2; }
