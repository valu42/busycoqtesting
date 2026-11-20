// Exact-integer necessary tests for an ordinary crossing at mass coordinate T.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using Word = std::uint64_t;
using Mask = std::uint16_t;
constexpr std::array<Word, 4> gain = {5, 9, 7, 7};
constexpr std::array<Word, 4> bias = {20, 35, 26, 29};
constexpr unsigned horizon = 512;
constexpr unsigned past_calls = 32;
constexpr unsigned presieve_calls = 10;

// Dropping input guards enlarges the set of admitted ordinary predecessors.
// The positive projection representative used by the presieve avoids rejecting
// a valid class just because its chosen representative is too close to zero.
bool has_past(unsigned calls, Word u, Word d, unsigned crossing_offset = 0) {
    if (calls < 2) return true;
    if (crossing_offset < 2 && (d + u) % 3 == 0 &&
        has_past(calls - 1, u - 2, (d + u - 3) / 3)) {
        return true;
    }
    for (unsigned r = 0; r < gain.size(); ++r) {
        if (crossing_offset >= gain[r] || 4 * d < bias[r]) continue;
        Word numerator = 4 * d - bias[r];
        if (numerator % 9 == 0 &&
            has_past(calls - 2, u - gain[r], numerator / 9)) {
            return true;
        }
    }
    return false;
}

unsigned future_length(Word u, Word d) {
    for (unsigned count = 0; count < horizon; ++count) {
        if (3 * d + 1 >= u) {
            d = 3 * d + 1 - u;
            u += 2;
        } else {
            unsigned r = d % 4;
            Word next = (9 * d + bias[r]) / 4;
            u += gain[r];
            if (2 * next >= u) return count;
            d = next;
        }
    }
    throw std::runtime_error("A candidate reached the search horizon.");
}

class Search {
    Word center, modulus = 1, scanned = 0, selected = 0, replays = 0, leaves = 0;
    Word arg_d = 0, arg_mass = 0, past_end = 0, previous_low = 0;
    unsigned max_depth = 0, longest = 0;
    std::vector<Mask> table;

    void evaluate(Word u, Word d) {
        unsigned n = future_length(u, d);
        if (n > longest) {
            longest = n;
            arg_mass = u;
            arg_d = d;
        }
    }

    void scan(Word low, Word high) {
        ++leaves;
        if (low < previous_low) throw std::logic_error("Unordered leaf intervals.");
        previous_low = low;
        low = std::max(low, past_end);
        if (high < low) return;
        scanned += high - low + 1;
        Word residue = low % modulus;
        for (Word d = low; d <= high; ++d) {
            unsigned mask = table[residue];
            if (++residue == modulus) residue = 0;
            while (mask) {
                unsigned i = __builtin_ctz(mask);
                mask &= mask - 1;
                if (2 * d >= center + i) continue;
                ++selected;
                if (!has_past(past_calls, center + i, d, i)) continue;
                ++replays;
                evaluate(center + i, d);
            }
        }
        past_end = high + 1;
    }

    // Prefix cylinder in frozen d units scaled by 32. A split is a convex
    // combination rounded to a grid point, giving error <= depth grid units.
    void cover(Word low, Word high, unsigned depth) {
        max_depth = std::max(max_depth, depth);
        Word width = high - low;
        if (width <= 32 * 24) {
            // Positive rounding only occurs at P and negative rounding only at J.
            // Their maximum errors in grid units are at most 9(depth+1)/14;
            // the note gives the two one-sided estimates.
            Word grid_error = (9 * (depth + 1)) / (14 * 32);
            Word padding = 7 + grid_error;
            Word left = low / 32;
            scan(left > padding ? left - padding : 0,
                 (high + 31) / 32 + 4 + grid_error);
            return;
        }
        cover(low, low + (4 * width + 8) / 9, depth + 1);
        cover(low + (2 * width) / 3, high, depth + 1);
    }

public:
    explicit Search(Word cut) : center(cut) {
        for (unsigned i = 0; i < presieve_calls; ++i) modulus *= 3;
        table.resize(modulus);
        for (Word d = 0; d < modulus; ++d) {
            for (unsigned i = 0; i < 9; ++i) {
                if (has_past(presieve_calls, center + i, d + 64 * modulus, i)) {
                    table[d] |= Mask(1) << i;
                }
            }
        }
    }

    void run(bool brute) {
        if (brute) {
            for (Word d = 0; d <= (center + 8) / 2; ++d) {
                for (unsigned i = 0; i < 9; ++i) {
                    if (2 * d < center + i && has_past(past_calls, center + i, d, i)) {
                        evaluate(center + i, d);
                    }
                }
            }
        } else {
            cover(0, 16 * center, 0);
        }
        std::cout << center << " " << leaves << " " << scanned << " " << selected
                  << " " << replays << " " << max_depth << " " << longest
                  << " " << arg_mass << " " << arg_d << std::endl;
    }
};

int main(int argc, char** argv) {
    bool brute = argc >= 2 && std::string(argv[1]) == "--brute";
    if (argc <= 1 + brute) {
        std::cerr << "Usage: ordinary_band_sieve [--brute] CUT [CUT ...]\n";
        return 1;
    }
    for (int i = 1 + brute; i < argc; ++i) {
        Word cut = std::stoull(argv[i]);
        if (cut <= 300 || cut >= (Word(1) << 58)) {
            throw std::invalid_argument("Cut outside the supported fixed-point range.");
        }
        Search(cut).run(brute);
    }
}
