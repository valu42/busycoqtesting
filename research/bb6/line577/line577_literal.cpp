// Independent one-transition controls for the ranking table and its reflected reference.
// Reads records produced by line577_replay.py --literal-checkpoints.
#include <algorithm>
#include <array>
#include <cassert>
#include <iostream>
#include <string>
#include <vector>

struct Transition {
    int value;
    int direction;
    int state;
};

int main(int argc, char** argv) {
    if (argc != 2 || (std::string(argv[1]) != "original" && std::string(argv[1]) != "reflected")) {
        std::cerr << "Choose original or reflected\n";
        return 2;
    }
    const bool original = std::string(argv[1]) == "original";
    const std::string table = original
        ? "1RB0LD1LC1RE1LA1RC1RA0LC0RF---0LD1RB"
        : "1LB1LE1RC1LB1LA0RD1LC0RB0LF---0RD1LA";
    std::array<std::array<Transition, 2>, 6> rules{};
    for (int state = 0; state < 6; ++state) {
        for (int bit = 0; bit < 2; ++bit) {
            const int index = 6 * state + 3 * bit;
            rules[state][bit] = {table[index] - '0', table[index + 1] == 'R' ? 1 : -1, table[index + 2] - 'A'};
        }
    }
    std::vector<char> tape(1024);
    int head = tape.size() / 2;
    int low = head, high = head, state = original ? 0 : 2;
    long long time = 0, reference_time, target_time;
    char expected_state;
    std::string ignore, left, right;
    while (std::cin >> reference_time >> target_time >> expected_state) {
        std::getline(std::cin, ignore);
        std::getline(std::cin, left);
        std::getline(std::cin, right);
        const long long stop = original ? target_time : reference_time;
        assert(time <= stop);
        while (time < stop) {
            if (head < 0 || head >= static_cast<int>(tape.size())) {
                const int offset = tape.size() / 2;
                std::vector<char> larger(tape.size() * 2);
                std::copy(tape.begin(), tape.end(), larger.begin() + offset);
                tape.swap(larger);
                head += offset;
                low += offset;
                high += offset;
            }
            low = std::min(low, head);
            high = std::max(high, head);
            const auto transition = rules[state][tape[head]];
            assert(transition.state >= 0);
            tape[head] = transition.value;
            head += transition.direction;
            state = transition.state;
            ++time;
        }
        const char mapped = original ? std::string("BCADEF")[expected_state - 'A'] : expected_state;
        assert(state == mapped - 'A');
        auto half = [&](int index, int direction) {
            std::string bits;
            while (index >= std::min(low, head) && index <= std::max(high, head)) {
                bits += index >= 0 && index < static_cast<int>(tape.size()) ? '0' + tape[index] : '0';
                index += direction;
            }
            while (!bits.empty() && bits.back() == '0') bits.pop_back();
            return bits;
        };
        const int direction = original ? -1 : 1;
        assert(half(head - direction, -direction) == left);
        assert(half(head, direction) == right);
        std::cout << time << " exact match\n";
    }
}
