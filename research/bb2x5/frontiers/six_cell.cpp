// Lines 14, 16 and 28 have periodic regions suited to six-cell tiles. At a cut, a first
// exit from its two adjacent tiles can move the cut by one whole tile.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using Count = std::int64_t;
constexpr int width = 6;
constexpr int words = 15625;
constexpr int powers[] = {1, 5, 25, 125, 625, 3125};
constexpr Count limit = Count(1) << 60;
const std::array<std::string, 3> supported = {
    "1RB2RA4LA1RB4RB_1LB2LA3RA---0LB",
    "1RB2LA0RB0LB3LB_2LA4RB3RA0RA---",
    "1RB3LB4LA0LB---_2LA0LA1RB0RA3RA",
};
struct Rule { int digit, move, next; };
Rule rules[2][5]{};

struct Run { int word; Count copies; };

class Stack {
public:
    // Nearest tile is at the back. Cells beyond the last stored tile are blank.
    std::vector<Run> runs;
    int top() const { return runs.empty() ? 0 : runs.back().word; }
    Count length() const { return runs.empty() ? 1 : runs.back().copies; }
    void push(int word, Count n = 1) {
        if (!n || (runs.empty() && !word)) return;
        if (!runs.empty() && runs.back().word == word) runs.back().copies += n;
        else runs.push_back({word,n});
    }
    void pop(Count n = 1) {
        if (runs.empty()) return;
        if (n > runs.back().copies) throw std::logic_error("short tile run");
        runs.back().copies -= n;
        if (!runs.back().copies) runs.pop_back();
    }
};

struct Exit { int left, right, pos, state, steps; bool halt; };

Exit trace(int left, int right, int pos, int state, int budget) {
    Exit e{left,right,pos,state,0,false};
    while (0 <= e.pos && e.pos < 2*width && e.steps < budget) {
        int &w = e.pos < width ? e.left : e.right;
        int place = powers[e.pos % width];
        int s = w / place % 5;
        Rule rule = rules[e.state][s];
        if (!rule.move) { e.halt = true; break; }
        w += (rule.digit-s)*place;
        e.state = rule.next;
        e.pos += rule.move;
        ++e.steps;
    }
    return e;
}

struct Slot { std::uint32_t key = UINT32_MAX; Exit answer{}; };
std::vector<Slot> cache(1 << 18);

Exit first_exit(int left, int right, bool enter_left, int state) {
    std::uint32_t key = ((left*words + right)*2 + state)*2 + enter_left;
    std::uint32_t hash = key*0x9e3779b9u;
    auto &slot = cache[(hash ^ (hash >> 14)) & (cache.size()-1)];
    if (slot.key != key) {
        slot.key = key;
        slot.answer = trace(left,right,width-enter_left,state,512);
    }
    return slot.answer;
}

struct Tape {
    Stack left, right;
    Count cut = 0, steps = 0, operations = 0;
    int pos = width, state = 0;

    void advance(Count target, Count budget) {
        while (steps < target && operations < budget) {
            ++operations;
            bool edge = pos == width || pos == width-1;
            Exit e = edge ? first_exit(left.top(),right.top(),pos<width,state)
                          : trace(left.top(),right.top(),pos,state,512);
            if (e.steps > target-steps)
                e = trace(left.top(),right.top(),pos,state,static_cast<int>(target-steps));
            steps += e.steps;
            state = e.state;
            left.pop(); right.pop();
            if (e.pos >= 0 && e.pos < 2*width) {
                left.push(e.left); right.push(e.right); pos = e.pos;
                if (e.halt) return;
                continue;
            }

            bool moving_left = e.pos < 0;
            Stack &behind = moving_left ? right : left;
            Stack &ahead = moving_left ? left : right;
            int guard = moving_left ? e.left : e.right;
            behind.push(moving_left ? e.right : e.left);
            behind.push(guard);
            int stride = moving_left ? -width : width;
            cut += stride;
            pos = width-moving_left;

            // One more crossing is repeatable if it restores the nearest
            // tile behind the head (the guard) and the entry control state.
            // Its other output tile is deposited behind that guard.
            Exit b = first_exit(left.top(),right.top(),moving_left,state);
            if (b.pos != e.pos || b.state != state ||
                    (moving_left ? b.left : b.right) != guard) continue;
            Count k = std::min(ahead.length(), (target-steps)/b.steps);
            if (k) {
                ahead.pop(k); behind.pop();
                behind.push(moving_left ? b.right : b.left,k); behind.push(guard);
                steps += k*b.steps; cut += k*stride;
            }
        }
    }
};

int main() try {
    Count target, budget, head, start; std::string encoding;
    Tape t;
    if (!(std::cin >> encoding >> target >> budget >> t.steps >> head >> t.state >> start)
            || std::find(supported.begin(), supported.end(), encoding) == supported.end()
            || t.steps < 0 || target < t.steps || target > limit
            || budget <= 0 || head < -t.steps || head > t.steps || t.state < 0 || t.state > 1
            || start % width || start < -t.steps-width || start > t.steps+width)
        throw std::runtime_error("invalid target or machine configuration");
    for (int q = 0; q < 2; ++q) for (int s = 0; s < 5; ++s) {
        const char *rule = encoding.c_str() + 16*q + 3*s;
        if (*rule != '-') rules[q][s] = {rule[0]-'0',rule[1]=='R' ? 1 : -1,rule[2]-'A'};
    }
    // Split the initial run stream at the beginning of the head's tile.
    int offset = int((head % width + width) % width);
    t.cut = head-offset; t.pos = width+offset;
    std::vector<Run> suffix;
    if (start > t.cut) suffix.push_back({0,(start-t.cut)/width});
    int w; Count n;
    while (std::cin >> w) {
        if (!(std::cin >> n) || w < 0 || w >= words || n < 1 || n > (t.steps+width-start)/width)
            throw std::runtime_error("invalid tile run");
        Count l = std::clamp((t.cut-start)/width, Count(0), n);
        t.left.push(w,l);
        if (l < n) suffix.push_back({w,n-l});
        start += n*width;
    }
    if (!std::cin.eof()) throw std::runtime_error("malformed tile stream");
    if (start < t.cut) t.left.push(0,(t.cut-start)/width);
    for (auto i = suffix.rbegin(); i != suffix.rend(); ++i) t.right.push(i->word,i->copies);
    t.advance(target,budget);

    int scanned = (t.pos < width ? t.left.top() : t.right.top()) / powers[t.pos % width] % 5;
    bool halt = !rules[t.state][scanned].move;
    Count leftmost = t.cut;
    for (auto r : t.left.runs) leftmost -= width*r.copies;
    std::cout << (halt ? "halt" : "unknown") << ' ' << t.operations << ' ' << t.steps << ' '
              << t.cut+t.pos-width << ' ' << t.state << ' ' << leftmost << '\n';
    for (auto r : t.left.runs) std::cout << r.word << ' ' << r.copies << '\n';
    for (auto i=t.right.runs.rbegin(); i!=t.right.runs.rend(); ++i)
        std::cout << i->word << ' ' << i->copies << '\n';
} catch (const std::exception &e) { std::cerr << e.what() << '\n'; return 2; }
