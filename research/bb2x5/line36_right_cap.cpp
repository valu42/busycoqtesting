// Compile with a C++17 compiler, e.g. c++ -O2 -std=c++17 line36_right_cap.cpp.
// Run in the directory containing BB2x5_Rocq_holdouts_37.txt.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Word = std::uint64_t;
const std::string machine = "1RB2LA1LA4RA2LA_0LA3RB3LB2RB---";

void require(bool condition, const char* error) {
    if (!condition) throw std::runtime_error(error);
}

Word blank_seed(int width) {
    std::ifstream list("BB2x5_Rocq_holdouts_37.txt");
    std::string line;
    for (int i = 0; i < 36; ++i) {
        require(static_cast<bool>(std::getline(list, line)), "missing machine list");
    }
    require(line == machine, "line 36 machine mismatch");

    std::map<int,int> tape;
    int head = 0, state = 0, epochs = 0;
    for (int steps = 0; steps < 1000000; ++steps) {
        auto it = tape.find(head);
        int digit = it == tape.end() ? 0 : it->second;
        int pos = 16 * state + 3 * digit;
        require(machine[pos] != '-', "halt before seed");
        int written = machine[pos] - '0';
        if (written) tape[head] = written;
        else tape.erase(head);
        head += machine[pos+1] == 'R' ? 1 : -1;
        state = machine[pos+2] == 'B';
        if (state || tape.empty() || head+1 != tape.begin()->first) continue;
        int length = tape.rbegin()->first - head;
        if (static_cast<int>(tape.size()) != length) continue;
        if (std::any_of(tape.begin(), tape.end(), [](const auto& item) {
            return item.second > 2;
        })) continue;
        if (++epochs == 32) {
            require(length == 92 && length >= width, "wrong epoch-32 length");
            Word seed = 0;
            for (auto [coordinate,value] : tape) seed = (seed << 1) | (value == 2);
            return seed & ((Word(1) << width) - 1);
        }
    }
    throw std::runtime_error("seed work limit");
}

// Bit j is one for tape digit 2 at distance j from the right edge.
struct Transition {
    Word first, second;
    int loss;
    bool has_survivor;
};

Transition cap_step(Word cap, int width) {
    int anchor = width-1;
    while (anchor >= 0 && !(cap & (Word(1) << anchor))) --anchor;
    require(anchor >= 0, "cap lacks a closing anchor");
    int debt = 0, cost_debt = 0, run = 0, odd_runs = 0;
    Word survivors = 0;
    for (int j = 0; j < width; ++j) {
        if (j == anchor) {
            cost_debt = debt;
            odd_runs += run % 2;
        }
        bool closing = cap & (Word(1) << j);
        bool survives = !closing && !debt;
        if (closing) ++debt;
        else if (debt) --debt;
        if (survives) survivors |= Word(1) << j;
        if (j < anchor) {
            if (survives) ++run;
            else {
                odd_runs += run % 2;
                run = 0;
            }
        }
    }
    int monomers = 0, previous = anchor;
    for (int j = anchor-1; j >= 0; --j) {
        if (j == 0 || (cap & (Word(1) << j))) {
            monomers += (previous-j) % 2;
            previous = j;
        }
    }
    int loss = monomers - cost_debt - odd_runs;
    require(loss >= 0 && loss % 2 == 0, "invalid cap loss");
    Word image = survivors ^ (survivors >> 1);
    if (!(cap & 1)) {
        Word mask = (Word(1) << width) - 1;
        image = ((image << 1) | 1) & mask;
        return {image, image, loss, survivors != 0};
    }
    Word other = debt ? image : image ^ (Word(1) << (width-1));
    return {image, other, loss, survivors != 0};
}

// Small independent audit using a left-to-right matching stack and a tiling DP.
int tiling_cost(const std::vector<int>& word) {
    std::vector<int> best(word.size()+1, static_cast<int>(word.size())+1);
    best[0] = 0;
    for (std::size_t i = 0; i < word.size(); ++i) {
        best[i+1] = std::min(best[i+1], best[i]+1);
        if (word[i] == 1 && i+1 < word.size()) best[i+2] = std::min(best[i+2], best[i]);
    }
    return best.back();
}

void check_small_cuts() {
    for (int length = 2; length <= 11; ++length) {
        for (Word raw = 0; raw < (Word(1) << length); ++raw) {
            std::vector<int> tape, remaining, survivor(length);
            int unpaid = 0;
            for (int i = 0; i < length; ++i) {
                bool closing = raw & (Word(1) << (length-1-i));
                tape.push_back(closing ? 2 : 1);
                if (!closing) remaining.push_back(i);
                else if (!remaining.empty()) remaining.pop_back();
                else ++unpaid;
            }
            for (int i : remaining) survivor[i] = 1;
            std::vector<int> next;
            Word encoded = 0;
            for (int i = 1; i < length; ++i) {
                next.push_back(1 + (survivor[i-1] ^ survivor[i]));
                encoded = (encoded << 1) | (next.back() == 2);
            }
            if (survivor.back()) {
                next.push_back(2);
                encoded = (encoded << 1) | 1;
            }
            int allowance = tiling_cost(tape) + !survivor.back() - tiling_cost(next) - 2*(unpaid/2);
            if (unpaid % 2 && !remaining.empty()) {
                auto extended = next;
                extended.insert(extended.begin(), 1);
                require(tiling_cost(extended)+1 == tiling_cost(next), "adaptive cut failed");
            }
            for (int width = 1; width < length; ++width) {
                Word mask = (Word(1) << width) - 1, cap = raw & mask;
                if (!cap) continue;
                auto step = cap_step(cap, width);
                Word target = encoded & mask;
                require(step.first == target || step.second == target, "small image mismatch");
                require(allowance >= step.loss, "small tiling inequality failed");
            }
        }
    }
}

