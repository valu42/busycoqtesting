// Exact first-d calculation for formal line 26. Build with a C++20 compiler.
#include <algorithm>
#include <bit>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>
#ifdef __BMI2__
#include <immintrin.h>
#endif

using Integer = std::uint64_t;

struct Gap {
    unsigned a, b;
};

std::vector<Gap> next_period(const std::vector<Gap>& word) {
    std::vector<Gap> output;
    output.reserve(3 * word.size());
    unsigned odd = 1, even = 0;
    Gap pending{};
    for (unsigned copy = 0; copy < 4; ++copy) {
        for (Gap g : word) {
            unsigned passes = g.a + (g.b + odd) / 2;
            if (even) pending.b += passes;
            else pending.a += passes;
            odd ^= g.b & 1;
            if (!odd || even) {
                output.push_back(pending);
                pending = {};
            }
            even ^= odd;
        }
        if (odd == 1 && even == 0) {
            assert(pending.a == 0 && pending.b == 0);
            return output;
        }
    }
    throw "column failed to return";
}

Integer extract(Integer bits, Integer mask) {
#ifdef __BMI2__
    return _pext_u64(bits, mask);
#else
    Integer result = 0, digit = 1;
    while (mask) {
        Integer low = mask & -mask;
        if (bits & low) result |= digit;
        mask -= low;
        digit <<= 1;
    }
    return result;
#endif
}

Integer deposit(Integer bits, Integer mask) {
#ifdef __BMI2__
    return _pdep_u64(bits, mask);
#else
    Integer result = 0;
    while (mask) {
        Integer low = mask & -mask;
        if (bits & 1) result |= low;
        mask -= low;
        bits >>= 1;
    }
    return result;
#endif
}

struct Counters {
    Integer u = 0, e = 0, wraps = 0;

    void safes(Gap g) {
        Integer low = u & 1;
        Integer pass = g.a + (g.b + 1 - low) / 2;
        low ^= g.b & 1;
        Integer high = u >> 1;
        if (pass) {
            Integer packed = extract(high, e);
            unsigned width = std::popcount(e);
            assert(width < 64);
            if (pass > packed) wraps += 1 + ((pass - packed - 1) >> width);
            // Unsigned subtraction followed by deposit retains just the selected low digits.
            high = (high & ~e) | deposit(packed - pass, e);
        }
        u = (high << 1) | low;
    }

    void single_safe(bool b) {
        Integer selector = 2*e + b;
        Integer common = u & selector;
        if (common) {
            Integer stop = common & -common;
            u ^= selector & (2*stop-1);
        } else {
            u ^= selector;
            ++wraps;
        }
    }
};

void audit_gaps() {
    for (Integer u = 0; u < 32; ++u)
        for (Integer e = 0; e < 32; ++e)
            for (unsigned n = 0; n <= 6; ++n)
                for (unsigned bits = 0; bits < (1U<<n); ++bits) {
                    Counters raw{u,e,0}, grouped = raw;
                    unsigned b = std::popcount(bits);
                    for (unsigned j = 0; j < n; ++j) raw.single_safe((bits >> j) & 1);
                    grouped.safes({n-b,b});
                    assert(grouped.u == raw.u && grouped.wraps == raw.wraps);
                }
}

struct Result {
    std::vector<Integer> values;
    Integer gaps;
};

Result first_d(unsigned cut, unsigned target) {
    // Prior to the first d reaching target, the high e uses at most target-cut bits.
    // Only u can use one additional bit. The shift operations below therefore fit.
    assert(target >= cut && target-cut < 62);
    std::vector<Gap> period{{2,0},{0,0}};
    for (unsigned k = 0; k < cut; ++k) period = next_period(period);
    Counters c;
    std::vector<Integer> values;
    Integer gaps = 0;
    for (;;) {
        for (Gap g : period) {
            c.safes(g);
            ++gaps;
            unsigned stop = std::countr_one(c.u | c.e);
            while (cut + values.size() <= std::min(cut+stop,target))
                values.push_back(c.wraps);
            if (cut + stop >= target) return {values,gaps};
            Integer bit = Integer(1) << stop;
            c.e ^= (~c.u) & (2*bit-1);
            assert((c.e >> (target-cut)) == 0);
        }
    }
}

int main() {
    audit_gaps();
    constexpr unsigned target = 71;
    auto wide = first_d(16,target);
    auto check = first_d(15,target);
    assert(std::equal(wide.values.begin(),wide.values.end(),check.values.begin()+1));
    assert(wide.gaps == 30139997 && wide.values.back() == 142);
    for (unsigned cut : {16,26,34,50,60,69,70,71})
        std::cout << "p(" << cut << ") = " << wide.values[cut-16] << '\n';
    std::cout << "cut 16 gaps through the first d at cut 71: " << wide.gaps << '\n';
    std::cout << "cut 15 gaps through the same event: " << check.gaps << '\n';
}
