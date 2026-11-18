// Exact simulation of a two-state, five-symbol TM with a moving two-word window.
// stdin: machine, steps head state, region count, then (start length symbol) rows.
// stdout: status and the same complete configuration (see survey.py).
#include <array>
#include <charconv>
#include <cstdint>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

using Count = std::uint64_t;
using Index = std::int64_t;
using Word = std::uint32_t;

struct Rule { unsigned write = 0; int move = 0; unsigned state = 0; };
struct Exit {
    Word word = 0;
    int pos = 0;
    unsigned state = 0, steps = 0;
    bool halt = false;
};
struct PairExit {
    Word left = 0, right = 0;
    int pos = 0;
    unsigned state = 0, steps = 0;
    bool halt = false;
};
struct Slot { std::uint64_t key = UINT64_MAX; PairExit value; };

Count number(const char* str) {
    Count value;
    auto size = std::char_traits<char>::length(str);
    auto parsed = std::from_chars(str, str + size, value);
    if (parsed.ec != std::errc{} || parsed.ptr != str + size) throw std::runtime_error("invalid unsigned integer");
    return value;
}

class Window {
    int width;
    std::array<Word, 11> power{};
    Rule rules[2][5]{};
    // Fixed memory with replacement. A hit requires an exact key comparison.
    struct SmallSlot { std::uint64_t key = UINT64_MAX; Exit value; };
    std::vector<SmallSlot> words;
    std::vector<Slot> pairs;
    std::vector<Word> negative, positive;
    static std::size_t hash(std::uint64_t k, std::size_t size) {
        k ^= k >> 30; k *= 0xbf58476d1ce4e5b9ULL;
        k ^= k >> 27; k *= 0x94d049bb133111ebULL;
        return (k ^ (k >> 31)) & (size - 1);
    }
    // Floor division also for negative coordinates.
    Index block(Index x) const { return x >= 0 ? x / width : -1 - ((-1-x) / width); }
    Word get(Index i) const {
        const auto &v = i < 0 ? negative : positive;
        auto index = static_cast<std::size_t>(i < 0 ? -1-i : i);
        return index < v.size() ? v[index] : 0;
    }
    void put(Index i, Word w) {
        auto &v = i < 0 ? negative : positive;
        auto index = static_cast<std::size_t>(i < 0 ? -1-i : i);
        if (index >= v.size()) {
            if (!w) return;
            v.resize(index + 1);
        }
        v[index] = w;
    }
    Rule read(Word w, int offset, unsigned q) const { return rules[q][w / power[offset] % 5]; }
    Word write(Word w, int p, unsigned value) const {
        return w + (value - (w / power[p] % 5)) * power[p];
    }
    Exit local(Word w, unsigned q, bool right_edge) {
        std::uint64_t key = (std::uint64_t(w) << 2) | (q << 1) | right_edge;
        auto &slot = words[hash(key, words.size())];
        if (key == slot.key) return slot.value;
        Exit a{w, right_edge ? width - 1 : 0, q, 0, false};
        while (a.pos >= 0 && a.pos < width && a.steps < 4096) {
            auto r = read(a.word, a.pos, a.state);
            if (!r.move) { a.halt = true; break; }
            a.word = write(a.word, a.pos, r.write);
            a.pos += r.move; a.state = r.state; ++a.steps;
        }
        slot = {key, a};
        return a;
    }
    PairExit window(Word left, Word right, unsigned q, bool entering_left) {
        std::uint64_t key = ((std::uint64_t(left) * power[width] + right) << 2) | (q << 1) | entering_left;
        auto &slot = pairs[hash(key, pairs.size())];
        if (key == slot.key) return slot.value;
        PairExit a{left, right, entering_left ? width - 1 : width, q, 0, false};
        // At the internal cut, enter one half and compose first exits. If a
        // bounded local evaluation stops inside, its entire prefix is valid.
        for (int crossing = 0; crossing < 128; ++crossing) {
            bool in_left = a.pos < width;
            auto answer = local(in_left ? a.left : a.right, a.state, in_left);
            if (in_left) a.left = answer.word; else a.right = answer.word;
            a.pos = (in_left ? 0 : width) + answer.pos;
            a.state = answer.state; a.steps += answer.steps; a.halt = answer.halt;
            if (a.halt || (answer.pos >= 0 && answer.pos < width) || a.pos < 0 || a.pos >= 2*width) break;
        }
        slot = {key, a};
        return a;
    }
public:
    Count steps = 0, work = 0;
    Index head = 0;
    unsigned state = 0;
    Window(int width_, const std::string &machine) : width(width_), words(1 << 15), pairs(1 << 17) {
        if (width < 2 || width > 10 || machine.size() != 31 || machine[15] != '_') throw std::runtime_error("bad width or encoding");
        power[0] = 1;
        for (int i = 0; i < width; ++i) power[i+1] = power[i] * 5;
        for (int q = 0; q < 2; ++q) for (int s = 0; s < 5; ++s) {
            std::string t = machine.substr(16*q + 3*s, 3);
            if (t == "---") continue;
            if (t[0] < '0' || t[0] > '4' || (t[1] != 'L' && t[1] != 'R') || (t[2] != 'A' && t[2] != 'B')) throw std::runtime_error("bad instruction");
            rules[q][s] = {unsigned(t[0]-'0'), t[1] == 'L' ? -1 : 1, unsigned(t[2]-'A')};
        }
    }
    void set(Index x, unsigned symbol) {
        Index i = block(x);
        put(i, write(get(i), int(x - i*width), symbol));
    }
    bool halted() const {
        Index i = block(head);
        return !read(get(i), int(head-i*width), state).move;
    }
    void run(Count target, Count budget) {
        if (steps > target) throw std::runtime_error("target precedes checkpoint");
        while (steps < target && work < budget) {
            ++work;
            Index i = block(head);
            int p = int(head-i*width);
            if (p == 0 || p == width-1) {
                bool entering_left = (p != 0);
                Index base = entering_left ? i : i-1;
                auto a = window(get(base), get(base+1), state, entering_left);
                if (a.steps <= target-steps) {
                    put(base,a.left); put(base+1,a.right);
                    steps += a.steps; head = base*width + a.pos; state = a.state;
                    if (a.halt) break;
                    continue;
                }
            }
            // Inside a word or the final jump would pass the exact step target.
            Word word = get(i);
            Rule r = read(word,p,state);
            if (!r.move) break;
            put(i,write(word,p,r.write)); head += r.move; state = r.state; ++steps;
        }
    }
    void print_runs() const {
        Index first = -Index(negative.size())*width, end = Index(positive.size())*width;
        unsigned previous = 0; Index start = first;
        for (Index x=first; x<=end; ++x) {
            Index i = block(x);
            unsigned symbol = get(i) / power[x-i*width] % 5;
            if (symbol != previous) {
                if (previous) std::cout << start << ' ' << x-start << ' ' << previous << '\n';
                start = x; previous = symbol;
            }
        }
    }
};

