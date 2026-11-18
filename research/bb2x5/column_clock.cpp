// First dangerous arrivals on line 26, preserving their original time stamps.
// Build: c++ -std=c++20 -O2 column_clock.cpp -o column-clock
#include <algorithm>
#include <bit>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <string_view>
#include <vector>
#ifdef __BMI2__
#include <immintrin.h>
#endif

using Integer = std::uint64_t;
struct Gap {
    unsigned p;
    std::uint32_t tick; // One-based within the period at the chosen cut.
};

std::vector<Gap> calendar(unsigned cut, Integer& period) {
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

struct State {
    Integer u = 0, e = 0, wraps = 0;

    void consume_p(unsigned count) {
        const Integer low = u & 1;
        Integer passes = (count+1-low)/2;
        Integer high = u >> 1;
        if (passes) {
            Integer subtract = 0;
#ifdef __BMI2__
            subtract = _pdep_u64(passes,e);
            // In this calculation e has fewer than 63 significant bits.
            passes >>= std::popcount(e);
#else
            // Deposit the low digits of passes into the selected positions.
            // Any unconsumed high digits count complete turns of the selected counter.
            Integer mask = e;
            while (mask && passes) {
                const Integer bit = mask & -mask;
                if (passes & 1) subtract |= bit;
                passes >>= 1;
                mask -= bit;
            }
#endif
            const Integer selected = high & e;
            wraps += passes + (selected < subtract);
            high = (high & ~e) | ((selected-subtract) & e);
        }
        u = (high << 1) | (low ^ (count & 1));
    }
};

void audit_subtraction() {
    for (Integer u = 0; u < 40; ++u) for (Integer e = 0; e < 40; ++e) {
        State literal{u,e,0};
        for (unsigned p = 0; p <= 80; ++p) {
            State grouped{u,e,0};
            grouped.consume_p(p);
            assert(literal.u == grouped.u && literal.wraps == grouped.wraps);
            const Integer mask = 2*e+1, shared = literal.u & mask;
            const Integer bit = shared & -shared;
            literal.u ^= mask & (2*bit-1);
            if (!bit) ++literal.wraps;
        }
    }
}

struct Arrival {
    Integer wraps, tick;
    bool operator==(const Arrival&) const = default;
};
struct Result {
    std::vector<Arrival> first;
    Integer gaps;
};

struct BlockMove {
    unsigned next, p;
    bool q;
};

std::vector<BlockMove> block_table(unsigned depth, unsigned largest_gap) {
    assert(depth <= 4);
    const unsigned states = 1U << (2*depth);
    std::vector<BlockMove> table(states*(largest_gap+1));
    for (unsigned state = 0; state < states; ++state) {
        for (unsigned gap = 0; gap <= largest_gap; ++gap) {
            unsigned next = 0, p = gap;
            bool q = true;
            for (unsigned j = 0; j < depth; ++j) {
                unsigned e = (state >> (2*j)) & 1;
                unsigned u = (state >> (2*j+1)) & 1;
                const unsigned sent = (2-e)*((p+1-u)/2);
                u ^= p & 1;
                const bool danger = q && (u || e);
                if (q && !u) e ^= 1;
                next |= (2*u+e) << (2*j);
                p = sent;
                q = danger;
            }
            table[state*(largest_gap+1)+gap] = {next,p,q};
        }
    }
    return table;
}

Result first_arrivals(unsigned cut, unsigned target, unsigned depth = 0) {
    const unsigned upper = cut+depth;
    assert(target >= upper && target-upper <= 63 && upper <= 22);
    Integer period;
    const auto gaps = calendar(cut,period);
    unsigned largest_gap = 0;
    for (auto gap : gaps) largest_gap = std::max(largest_gap,gap.p);
    const auto table = block_table(depth,largest_gap);
    unsigned block = 0, pending = 0;
    State state;
    Result result{{},0};
    for (Integer offset = 0;; offset += period) {
        for (auto [p,tick] : gaps) {
            const auto move = table[block*(largest_gap+1)+p];
            block = move.next;
            pending += move.p;
            // G(j)+1 <= 10*(3/2)^(j-3), so the bound covers every upper gap.
            assert(pending < 30000);
            ++result.gaps;
            if (!move.q) continue;
            state.consume_p(pending);
            pending = 0;
            const unsigned stop = std::countr_one(state.u | state.e);
            while (upper+result.first.size() <= std::min(upper+stop,target))
                result.first.push_back({state.wraps,offset+tick});
            if (upper+stop >= target) return result;
            state.e ^= ~state.u & ((Integer(2)<<stop)-1);
            assert((state.e >> (target-upper)) == 0);
        }
    }
}

int main(int argc, char** argv) {
    audit_subtraction();
    if (argc == 2 && std::string_view(argv[1]) == "--extended") {
        constexpr unsigned target = 84;
        const auto low = first_arrivals(17,target,4);
        const auto high = first_arrivals(18,target,4);
        assert(std::equal(high.first.begin(),high.first.end(),low.first.begin()+1));
        assert((low.first[78-21] == Arrival{151,4636999907}));
        assert((low.first.back() == Arrival{173,54306954019}));
        for (unsigned j = 79; j <= target; ++j) {
            const auto [p,tick] = low.first[j-21];
            std::cout << "p(" << j << ") = " << p << ", first Q at tick " << tick << '\n';
        }
        std::cout << "streamed gaps at cut 17: " << low.gaps << '\n';
        std::cout << "streamed gaps at cut 18: " << high.gaps << '\n';
        return 0;
    }
    if (argc != 1) return 2;
    constexpr unsigned target = 78;
    const auto low = first_arrivals(16,target);
    const auto high = first_arrivals(17,target);
    assert(std::equal(high.first.begin(),high.first.end(),low.first.begin()+1));
    assert((low.first[71-16] == Arrival{142,1268654660}));
    assert((low.first.back() == Arrival{151,4636999907}));
    for (unsigned j = 71; j <= target; ++j) {
        const auto [p,tick] = low.first[j-16];
        std::cout << "p(" << j << ") = " << p << ", first Q at tick " << tick << '\n';
    }
    std::cout << "gaps processed at cut 16: " << low.gaps << '\n';
    std::cout << "gaps processed at cut 17: " << high.gaps << '\n';
}
