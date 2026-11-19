// Exhaust exact halting basins in equally sized neighborhoods of the listed terminal pairs.
// c++ -std=c++17 -O3 terminal_neighborhoods_758.cpp -lgmpxx -lgmp -o terminal_neighborhoods
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <gmpxx.h>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

using Integer = mpz_class;
constexpr int radius = 5'000'000;
constexpr int gap = 5'000;

struct Opening {
    int jumps = -1;
    Integer power, left, right_offset;

    void set(const Integer& seed, bool even) {
        power = even ? 2 : 1;
        jumps = 0;
        while (3*power <= seed+2*(jumps+1)+4*even) {
            power *= 3;
            ++jumps;
        }
        left = 2*power-1;
        right_offset = 2*jumps+4*even-power+1;
    }
};

struct Trace {
    int gain = 0;
    int ceiling = 0;
    int opening = 0;
    std::string word;
};

class Excursions {
    std::array<Opening,2> starts;
public:
    Trace trace(const Integer& seed, bool record_word) {
        const bool even = mpz_even_p(seed.get_mpz_t());
        auto& start = starts[even];
        Integer right = seed+start.right_offset;
        if (start.jumps<0 || right<1 || right>=start.left) {
            start.set(seed,even);
            right = seed+start.right_offset;
        }
        Integer left = start.left, diff;
        int cost = 4*start.jumps+8*even;
        int upper = cost;
        Trace out;
        out.opening = start.jumps;
        for (int i=0; i<10'000; ++i) {
            if (left==1) {
                if (record_word) out.word.push_back('I');
                out.gain = cost/2;
                out.ceiling = upper/2;
                return out;
            }
            mpz_sub(diff.get_mpz_t(),left.get_mpz_t(),right.get_mpz_t());
            if (diff<=0) {
                if (mpz_even_p(left.get_mpz_t())) {
                    if (record_word) out.word.push_back('R');
                    out.gain = (cost+5)/2;
                    out.ceiling = (upper+5)/2;
                    return out;
                }
                if (record_word) out.word.push_back('J');
                right=1-diff;
                left=3*left+2;
                cost+=4;
                upper+=4;
                continue;
            }
            const bool high = mpz_tstbit(right.get_mpz_t(),1);
            const int sub = high ? 4 : 2;
            if (diff>=sub) {
                if (record_word) out.word.push_back('L');
                left=diff-sub;
                right=(3*right+(high?13:7))/2;
                cost+=high?9:5;
                upper+=9;
            } else if (mpz_even_p(left.get_mpz_t())) {
                out.gain = -1;
                return out;
            } else {
                if (record_word) out.word.push_back('E');
                left=3*right+8;
                right=1;
                cost+=8;
                upper+=8;
            }
        }
        throw std::runtime_error("unverified excursion above the step limit");
    }
};

struct Survey {
    Integer target;
    Excursions engine;
    int population = 0, last_hit = -2, widest = 0, far_edge = -2, direct = 0;
    std::uint64_t leaves = 0;

    void cover(int low, int high, int limit) {
        if (low>high) return;
        const Trace a = engine.trace(target-low,true);
        if (low==high) {
            if (a.gain<=0 || a.gain>limit) throw std::runtime_error("failed point");
            ++leaves;
            return;
        }
        const Trace b = engine.trace(target-high,true);
        if (a.gain>0 && b.gain>0 && a.opening==b.opening && a.word==b.word &&
            a.word.back()=='R' && a.word.find('E')==std::string::npos &&
            a.ceiling==b.ceiling && a.ceiling<=limit) {
            ++leaves;
            return;
        }
        int mid=low+2*((high-low)/4);
        cover(low,mid,limit);
        cover(mid+2,high,limit);
    }

    void run() {
        std::vector<char> hits(radius+3);
        int width = 0;
        for (int d=-2; d<=radius; ++d) {
            int step=engine.trace(target-d,false).gain;
            if (step==0) throw std::runtime_error("nonincreasing reset");
            if (step<0) {
                if (d!=0 && d!=-2) throw std::runtime_error("additional direct terminal");
                ++direct;
            }
            bool hit = step<0 || (step<=d+2 && hits[d+2-step]);
            hits[d+2] = hit;
            if (hit) {
                last_hit=d;
                ++population;
                if (++width>widest) {
                    widest=width;
                    far_edge=d;
                }
            } else {
                width=0;
            }
            if (d-last_hit==gap) {
                for (int parity=0;parity<2;++parity) {
                    int low=d+1,high=radius;
                    if (low%2!=parity) ++low;
                    if (high%2!=parity) --high;
                    cover(low,high,gap);
                }
                break;
            }
        }
        if (direct!=2) throw std::runtime_error("missing terminal sibling");
    }
};

int main(int argc, char** argv) {
    if (argc>2) return 2;
    int row=argc==2?std::stoi(argv[1]):0;
    if (row<0 || row>257) return 2;
    std::ifstream input("mixed_terminal_windows_758.tsv");
    if (!input) throw std::runtime_error("run beside mixed_terminal_windows_758.tsv");
    std::string line;
    std::getline(input,line);
    int count=0;
    while (std::getline(input,line)) {
        ++count;
        if (row && count!=row) continue;
        std::istringstream fields(line);
        Survey s;
        if (!(fields>>s.target)) throw std::runtime_error("missing seed");
        s.run();
        std::cout<<s.target<<'\t'<<s.population<<'\t'<<s.widest<<'\t'<<s.far_edge
                 <<'\t'<<s.last_hit<<'\n'<<std::flush;
    }
    if (count!=257) throw std::runtime_error("incomplete candidate list");
}