int main(int argc, char **argv) try {
    if (argc != 4) throw std::runtime_error("usage: window WIDTH ABSOLUTE_STEP_TARGET WORK_BUDGET < state");
    Count width = number(argv[1]), target = number(argv[2]), budget = number(argv[3]);
    // Keeps all signed coordinate and block-boundary arithmetic representable.
    constexpr Count limit = Count(1) << 60;
    if (width < 2 || width > 10 || target > limit) throw std::runtime_error("require width 2..10 and target <= 2^60");
    std::string machine;
    if (!(std::cin >> machine)) throw std::runtime_error("missing machine");
    Window sim(int(width), machine);
    if (!(std::cin >> sim.steps >> sim.head >> sim.state) || sim.steps>target || sim.state>1 || sim.head < -Index(sim.steps) || sim.head > Index(sim.steps)) throw std::runtime_error("invalid checkpoint header");
    Index x, count, prev_end = -Index(limit);
    unsigned digit;
    while (std::cin >> x) {
        if (!(std::cin >> count >> digit) || count<=0 || digit<1 || digit>4 || x<prev_end || x < -Index(sim.steps) || x>Index(sim.steps) || count>Index(sim.steps)-x+1) throw std::runtime_error("invalid tape run");
        for (Index j=0; j<count; ++j) sim.set(x+j,digit);
        prev_end = x+count;
    }
    if (!std::cin.eof()) throw std::runtime_error("invalid checkpoint trailer");
    sim.run(target,budget);
    std::cout << (sim.halted()?"halt":"unknown") << ' ' << sim.work << '\n' << machine << '\n' << sim.steps << ' ' << sim.head << ' ' << sim.state << '\n';
    sim.print_runs();
    return 0;
} catch (const std::exception &e) { std::cerr << e.what() << '\n'; return 2; }
