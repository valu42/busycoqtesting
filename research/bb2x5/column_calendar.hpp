#pragma once

#include <cassert>
#include <cstdint>
#include <vector>

using Integer = std::uint64_t;
struct Gap {
    unsigned p;
    std::uint32_t tick; // One-based within the period at the chosen cut.
};

inline std::vector<Gap> calendar(unsigned cut, Integer& period) {
    assert(cut >= 3 && cut <= 18);
    std::vector<Gap> gaps{{9,1}};
    period = 1;
    for (unsigned level = 3; level < cut; ++level) {
        std::vector<Gap> next;
        next.reserve(3*gaps.size());
        unsigned u = 0, e = 0, pending = 0;
        for (unsigned copy = 0; copy < 4; ++copy) {
            for (auto [p,tick] : gaps) {
                pending += (2-e)*((p+1-u)/2);
                u ^= p & 1;
                if (u || e) {
                    const auto time = static_cast<std::uint32_t>(copy*period+tick);
                    next.push_back({pending,time});
                    pending = 0;
                }
                e ^= 1-u;
            }
        }
        assert(u == 0 && e == 0 && pending == 0 && next.size() == 3*gaps.size());
        period *= 4;
        assert(next.back().tick == period);
        gaps.swap(next);
    }
    return gaps;
}
