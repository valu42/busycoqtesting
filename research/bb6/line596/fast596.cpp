// Replay certified affine rows for BB(6) line 596. Requires GMP.
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>
#include <gmpxx.h>

using Count = std::uint64_t;
struct Rule { int next, add; };
struct Group { int next, add; bool complete; };

class Replay {
    std::vector<std::array<Rule, 3>> rules;
    std::vector<std::string> words;
    std::vector<std::array<Group, 243>> groups;
    std::map<Count, mpz_class> powers;
    int state = -1;
    bool grouped;
    Count completed = 9;

    const mpz_class& power_of_three(Count n) {
        auto it = powers.find(n);
        if (it != powers.end()) return it->second;
        mpz_class v;
        mpz_ui_pow_ui(v.get_mpz_t(), 3, n);
        return powers.emplace(n, std::move(v)).first->second;
    }

    bool valid(int dest) const {
        return dest >= 0 && static_cast<std::size_t>(dest) < rules.size();
    }

    void prepare_groups() {
        groups.resize(rules.size());
        for (std::size_t i = 0; i < rules.size(); ++i) {
            for (int residue = 0; residue < 243; ++residue) {
                int q = i, v = residue;
                bool complete = true;
                for (int j = 0; j < 5; ++j) {
                    auto rule = rules[q][v % 3];
                    if (!valid(rule.next)) {
                        complete = false;
                        break;
                    }
                    v = 4 * (v / 3) + rule.add;
                    q = rule.next;
                }
                groups[i][residue] = {q, v, complete};
            }
        }
    }

    void one(Count& low) {
        const int r = low % 3;
        auto rule = rules[state][r];
        if (!valid(rule.next)) {
            std::cout << "Return " << completed + 1 << ", suffix " << words[state]
                      << ", residue " << r << '\n';
            throw std::runtime_error(rule.next == -1 ? "Certified halting row"
                                                     : "No verified row in this table");
        }
        low = 4 * (low / 3) + rule.add;
        state = rule.next;
        ++completed;
    }

    void advance(mpz_class& n, Count length) {
        const auto& divisor = power_of_three(length);
        mpz_class high, low;
        mpz_tdiv_qr(high.get_mpz_t(), low.get_mpz_t(), n.get_mpz_t(), divisor.get_mpz_t());
        if (length <= 20) {
            Count v = low.get_ui(), j = 0;
            if (grouped) {
                for (; j + 5 <= length; j += 5) {
                    const auto g = groups[state][v % 243];
                    if (!g.complete) {
                        for (int i = 0; i < 5; ++i) one(v);
                        throw std::logic_error("Inconsistent five-return group");
                    }
                    v = 1024 * (v / 243) + g.add;
                    state = g.next;
                    completed += 5;
                }
            }
            for (; j < length; ++j) one(v);
            low = v;
        } else {
            Count first = length / 2;
            advance(low, first);
            advance(low, length - first);
        }
        mpz_mul_2exp(high.get_mpz_t(), high.get_mpz_t(), 2 * length);
        n = high + low;
    }

public:
    Replay(const std::string& path, bool grouped) : grouped(grouped) {
        static_assert(sizeof(unsigned long) >= 8, "This verifier uses 64-bit GMP limbs");
        std::ifstream in(path);
        if (!in) throw std::runtime_error("Cannot open affine table");
        int idx;
        std::string word;
        while (in >> idx >> word) {
            if (idx != static_cast<int>(rules.size())) throw std::runtime_error("Bad row index");
            std::array<Rule, 3> row;
            for (auto& r : row) {
                if (!(in >> r.next >> r.add) || r.add < 0 || r.add > 100000)
                    throw std::runtime_error("Invalid affine constant");
            }
            if (word == "010111") state = idx;
            words.push_back(word);
            rules.push_back(row);
        }
        if (state < 0) throw std::runtime_error("Missing initial suffix");
        if (grouped) prepare_groups();
    }

    void run(Count limit) {
        if (limit < 9 || limit > 1000000000000ULL)
            throw std::runtime_error("Return count outside supported range");
        // The direct verifier reaches P(306,010111) after nine complete returns.
        mpz_class n = 306;
        Count checkpoint = 20;
        while (completed < limit) {
            const Count goal = std::min(checkpoint, limit);
            advance(n, goal - completed);
            std::cout << completed << " returns, " << mpz_sizeinbase(n.get_mpz_t(), 2)
                      << " bits in n, n mod 1000000007 = " << mpz_fdiv_ui(n.get_mpz_t(), 1000000007)
                      << ", suffix " << words[state] << std::endl;
            checkpoint *= 2;
        }
    }
};

int main(int argc, char** argv) {
    if (argc < 3 || argc > 4) {
        std::cerr << "Usage: fast596 TABLE RETURNS [--single]\n";
        return 2;
    }
    try {
        if (argc == 4 && std::string(argv[3]) != "--single") return 2;
        Replay run(argv[1], argc == 3);
        run.run(std::stoull(argv[2]));
    } catch (const std::exception& e) {
        std::cerr << e.what() << '\n';
        return 1;
    }
}
