// Prove a near-H gateway segment for BB(3,3) #758. Requires GMP and C++17.
// c++ -O3 -std=c++17 gateway_758.cpp -lgmpxx -lgmp -o gateway_758
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>
#include <gmpxx.h>

using Big = mpz_class;
using Distance = std::int64_t;
constexpr Distance input_width = 5000;
constexpr Distance direct_span = 250000;
constexpr int period = 1 << 15;

void require(bool condition, const char* message) {
    if (!condition) throw std::runtime_error(message);
}

struct State { Big a, c; };
struct Prefix { Distance a; int gain; };
struct Ending {
    int jumps;
    int increment;  // zero denotes a halt
    int bound;
    std::string word;
};

bool odd(const Big& x) { return mpz_odd_p(x.get_mpz_t()); }

void bulk(State& s, int& gain, bool guarded) {
    Big q = (s.c + 1)/4;
    if (guarded) require(odd(s.c) && s.a >= 4*q+3, "bulk guard");
    gain += mpz_tstbit(s.c.get_mpz_t(), 1) ? 9 : 5;
    s.a -= 4*q+3;
    s.c = 6*q+5;
}

void jump(State& s, int& gain, bool guarded) {
    if (guarded) require(odd(s.a) && odd(s.c) && s.a <= s.c, "jump guard");
    s.c -= s.a-1;
    s.a = 3*s.a+2;
    gain += 4;
}

class LocalMap {
    std::vector<Big> powers{1};
    Big H;
    std::array<Prefix,period> heads{};
    std::array<int,64> even_gain{};
    Distance slope = 0;
    Distance low, high;

    Prefix odd_head(Distance d, bool guarded) const {
        // Apply J^292 from A(1,H-d). Positivity of the last right counter
        // implies legality of every J because c' = c-a+1 and a increases.
        State s{2*powers[292]-1, H-d-powers[292]+585};
        if (guarded) require(s.c >= 1, "initial 292 jumps");
        int gain = 4*292;
        for (int i=0; i<14; ++i) {
            if (i==8) jump(s, gain, guarded);
            bulk(s, gain, guarded);
        }
        require(mpz_fits_slong_p(s.a.get_mpz_t()), "prefix exceeds long");
        return {s.a.get_si(), gain};
    }

    int even_return(Distance d) const {
        // I followed by 291 J's from the even reset; check their common guard.
        Big p = 2*powers[291];
        State s{2*p-1, H-d-p+2*291+5};
        require(s.c >= 1, "initial 291 jumps");
        int gain = 8+4*291;
        for (char letter : std::string("LLJLLJL")) {
            if (letter=='L') bulk(s,gain,true);
            else jump(s,gain,true);
        }
        require(!odd(s.a) && s.a <= s.c, "even return guard");
        return (gain+5)/2;
    }

public:
    LocalMap(Distance near, Distance far): low(near), high(far) {
        require(sizeof(long)>=8 && low>=1000000 && high<=11000000000000L,
                "supported distance range is 10^6 to 11*10^12 on LP64");
        while (powers.size()<310) powers.push_back(3*powers.back());
        require((powers[307]-8282708212L)%13959275==0, "halting seed");
        H = (powers[307]-8282708212L)/13959275;
        // Evaluate the word without guards at the canonical representatives.
        // A translation by period preserves all 14 bulk residues and induces
        // exactly the same affine displacement for every representative.
        for (int r=0; r<period; r+=2) heads[r]=odd_head(r,false);
        slope = odd_head(period,false).a-heads[0].a;
        require(slope>0, "prefix direction");
        for (int r=0; r<period; r+=2) {
            Prefix shifted=odd_head(r+period,false), base=heads[r];
            require(shifted.a-base.a==slope && shifted.gain==base.gain,
                    "periodic prefix");
            Big extreme=Big(slope)*(high/period)+base.a+1;
            require(mpz_fits_slong_p(extreme.get_mpz_t()) && extreme>0,
                    "fixed-width prefix bound");
        }
        for (Distance d : {low+low%2, high-high%2}) {
            Prefix actual = odd_head(d,true), base=heads[d%period];
            require(actual.a==base.a+slope*(d/period) && actual.a>1,
                    "odd endpoint");
        }
        for (int r=1; r<64; r+=2) {
            Distance d=low+(r-low%64+64)%64;
            even_gain[r]=even_return(d);
            require(0<even_gain[r] && even_gain[r]<=615,"even increment");
        }
        even_return(low+(low%2==0));
        even_return(high-(high%2==0));
    }

