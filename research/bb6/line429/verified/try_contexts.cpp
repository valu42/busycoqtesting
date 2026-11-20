// Attempt an invariant for the five-state model in Line429Sibling.v.
// The head window keeps k symbols on each side. Farther windows are stored
// independently, so an abstract hit of C:01 can be a false positive.
#include <array>
#include <cstdint>
#include <deque>
#include <iostream>
#include <string>
#include <unordered_set>
#include <vector>

enum State { A, B, C, P, Q };
enum Side { Left, Right };
struct Action { unsigned write; Side face; State next; };
constexpr Action table[5][2] = {
    {{1,Right,B}, {0,Left,C}}, {{1,Right,C}, {1,Right,A}},
    {{1,Left,P}, {0,Right,Q}}, {{1,Left,A}, {1,Left,P}},
    {{0,Right,A}, {0,Right,Q}}
};
struct Window { State state; unsigned symbol; std::array<unsigned,2> half; };

int main(int argc, char** argv) {
    if (argc != 2) { std::cerr << "usage: try_contexts WIDTH\n"; return 2; }
    const int width = std::stoi(argv[1]);
    if (width < 1 || width > 18) { std::cerr << "tested widths are 1 through 18\n"; return 2; }
    const unsigned size = 1u << width, mask = size - 1;
    // extension[side][word] is a two-bit set of possible next outward bits.
    std::array<std::vector<unsigned char>,2> extension;
    std::array<std::vector<std::vector<Window>>,2> waiting;
    for (Side side : {Left,Right}) {
        extension[side].resize(size);
        waiting[side].resize(size);
        extension[side][0] = 1;
    }
    std::unordered_set<std::uint64_t> visited;
    std::deque<Window> queue;
    auto enqueue = [&](Window w) {
        const auto id = ((std::uint64_t(w.state)*2 + w.symbol)*size + w.half[Left])*size + w.half[Right];
        if (visited.insert(id).second) queue.push_back(w);
    };
    auto extend = [&](Window w, Side side, unsigned bit) {
        w.half[side] = (w.half[side] >> 1) | (bit << (width-1));
        enqueue(w);
    };
    enqueue({A,0,{0,0}});
    while (!queue.empty()) {
        const Window w = queue.front(); queue.pop_front();
        if (w.state == C && w.symbol == 0 && (w.half[Right]&1)) {
            std::cout << "abstract guard at width " << width << ", " << visited.size() << " windows discovered\n";
            return 0;
        }
        if (visited.size() > 3000000) { std::cout << "window budget exhausted\n"; return 0; }
        const Action move = table[w.state][w.symbol];
        const Side face = move.face, back = face == Right ? Left : Right;
        const unsigned ahead = w.half[face];
        const unsigned deposited = (w.half[back] << 1) | move.write;
        const unsigned word = deposited & mask, far_bit = deposited >> width;
        if (!(extension[back][word] & (1u << far_bit))) {
            extension[back][word] |= 1u << far_bit;
            for (Window old : waiting[back][word]) extend(old, back, far_bit);
        }
        Window next{move.next, ahead & 1u, w.half};
        next.half[back] = word;
        waiting[face][ahead].push_back(next);
        for (unsigned bit : {0u,1u}) {
            if (extension[face][ahead] & (1u << bit)) extend(next, face, bit);
        }
    }
    std::cout << "closed safe family at width " << width << ", " << visited.size() << " windows\n";
}
