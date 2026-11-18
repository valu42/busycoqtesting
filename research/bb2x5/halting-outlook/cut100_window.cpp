// Enumerate the phase and ordinary tape between the protected cut and 100+k.
// Input consists of the literal seed substring and the two certified 52-phase schedules.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

using Word = std::uint64_t;

Word mask(int width) { return (Word(1) << width) - 1; }

void require(bool condition) {
    if (!condition) throw std::runtime_error("certificate check failed");
}

Word pack(const std::string& word) {
    unsigned bit = 0;
    for (char c : word) {
        if (c != '1') { bit = c == '2'; break; }
    }
    Word code = bit;
    for (char c : word) {
        require(c >= '1' && c <= '3');
        if (c != '1') { require(bit == (c == '2')); bit = c == '3'; }
        code = 2 * code + bit;
    }
    return code;
}

struct Match {
    Word survivors;
    int inner_debt, tail_debt, tail_balance;
};

Match matched(Word code, int width, int k) {
    Word left = code >> 1;
    Word opens = ~(code ^ left) & mask(width);
    Word closes = code & ~left & mask(width);
    int tail_balance = __builtin_popcountll(opens & mask(k)) - __builtin_popcountll(closes & mask(k));
    int inner = 0, tail = 0;
    while (closes) {
        Word occupied = (closes + ~opens) ^ closes ^ ~opens;
        inner += (occupied >> width) & 1;
        tail += (occupied >> k) & 1;
        closes &= occupied;
        opens &= ~occupied;
    }
    return {opens, inner, tail, tail_balance};
}

// Independent scalar right-to-left matcher. Add an actual exterior of z closing
// symbols and emit the next middle word directly from adjacent bits.
void check_edge(Word code, int width, int k, int u, int left_bit, int z,
                int d100, int inner, Word next) {
    int debt = z;
    Word survivors = 0;
    for (int i = 0; i < width; ++i) {
        if (i == k) require(debt == d100);
        int b = (code >> i) & 1, prev = (code >> (i+1)) & 1;
        if (prev == b) {
            if (debt == 0) survivors |= Word(1) << i;
            else --debt;
        } else if (b) ++debt;
    }
    require(debt == inner);
    if (debt > u) return;
    Word computed = left_bit;
    for (int i = 0; i < u; ++i) computed = 2 * computed + (i < u-debt);
    // The cutoff drops the rightmost ordinary output, independent of its digit.
    for (int i = width-1; i >= 1; --i) computed = 2 * computed + ((survivors >> i) & 1);
    if (computed == mask(width+u)) computed = 0;
    require(computed == next);
}

struct Node {
    Word code;
    int parent;
    unsigned char exterior;
};

void run(const std::string& seed, const std::string& allowances, const std::string& bits) {
    int k = int(seed.size()) - 33;
    require((k == 3 || k == 8 || k == 9) && allowances.size() == 52 && bits.size() == 52);
    int w = int(seed.size());
    std::array<int, 52> widths{};
    for (int p = 0; p < 52; ++p) {
        widths[p] = w;
        w += (allowances[p] - '0') - 1;
    }
    require(w == int(seed.size()) && *std::max_element(widths.begin(),widths.end()) < 60);
    std::array<std::unordered_map<Word,int>,52> known;
    std::vector<Node> nodes{{pack(seed), -1, 0}};
    known[0].emplace(nodes[0].code,0);
    std::array<std::uint64_t,16> uses{};
    std::size_t first = 0, last = 1;
    for (int time = 0; first != last; ++time) {
        int p = time % 52, u = allowances[p] - '0', left_bit = bits[p] - '0';
        w = widths[p];
        for (std::size_t i = first; i < last; ++i) {
            Word code = nodes[i].code;
            Match m = matched(code,w,k);
            // d100 = max(h(T), z - balance(T)). Allow d100 at most max(1,h(T)).
            int cap = std::max(1,m.tail_debt);
            for (int z = 0; z <= m.tail_balance + cap; ++z) {
                int d100 = std::max(m.tail_debt,z-m.tail_balance);
                ++uses.at(d100);
                Word next = 0;
                if (m.inner_debt <= u) {
                    Word supplied = mask(u-m.inner_debt) << (w+m.inner_debt);
                    next = ((Word(left_bit) << (w+u)) | supplied | m.survivors) >> 1;
                    if (next == mask(w+u)) next = 0;
                }
                check_edge(code,w,k,u,left_bit,z,d100,m.inner_debt,next);
                if (m.inner_debt > u) {
                    std::vector<int> word{z};
                    for (int j = int(i); nodes[j].parent >= 0; j = nodes[j].parent)
                        word.push_back(nodes[j].exterior);
                    std::reverse(word.begin(),word.end());
                    std::cout << "Window " << k << ": loss at update " << time+1
                              << ", phase " << p << ", from " << nodes.size() << " discovered states.\n";
                    std::cout << "Exterior inputs at cut " << 100+k << ':';
                    for (int x : word) std::cout << ' ' << x;
                    std::cout << '\n';
                    return;
                }
                auto& dest = known[(p+1)%52];
                if (dest.emplace(next,int(nodes.size())).second)
                    nodes.push_back({next,int(i),static_cast<unsigned char>(z)});
                if (m.survivors) m.survivors &= m.survivors-1;
                else ++m.inner_debt;
            }
        }
        first = last;
        last = nodes.size();
    }
    std::cout << "Window " << k << ": closed, " << nodes.size() << " states. Allowed edges by cut-100 debt:";
    for (unsigned i = 0; i < uses.size(); ++i) if (uses[i]) std::cout << ' ' << i << '=' << uses[i];
    std::cout << '\n';
}

int main(int argc, char** argv) {
    if (argc != 4) return 1;
    run(argv[1],argv[2],argv[3]);
}
