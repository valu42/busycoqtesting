#pragma once
#include "packed_return_758.hpp"

inline Num keep_seed(Num seed) { return seed; }

#ifndef BB758_DOUBLE_POWER
#define BB758_DOUBLE_POWER 35
#endif

static_assert(BB758_DOUBLE_POWER == 35 || BB758_DOUBLE_POWER == 36);
constexpr int grid_exponent = BB758_DOUBLE_POWER;
constexpr Num grid_power = grid_exponent == 35 ? 50'031'545'098'999'707LL : 150'094'635'296'999'121LL;
constexpr Num grid_first = grid_power + (grid_exponent == 35 ? 34'754 : 112'032);
constexpr Num grid_last = grid_exponent == 35 ? 90'056'781'178'199'398LL : 270'170'343'534'399'339LL;
constexpr int grid_pairs = grid_exponent == 35 ? 4 : 3;
#if BB758_DOUBLE_POWER == 36
#define BB758_MAX_WINDOW_CUT grid_last
#endif

class ReturnPrefix {
    // Even launches take I and m-1 jumps. Odd launches take m jumps.
    // The common launch state is u=seed+bias, d=(u-h)/2.
    PackedReturn<0, 2*(grid_power/3), 2*grid_exponent+2, grid_last+50'000, grid_pairs, keep_seed> even;
    PackedReturn<1, grid_power, 2*grid_exponent, grid_last+50'000, grid_pairs, keep_seed> odd;

public:
    void reset(Num lo, Num hi) {
        if (lo < grid_first || hi > grid_last) throw std::invalid_argument("outside certified two-parity launch interval");
        even.reset(lo,hi);
        odd.reset(lo,hi);
    }

    Num first_return(Num seed, const Cover&) {
        return seed%2 ? odd.get(seed) : even.get(seed);
    }
};
