// Read the checked six-phase grammar from line36_left.py.
#include <algorithm>
#include <cassert>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

#ifdef NDEBUG
#error "Compile with assertions enabled"
#endif

using std::string;
using std::vector;

constexpr int phases = 6;
constexpr int halo_size = 3;
constexpr int debt_limit = 28;
constexpr int earlier_pieces = 4;
string prefix[phases], piece[phases][6][2];
int header_size[phases];

struct State {
    int phase, kind, last_choice;
    string partial, halo;

    auto key() const { return std::tie(phase, kind, last_choice, partial, halo); }
    bool operator<(const State& other) const { return key() < other.key(); }
};

struct Edge {
    int destination, displacement, charge, debt;
    auto key() const { return std::tie(destination, displacement, charge, debt); }
    bool operator<(const Edge& other) const { return key() < other.key(); }
};

vector<State> states;
std::map<State, int> ids;

int parity(int n) {
    return ((n % 2) + 2) % 2;
}

int last_closing(const string& text, int end) {
    assert(end > 0);
    auto position = text.rfind('2', end - 1);
    assert(position != string::npos);
    return static_cast<int>(position);
}

void enumerate_states() {
    for (int t = 0; t < phases; ++t) {
        for (int k = 0; k < 6; ++k) {
            for (int previous : {0, 1}) {
                for (int variant : {0, 1}) {
                    const auto& text = piece[t][k][variant];
                    for (size_t length = 0; length < text.size(); ++length) {
                        for (int mask = 0; mask < (1 << halo_size); ++mask) {
                            string halo;
                            for (int i = 0; i < halo_size; ++i)
                                halo += (mask & (1 << i)) ? '2' : '1';
                            State s{t, k, previous, text.substr(0, length), halo};
                            if (ids.emplace(s, static_cast<int>(states.size())).second)
                                states.push_back(s);
                        }
                    }
                }
            }
        }
    }
}

struct Parsed {
    int complete, last_choice, end;
    string partial;
};

Parsed parse(int phase, const string& text) {
    assert(text.compare(0, prefix[phase].size(), prefix[phase]) == 0);
    int position = static_cast<int>(prefix[phase].size());
    int limit = static_cast<int>(text.size()) - halo_size;
    int complete = 0, last = -1;
    while (true) {
        const auto& alternatives = piece[phase][complete % 6];
        int choice = 0;
        for (; choice < 2; ++choice) {
            const auto& p = alternatives[choice];
            if (position + static_cast<int>(p.size()) <= limit &&
                    text.compare(position, p.size(), p) == 0)
                break;
        }
        if (choice == 2) {
            int longest = 0;
            for (const auto& p : alternatives) {
                int j = 0;
                while (position + j < limit && j < static_cast<int>(p.size()) &&
                       text[position+j] == p[j])
                    ++j;
                longest = std::max(longest, j);
            }
            assert(last >= 0);
            return {complete, last, position+longest, text.substr(position, longest)};
        }
        position += static_cast<int>(alternatives[choice].size());
        last = choice;
        ++complete;
    }
}

struct ZeroImage {
    string text;
    vector<int> survivors_from_right;
};

ZeroImage zero_image(const string& word, int expected_header) {
    vector<bool> bits(word.size());
    vector<int> survivors;
    int debt = 0;
    for (int j = static_cast<int>(word.size()) - 1; j >= 0; --j) {
        if (word[j] == '2') ++debt;
        else if (debt) --debt;
        else {
            bits[j] = true;
            survivors.push_back(j);
        }
    }
    assert(debt < 6);
    string old_header = debt >= 3 ? "1334" : "";
    old_header += "132"[debt % 3];
    if (debt >= 3) old_header += '2';
    assert(static_cast<int>(old_header.size()) == expected_header);
    bool carry = false;
    string output;
    for (char c : old_header) {
        output += ((c == '2') != carry) ? '1' : '2';
        carry = c == '3';
    }
    for (bool bit : bits) {
        output += bit != carry ? '2' : '1';
        carry = bit;
    }
    return {output, survivors};
}

