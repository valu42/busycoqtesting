#include "reset_cover_758.hpp"
#include <array>
#include <stdexcept>

#ifndef POWER_EXPONENT
#define POWER_EXPONENT 33
#endif

static_assert(POWER_EXPONENT == 32 || POWER_EXPONENT == 33, "verified word-size range");
constexpr int exponent = POWER_EXPONENT;
constexpr Num power = exponent == 32 ? 1853020188851841LL : 5559060566555523LL;
constexpr int launch_mass = 2*exponent + 4;
constexpr int launch_offset = exponent + 2;
constexpr int odd_gain = 2*exponent + 5;

inline Num normalize(Num seed) {
    return seed % 2 ? seed + odd_gain + (seed & 2) : seed;
}

#include "even_power_prefix_758.hpp"

// Keep a set of half-seeds in a circular bitset. A symbolic crossing creates
// a contiguous set, which need only be materialized before an exact crossing.
class Front {
    static constexpr int slots = 1024;
    std::array<std::uint64_t, slots> bits{};
    int count = 0;
    Num low = 0, high = 0;
    bool interval = false;

    std::uint64_t& word(Num x) { return bits[(x >> 6) & (slots-1)]; }

public:
    bool empty() const { return !interval && count == 0; }
    Num first() const { return 2*low; }
    Num last() const { return 2*high; }

    void clear() {
        if (count) {
            for (Num w = low >> 6; w <= high >> 6; ++w) bits[w & (slots-1)] = 0;
            count = 0;
        }
        interval = false;
    }

    void range(Num lo, Num hi) {
        clear();
        low = (lo+1)/2;
        high = hi/2;
        interval = low <= high;
    }

    void open() {
        if (!interval) return;
        Num l = low, h = high;
        interval = false;
        for (Num i = l; i <= h; ++i) add(2*i);
    }

    void add(Num seed) {
        if (seed % 2 || interval) throw std::logic_error("even set");
        Num x = seed >> 1;
        if (count) {
            low = std::min(low, x);
            high = std::max(high, x);
        } else {
            low = high = x;
        }
        if (high-low >= 64*slots) throw std::runtime_error("frontier exceeds bitset");
        auto mask = std::uint64_t{1} << (x & 63);
        auto& value = word(x);
        if (!(value & mask)) {
            value |= mask;
            ++count;
        }
    }

    Num pop() {
        Num x = low;
        auto& value = word(x);
        value &= ~(std::uint64_t{1} << (x & 63));
        if (--count) {
            Num i = x >> 6;
            auto w = value & (~std::uint64_t{0} << (x & 63));
            while (!w) w = bits[(++i) & (slots-1)];
            low = 64*i + __builtin_ctzll(w);
        }
        return 2*x;
    }
};

struct Solver {
    Packed packed;
    Cover proof;
    Front front;
    Num blocks = 0, calls = 0;

    void exact(Num limit) {
        front.open();
        while (front.first() <= limit) {
            Num seed = front.pop();
            do {
                Num next = packed.get(seed);
                if (next <= seed) throw std::logic_error("nonmonotone return");
                ++calls;
                seed = next;
            } while (front.empty() && seed <= limit);
            front.add(seed);
        }
    }

    void walk(Num lo, Num hi) {
        if (front.first() > hi) return;
        Num first_even = lo + (lo & 1), last_even = hi - (hi & 1);
        int cap = proof.bound(first_even, last_even);
        if (cap) {
            // On a common coarse word every seed gain has the parity of cap.
            if (cap & 1) cap += odd_gain + 2;
            front.range(hi+1, std::max(front.last(), hi+cap));
            ++blocks;
        } else if (hi-lo <= 250000) {
            exact(hi);
        } else {
            Num mid = (hi+lo)/2;
            walk(lo, mid);
            walk(mid+1, hi);
        }
    }

    void run(Num lo, Num cut) {
        if (lo < 2*power || lo >= cut || cut > 3*power-2*exponent-6-50000)
            throw std::runtime_error("outside verified odd corridor");
        packed.reset(lo, cut-1);
        for (Num i = 0; i <= 5000; ++i) front.add(normalize(lo+i));
        walk(lo, cut-1);
        if (front.first() < cut || front.last() > cut+5000)
            throw std::runtime_error("exit too wide");
        std::cout << lo << ' ' << cut << ' ' << front.first() << ' ' << front.last()
                  << ' ' << blocks << ' ' << calls << '\n';
    }
};

#ifndef AUDIT_EVEN_POWER
int main(int argc, char** argv) {
    if (argc != 3) return 2;
    try {
        Solver s;
        s.run(std::stoll(argv[1]), std::stoll(argv[2]));
    } catch (const std::exception& e) {
        std::cerr << e.what() << '\n';
        return 1;
    }
}
#endif
