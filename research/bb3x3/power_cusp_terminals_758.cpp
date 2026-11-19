// Search every direct ordinary terminal after the maximal initial bulk-pair run.
// c++ -O3 -std=c++17 power_cusp_terminals_758.cpp -lgmpxx -lgmp -o cusp_terminals
#include <algorithm>
#include <array>
#include <cstdint>
#include <gmpxx.h>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using Big = mpz_class;
struct Strip { Big slope,den,low,high; };

Strip inverse_pair(const Strip& s) {
    return {4*s.slope,9*s.den,4*s.low+36*s.slope-35*s.den,4*s.high+20*s.slope-20*s.den};
}

Strip inverse_jump(const Strip& s) {
    return {s.slope+s.den,3*s.den,s.low+2*s.slope-s.den,s.high+2*s.slope-s.den};
}

constexpr unsigned gains[]={5,9,7,7}, shifts[]={20,35,26,29};
constexpr unsigned pack=8, modulus=1u<<(2*pack), multiplier=43046721; // 9^8
struct Block { unsigned d,gain; };
std::vector<Block> table(modulus);

void prepare() {
    for (unsigned r=0;r<modulus;++r) {
        unsigned d=r,gain=0;
        for (unsigned i=0;i<pack;++i) {
            const auto j=d%4;
            d=(9*d+shifts[j])/4;
            gain+=gains[j];
        }
        table[r]={d,gain};
    }
}

void apply_pairs(Big& u,Big& d,unsigned count) {
    for (unsigned i=0;i<count/pack;++i) {
        const auto& block=table[d.get_ui()&(modulus-1)];
        d>>=2*pack;
        d*=multiplier;
        d+=block.d;
        u+=block.gain;
    }
    for (unsigned i=0;i<count%pack;++i) {
        const auto r=d.get_ui()%4;
        d=(9*d+shifts[r])/4;
        u+=gains[r];
    }
}

const Big power=[] { Big p; mpz_ui_pow_ui(p.get_mpz_t(),3,292); return p; }();
const Big target=(power*14348907-8282708212L)/13959275;
const Big last_checkpoint("21421649218912165665535344121134262578863444101821100068564006584690782511736332469949435004280779519313100689676802573076028282212569704429");

struct Group {
    Big h, xlow, xhigh;
    unsigned maximum_pairs=0, opening_gain=0;
    bool secondary=false;
    // On secondary input x=seed-last_checkpoint, u=last_checkpoint+x+g
    // and 512*d=19171*x+beta. The representative stores d at the lane's origin.
    struct Lane { Big d; unsigned gain; };
    std::array<Lane,256> lanes;
    Big beta_low,beta_high;
    unsigned gain_low=0,gain_high=0;

    void prepare_secondary() {
        secondary=true;
        h=last_checkpoint;
        xlow=0;
        xhigh=target-h;
        for (unsigned i=0;i<256;++i) {
            Big x=2*i;
            Big u=h+x+584,d=(u-power)/2;
            apply_pairs(u,d,4);
            if (2*d+1>=u) throw std::runtime_error("secondary initial pairs");
            d=3*d-u+1; u+=2;
            if (d<0 || 2*d+1>=u) throw std::runtime_error("secondary initial jump");
            const Big gain=u-h-x, beta=512*d-19171*x;
            lanes[i]={d,static_cast<unsigned>(gain.get_ui())};
            if (i==0 || beta<beta_low) beta_low=beta;
            if (i==0 || beta>beta_high) beta_high=beta;
            if (i==0 || lanes[i].gain<gain_low) gain_low=lanes[i].gain;
            if (i==0 || lanes[i].gain>gain_high) gain_high=lanes[i].gain;
        }
        // The extremal odd origins certify the guarded prefix by counter order.
        for (const Big& seed : {last_checkpoint,target}) {
            Big u=seed+584, d=(u-power)/2;
            apply_pairs(u,d,4);
            if (2*d+1>=u) throw std::runtime_error("upper initial pairs");
            d=3*d-u+1; u+=2;
            if (d<0 || 2*d+1>=u) throw std::runtime_error("upper initial jump");
            const auto coordinates=state(seed-last_checkpoint);
            if (coordinates.first!=u || coordinates.second!=d) throw std::runtime_error("secondary lane");
            apply_pairs(u,d,2);
            if (2*d+1>=u) throw std::runtime_error("secondary compulsory pairs");
        }
    }

    std::pair<Big,Big> state(const Big& x) const {
        if (!secondary) return {h+x,x/2};
        const Lane& lane=lanes[(x.get_ui()%512)/2];
        return {h+x+lane.gain,lane.d+19171*(x/512)};
    }

    void bounds(const Strip& s, Big& den, Big& lo, Big& hi) const {
        if (secondary) {
            den=19171*s.den-512*s.slope;
            const Big center=512*s.slope*h;
            lo=center+512*(s.low+s.slope*gain_low)-s.den*beta_high;
            hi=center+512*(s.high+s.slope*gain_high)-s.den*beta_low;
        } else {
            den=s.den-2*s.slope;
            const Big center=2*s.slope*h;
            lo=center+2*s.low;
            hi=center+2*s.high;
        }
    }
};

struct Tail { unsigned bits,length,jumps,pairs; };

class Search {
    std::vector<Group> groups;
    std::vector<Big> powers{1};
    std::uint64_t classes=0,candidates=0,filtered=0,hits=0;