void flip(char& c) {
    c = c == '1' ? '2' : '1';
}

vector<Edge> outgoing(const State& s) {
    const int t = s.phase, next = (t+1) % phases, h = header_size[t];
    int count = 1 + earlier_pieces;
    count += (s.kind - count + 60) % 6;
    count += 6;
    std::set<Edge> edges;
    for (int mask = 0; mask < (1 << earlier_pieces); ++mask) {
        string protected_word = prefix[t];
        for (int j = 0; j < count; ++j) {
            int choice = 0;
            if (j == count-1) choice = s.last_choice;
            else if (j >= count-1-earlier_pieces)
                choice = (mask >> (j-(count-1-earlier_pieces))) & 1;
            protected_word += piece[t][j % 6][choice];
        }
        protected_word += s.partial;
        int x = static_cast<int>(protected_word.size()), y = x + halo_size;
        int old_color = parity(last_closing(protected_word, x)), old_switches = 0;
        for (int j = 0; j < halo_size; ++j) {
            if (s.halo[j] == '2') {
                old_switches += old_color != parity(x+j);
                old_color = parity(x+j);
            }
        }
        string word = protected_word + s.halo;
        auto image = zero_image(word, h);
        assert(static_cast<int>(image.survivors_from_right.size()) > debt_limit);
        for (int d = 0; d <= debt_limit; ++d) {
            if (d) {
                int old_index = image.survivors_from_right[d-1];
                flip(image.text[old_index+h]);
                if (old_index+1 < y) flip(image.text[old_index+1+h]);
            }
            const string& out = image.text;
            Parsed parsed = parse(next, out);
            assert(parsed.complete >= count-earlier_pieces);
            int pos = parsed.end;
            State dest{next, parsed.complete % 6, parsed.last_choice,
                       parsed.partial, out.substr(pos, halo_size)};
            int dest_id = ids.at(dest);

            int label = parity(last_closing(out, pos)-h+1);
            int switches = 0;
            for (int j = pos; j < static_cast<int>(out.size()); ++j) {
                if (out[j] == '2') {
                    int color = parity(j-h+1);
                    switches += label != color;
                    label = color;
                }
            }
            bool survives = word.back() == '1' && d == 0;
            int bridge = parity(y+1), endpoint = parity(y+d+1);
            int alignment = old_color != parity(y-1);
            int consumed = std::max(0, d-alignment);
            if (parity(consumed) != (old_color != endpoint)) ++consumed;
            int nonempty = survives ? (label != bridge) + (bridge != endpoint)
                                    : (label != endpoint);
            int charge = switches + nonempty - old_switches - consumed;
            if (!d) {
                int empty = survives ? (label != old_color)
                                     : (label != bridge) + (bridge != old_color);
                charge = std::max(charge, switches + empty - old_switches);
            }
            edges.insert({dest_id, pos-x, charge, d});
        }
    }
    return {edges.begin(), edges.end()};
}

int weight(const Edge& e) {
    return 6*e.displacement - 24*e.charge - 4;
}

