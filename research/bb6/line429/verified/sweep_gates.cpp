// Track both finite-word tests at every shaped configuration of normalized line 429.
// A stored mask says which DFA starting states accept the half-tape at this cell.
#include <array>
#include <cstdint>
#include <iostream>
#include <set>
#include <string>
#include <vector>

using DFA = std::array<std::array<unsigned, 2>, 6>;
constexpr unsigned reject = 6, accept = 7;
// The left DFA merges l0 with j, and l1 with b, of LeftDFA429.hop.
constexpr DFA left_dfa{{{1,5},{2,0},{3,4},{reject,accept},{5,4},{1,reject}}};
// TT/fresh, TT/0, TT/01, FT/fresh, FT/0, FT/01 in Gate429.gate.
// FF cannot enable the test, so it is the reject state.
constexpr DFA right_dfa{{{1,3},{accept,2},{0,1},{4,reject},{reject,5},{reject,1}}};

struct Cell { unsigned char symbol, mask; };
class HalfTape {
    std::vector<Cell> cells;
    std::array<std::array<unsigned char, 64>, 2> prepend{};
public:
    HalfTape(const DFA& dfa, unsigned char blank_mask) : cells{{0,blank_mask}} {
        for (unsigned b = 0; b < 2; ++b) {
            for (unsigned mask = 0; mask < 64; ++mask) {
                unsigned updated = 0;
                for (unsigned q = 0; q < 6; ++q) {
                    unsigned next = dfa[q][b];
                    if (next == accept || (next < 6 && (mask & (1u << next))))
                        updated |= 1u << q;
                }
                prepend[b][mask] = static_cast<unsigned char>(updated);
            }
        }
    }
    void push(unsigned char b) { cells.push_back({b, prepend[b][cells.back().mask]}); }
    unsigned char pop() {
        unsigned char b = cells.back().symbol;
        if (cells.size() > 1) cells.pop_back();
        return b;
    }
    unsigned nearest() const { return cells.back().symbol; }
    bool accepts(unsigned q, bool skip_nearest) const {
        auto index = cells.size() - 1;
        if (skip_nearest && index > 0) --index;
        return (cells[index].mask & (1u << q)) != 0;
    }
};

int main(int argc, char** argv) {
    if (argc < 2) { std::cerr << "usage: sweep_gates MOVES [NORMALIZED_NONBLANK_CELLS...]\n"; return 2; }
    const auto limit = std::stoull(argv[1]);
    HalfTape left(left_dfa, 0), right(right_dfa, 7);
    std::set<int> ones;
    for (int i = 2; i < argc; ++i) ones.insert(std::stoi(argv[i]));
    if (!ones.empty()) {
        for (int i = *ones.begin(); i < 0; ++i) left.push(ones.count(i));
        for (int i = *ones.rbegin(); i > 0; --i) right.push(ones.count(i));
    }
    struct Action { unsigned char write; bool right; unsigned next; };
    constexpr Action table[6][2] = {
        {{1,true,1},{1,true,0}}, {{1,false,2},{0,true,3}},
        {{1,false,3},{1,false,1}}, {{1,false,5},{0,false,4}},
        {{0,false,1},{0,false,4}}, {{0,true,0},{0,false,6}}
    };
    std::uint64_t counts[2][2]{};
    unsigned q = 1;
    unsigned char bit = ones.count(0);
    for (std::uint64_t t = 0; t < limit; ++t) {
        if (q == 0 && bit == 1 && left.nearest() == 0) {
            bool stop = left.accepts(1, true), open = right.accepts(0, false);
            if (counts[stop][open]++ == 0)
                std::cout << "first left_stop=" << stop << " right_open=" << open << " at " << t << '\n';
        }
        auto a = table[q][bit];
        if (a.next == 6) { std::cout << "HALT " << t << '\n'; return 0; }
        if (a.right) { left.push(a.write); bit = right.pop(); }
        else { right.push(a.write); bit = left.pop(); }
        q = a.next;
    }
    std::cout << "configurations=" << limit << " left_turn_right_closed=" << counts[0][0]
              << " left_turn_right_open=" << counts[0][1] << " left_stop_right_closed=" << counts[1][0]
              << " left_stop_right_open=" << counts[1][1] << '\n';
}
