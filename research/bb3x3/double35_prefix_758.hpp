#pragma once
#include "packed_return_758.hpp"

inline Num keep_seed(Num seed) { return seed; }

class ReturnPrefix {
    static constexpr Num power = 50'031'545'098'999'707LL;  // 3^35
    static constexpr Num first = power + 34'754;
    static constexpr Num last = 90'056'781'178'199'398LL;
    static constexpr Num ceiling = last + 50'000;
    // 34 even-launch J calls after I, or 35 odd-launch J calls. With the
    // angular coordinates (u,d), launch gives u=seed+bias, d=(u-h)/2.
    PackedReturn<0, 2*(power/3), 72, ceiling, 4, keep_seed> even;
    PackedReturn<1, power, 70, ceiling, 4, keep_seed> odd;

public:
    void reset(Num lo, Num hi) {
        if (lo < first || hi > last) throw std::invalid_argument("outside power-35 launch interval");
        even.reset(lo,hi);
        odd.reset(lo,hi);
    }

    Num first_return(Num seed, const Cover&) {
        return seed%2 ? odd.get(seed) : even.get(seed);
    }
};
