// Independent replay of line 429. The only machine-specific data are these twelve entries.
// With --single, every loop iteration performs exactly one ordinary transition.
#include <array>
#include <cstdint>
#include <deque>
#include <iostream>
#include <string>
#include <vector>

constexpr std::array<const char*, 12> table = {
    "1RB", "0LC", "1RC", "1RA", "1RD", "0RF",
    "0LE", "---", "1LA", "1LE", "0RA", "0RF"
};

struct Instruction { int write, delta, state; };
struct Exit {
    unsigned steps = 0;
    uint16_t word = 0;
    int head = 0, state = 0;
    bool tried = false;
};

class Tape {
    std::deque<uint16_t> cells{0};
    long long first = 0;
public:
    uint16_t& word(long long i) {
        while (i < first) { cells.push_front(0); --first; }
        while (i >= first + static_cast<long long>(cells.size())) cells.push_back(0);
        return cells[static_cast<size_t>(i - first)];
    }
    std::string hex_half(long long head, int direction) const {
        long long cell = head;
        std::string hex;
        while (cell >= 16 * first && cell < 16 * (first + static_cast<long long>(cells.size()))) {
            unsigned nibble = 0;
            for (int bit = 0; bit < 4; ++bit, cell += direction) {
                const long long d = cell - 16 * first;
                if (d >= 0 && d < 16 * static_cast<long long>(cells.size()))
                    nibble |= ((cells[d / 16] >> (d % 16)) & 1u) << bit;
            }
            hex.push_back("0123456789abcdef"[nibble]);
        }
        while (!hex.empty() && hex.back() == '0') hex.pop_back();
        return hex.empty() ? "0" : std::string(hex.rbegin(), hex.rend());
    }
};

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "usage: literal MOVES [--single] [--one COORDINATE]...\n";
        return 2;
    }
    const uint64_t target = std::stoull(argv[1]);
    bool single = false;
    Tape tape;
    for (int i = 2; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg == "--single") {
            single = true;
        } else if (arg == "--one" && i+1 < argc) {
            const long long cell = std::stoll(argv[++i]);
            const int bit = static_cast<int>((cell % 16 + 16) % 16);
            tape.word((cell - bit) / 16) |= static_cast<uint16_t>(1u << bit);
        } else {
            std::cerr << "unknown or incomplete argument " << arg << '\n';
            return 2;
        }
    }
    std::array<Instruction,12> program;
    for (size_t i = 0; i < table.size(); ++i) {
        const char* s = table[i];
        program[i] = {s[0] - '0', s[1] == 'R' ? 1 : -1, s[2] - 'A'};
    }
    std::vector<Exit> cache(single ? 0 : 12 * 65536);
    long long block = 0;
    int pos = 0, q = 0;
    uint64_t time = 0;
    while (time < target) {
        uint16_t& cells = tape.word(block);
        bool crossed = false;
        if (!single && (pos == 0 || pos == 15)) {
            Exit& e = cache[(12 * unsigned(cells)) + 2*q + (pos == 15)];
            if (!e.tried) {
                e.tried = true;
                uint16_t x = cells;
                int p = pos, s = q;
                // A slow or halting block falls back to ordinary transitions.
                for (unsigned t = 1; t <= 65536; ++t) {
                    const auto& a = program[2*s + ((x >> p) & 1)];
                    if (a.state < 0) break;
                    x = static_cast<uint16_t>((x & ~(1u << p)) | (unsigned(a.write) << p));
                    s = a.state;
                    p += a.delta;
                    if (p < 0 || p == 16) { e = {t,x,p,s,true}; break; }
                }
            }
            if (e.steps && e.steps <= target - time) {
                cells = e.word; time += e.steps; q = e.state; pos = e.head;
                crossed = true;
            }
        }
        if (!crossed) {
            const auto& a = program[2*q + ((cells >> pos) & 1)];
            if (a.state < 0) break;
            cells = static_cast<uint16_t>((cells & ~(1u << pos)) | (unsigned(a.write) << pos));
            pos += a.delta; q = a.state; ++time;
        }
        if (pos < 0) { --block; pos = 15; }
        else if (pos == 16) { ++block; pos = 0; }
    }
    const long long h = 16*block + pos;
    // Include a boundary cell beyond the visited range even if the final move just exited it.
    tape.word(block);
    std::cout << time << ' ' << char('A'+q) << ' ' << h << '\n'
              << tape.hex_half(h-1, -1) << '\n' << tape.hex_half(h, 1) << '\n';
}