    Ending probe(Distance d) const {
        require(low<=d && d<=high && !(d%2), "odd seed outside segment");
        Prefix h=heads[d%period];
        Distance u=h.a+slope*(d/period)+1;
        require(u>1, "post-prefix counter");
        Big total=2*H-2*d+h.gain+2;  // current mass plus one
        Big threshold=total/u;
        int k=int(std::upper_bound(powers.begin(),powers.end(),threshold)
                  -powers.begin())-1;
        require(k>=0 && k+1<int(powers.size()), "jump batch range");
        Big a=powers[k]*u-1;
        State s{a, (total-a-1)/2+2*k};
        int gain=h.gain+4*k, bound=4*(293+k)+9*14;
        std::string word;
        for (int i=0; i<10000; ++i) {
            if (s.a<=s.c) {
                if (!odd(s.a)) return {k,(gain+5)/2,(bound+5)/2,word};
                jump(s,gain,true);
                bound+=4; word+='J';
            } else {
                Big q=(s.c+1)/4;
                if (s.a>=4*q+3) {
                    bulk(s,gain,true);
                    bound+=9; word+='L';
                } else if (!odd(s.a)) {
                    return {k,0,(bound+5)/2,word};
                } else {
                    require(s.a==s.c+2 && s.c%4==3,"exceptional guard");
                    s={3*s.c+8,1};
                    gain+=8; bound+=8; word+='E';
                }
            }
        }
        throw std::runtime_error("trace limit exhausted");
    }

    int increment(Distance d) const {
        return d%2 ? even_gain[d%64] : probe(d).increment;
    }
};

class Crossing {
    LocalMap map;
    std::set<Distance,std::greater<Distance>> possible;
    Distance nodes=0, calls=0, halts=0;
    int max_gain=0;

    void walk(Distance far, Distance near) {
        if (possible.empty() || *possible.begin()<near) return;
        ++nodes;
        Distance odd_left=far-far%2, odd_right=near+near%2;
        int cap=615;
        if (odd_right<=odd_left) {
            Ending l=map.probe(odd_left), r=map.probe(odd_right);
            cap=(l.jumps==r.jumps && l.word==r.word) ? std::max(cap,l.bound) : 0;
        }
        if (cap) {
            // Continuing resets advance, so they eventually leave this finite
            // block. Every first exit is within cap of the near boundary.
            while (!possible.empty() && *possible.begin()>=near)
                possible.erase(possible.begin());
            for (int i=1; i<=cap; ++i) possible.insert(near-i);
            max_gain=std::max(max_gain,cap);
        } else if (far-near>direct_span) {
            Distance mid=near+(far-near)/2;
            walk(far,mid+1);
            walk(mid,near);
        } else {
            while (!possible.empty() && *possible.begin()>=near) {
                Distance d=*possible.begin();
                possible.erase(possible.begin());
                ++calls;
                int delta=map.increment(d);
                require(delta>=0,"negative increment");
                if (delta==0) ++halts;
                else possible.insert(d-delta);
                max_gain=std::max(max_gain,delta);
            }
        }
    }

public:
    Crossing(Distance far,Distance near): map(near,far) {
        for (int j=0; j<=input_width; ++j) possible.insert(far-j);
        walk(far,near);
        std::cout<<"nodes "<<nodes<<" returns "<<calls<<" halts "<<halts
                 <<" remaining "<<possible.size()<<" maxgain "<<max_gain;
        if (!possible.empty()) {
            require(*possible.rbegin()>=near-input_width && *possible.begin()<near,
                    "exit outside next gateway");
            std::cout<<" exits "<<*possible.rbegin()<<".."<<*possible.begin();
        }
        std::cout<<'\n';
    }
};

int main(int argc,char** argv) {
    if (argc!=3) { std::cerr<<"Usage: gateway_758 FAR NEAR\n"; return 2; }
    try {
        Distance far=std::stoll(argv[1]),near=std::stoll(argv[2]);
        require(near>=1000000 && near<=far && far<=11000000000000L && far-near>=5000,
                "invalid segment endpoints");
        Crossing check(far,near);
    } catch (const std::exception& e) {
        std::cerr<<e.what()<<'\n'; return 1;
    }
}
