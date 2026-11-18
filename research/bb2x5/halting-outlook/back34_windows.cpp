// Iterate the finite projection of the line-34 bulk survivor map. C++17.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>

using Mask = std::uint32_t;

void check_width(int width, int expected_count, int expected_passes) {
    const Mask size = Mask(1) << width;
    const Mask mask = size - 1;
    std::vector<bool> present(size, true);
    int passes = 0;
    for (;;) {
        ++passes;
        std::vector<bool> next(size, false);
        for (Mask bits = 0; bits < size; ++bits) {
            if (!present[bits]) continue;
            // Bit i refers to physical index i, increasing from the left.
            for (Mask entering : {0u, 1u}) {
                const Mask preceding = ((bits << 1) | entering) & mask;
                const Mask openings = ~(bits ^ preceding) & mask;
                const Mask closings = bits & ~preceding;
                Mask remaining = 0;
                int debt = 0;
                for (int pos = width - 1; pos >= 0; --pos) {
                    const Mask bit = Mask(1) << pos;
                    if (closings & bit) ++debt;
                    if (openings & bit) {
                        if (debt) --debt;
                        else remaining |= bit;
                    }
                }
                // Increasing the exterior debt deletes the rightmost surviving
                // opening each time, then has no further effect on this window.
                next[remaining] = true;
                for (int pos = width - 1; pos >= 0; --pos) {
                    const Mask bit = Mask(1) << pos;
                    if (remaining & bit) {
                        remaining ^= bit;
                        next[remaining] = true;
                    }
                }
            }
        }
        if (next == present) break;
        present.swap(next);
    }
    const auto count = std::count(present.begin(), present.end(), true);
    assert(count == expected_count && passes == expected_passes);
    // A rise is a closing, a fall a neutral. The initial phase before the
    // first cell of this particular period is fixed by its first rise.
    const std::string last_word = "31232131232132321312321312321312321312321312321";
    int previous = 0;
    std::vector<int> ring;
    for (char digit : last_word) {
        if (digit == '3') { assert(previous == 0); previous = 1; }
        if (digit == '2') { assert(previous == 1); previous = 0; }
        ring.push_back(previous);
    }
    assert(previous == 0);
    for (std::size_t offset = 0; offset < ring.size(); ++offset) {
        Mask factor = 0;
        for (int i = 0; i < width; ++i)
            factor |= Mask(ring[(offset + i) % ring.size()]) << i;
        assert(present[factor]);
    }
    std::cout << width << " cells: " << count << " survivor masks, fixed at pass "
              << passes << "; every cyclic factor of the failing period admitted.\n";
}

int main() {
#ifdef NDEBUG
    std::cerr << "Enable assertions.\n";
    return 2;
#endif
    check_width(12, 2235, 3);
    check_width(15, 12604, 3);
    check_width(18, 68999, 4);
    check_width(21, 369956, 5);
}
