#include "double35_prefix_758.hpp"
#include <random>
static Num literal(Num seed) {
    State s = seed % 2 ? State{5,seed} : State{3,seed+3};
    for (int moves = 0; moves <= 11000; ++moves) {
        if (s.a == 1) return s.c;
        Num q = (s.c+1)/4;
        if (s.a >= 4*q+3) {
            s = {s.a-4*q-3, 6*q+5};
        } else if (s.a <= s.c) {
            if (s.a % 2 == 0) return s.c+s.a/2+2;
            s = {3*s.a+2, s.c-s.a+1};
        } else {
            if (s.a % 2 == 0) return -1;
            s = {3*s.c+8, 1};
        }
    }
    throw std::runtime_error("literal iteration limit");
}


int main() {
    constexpr Num low = grid_first, high = grid_last;
    constexpr Num width = 1 << 20;
    std::mt19937_64 random(758);
    ReturnPrefix prefix;
    Cover cover;
    for (int i = 0; i < 1000; ++i) {
        Num lo = low + random() % (high-low-width+1);
        if (i == 0) lo = low;
        if (i == 1) lo = high-width+1;
        prefix.reset(lo,lo+width-1);
        for (int j = 0; j < 2048; ++j) {
            Num seed = lo + (j < 1024 ? j : random()%width);
            Num expected = literal(seed), actual = prefix.first_return(seed,cover);
            if (actual != expected) {
                std::cerr << seed << ' ' << actual << ' ' << expected << '\n';
                return 1;
            }
        }
    }
    std::cout << "2,048,000 literal first returns match\n";
}
