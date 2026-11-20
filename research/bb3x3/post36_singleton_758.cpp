// On-demand common-word skips from one known reset above 3^36.
// c++ -O3 -std=c++17 post36_singleton_758.cpp -o post36_singleton
#include "packed_return_758.hpp"
#include <array>
#include <set>
#include <stdexcept>

constexpr Num post36_power = 150'094'635'296'999'121LL;
constexpr Num post36_limit = post36_power + post36_power/10;
constexpr Num post36_ceiling = post36_limit + 100'000;
constexpr Num post36_probe_width = 250'000;
constexpr unsigned post36_merge_budget = 16'384;
inline Num post36_keep(Num s) { return s; }

// The live set spans less than 2^16 consecutive seed positions. Deleting
// its minimum and inserting a successor less than 2^16 farther preserves
// that invariant. Full coordinates disambiguate the circular bit positions.
class Post36Ring {
    static constexpr Num width=65'536;
    std::array<std::uint64_t,1024> bits{};
    unsigned count=0;
    Num low=0, high=0;
#ifdef POST36_SHADOW_REFERENCE
    std::set<Num> shadow;
    void check() const {
        if (shadow.size()!=count || (count && (*shadow.begin()!=low || *shadow.rbegin()!=high)))
            throw std::logic_error("ring/reference mismatch");
    }
#endif
public:
    unsigned size() const { return count; }
    bool empty() const { return count==0; }
    Num first() const { return low; }
    void insert(Num seed) {
        if (count && std::max(high,seed)-std::min(low,seed)>=width)
            throw std::runtime_error("merger exceeds circular-bitset span");
        auto& word=bits[(seed>>6)&1023];
        auto mask=std::uint64_t{1}<<(seed&63);
        if (!(word&mask)) {
            word|=mask;
            if (!count) low=high=seed;
            else { low=std::min(low,seed); high=std::max(high,seed); }
            ++count;
        }
#ifdef POST36_SHADOW_REFERENCE
        shadow.insert(seed);
        check();
#endif
    }
    Num pop() {
        if (!count) throw std::logic_error("empty merger");
        Num seed=low;
        bits[(seed>>6)&1023]&=~(std::uint64_t{1}<<(seed&63));
        if (--count) {
            Num i=seed>>6;
            auto word=bits[i&1023]&(~std::uint64_t{0}<<(seed&63));
            while (!word) word=bits[(++i)&1023];
            low=64*i+__builtin_ctzll(word);
        } else low=high=0;
#ifdef POST36_SHADOW_REFERENCE
        shadow.erase(seed);
        check();
#endif
        return seed;
    }
};

class Post36 {
    PackedReturn<0, 2*(post36_power/3), 74, post36_ceiling, 3, post36_keep> even;
    PackedReturn<1, post36_power, 72, post36_ceiling, 3, post36_keep> odd;
    Cover proof;
    std::uint64_t direct_calls=0, merge_calls=0, joins=0;
    Num saved_width=0;

    Num next(Num seed) {
        if (seed < post36_power || seed > post36_limit)
            throw std::runtime_error("outside the verified power-36 launch interval");
        Num result = seed%2 ? odd.get(seed) : even.get(seed);
        if (result <= seed) throw std::runtime_error("nonincreasing return");
        return result;
    }

    // Close the reachable parity set under the selected common-word returns.
    // A zero bound is harmless only when that parity cannot be reached.
    bool bounds(Num low, Num high, std::array<int,2>& cap, int& mask) const {
        cap={};
        mask=1<<(low%2);
        for (int pass=0; pass<2; ++pass) {
            for (int parity=0; parity<2; ++parity) {
                if (!(mask & (1<<parity))) continue;
                if (!cap[parity]) {
                    Num a=low+(low%2!=parity), b=high-(high%2!=parity);
                    if (a>b) return false;
                    cap[parity]=proof.bound(a,b);
                    if (cap[parity]<=0) return false;
                }
                mask|=1<<((parity+cap[parity])%2);
            }
        }
        return true;
    }

