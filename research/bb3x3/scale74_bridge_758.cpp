// Verify a band of post-change scale-74 reset offsets using exact GMP arithmetic.
// c++ -std=c++17 -O3 scale74_bridge_758.cpp -lgmpxx -lgmp -o scale74_bridge_758
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
#include <gmpxx.h>

using Big = mpz_class;
using Offset = std::int64_t;
constexpr int period = 32768;
const Big origin("1865347548659819442523519543121952886355592304");
constexpr Offset initial = 812, far_end = 1'000'000'000'000LL;

void check(bool condition, const char* message) {
    if (!condition) throw std::runtime_error(message);
}

struct State { Big a, c; };
struct Head { Big c; Offset selector; int gain; };
struct Trace { int initial_bulk; std::string word; int increment, bound; };
struct BulkBlock { unsigned c, gain; };

void jump(State& s) {
    check(s.a <= s.c && mpz_odd_p(s.a.get_mpz_t()), "jump guard");
    s.c -= s.a-1;
    s.a = 3*s.a+2;
}

void bulk(State& s) {
    Big q = (s.c+1)/4;
    check(mpz_odd_p(s.c.get_mpz_t()) && s.a >= 4*q+3, "bulk guard");
    s.a -= 4*q+3;
    s.c = 6*q+5;
}

class LocalMap {
    std::vector<Big> powers{1};
    Big h, delta_c;
    Offset scaled_mass;
    int shift;
    std::array<Head,period> heads{};
    std::array<int,128> batch_length{};
    std::array<std::array<BulkBlock,8192>,13> blocks{};

    std::pair<Big,int> launch(Offset z, bool guarded) const {
        Big seed = h-origin+z;
        State s{2*powers[292]-1, seed-powers[292]+585};
        check(s.c >= 1, "leading jumps");
        for (int i=0; i<14; ++i) {
            if (i==8) jump(s);
            bulk(s);
        }
        int gain = mpz_class(s.a+2*s.c-2*seed-1).get_si();
        Big next_c = s.c-(s.a+1)*((powers[191]-1)/2)+382;
        if (guarded) check(next_c>=1, "191-jump guard");
        return {next_c,gain+764};
    }

public:
    LocalMap() {
        for (int i=0; i<405; ++i) powers.push_back(3*powers.back());
        h=(powers[307]-8282708212L)/13959275;
        Big twice=2*h;
        shift=int(mpz_sizeinbase(twice.get_mpz_t(),2))-54;
        scaled_mass=mpz_class(twice>>shift).get_si();
        delta_c=period+27918550*powers[191];
        for (int r=0; r<period; r+=2) {
            auto [c,g]=launch(r,false);
            auto [cc,gg]=launch(r+period,false);
            check(cc==c+delta_c && gg==g,"prefix translation");
            Big fixed, numerator=(c-r)<<32;
            mpz_fdiv_q(fixed.get_mpz_t(),numerator.get_mpz_t(),powers[191].get_mpz_t());
            check(mpz_fits_slong_p(fixed.get_mpz_t()),"selector too large");
            heads[r]={c,fixed.get_si(),g};
        }
        launch(initial,true);
        launch(far_end,true);
        // Pick an even number of initial bulks using an exact integer index.
        // The actual guards below are checked independently of this choice.
        for (int e=0; e<128; ++e) {
            int n=0;
            while (n+2<=400) {
                Big v=(powers[n+2]*powers[191])<<(60+e);
                v>>=32+shift+n+2;
                if ((v<<51)>=(Big(scaled_mass-100)<<58)) break;
                n+=2;
            }
            batch_length[e]=n;
        }
        for (unsigned l=1; l<=12; ++l) {
            for (unsigned r=1; r<(1U<<(l+1)); r+=2) {
                unsigned c=r,g=0;
                for (unsigned j=0; j<l; ++j) {
                    g+=c%4==3?9:5;
                    c=6*((c+1)/4)+5;
                }
                blocks[l][r]={c,g};
            }
        }
    }

    Trace probe(Offset z) const {
        int r=int(z%period);
        Offset k=z/period;
        const Head& q=heads[r];
        Big selector=((Big(k)*27918550)<<32)+q.selector;
        check(selector>0,"nonpositive selector");
        int e=std::max(0,int(mpz_sizeinbase(selector.get_mpz_t(),2))-51);
        check(e<128,"selector exceeds table");
        int n=batch_length[e], gain=q.gain;
        Big c=q.c+delta_c*k, starting_mass=2*(h-origin+z)+1;
        check(c>0,"191-jump endpoint");
        for (int j=0; j<n; j+=12) {
            int l=std::min(12,n-j), mask=(1<<(l+1))-1;
            const auto& item=blocks[l][c.get_ui()&mask];
            c=(c>>(l+1))*(2*powers[l])+item.c;
            gain+=int(item.gain);
            check(starting_mass+gain-2*c>1,"bulk block guard");
        }
        State s{starting_mass+gain-2*c,c};
        int bound=4*484+9*(14+n);
        std::string word;
        for (int i=0;i<10000;++i) {
            if (s.a<=s.c) {
                if (mpz_even_p(s.a.get_mpz_t())) return {n,word,(gain+5)/2,(bound+5)/2};
                jump(s); gain+=4;bound+=4;word+='J';
            } else if (s.a-s.c >= (s.c.get_ui()%4==3?4:2)) {
                gain+=s.c.get_ui()%4==3?9:5;
                bulk(s);bound+=9;word+='L';
            } else {
                check(mpz_odd_p(s.a.get_mpz_t()) && s.a==s.c+2 && s.c.get_ui()%4==3,
                      "halting terminal reached");
                s.a=3*s.c+8;s.c=1;gain+=8;bound+=8;word+='E';
            }
        }
        throw std::runtime_error("tail budget exceeded");
    }
};

struct Result { std::uint64_t nodes=0, leaves=0; int max_bound=0; };
void cover(const LocalMap& map,Offset lo,Offset hi,const Trace& l,const Trace& r,Result& result) {
    ++result.nodes;
    if (l.initial_bulk==r.initial_bulk && l.word==r.word) {
        ++result.leaves;
        result.max_bound=std::max(result.max_bound,l.bound);
        return;
    }
    check(lo<hi,"singleton inconsistency");
    Offset mid=lo+2*((hi-lo)/4);
    cover(map,lo,mid,l,mid==lo?l:map.probe(mid),result);
    cover(map,mid+2,hi,mid+2==hi?r:map.probe(mid+2),r,result);
}

int main(int argc,char** argv) {
    if (argc!=3) { std::cerr<<"Usage: scale74_bridge_758 LOW HIGH\n";return 2; }
    try {
        Offset lo=std::stoll(argv[1]),hi=std::stoll(argv[2]);
        check(lo>=initial && hi<=far_end && lo<=hi && lo%2==0 && hi%2==0,"bad band");
        LocalMap map;Result r;
        cover(map,lo,hi,map.probe(lo),map.probe(hi),r);
        std::cout<<lo<<' '<<hi<<' '<<r.nodes<<' '<<r.leaves<<' '<<r.max_bound<<'\n';
    } catch (const std::exception& e) {std::cerr<<e.what()<<'\n';return 1;}
}
