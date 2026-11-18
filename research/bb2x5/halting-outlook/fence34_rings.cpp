// Ordinary line-34 sweeps on every spatially periodic survivor mask through width 24.
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <vector>

using Mask = std::uint32_t;

Mask successor(Mask old, int width) {
    const Mask mask = (Mask{1} << width) - 1;
    auto advance = [width, mask](Mask w) {
        return ((w << 1) & mask) | (w >> (width - 1));
    };
    const Mask current = advance(old);
    const Mask previous = advance(current);
    const Mask open = mask & ~(current ^ previous);
    const Mask close = current & ~previous;
    if (__builtin_popcount(open) <= __builtin_popcount(close)) {
        // Balanced rings have no survivors. Negative rings cannot supply a
        // finite guard debt. Either sentinel maps into the all-open fixed point.
        return 0;
    }
    int debt = 0;
    auto scan = [&]() {
        Mask survivors = 0;
        for (int i = width - 1; i >= 0; --i) {
            const Mask bit = Mask{1} << i;
            if (close & bit) {
                ++debt;
            } else if (open & bit) {
                if (debt == 0) survivors |= bit;
                else --debt;
            }
        }
        return survivors;
    };
    scan();
    const int seam = debt;
    const Mask answer = scan();
    if (debt != seam) throw std::logic_error("cyclic matching debt did not close");
    return answer;
}

int main() {
    std::uint64_t total = 0;
    for (int width = 1; width <= 24; ++width) {
        const Mask n = Mask{1} << width;
        const Mask mask = n - 1;
        std::vector<Mask> next(n), visited(n);
        for (Mask start = 0; start < n; ++start) next[start] = successor(start, width);
        int fixed = 0, travelling = 0;
        for (Mask start = 0; start < n; ++start) {
            if (visited[start]) continue;
            const auto tag = start + 1;
            auto v = start;
            while (!visited[v]) {
                visited[v] = tag;
                v = next[v];
            }
            if (visited[v] != tag) continue;
            const auto first = v;
            int period = 0;
            do {
                ++period;
                v = next[v];
            } while (v != first);
            if (52 % period != 0) continue;
            if (period == 1 && first == mask) {
                ++fixed;
            } else if (period == 4 && width % 4 == 0) {
                do {
                    bool matches = false;
                    for (int r = 0; r < 4; ++r) {
                        Mask candidate = 0;
                        for (int i = r; i < width; i += 4) candidate |= Mask{1} << i;
                        matches |= v == candidate;
                    }
                    if (!matches) throw std::logic_error("unexpected four-cycle");
                    v = next[v];
                } while (v != first);
                ++travelling;
            } else {
                throw std::logic_error("unexpected periodic tail");
            }
        }
        if (fixed != 1 || travelling != (width % 4 == 0))
            throw std::logic_error("missing expected cycle");
        total += n;
        std::cout << width << " cells: fixed=" << fixed << ", period four=" << travelling << '\n';
    }
    std::cout << total << " survivor masks exhausted. No other temporal period dividing 52.\n";
}
