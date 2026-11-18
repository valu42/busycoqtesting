// Literal blank-tape replay for the BBi(9) 3-state, 5-symbol holdout on line 3059.
// Build with c++ -O3 -std=c++17 line3059.cpp -o literal
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <vector>

struct Rule {
    int write;
    int move;
    int state;
};

constexpr int A = 0, B = 1, C = 2;
constexpr Rule halt{0, 0, -1};
// Columns are read symbols 0, 1, 2, 3, 4, in that order.
constexpr Rule rules[3][5] = {
    {{1, 1, B}, {0, -1, C}, {3, 1, A}, halt, halt},
    {{1, 1, C}, {2, 1, A}, halt, halt, halt},
    {{1, -1, A}, {0, 1, B}, {4, 1, A}, {1, -1, C}, halt},
};

int main(int argc, char** argv) {
    if (argc > 2) {
        std::cerr << "usage: literal [final-tape.txt]\n";
        return 2;
    }
    std::vector<unsigned char> tape(4096, 0);
    std::int64_t origin = -2048;
    std::int64_t index = -origin;
    std::uint64_t steps = 0;
    int state = A;

    for (;;) {
        const Rule& r = rules[state][tape[index]];
        if (r.state < 0)
            break;
        tape[index] = static_cast<unsigned char>(r.write);
        state = r.state;
        index += r.move;
        ++steps;
        if (index < 0 || index == static_cast<std::int64_t>(tape.size())) {
            const std::int64_t shift = index < 0 ? static_cast<std::int64_t>(tape.size()) : 0;
            std::vector<unsigned char> grown(tape.size() * 2, 0);
            std::copy(tape.begin(), tape.end(), grown.begin() + shift);
            tape.swap(grown);
            origin -= shift;
            index += shift;
        }
    }

    auto first = std::find_if(tape.begin(), tape.end(), [](auto s) { return s != 0; });
    auto last = std::find_if(tape.rbegin(), tape.rend(), [](auto s) { return s != 0; }).base();
    const bool empty = first == tape.end();
    if (empty) last = first;
    const auto left = empty ? 0 : origin + (first - tape.begin());
    const auto right = left + (last - first) - 1;
    std::cout << "defined steps " << steps << "\nundefined entry " << char('A' + state)
              << int(tape[index]) << "\nhead " << origin + index
              << "\nsupport bounds " << left << ' ' << right << '\n';
    std::array<std::uint64_t, 5> counts{};
    for (auto it = first; it != last; ++it) ++counts[*it];
    std::cout << "symbols 1-4";
    for (int s = 1; s <= 4; ++s) std::cout << ' ' << counts[s];
    std::cout << '\n';
    if (argc == 2) {
        std::ofstream file(argv[1], std::ios::binary);
        for (auto it = first; it != last; ++it) file.put(char('0' + *it));
        file.put('\n');
        file.close();
        if (!file) {
            std::cerr << "could not write final tape\n";
            return 1;
        }
    }
}