    bool reaches_terminal(Big u,Big d,const Tail& tail) const {
        if (tail.jumps) {
            Big h=u-2*d;
            u+=2*tail.jumps;
            d=(u-powers[tail.jumps]*h)/2;
            if (d<0) return false;
        }
        if (tail.pairs) {
            apply_pairs(u,d,tail.pairs);
            if (2*d+1>=u) return false;
        }
        for (unsigned i=0;i<tail.length;++i) {
            if ((tail.bits>>i)&1) apply_pairs(u,d,1);
            else { d=3*d-u+1; u+=2; }
            if (d<0 || 2*d+1>=u) return false;
        }
        const Big a=2*u-4*d-1, q=(d+1)/2;
        return a==10*q+9 || (mpz_odd_p(q.get_mpz_t()) && a==10*q+11);
    }

    void test(const Strip& tail_strip,const Tail& tail) {
        std::vector<Strip> strips;
        strips.reserve(groups[0].maximum_pairs+1);
        strips.push_back(tail_strip);
        for (unsigned b=0;b<=groups[0].maximum_pairs;++b) {
            const auto& st=strips[b];
            for (const auto& group:groups) {
                // A word starting with J cannot meet the reset launch cone at b=0:
                // in that case its denominator can be positive but very small.
                if (b>group.maximum_pairs) continue;
                ++classes;
                Big denominator, low_num, high_num;
                group.bounds(st,denominator,low_num,high_num);
                if (denominator<=0) throw std::runtime_error("invalid launch denominator");
                if (high_num<group.xlow*denominator || low_num>group.xhigh*denominator) continue;
                Big l,r;
                mpz_cdiv_q(l.get_mpz_t(),low_num.get_mpz_t(),denominator.get_mpz_t());
                mpz_fdiv_q(r.get_mpz_t(),high_num.get_mpz_t(),denominator.get_mpz_t());
                if (l<group.xlow) l=group.xlow;
                if (r>group.xhigh) r=group.xhigh;
                if (mpz_odd_p(l.get_mpz_t())) ++l;
                for (Big x=l;x<=r;x+=2) {
                    ++candidates;
                    auto [u,d]=group.state(x);
                    const unsigned front=std::min(pack,b);
                    apply_pairs(u,d,front);
                    if (2*d+1>=u) continue;
                    const auto& remaining=strips[b-front];
                    const Big offset=remaining.den*d-remaining.slope*u;
                    if (offset<remaining.low || offset>remaining.high) continue;
                    ++filtered;
                    apply_pairs(u,d,b-front);
                    if (2*d+1>=u || !reaches_terminal(u,d,tail)) continue;
                    ++hits;
                    std::cout<<group.h+x-group.opening_gain<<' '<<b<<' '<<tail.length
                             <<' '<<tail.bits<<' '<<tail.jumps<<' '<<tail.pairs<<'\n';
                }
            }
            if (b<groups[0].maximum_pairs) strips.push_back(inverse_pair(st));
        }
    }

    void traverse(const Strip& s,unsigned bits,unsigned n,unsigned depth) {
        // Any leading pairs are already included in b. Every nonempty tail starts with a jump.
        if (n==0 || !(bits&1)) test(s,{bits,n,0,0});
        if (n==depth) return;
        traverse(inverse_jump(s),bits<<1,n+1,depth);
        traverse(inverse_pair(s),(bits<<1)|1,n+1,depth);
    }

public:
    explicit Search(bool secondary) : groups(secondary?1:2) {
        for (unsigned even=0;even<groups.size();++even) {
            auto& g=groups[even];
            if (secondary) g.prepare_secondary();
            else {
                g.h=even?2*(power/3):power;
                g.opening_gain=even?586:584;
                g.xlow=power+even+g.opening_gain-g.h;
                g.xhigh=target+g.opening_gain-g.h;
            }
            auto [u,d]=g.state(g.xlow);
            while (true) {
                apply_pairs(u,d,1);
                if (2*d+1>=u) break;
                ++g.maximum_pairs;
            }
            if (groups[0].maximum_pairs<g.maximum_pairs) throw std::runtime_error("group bound");
        }
        for (unsigned j=1;j<=293;++j) powers.push_back(3*powers.back());
    }

    void words(unsigned depth) { traverse({2,9,-17,-10},0,0,depth); }

    void runs() {
        const Big mass=target+std::max(586u,groups[0].gain_high)+9*groups[0].maximum_pairs+2*293;
        if (powers[293]<=mass) throw std::runtime_error("jump bound");
        Big d=0,u=mass;
        unsigned max_pairs=0;
        while (true) {
            apply_pairs(u,d,1);
            if (2*d+1>=mass+9*(max_pairs+1)) break;
            ++max_pairs;
        }
        std::cerr<<"jump limit 292, trailing-pair limit "<<max_pairs<<'\n';
        Strip last{2,9,-17,-10};
        test(last,{0,0,0,0});
        for (unsigned f=0;f<=max_pairs;++f) {
            auto s=last;
            for (unsigned j=1;j<=292;++j) {
                s=inverse_jump(s);
                test(s,{0,0,j,f});
            }
            last=inverse_pair(last);
        }
    }

    void report() const {
        std::cerr<<"max_initial_pairs "<<groups[0].maximum_pairs<<' '<<(groups.size()==2?groups[1].maximum_pairs:0)
                 <<" classes "<<classes<<" candidates "<<candidates<<" after_filter "<<filtered
                 <<" hits "<<hits<<'\n';
    }
};

int main(int argc,char** argv) {
    if (argc!=2) { std::cerr<<"usage: cusp_terminals DEPTH | --runs | --secondary-runs\n"; return 2; }
    try {
        prepare();
        const bool secondary=std::string(argv[1])=="--secondary-runs";
        Search search(secondary);
        if (secondary || std::string(argv[1])=="--runs") search.runs();
        else {
            const unsigned depth=std::stoul(argv[1]);
            if (depth>25) throw std::runtime_error("depth must be 0 through 25");
            search.words(depth);
        }
        search.report();
    } catch (const std::exception& e) { std::cerr<<e.what()<<'\n'; return 1; }
}
