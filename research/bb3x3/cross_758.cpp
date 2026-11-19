// Certify that every incoming reset in [start,start+5000] passes a cut alive.
#include "reset_cover_758.hpp"
#include <array>
#include <set>
#include <stdexcept>

constexpr Num incoming_width = 5000;
constexpr Num direct_span = 250000;

class Crossing {
    Cover proof;
    std::set<Num> points;
    bool interval = false;
    Num low = 0;
    Num high = 0;
    std::uint64_t blocks = 0;
    std::uint64_t direct_calls = 0;

    Num first_return(Num seed) const {
        Num a = seed % 2 ? 5 : 3;
        Num c = seed % 2 ? seed : seed + 3;
        Num u = a + 1;
        Num threshold = (2*c + u)/u;
        auto it = std::upper_bound(proof.powers.begin(), proof.powers.end(), threshold);
        int k = int(it - proof.powers.begin()) - 1;
        Num p = proof.powers[k];
        State s{u*p - 1, c - u*((p - 1)/2) + 2*k};
        for (int i = 0; i < 5000; ++i) {
            if (s.a == 1) return s.c;
            Branch op = branch(s);
            if (op == returned) return s.a/2 + s.c + 2;
            if (op == halted)
                throw std::runtime_error("possible halt from seed " + std::to_string(seed));
            s = advance(s, op);
        }
        throw std::runtime_error("first-return budget reached");
    }

    Num earliest() const { return interval ? low : *points.begin(); }
    Num latest() const { return interval ? high : *points.rbegin(); }

    void trace(Num end) {
        if (interval) {
            for (Num s = low; s <= high; ++s) points.insert(s);
            interval = false;
        }
        while (*points.begin() <= end) {
            Num seed = *points.begin();
            points.erase(points.begin());
            do {
                ++direct_calls;
                Num next = first_return(seed);
                if (next <= seed) throw std::logic_error("nonincreasing reset");
                seed = next;
                // On a singleton frontier the unique continuing path can be
                // followed directly until it leaves this interval.
            } while (points.empty() && seed <= end);
            points.insert(seed);
        }
    }

    void cross(Num start, Num end, std::array<int,2> bounds = {}) {
        if (earliest() > end) return;
        for (int parity = 0; parity < 2; ++parity) {
            if (bounds[parity] != 0) continue;
            Num lo = start + (start % 2 != parity);
            Num hi = end - (end % 2 != parity);
            bounds[parity] = lo > hi ? 1 : proof.bound(lo, hi);
        }
        if (bounds[0] && bounds[1]) {
            Num limit = end + std::max(bounds[0], bounds[1]);
            high = std::max(latest(), limit);
            low = end + 1;
            interval = true;
            points.clear();
            ++blocks;
        } else if (end - start <= direct_span) {
            trace(end);
        } else {
            Num mid = start + (end - start)/2;
            cross(start, mid, bounds);
            cross(mid + 1, end, bounds);
        }
    }

public:
    void check(Num start, Num next_cut) {
        low = start;
        high = start + incoming_width;
        interval = true;
        cross(start, next_cut - 1);
        if (earliest() < next_cut || latest() > next_cut + incoming_width)
            throw std::runtime_error("output outside the next incoming window");
        std::cout << start << ' ' << next_cut << ' ' << earliest() << ' '
                  << latest() << ' ' << blocks << ' ' << direct_calls << '\n';
    }
};

int main(int argc, char** argv) {
    if (argc != 3) {
        std::cerr << "Usage: cross_758 start next_cut\n";
        return 2;
    }
    Num start = std::stoll(argv[1]);
    Num cut = std::stoll(argv[2]);
    if (start < 3 || cut <= start || cut > 100000000000000000LL) return 2;
    try {
        Crossing check;
        check.check(start, cut);
    } catch (const std::exception& e) {
        std::cerr << e.what() << '\n';
        return 1;
    }
}
