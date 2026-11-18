// Literal blank-tape replay for BB(6) line 33. Build with c++ -O3 -std=c++17.
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

struct Op { int write; int move; int state; };
constexpr int A = 0, B = 1, C = 2, D = 3, E = 4, F = 5;
constexpr Op transition[6][2] = {
    {{1, 1, B}, {0, -1, F}},
    {{1, -1, C}, {0, 1, B}},
    {{0, -1, D}, {1, -1, A}},
    {{0, 1, A}, {1, -1, E}},
    {{0, -1, A}, {0, 1, A}},
    {{1, -1, A}, {0, 0, -1}}
};

std::string pairs(int n) {
    std::string s;
    s.reserve(2 * n);
    for (int i = 0; i < n; ++i) s += "10";
    return s;
}

struct Checkpoint { std::uint64_t step; std::string right; };

int main() {
    const std::string prefix = pairs(4) + "110";
    const std::array<Checkpoint, 4> checks{{
        {1817ULL, prefix + pairs(13) + "10010" + pairs(11) + "1"},
        {1842640229ULL, prefix + pairs(19199) + "10010" + "1" + pairs(15998) + "1" + pairs(9) + "0101101"},
        {4516954072ULL, prefix + pairs(28802) + "1110" + pairs(30401) + "110" + pairs(6) + "0101101101"},
        {10536838532ULL, prefix + pairs(43211) + "1110" + pairs(21601) + "110" + pairs(30402) + "0" + pairs(12) + "1"}
    }};
    const int middle = 1 << 20;
    std::vector<unsigned char> tape(2 * middle, 0);
    int head = middle, state = A;
    std::uint64_t clock = 0;
    for (const auto& point : checks) {
        while (clock < point.step) {
            // Stop before any out-of-bounds access. All unvisited cells are blank.
            if (static_cast<unsigned>(head) >= tape.size()) throw std::runtime_error("tape budget");
            const Op op = transition[state][tape[head]];
            if (op.state < 0) throw std::runtime_error("unexpected F1 at " + std::to_string(clock));
            tape[head] = static_cast<unsigned char>(op.write);
            head += op.move;
            state = op.state;
            ++clock;
        }
        if (state != A) throw std::runtime_error("wrong state at " + std::to_string(clock));
        for (int i = 0; i < static_cast<int>(tape.size()); ++i) {
            const int offset = i - head;
            const int expected = offset >= 0 && static_cast<std::size_t>(offset) < point.right.size()
                ? point.right[offset] - '0' : 0;
            if (tape[i] != expected) throw std::runtime_error("tape mismatch at " + std::to_string(clock));
        }
        std::cout << clock << "  A  head=" << head - middle << "  full tape matched" << std::endl;
    }
}
