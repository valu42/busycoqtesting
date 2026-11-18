// A reduced right-boundary certificate for line 36. Invoke via line36_cap_blocks.py.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>

#ifdef NDEBUG
#error "This verifier requires assertions."
#endif
using Word = std::uint64_t;
constexpr unsigned width = 41;
constexpr unsigned extra = 1;
constexpr unsigned ticks = 8;
constexpr Word visible_mask = (Word(1)<<width)-1;

struct Measure {
    Word survivors;
    int debt, loss;
};

Measure measure(Word word, unsigned length) {
    Word survivors = 0;
    int debt = 0, odd_runs = 0, run = 0, monomers = 0;
    unsigned previous_closing = 0;  // Repeated terminal if the last digit closes.
    for (unsigned j = 0; j < length; ++j) {
        const bool closes = (word >> j) & 1;
        if (!closes && !debt) {
            survivors |= Word(1)<<j;
            ++run;
        } else {
            odd_runs += run % 2;
            run = 0;
            if (closes) {
                ++debt;
                monomers += (j-previous_closing) % 2;
                previous_closing = j;
            } else --debt;
        }
    }
    odd_runs += run % 2;
    monomers += (length-previous_closing) % 2;  // Left sentinel.
    const int loss = monomers-debt-odd_runs;
    assert(loss >= 0);
    return {survivors,debt,loss};
}

struct Move { Word word; int cost; };
using Moves = std::vector<Move>;

void keep_minimum(Moves& moves, Word word, int cost) {
    for (auto& move : moves) {
        if (move.word == word) {
            move.cost = std::min(move.cost,cost);
            return;
        }
    }
    moves.push_back({word,cost});
}

void step(Moves& next, Move input, unsigned length) {
    const Word word = input.word;
    const auto m = measure(word,length);
    assert(word && m.survivors); // The matching ledger requires a cap survivor.
    const int open_loss = measure(word,length+1).loss; // Prepend digit 1 (a zero bit).
    const int minimum = std::min(m.loss,open_loss);
    const Word image = m.survivors ^ (m.survivors>>1);
    if (!(word & 1)) {
        const Word mask = (Word(1)<<length)-1;
        keep_minimum(next,((image<<1)|1)&mask,input.cost+minimum);
    } else if (m.debt) {
        keep_minimum(next,image,input.cost+minimum);
    } else {
        // On the unflipped branch the actual preceding digit closes. An optimal
        // dimer tiling splits there, giving the stronger full-word loss.
        keep_minimum(next,image,input.cost+m.loss);
        keep_minimum(next,image^(Word(1)<<(length-1)),input.cost+minimum);
    }
}

Moves block(Word visible, int& prefix_minimum) {
    prefix_minimum = 0;
    Moves current{{visible,0},{visible|(Word(1)<<width),0}};
    for (unsigned t = 0; t < ticks; ++t) {
        Moves next;
        for (auto source : current) step(next,source,width+extra);
        current.swap(next);
        if (t+1 < ticks)
            for (auto move : current)
                prefix_minimum = std::min(prefix_minimum,3*move.cost-int(t+1));
    }
    Moves output;
    for (auto move : current) keep_minimum(output,move.word&visible_mask,move.cost);
    return output;
}

struct Edge { unsigned to; int cost; };

int main(int argc, char** argv) {
    assert(argc == 2 || argc == 3);
    const Word seed = std::stoull(argv[1]);
    assert(seed <= visible_mask);
    std::unordered_map<Word,unsigned> index;
    std::vector<Word> words;
    std::vector<Edge> edges;
    std::vector<int> prefix_minima;
    std::vector<std::size_t> end{0};
    auto insert = [&](Word word) {
        auto [entry,fresh] = index.emplace(word,static_cast<unsigned>(words.size()));
        if (fresh) words.push_back(word);
        return entry->second;
    };
    insert(seed);
    for (std::size_t i = 0; i < words.size(); ++i) {
        int minimum;
        for (auto move : block(words[i],minimum)) edges.push_back({insert(move.word),move.cost});
        prefix_minima.push_back(minimum);
        end.push_back(edges.size());
    }
    assert(words.size() == 62671 && edges.size() == 200597);
    std::vector<int> value(words.size()), next(words.size());
    unsigned rounds = 0;
    for (;;) {
        assert(rounds < 40);
        for (std::size_t i = 0; i < words.size(); ++i) {
            int best = prefix_minima[i];
            for (std::size_t j = end[i]; j < end[i+1]; ++j) {
                auto edge = edges[j];
                best = std::min(best,3*edge.cost-int(ticks)+value[edge.to]);
            }
            next[i] = best;
        }
        if (next == value) break;
        value.swap(next);
        ++rounds;
    }
    assert(rounds == 32 && value[0] == -2);
    assert(*std::min_element(value.begin(),value.end()) == -16);
    assert(*std::max_element(value.begin(),value.end()) == 0);
    for (std::size_t i = 0; i < words.size(); ++i)
        for (std::size_t j = end[i]; j < end[i+1]; ++j)
            assert(value[i] <= 3*edges[j].cost-int(ticks)+value[edges[j].to]);
    std::cout << words.size() << " block states, " << edges.size() << " edges, "
              << rounds << " changing rounds, potential [-16,0], seed " << value[0] << '\n';

    // Reconstruct intermediate potentials with at most seven one-sweep lookups.
    // The endpoint table is the sole numeric input needed by a replay checker.
    std::vector<std::unordered_map<Word,int>> intermediate(ticks);
    auto lift = [&](auto& self, unsigned phase, Word cap) -> int {
        if (phase == ticks) return value[index.at(cap & visible_mask)];
        auto& cache = intermediate[phase];
        if (phase) {
            auto found = cache.find(cap);
            if (found != cache.end()) return found->second;
        }
        Moves moves;
        step(moves,{cap,0},width+extra);
        int best = 0;
        for (auto move : moves)
            best = std::min(best,3*move.cost-1+self(self,phase+1,move.word));
        if (phase) cache.emplace(cap,best);
        return best;
    };
    for (std::size_t i = 0; i < words.size(); ++i) {
        const int a = lift(lift,0,words[i]);
        const int b = lift(lift,0,words[i]|(Word(1)<<width));
        assert(value[i] == std::min(a,b));
    }
    int overall_minimum = *std::min_element(value.begin(),value.end());
    std::size_t count = 0;
    for (unsigned phase = 1; phase < ticks; ++phase) {
        count += intermediate[phase].size();
        for (auto [cap,h] : intermediate[phase]) {
            overall_minimum = std::min(overall_minimum,h);
            assert(h <= 0);
        }
    }
    assert(count == 769600 && overall_minimum == -21);
    std::cout << count << " intermediate phase/cap pairs, one-sweep potential [-21,0]\n";
    if (argc == 3) {
        std::vector<Word> sorted = words;
        std::sort(sorted.begin(),sorted.end());
        std::ofstream output(argv[2]);
        for (Word word : sorted) output << word << '\t' << value[index.at(word)] << '\n';
        output.close();
        if (!output) return 1;
    }
}