struct Node {
    int a, b, loss;
};

// The table stores one integer index per slot. The 50-cell graph peaks
// below 500 MB when built with 32-bit int and 64-bit Word.
std::vector<Node> cap_graph(Word seed, int width, int expected) {
    std::size_t capacity = 1;
    while (capacity * 7 < static_cast<std::size_t>(expected) * 10) capacity *= 2;
    std::vector<int> index(capacity, -1);
    std::vector<Word> words;
    std::vector<Node> graph;
    words.reserve(expected);
    graph.reserve(expected);
    auto insert = [&](Word word) {
        Word key = word;
        key = (key ^ (key >> 30)) * 0xbf58476d1ce4e5b9ULL;
        key = (key ^ (key >> 27)) * 0x94d049bb133111ebULL;
        std::size_t slot = (key ^ (key >> 31)) & (capacity - 1);
        while (index[slot] != -1) {
            if (words[index[slot]] == word) return index[slot];
            slot = (slot + 1) & (capacity - 1);
        }
        require(words.size() < static_cast<std::size_t>(expected), "larger cap graph than expected");
        index[slot] = static_cast<int>(words.size());
        words.push_back(word);
        return index[slot];
    };
    insert(seed);
    for (std::size_t i = 0; i < words.size(); ++i) {
        auto step = cap_step(words[i], width);
        require(step.has_survivor, "reachable cap has no survivor");
        int a = insert(step.first), b = insert(step.second);
        graph.push_back({a, b, step.loss});
    }
    require(static_cast<int>(graph.size()) == expected, "smaller cap graph than expected");
    return graph;
}

struct Certificate {
    int width, vertices, start, period, increment;
};

void check(Certificate c) {
    auto graph = cap_graph(blank_seed(c.width), c.width, c.vertices);
    std::vector<int> value(graph.size()), next(graph.size()), earlier;
    int worst = 0, seed_worst = 0;
    for (int t = 0; t <= c.start+c.period; ++t) {
        if (t == c.start) earlier = value;
        int min_value = *std::min_element(value.begin(), value.end());
        worst = std::max(worst, t*c.increment - c.period*min_value);
        seed_worst = std::max(seed_worst, t*c.increment - c.period*value[0]);
        if (t == c.start+c.period) {
            for (std::size_t i = 0; i < graph.size(); ++i) {
                require(value[i] == earlier[i]+c.increment, "period equality failed");
            }
            break;
        }
        for (std::size_t i = 0; i < graph.size(); ++i) {
            auto n = graph[i];
            next[i] = n.loss + std::min(value[n.a], value[n.b]);
        }
        value.swap(next);
    }
    std::cout << "width " << c.width << ", " << c.vertices << " states, "
              << "D(t+" << c.period << ") = D(t)+" << c.increment
              << " for t >= " << c.start << "\n";
    std::cout << "loss >= (" << c.increment << "*t-" << worst << ")/" << c.period
              << " from every reachable cap, (" << c.increment << "*t-"
              << seed_worst << ")/" << c.period << " from epoch 32\n";
}

void check_one_third() {
    const int width = 50;
    auto graph = cap_graph(blank_seed(width), width, 16939461);
    std::vector<int> value(graph.size()), next(graph.size());
    // Include the empty path at every vertex. At convergence the resulting
    // potential is a lower bound for every finite path's 3*cost - length.
    for (int t = 1; t <= 800; ++t) {
        bool changed = false;
        for (std::size_t i = 0; i < graph.size(); ++i) {
            Node n = graph[i];
            next[i] = std::min(0, 3*n.loss - 1 + std::min(value[n.a], value[n.b]));
            changed |= next[i] != value[i];
        }
        if (!changed) {
            require(value[0] == 0 && *std::min_element(value.begin(), value.end()) == -21,
                    "unexpected potential range");
            for (std::size_t i = 0; i < graph.size(); ++i) {
                Node n = graph[i];
                require(value[i] <= 3*n.loss-1 + value[n.a] &&
                        value[i] <= 3*n.loss-1 + value[n.b], "invalid potential");
            }
            std::cout << "width 50, " << graph.size() << " states, integer potential fixed "
                      << "at update " << t << ", range [-21,0], seed 0\n";
            return;
        }
        value.swap(next);
    }
    throw std::runtime_error("potential did not converge");
}

int main(int argc, char** argv) {
    check_small_cuts();
    const int width = argc == 2 ? std::stoi(argv[1]) : 36;
    if (width == 50) { check_one_third(); return 0; }
    for (auto c : std::vector<Certificate>{
            {20,264,15,64,10}, {30,10437,162,8,2}, {36,95863,255,152,46},
            {40,419099,284,152,48}, {44,1833538,594,80,26},
            {46,3840923,353,104,34}}) {
        if (c.width == width) { check(c); return 0; }
    }
    throw std::runtime_error("choose width 20, 30, 36, 40, 44, 46 or 50");
}
