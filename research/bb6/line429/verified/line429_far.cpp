// Enumerate one-sided finite automata for pinned ranking line 429.
// Build with g++ -O3 -std=c++17 line429_far.cpp -o line429_far.
// Run ./line429_far 5 0 for the original machine, or 5 1 for its reflection.
#include <algorithm>
#include <array>
#include <charconv>
#include <cstdint>
#include <iostream>
#include <string_view>
#include <system_error>

using StateSet = std::uint64_t;
constexpr int tm_states = 6;
constexpr int max_dfa_states = 10;
constexpr int max_nfa_states = tm_states * max_dfa_states + 1;
using BinaryDfa = std::array<std::array<int, 2>, max_dfa_states>;
using Nfa = std::array<std::array<StateSet, max_nfa_states>, 2>;

struct Action {
    int write;
    bool right;
    int next;  // -1 means halt
};

constexpr char table[] = "1RB0LC_1RC1RA_1RD0RF_0LE---_1LA1LE_0RA0RF";

Action action_at(int state, int bit) {
    const char* rule = table + 7 * state + 3 * bit;
    if (rule[0] == '-') return {0, false, -1};
    return {rule[0] - '0', rule[1] == 'R', rule[2] - 'A'};
}

StateSet singleton(int state) {
    return StateSet{1} << state;
}

StateSet advance(const Nfa& nfa, StateSet states, int bit) {
    StateSet result = 0;
    while (states != 0) {
        int state = __builtin_ctzll(states);
        states &= states - 1;
        result |= nfa[bit][state];
    }
    return result;
}

bool accepts_blank(const Nfa& nfa, StateSet final_state) {
    // Any finite prefix of 0^omega can witness acceptance. The final state
    // loops on both symbols, so reaching it suffices for every continuation.
    StateSet reached = singleton(0);
    while (true) {
        StateSet extended = reached | advance(nfa, reached, 0);
        if (extended & final_state) return true;
        if (extended == reached) return false;
        reached = extended;
    }
}

struct PopRule {
    int read;
    int source;
    int predecessor;
    int popped_bit;
    int written_bit;
};

bool certifies_nonhalting(const BinaryDfa& dfa, int size, bool reflect) {
    // The DFA summarizes the left half-tape, read from far left to the head.
    // The NFA reads the exact right half starting at the scanned symbol. Its
    // product state pairs the Turing control with the left DFA state.
    int final_index = tm_states * size;
    StateSet final_state = singleton(final_index);
    Nfa nfa{};
    nfa[0][final_index] = nfa[1][final_index] = final_state;
    std::array<PopRule, 4 * tm_states * max_dfa_states> pop_rules;
    int rule_count = 0;

    for (int state = 0; state < tm_states; ++state) {
        for (int bit = 0; bit < 2; ++bit) {
            Action action = action_at(state, bit);
            for (int left = 0; left < size; ++left) {
                int product = state * size + left;
                if (action.next < 0) {
                    nfa[bit][product] = final_state;
                } else if (action.right != reflect) {
                    int new_left = dfa[left][action.write];
                    nfa[bit][product] = singleton(action.next * size + new_left);
                } else {
                    // A left move pops an unknown bit. For every possible
                    // previous DFA state and popped bit, the new right tape
                    // starts with that bit followed by the bit just written.
                    for (int popped = 0; popped < 2; ++popped) {
                        int old_left = dfa[left][popped];
                        pop_rules[rule_count++] = {
                            bit, state * size + old_left, action.next * size + left,
                            popped, action.write
                        };
                    }
                }
            }
        }
    }

    while (true) {
        bool changed = false;
        for (int i = 0; i < rule_count; ++i) {
            const PopRule& rule = pop_rules[i];
            StateSet intermediate = nfa[rule.popped_bit][rule.predecessor];
            StateSet added = advance(nfa, intermediate, rule.written_bit);
            StateSet& old = nfa[rule.read][rule.source];
            if ((added & ~old) != 0) {
                old |= added;
                changed = true;
            }
        }
        if (accepts_blank(nfa, final_state)) return false;
        if (!changed) return true;
    }
}

struct Search {
    int size;
    bool reflect;
    BinaryDfa dfa{};
    std::uint64_t tested = 0;
    std::uint64_t certificates = 0;

    void enumerate(int slot, int highest) {
        if (slot == 2 * size) {
            if (highest != size - 1) return;
            ++tested;
            if (certifies_nonhalting(dfa, size, reflect)) {
                ++certificates;
                std::cout << "certificate";
                for (int state = 0; state < size; ++state)
                    std::cout << ' ' << dfa[state][0] << ' ' << dfa[state][1];
                std::cout << '\n';
            }
            return;
        }

        // Number states in the order their transitions first discover them.
        // If the current state is still undiscovered, this table cannot be
        // accessible. One canonical table represents each rooted DFA.
        if (slot / 2 > highest) return;
        int largest_destination = std::min(highest + 1, size - 1);
        for (int dest = 0; dest <= largest_destination; ++dest) {
            dfa[slot / 2][slot % 2] = dest;
            enumerate(slot + 1, std::max(highest, dest));
        }
    }
};

int main(int argc, char** argv) {
    int size = 0;
    if (argc == 3) {
        std::string_view arg(argv[1]);
        auto result = std::from_chars(arg.data(), arg.data() + arg.size(), size);
        if (result.ec != std::errc{} || result.ptr != arg.data() + arg.size())
            size = 0;
    }
    if (argc != 3 || size < 1 || size > max_dfa_states ||
            (std::string_view(argv[2]) != "0" && std::string_view(argv[2]) != "1")) {
        std::cerr << "usage: line429_far N REFLECT (N=1..10, REFLECT=0 or 1)\n";
        return 2;
    }
    bool reflect = std::string_view(argv[2]) == "1";
    Search search{size, reflect};
    // The infinitely blank part of the summarized half-tape is the start
    // state. Adding another leading zero must preserve that state.
    search.dfa[0][0] = 0;
    search.enumerate(1, 0);
    std::cout << "states=" << size << " reflected=" << reflect
              << " accessible=" << search.tested << " tested=" << search.tested
              << " certificates=" << search.certificates << '\n';
}