    bool join(Num end, const std::array<int,2>& cap, int mask, Num& result) {
        Post36Ring live;
        for (int p=0; p<2; ++p) {
            if (!(mask & (1<<p))) continue;
            int parity=(p+cap[p])%2;
            Num first=end+1;
            if (first%2!=parity) ++first;
            for (Num s=first; s<=end+cap[p]; s+=2) live.insert(s);
        }
        if (live.empty()) throw std::logic_error("empty exit enclosure");
        unsigned count=0;
        while (live.size()>1 && count<post36_merge_budget) {
            Num s=live.pop();
            Num result=next(s);
            if (result-s>=65'536) throw std::runtime_error("return exceeds merger span");
            live.insert(result);
            ++count;
        }
        merge_calls+=count;
        if (live.size()!=1) return false;
        result=live.first();
        return true;
    }

    static Num slow(Num seed) {
        State s=seed%2 ? State{5,seed} : State{3,seed+3};
        for (int i=0; i<10'000; ++i) {
            if (s.a==1) return s.c;
            Branch action=branch(s);
            if (action==halted) return -1;
            if (action==returned) return s.a/2+s.c+2;
            s=advance(s,action);
        }
        throw std::runtime_error("literal audit budget");
    }

public:
    Post36() {
        even.reset(post36_power,post36_limit);
        odd.reset(post36_power,post36_limit);
    }

    void audit() {
        // Force word and full-ring wraparound, duplicates, and the span guard.
        Post36Ring ring;
        std::set<Num> reference;
        Num base=(post36_power & ~Num{65'535})+65'500;
        for (Num offset : {0,3,19,37,63,256,1024,32767,65535}) {
            ring.insert(base+offset);
            reference.insert(base+offset);
        }
        for (int i=0; i<10'000; ++i) {
            Num expected=*reference.begin();
            reference.erase(reference.begin());
            if (ring.pop()!=expected) throw std::logic_error("circular order mismatch");
            ring.insert(expected+65'535);
            reference.insert(expected+65'535);
            if (ring.size()!=reference.size() || ring.first()!=*reference.begin())
                throw std::logic_error("circular set mismatch");
        }
        bool refused=false;
        try { ring.insert(ring.first()+65'536); }
        catch (const std::runtime_error&) { refused=true; }
        if (!refused) throw std::logic_error("missing circular span guard");
        std::cout<<"10,000 circular-merger updates agree with the ordered-set reference.\n";
        // Cover both parities near the cusp and across the supported interval.
        std::uint64_t random=0x32758758;
        for (int i=0; i<10'000; ++i) {
            random=random*6364136223846793005ULL+1442695040888963407ULL;
            Num s=i<5'000 ? post36_power+i :
                post36_power+Num(random%std::uint64_t(post36_limit-post36_power));
            if (next(s)!=slow(s)) throw std::runtime_error("literal mismatch");
        }
        std::cout<<"10,000 packed returns agree with literal counter calls.\n";
    }

    void link(Num start, Num goal) {
        if (start<post36_power || goal<=start || goal>post36_limit-1'000'000)
            throw std::runtime_error("require an increasing link inside the power-36 interval");
        Num seed=start;
        while (seed<goal) {
            Num first_end=std::min(goal-1,seed+post36_probe_width);
            std::array<int,2> cap{};
            int mask=0;
            bool jumped=false;
            if (bounds(seed,first_end,cap,mask)) {
                Num good=first_end, bad=goal;
                Num span=first_end-seed+1;
                while (good+1<goal) {
                    Num trial=std::min(goal-1,seed+2*span-1);
                    std::array<int,2> candidate{};
                    int candidate_mask=0;
                    if (!bounds(seed,trial,candidate,candidate_mask)) {
                        bad=trial;
                        break;
                    }
                    good=trial; cap=candidate; mask=candidate_mask;
                    span=good-seed+1;
                }
                // Retain only endpoints rechecked successfully. Correctness
                // does not depend on failed probes remaining failed later.
                while (good+1<bad) {
                    Num mid=good+(bad-good)/2;
                    std::array<int,2> candidate{};
                    int candidate_mask=0;
                    if (bounds(seed,mid,candidate,candidate_mask)) {
                        good=mid; cap=candidate; mask=candidate_mask;
                    } else bad=mid;
                }
                Num destination=0;
                if (join(good,cap,mask,destination)) {
                    if (destination<=good) throw std::logic_error("invalid merger");
                    saved_width+=good-seed+1;
                    seed=destination;
                    ++joins;
                    jumped=true;
                }
            }
            if (!jumped) {
                // A short unsuccessful probe leaves the actual singleton
                // intact. Follow it exactly to the next probe position.
                do { seed=next(seed); ++direct_calls; } while (seed<=first_end);
            }
        }
        std::cout<<start<<' '<<goal<<' '<<seed<<' '<<direct_calls<<' '
                 <<merge_calls<<' '<<joins<<' '<<saved_width<<'\n';
    }
};

int main(int argc,char** argv) {
    try {
        Post36 solver;
        if (argc==2 && std::string(argv[1])=="--audit") solver.audit();
        else if (argc==3) solver.link(std::stoll(argv[1]),std::stoll(argv[2]));
        else { std::cerr<<"Usage: post36_singleton START GOAL | --audit\n"; return 2; }
    } catch (const std::exception& e) { std::cerr<<e.what()<<'\n'; return 1; }
}
