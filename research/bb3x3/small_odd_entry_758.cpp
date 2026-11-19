// g++ -O3 -std=c++17 small_odd_entry_758.cpp -lgmpxx -lgmp -o /tmp/odd758
#include <gmpxx.h>
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <stdexcept>

using Word = std::uint64_t;
using Wide = unsigned __int128;
constexpr Word divisor = 13959275;
constexpr Word largest = 14365290;
constexpr unsigned limit = 245;

mpz_class large(Wide value) {
    mpz_class out;
    mpz_import(out.get_mpz_t(), 1, 1, sizeof(value), 0, 0, &value);
    return out;
}

template<class Integer>
bool advance(Integer& a, Integer& q, unsigned& depth) {
    if (3*a == q || 9*a == 5*q || a == 0 || a >= q)
        throw std::runtime_error("exact guard contact");
    if (3*a < q) {
        a *= 3;
        ++depth;
    } else if (9*a > 5*q) {
        a = 9*a-5*q;
        q *= 4;
        depth += 2;
    } else {
        return false;
    }
    if (depth > limit) throw std::runtime_error("past the physical guard bound");
    return true;
}

int main() {
    Word checked = 0, witness = 0, denominator = 1;
    unsigned longest = 0;
    for (Word h=3; h<=largest; h+=2) {
        if (h%3==0) continue;  // 3-adic multiples have the identical aligned direction.
        const Word numerator = h*divisor;
        while (denominator < numerator) denominator *= 3;
        Wide a=numerator, q=denominator;
        unsigned depth=0;
        bool continuing=true;
        while (continuing && q < (Wide(1)<<123)) continuing=advance(a,q,depth);
        if (continuing) {
            auto aa=large(a), qq=large(q);
            while (advance(aa,qq,depth)) {}
        }
        ++checked;
        if (depth > longest) {
            longest=depth;
            witness=h;
        }
    }
    std::cout << checked << " primitive odd integers, latest return guard " << longest
              << ", first maximizing h " << witness << '\n';
}
