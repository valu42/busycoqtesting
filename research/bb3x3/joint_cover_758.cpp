// Count exact positive overlaps of odd K and even (3/2)K stopping cylinders.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <string>

using Int = __int128_t;
using Count = std::uint64_t;

class Cover {
    int cutoff;
    std::array<Int, 78> powers{};
    Count pairs = 0, odd_cells = 0, even_cells = 0, last_odd = 0, last_even = 0;

    // The odd interval is [0,a], the even interval [x,x+b]. All three
    // integers use the common denominator 2*3^max(odd_depth,even_depth).
    void visit(Int a, Int b, Int x, int odd_depth, int even_depth, Count odd_id, Count even_id) {
        if (x >= a || x+b <= 0) return;
        const int depth = std::max(odd_depth, even_depth);
        if (depth >= cutoff && std::max(a,b) <= 2*powers[depth-cutoff]) {
            ++pairs;
            // Positive overlap intervals are encountered from left to right.
            if (last_odd != odd_id) { ++odd_cells; last_odd = odd_id; }
            if (last_even != even_id) { ++even_cells; last_even = even_id; }
            return;
        }
        if (a > b) {
            Int z = odd_depth == depth ? 3 : 1;
            visit(a*z/3, b*z, x*z, odd_depth+1, even_depth, 2*odd_id, even_id);
            z = powers[std::max(0, odd_depth+2-depth)];
            Int unit = a*z/9;
            visit(4*unit, b*z, x*z-5*unit, odd_depth+2, even_depth, 2*odd_id+1, even_id);
        } else {
            Int z = even_depth == depth ? 3 : 1;
            visit(a*z, b*z/3, x*z, odd_depth, even_depth+1, odd_id, 2*even_id);
            z = powers[std::max(0, even_depth+2-depth)];
            Int unit = b*z/9;
            visit(a*z, 4*unit, x*z+5*unit, odd_depth, even_depth+2, odd_id, 2*even_id+1);
        }
    }
public:
    explicit Cover(int exponent) : cutoff(exponent) {
        assert(1 <= exponent && exponent <= 35);
        powers[0] = 1;
        for (unsigned i = 1; i < powers.size(); ++i) powers[i] = 3*powers[i-1];
    }
    void run() {
        visit(2, 3, 0, 0, 0, 1, 1);
        std::cout << cutoff << ' ' << pairs << ' ' << odd_cells << ' ' << even_cells << '\n';
    }
};

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    int cutoff = std::stoi(argv[1]);
    if (cutoff < 1 || cutoff > 35) return 2;
    Cover(cutoff).run();
}
