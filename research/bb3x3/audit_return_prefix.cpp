// Test driver for original and accelerated first-positive return paths.
#include "return_prefix_758.hpp"

int main() {
    Cover proof;
    ReturnPrefix cached;
    Num last_lo = -1, last_hi = -1;
    Num lo, hi, seed;
    while (std::cin >> lo >> hi >> seed) {
        if (lo != last_lo || hi != last_hi) {
            cached.reset(lo, hi);
            last_lo = lo;
            last_hi = hi;
        }
        std::cout << cached.first_return(seed, proof) << '\n';
    }
}
