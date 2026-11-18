// Read line36_left.py's six-phase grammar on stdin. Optional argument: potential TSV.
#include <algorithm>
#include <cassert>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <tuple>
#include <vector>

#ifdef NDEBUG
#error "Keep assertions enabled for the certificate checks."
#endif
using std::string;
using std::vector;
constexpr int last_finite_debt = 12;
string piece[6][6][2];
int header[6];

struct State {
    int phase, kind;
    string partial;
    char halo;
    bool operator<(const State& s) const {
        return std::tie(phase,kind,partial,halo) < std::tie(s.phase,s.kind,s.partial,s.halo);
    }
};

int parity(int i) { return (i%2+2)%2; }

int last_closing(const string& s, int end) {
    assert(end > 0);
    const auto pos = s.rfind('2',end-1);
    assert(pos != string::npos);
    return static_cast<int>(pos);
}

vector<bool> mark(const string& word, int debt) {
    vector<bool> mask(word.size());
    for (int i = static_cast<int>(word.size())-1; i >= 0; --i) {
        if (word[i] == '2') ++debt;
        else if (debt) --debt;
        else mask[i] = true;
    }
    return mask;
}

struct Parse { int end, kind; string partial; };

Parse parse(int t, int kind, const string& out, int limit) {
    int pos = 0;
    for (;;) {
        int complete = 0, longest = 0;
        for (const auto& p : piece[t][kind]) {
            int n = 0;
            while (pos+n < limit && n < static_cast<int>(p.size()) && out[pos+n] == p[n]) ++n;
            if (n == static_cast<int>(p.size())) complete = n;
            longest = std::max(longest,n);
        }
        if (!complete) return {pos+longest,kind,out.substr(pos,longest)};
        pos += complete;
        kind = (kind+1)%6;
    }
}

int switches(const string& word, int begin, int end, int shift, int& label) {
    int count = 0;
    for (int j = begin; j < end; ++j) {
        if (word[j] == '2') {
            const int color = parity(j+shift);
            count += label != color;
            label = color;
        }
    }
    return count;
}

struct Move { State to; int displacement, charge; };

Move local_step(const State& s, int first, int second, int debt, int& minimum_balance) {
    // Old and new coordinates both start at the first of two known complete pieces.
    const int start = (s.kind+4)%6, next = (s.phase+1)%6, h = header[s.phase];
    const string known = piece[s.phase][start][first] + piece[s.phase][(start+1)%6][second] + s.partial;
    const int x = static_cast<int>(known.size()), y = x+1;
    const int balance = x-2*static_cast<int>(std::count(known.begin(),known.end(),'2'));
    minimum_balance = std::min(minimum_balance,balance);
    assert(balance >= 20);
    const string old = known+s.halo;
    const auto mask = mark(old,debt);
    // Even the first old survivor is untouched by a debt <= 13. The derivative
    // through new index h, including its unknown old left neighbor, is pristine.
    string out = piece[next][start][first].substr(0,h+1);
    assert(static_cast<int>(out.size()) == h+1);
    for (int j = h+1; j < y+h; ++j) out += mask[j-h] == mask[j-h-1] ? '1' : '2';
    const auto parsed = parse(next,start,out,x+h);
    const int z = parsed.end;
    int alpha = parity(last_closing(known,x));
    const int old_changes = switches(old,x,y,0,alpha);
    int gamma = parity(last_closing(out,z)-h+1);
    const int new_changes = switches(out,z,y+h,1-h,gamma);
    const bool survives = s.halo == '1' && debt == 0;
    const int bridge = parity(y+1), endpoint = parity(y+debt+1);
    const int align = alpha != parity(y-1);
    const int fee = debt ? debt-align : align;
    const int zero = survives ? (gamma!=bridge)+(bridge!=endpoint) : (gamma!=endpoint);
    int charge = new_changes-old_changes+zero-fee;
    if (!debt) {
        const int live = survives ? (gamma!=alpha) : (gamma!=bridge)+(bridge!=alpha);
        charge = std::max(charge,new_changes-old_changes+live);
    }
    return {{next,parsed.kind,parsed.partial,out[z]},z-x,charge};
}

int main(int argc, char** argv) {
    assert(argc == 1 || argc == 2);
    for (int t = 0; t < 6; ++t) {
        string prefix;
        assert(std::cin >> prefix >> header[t]);
        for (auto& row : piece[t]) assert(std::cin >> row[0] >> row[1]);
    }
    std::map<State,int> ids;
    vector<State> states;
    for (int t = 0; t < 6; ++t) for (int k = 0; k < 6; ++k) {
        for (const auto& p : piece[t][k]) for (std::size_t n = 0; n < p.size(); ++n) {
            for (char halo : {'1','2'}) {
                State state{t,k,p.substr(0,n),halo};
                if (ids.emplace(state,static_cast<int>(states.size())).second) states.push_back(state);
            }
        }
    }
    assert(states.size() == 3588);
    vector<std::map<int,int>> edges(states.size());
    std::size_t pairs = 0;
    int minimum_balance = 1000;
    for (std::size_t i = 0; i < states.size(); ++i) {
        for (int a : {0,1}) for (int b : {0,1}) for (int d = 0; d <= last_finite_debt; ++d) {
            const auto move = local_step(states[i],a,b,d,minimum_balance);
            const int cost = 3*move.displacement-24*move.charge-4;
            auto [entry,fresh] = edges[i].emplace(ids.at(move.to),cost);
            if (!fresh) entry->second = std::min(entry->second,cost);
        }
        pairs += edges[i].size();
    }
    assert(pairs == 61932 && minimum_balance == 20);
    vector<int> potential(states.size());
    int rounds = 0;
    for (;;) {
        auto next = potential;
        for (std::size_t i = 0; i < states.size(); ++i)
            for (auto [to,cost] : edges[i]) next[to] = std::min(next[to],potential[i]+cost);
        if (next == potential) break;
        potential.swap(next);
        ++rounds;
        assert(rounds <= 23);
    }
    assert(rounds == 23 && *std::min_element(potential.begin(),potential.end()) == -56);
    assert(*std::max_element(potential.begin(),potential.end()) == 0);
    for (std::size_t i = 0; i < states.size(); ++i)
        for (auto [to,cost] : edges[i]) assert(potential[to] <= potential[i]+cost);
    assert(18*(last_finite_debt+1)-145 >= 56);
    std::cout << states.size() << " cut states, " << pairs << " weighted pairs, " << rounds
              << " changing rounds; potential [-56,0], minimum two-piece balance " << minimum_balance << '\n';
    std::cout << "phase-0 seed potential " << potential[ids.at({0,0,"",'1'})] << '\n';
    if (argc == 2) {
        std::ofstream out(argv[1]);
        for (auto& [s,id] : ids)
            out << s.phase << '\t' << s.kind << '\t' << s.partial << '\t' << s.halo << '\t' << potential[id] << '\n';
        out.close();
        if (!out) return 1;
    }
}
