// Scan original, elementary configurations at indices 0 through limit-1.
// Only defined transitions advance the clock. A dense tape with dynamic extension represents
// both infinite zero tails, so "blank beyond the head" is checked exactly.
#include <array>
#include <cstdint>
#include <iostream>
#include <deque>
#include <string>

struct Station {
    std::uint64_t count = 0, nonblank = 0, inside_visited = 0;
    std::uint64_t on_previous_edge = 0, beyond_previous_edge = 0;
};
int main(int argc, char** argv) {
    if (argc != 2) return 2;
    const std::uint64_t limit = std::stoull(argv[1]);
    const std::array<std::string, 6> table = {
        "1RB0LC", "1RC1RA", "1RD0RF", "0LE---", "1LA1LE", "0RA0RF"
    };
    // Dynamically extend a dense tape for O(1) reads. The last one on the
    // right is maintained separately and verified after each removal.
    static constexpr int block = 4096;
    std::deque<unsigned char> tape(block);
    std::int64_t head = 0, origin = -block/2, previous_max = -1;
    std::int64_t rightmost = 0;
    bool empty = true;
    auto cell = [&](std::int64_t p) -> unsigned char& {
        while (p < origin) { tape.insert(tape.begin(), block, 0); origin -= block; }
        while (p >= origin + static_cast<std::int64_t>(tape.size()))
            tape.insert(tape.end(), block, 0);
        return tape[static_cast<std::size_t>(p-origin)];
    };
    auto update = [&](int b) {
        cell(head) = static_cast<unsigned char>(b);
        if (b && (empty || head > rightmost)) { empty = false; rightmost = head; }
        if (!b && !empty && head == rightmost) {
            while (rightmost >= origin && !cell(rightmost)) --rightmost;
            if (rightmost < origin) empty = true;
        }
    };
    Station station;
    int q = 0;
    for (std::uint64_t t = 0; t < limit; ++t) {
        int b = cell(head);
        if (q == 1 && !b && !cell(head+1)) {
            ++station.count;
            if (!empty && rightmost >= head) ++station.nonblank;
            if (head < previous_max) ++station.inside_visited;
            if (head == previous_max) ++station.on_previous_edge;
            if (head > previous_max) ++station.beyond_previous_edge;
        }
        if (head > previous_max) previous_max = head;
        const char* ins = &table[q][3*b];
        if (ins[0] == '-') { std::cout << "halt at " << t << '\n'; return 1; }
        update(ins[0]-'0');
        head += (ins[1] == 'R') ? 1 : -1;
        q = ins[2] - 'A';
    }
    std::cout << "steps=" << limit << " B00_visits=" << station.count
              << " nonblank_suffix=" << station.nonblank
              << " interior=" << station.inside_visited
              << " at_prior_edge=" << station.on_previous_edge
              << " new_edge=" << station.beyond_previous_edge << '\n';
}
