// Certify that every incoming reset in [start,start+5000] passes a cut alive.
#include "return_prefix_758.hpp"
#include <array>
#include <set>
#include <stdexcept>

constexpr Num incoming_width = 5000;
constexpr Num direct_span = 250000;

class Crossing {
    Cover proof;
    ReturnPrefix prefix;
    std::set<Num> points;

    std::uint64_t blocks = 0;
    std::uint64_t direct_calls = 0;

    int input_mask(Num end) const {
        int mask = 0;
        for (Num seed : points) {
            if (seed > end) break;
            mask |= 1 << (seed % 2);
            if (mask == 3) break;
        }
        return mask;
    }

    // Add a sound superset of the resets by which this class leaves the block.
    void exits(Num end, int parity, int gain) {
        Num first = end + 1;
        if (first % 2 != parity) ++first;
        for (Num s = first; s <= end + gain; s += 2) points.insert(s);
    }

    bool jump(Num end, const std::array<int,2>& bounds) {
        int seen = input_mask(end);
        if (seen == 0) return true;
        // Only two parities exist, so two scans close the set of classes.
        for (int pass = 0; pass < 2; ++pass) {
            for (int p = 0; p < 2; ++p) {
                if (!(seen & (1 << p))) continue;
                if (bounds[p] == 0) return false;
                // Each mass charge agrees modulo four with its bound. The
                // selected later h-return thus has c' = c + gain (mod 2).
                int next = (p + bounds[p]) % 2;
                seen |= 1 << next;
            }
        }
        points.erase(points.begin(), points.upper_bound(end));
        for (int p = 0; p < 2; ++p) {
            if (seen & (1 << p)) exits(end, (p + bounds[p]) % 2, bounds[p]);
        }
        ++blocks;
        return true;
    }

    void trace(Num end, const std::array<int,2>& bounds) {
        Num first = *points.begin();
        if (first > end) return;
        Num first_word = first >> 6;
        std::vector<std::uint64_t> events((end >> 6) - first_word + 1);
        int pending = 0;
        auto schedule = [&](Num seed) {
            if (seed > end) {
                points.insert(seed);
                return;
            }
            auto& word = events[(seed >> 6) - first_word];
            std::uint64_t bit = std::uint64_t{1} << (seed%64);
            if (!(word & bit)) {
                word |= bit;
                ++pending;
            }
        };

        // In-window seeds are processed in ascending order; one bit per seed
        // preserves the same duplicate suppression as the ordered set.
        auto incoming = std::move(points);
        points.clear();
        for (Num seed : incoming) schedule(seed);
        std::array<bool,2> emitted{};
        for (std::size_t i = 0; i < events.size() && pending; ++i) {
            auto& bits = events[i];
            while (bits) {
                Num seed = (first_word+Num(i))*64 + __builtin_ctzll(bits);
                bits &= bits-1;
                --pending;
                for (;;) {
                    int p = seed%2;
                    if (bounds[p] > 0 && bounds[p]%2 == 0) {
                        if (!emitted[p]) {
                            exits(end, p, bounds[p]);
                            emitted[p] = true;
                        }
                        break;
                    }
                    ++direct_calls;
                    Num next = prefix.first_return(seed, proof);
                    if (next == -1)
                        throw std::runtime_error("possible halt from seed " + std::to_string(seed));
                    if (next == -2) throw std::runtime_error("first-return budget reached");
                    if (next <= seed) throw std::logic_error("nonincreasing reset");
                    seed = next;
                    if (seed > end || pending || !points.empty()) {
                        schedule(seed);
                        break;
                    }
                    // A lone active seed follows its exact path until it exits
                    // the interval or enters a certified parity class.
                }
            }
        }
    }

    void cross(Num start, Num end, std::array<int,2> bounds = {}) {
        if (*points.begin() > end) return;
        for (int parity = 0; parity < 2; ++parity) {
            if (bounds[parity] != 0) continue;
            Num lo = start + (start % 2 != parity);
            Num hi = end - (end % 2 != parity);
            bounds[parity] = lo > hi ? 1 : proof.bound(lo, hi);
        }
        if (jump(end, bounds)) return;
        if (end - start <= direct_span) {
            trace(end, bounds);
        } else {
            Num mid = start + (end - start)/2;
            cross(start, mid, bounds);
            cross(mid + 1, end, bounds);
        }
    }

public:
    void check(Num start, Num next_cut) {
        prefix.reset(start, next_cut-1);
        for (Num s = start; s <= start + incoming_width; ++s) points.insert(s);
        cross(start, next_cut - 1);
        if (*points.begin() < next_cut || *points.rbegin() > next_cut + incoming_width)
            throw std::runtime_error("output outside the next incoming window");
        std::cout << start << ' ' << next_cut << ' ' << *points.begin() << ' '
                  << *points.rbegin() << ' ' << blocks << ' ' << direct_calls << '\n';
    }
};

int main(int argc, char** argv) {
    if (argc != 3) {
        std::cerr << "Usage: cross_758_fast start next_cut\n";
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