// The earlier complete piece remains part of the local word enumeration.
// A single potential can cover both of its choices.
void check_projected(const vector<vector<Edge>>& graph) {
    std::map<State,int> projected_ids;
    vector<int> image;
    for (State state : states) {
        state.last_choice = 0;
        auto [entry, fresh] = projected_ids.emplace(state, static_cast<int>(projected_ids.size()));
        image.push_back(entry->second);
    }
    assert(projected_ids.size() == 14352);
    vector<std::map<int,int>> costs(projected_ids.size());
    for (size_t i = 0; i < graph.size(); ++i) {
        auto& moves = costs[image[i]];
        for (const auto& edge : graph[i]) {
            auto [entry, fresh] = moves.emplace(image[edge.destination],weight(edge));
            if (!fresh) entry->second = std::min(entry->second,weight(edge));
        }
    }
    size_t arcs = 0;
    for (const auto& moves : costs) arcs += moves.size();
    assert(arcs == 657878);
    vector<int> potential(costs.size());
    int rounds = 0;
    for (;;) {
        auto next = potential;
        for (size_t i = 0; i < costs.size(); ++i)
            for (const auto& [to,cost] : costs[i])
                next[to] = std::min(next[to],potential[i]+cost);
        if (next == potential) break;
        potential.swap(next);
        ++rounds;
        assert(rounds <= 17);
    }
    assert(rounds == 17);
    assert(*std::min_element(potential.begin(),potential.end()) == -110);
    assert(*std::max_element(potential.begin(),potential.end()) == 0);
    for (size_t i = 0; i < graph.size(); ++i)
        for (const auto& edge : graph[i])
            assert(potential[image[edge.destination]] <= potential[image[i]] + weight(edge));
    assert(12*(debt_limit+1)-238 >= 110);
    std::cout << "14352 projected states, 657878 weighted pairs, potential [-110,0], 17 rounds.\n";

    // A closed walk in the original finite-debt graph limits the rate
    // obtainable by changing the two coefficients in this left inequality.
    struct Witness { int state, movement, charge; };
    const vector<Witness> cycle{
        {121,3,0}, {5089,-14,-1}, {9600,0,0}, {14585,5,0},
        {19532,0,0}, {24171,-1,0}, {257,3,0}, {5185,1,-1},
        {9666,0,0}, {14449,5,0}, {19437,0,0}, {24057,-2,0}
    };
    int movement = 0, charge = 0;
    for (size_t i = 0; i < cycle.size(); ++i) {
        const auto step = cycle[i];
        const int to = cycle[(i+1) % cycle.size()].state;
        const auto& moves = graph[step.state];
        assert(std::any_of(moves.begin(),moves.end(),[&](const Edge& e) {
            return e.destination == to && e.displacement == step.movement && e.charge == step.charge;
        }));
        movement += step.movement;
        charge += step.charge;
    }
    assert(movement == 0 && charge == -2);
    std::cout << "12-edge closed walk, total displacement 0, total charge -2.\n";
}

int main(int argc, char** argv) {
    assert(argc == 1 || (argc == 2 && string(argv[1]) == "--projected"));
    for (int t = 0; t < phases; ++t) {
        assert(std::cin >> prefix[t] >> header_size[t]);
        for (auto& alternatives : piece[t])
            assert(std::cin >> alternatives[0] >> alternatives[1]);
    }
    enumerate_states();
    assert(states.size() == 28704);
    vector<vector<Edge>> graph;
    size_t edge_count = 0;
    for (const auto& s : states) {
        graph.push_back(outgoing(s));
        edge_count += graph.back().size();
    }
    assert(edge_count == 1752900);
    if (argc == 2) {
        check_projected(graph);
        return 0;
    }
    vector<int> potential(states.size());
    int rounds = 0;
    for (; rounds <= 17; ++rounds) {
        auto updated = potential;
        for (size_t i = 0; i < graph.size(); ++i)
            for (const auto& edge : graph[i])
                updated[edge.destination] = std::min(updated[edge.destination],
                                                     potential[i] + weight(edge));
        if (updated == potential) break;
        potential.swap(updated);
    }
    assert(rounds == 17);
    assert(*std::min_element(potential.begin(), potential.end()) == -110);
    assert(*std::max_element(potential.begin(), potential.end()) == 0);
    for (size_t i = 0; i < graph.size(); ++i)
        for (const auto& edge : graph[i])
            assert(potential[edge.destination] <= potential[i] + weight(edge));
    assert(12*(debt_limit+1)-238 >= 110);  // the analytic bound for all greater debts
    std::cout << "28704 states, 1752900 finite edges, potential [-110,0], 17 rounds.\n";
}
