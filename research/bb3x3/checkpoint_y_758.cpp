// Replay the connected return gates starting at the last annular merger Y.
// c++ -O3 -std=c++17 checkpoint_y_758.cpp -lgmpxx -lgmp -o checkpoint_y
#include <algorithm>
#include <array>
#include <cstdint>
#include <gmpxx.h>
#include <iostream>
#include <limits>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>

using Big = mpz_class;
using Offset = unsigned long;
static_assert(std::numeric_limits<Offset>::digits >= 64);
constexpr Offset limit = 1'000'000'000'000'000'000UL;
const Big power = [] {
    Big result;
    mpz_ui_pow_ui(result.get_mpz_t(), 3, 292);
    return result;
}();
const Big checkpoint = power * 19683 / 19171 + 4510976;

Big base = checkpoint;
struct State { Big a, c; };
struct Block { Offset y; unsigned gain; };
constexpr unsigned bits = 16;
constexpr unsigned mask = (1U << bits) - 1;
std::array<Block, 1U << bits> table;
std::array<State, 256> lanes;
std::array<unsigned, 64> even_gains, initial_packs;
Offset factor = 1;

void bulk(State& s) {
    const bool low = (s.c.get_ui() & 3) == 1;
    s.a -= s.c + (low ? 2 : 4);
    if (s.a < 0) throw std::runtime_error("illegal bulk");
    s.c = 3 * (s.c / 2) + (low ? 5 : 8);
}

void jump(State& s) {
    if (s.a > s.c || !(s.a.get_ui() & 1)) throw std::runtime_error("illegal jump");
    s.c -= s.a - 1;
    s.a = 3 * s.a + 2;
}

State odd_header(const Big& x) {
    State s{2 * power - 1, base + x - power + 585};
    if (s.c <= 0) throw std::runtime_error("illegal initial jumps");
    for (unsigned i = 0; i < 8; ++i) {
        bulk(s);
        if (s.a <= 1) throw std::runtime_error("early header return");
    }
    jump(s);
    return s;
}

unsigned even_gain(Offset x) {
    State s{4 * (power / 3) - 1, base + x - 2 * (power / 3) + 587};
    if (s.c <= 0) throw std::runtime_error("illegal even launch");
    for (char op : std::string("LLJLLJL")) {
        if (op == 'J') jump(s); else bulk(s);
        if (s.a <= 1) throw std::runtime_error("early even return");
    }
    if (s.a > s.c || s.a.get_ui() % 2) throw std::runtime_error("even return guard");
    Big gain = s.a / 2 + s.c + 2 - base - x;
    return gain.get_ui();
}

void prepare() {
    factor = 1;
    initial_packs.fill(0);
    for (unsigned i = 0; i < bits; ++i) factor *= 3;
    for (unsigned r = 0; r <= mask; ++r) {
        Offset y = r;
        unsigned gain = 0;
        for (unsigned i = 0; i < bits; ++i) {
            gain += 5 + 4 * (y & 1);
            y = 3 * ((y + 1) / 2);
        }
        table[r] = {y, gain};
    }

    odd_header(limit);
    Big max_c = 0;
    for (unsigned r = 0; r < 256; ++r) {
        lanes[r] = odd_header(2 * r);
        auto next_lane = odd_header(2 * r + 512);
        if (next_lane.c - lanes[r].c != 38342 || next_lane.a - lanes[r].a != -75660)
            throw std::runtime_error("header slope");
        max_c = std::max(max_c, lanes[r].c);
    }
    for (unsigned r = 1; r < 64; r += 2) {
        even_gains[r] = even_gain(r);
        if (even_gains[r] != even_gain(limit - (limit - r) % 64) || even_gains[r] > 615)
            throw std::runtime_error("even seed gain");
    }

    // Every c increases by at most (3c+13)/2 on a proposed bulk.
    // Keep c+13 below a quarter of both bases. The formal mass never decreases,
    // so every formal intermediate state still satisfies a>c+4.
    for (unsigned j = 0; j < initial_packs.size(); ++j) {
        Big bound = max_c + 13 + 38342 * ((Big(1) << j) / 512);
        for (;;) {
            bound = (bound * factor + mask) >> bits;
            if (4 * bound > std::min(base, checkpoint)) break;
            ++initial_packs[j];
        }
    }
}

unsigned apply_block(Big& y) {
    const Block& block = table[y.get_ui() & mask];
    mpz_fdiv_q_2exp(y.get_mpz_t(), y.get_mpz_t(), bits);
    mpz_mul_ui(y.get_mpz_t(), y.get_mpz_t(), factor);
    mpz_add_ui(y.get_mpz_t(), y.get_mpz_t(), block.y);
    return block.gain;
}

Offset checked_exit(const Big& c, Offset from) {
    Big x = c - base;
    if (!x.fits_ulong_p() || x <= from || x > limit)
        throw std::runtime_error("exit outside verifier range");
    return x.get_ui();
}

struct ReturnWord {
    unsigned opening_bulks = 0, max_mass_gain = 4 * 293 + 9 * 8;
    std::string suffix;
    bool ordinary = true;

    void bulks(unsigned count) {
        if (suffix.empty()) opening_bulks += count;
        else suffix.append(count, 'L');
        max_mass_gain += 9 * count;
    }
};

Offset next_reset(Offset x, ReturnWord* word = nullptr) {
    if (x & 1) return x + even_gains[x % 64];

    State s = lanes[(x % 512) / 2];
    const Offset periods = x / 512;
    s.c += Big(38342) * periods;
    s.a -= Big(75660) * periods;
    Big y = (s.c + 7) / 2;
    unsigned gain = 0;
    const unsigned bucket = x == 0 ? 0 : std::numeric_limits<Offset>::digits - __builtin_clzl(x);
    const unsigned packets = initial_packs.at(bucket);
    for (unsigned i = 0; i < packets; ++i) gain += apply_block(y);
    if (word) word->bulks(packets * bits);
    Big nc = 2 * y - 7;
    s.a += 2 * (s.c - nc) + gain;
    s.c = nc;

    for (unsigned step = 0; step < 5000; ++step) {
        if (s.a == 1) {
            if (word) word->suffix += 'Z';
            return checked_exit(s.c, x);
        }
        if (s.a <= s.c) {
            if (!(s.a.get_ui() & 1)) {
                if (word) {
                    word->suffix += 'R';
                    word->max_mass_gain += 5;
                }
                return checked_exit(s.a / 2 + s.c + 2, x);
            }
            jump(s);
            if (word) {
                word->suffix += 'J';
                word->max_mass_gain += 4;
            }
            continue;
        }
        y = (s.c + 7) / 2;
        const unsigned block_gain = apply_block(y);
        nc = 2 * y - 7;
        Big na = s.a + 2 * (s.c - nc) + block_gain;
        if (na > 1) {
            s = {na, nc};
            if (word) word->bulks(bits);
            continue;
        }
        const bool low = (s.c.get_ui() & 3) == 1;
        const Big difference = s.a - s.c;
        if (difference >= (low ? 2 : 4)) {
            bulk(s);
            if (word) word->bulks(1);
        } else if (difference == 2 && !low) {
            s = {3 * s.c + 8, 1};
            if (word) word->ordinary = false;
        } else {
            throw std::runtime_error("direct halt at offset " + std::to_string(x));
        }
    }
    throw std::runtime_error("individual return exceeded budget");
}

struct Probe {
    ReturnWord word;
    Offset bound;
    explicit Probe(Offset x) {
        const Offset gain = next_reset(x, &word) - x;
        bound = word.ordinary ? word.max_mass_gain / 2 : gain;
        if (gain > bound) throw std::runtime_error("invalid word bound");
    }
};

struct CoverCount { Offset nodes = 0, leaves = 0, bound = 615; };

void cover_odds(Offset lo, Offset last, const Probe& left, const Probe& right,
                CoverCount& result) {
    ++result.nodes;
    const auto& a = left.word;
    const auto& b = right.word;
    if (lo == last || (a.ordinary && b.ordinary && a.opening_bulks == b.opening_bulks &&
                       a.suffix == b.suffix)) {
        ++result.leaves;
        result.bound = std::max(result.bound, left.bound);
        return;
    }
    const Offset mid = lo + 2 * ((last - lo) / 4);
    cover_odds(lo, mid, left, mid == lo ? left : Probe(mid), result);
    cover_odds(mid + 2, last, mid + 2 == last ? right : Probe(mid + 2), right, result);
}

void cover_gaps() {
    // Signed values are seed offsets relative to Y. The domain of the
    // post-header table begins 4,500,000 below Y.
    long lo, hi;
    while (std::cin >> lo >> hi) {
        if (lo < -4500000 || lo >= hi || (lo | hi) % 2 || hi > long(limit))
            throw std::runtime_error("invalid gap");
        const long shift = std::min(0L, lo);
        base = checkpoint + shift;
        prepare();
        const Offset first = lo - shift, last = hi - shift - 2;
        CoverCount result;
        cover_odds(first, last, Probe(first), Probe(last), result);
        std::cout << lo << ' ' << hi << ' ' << result.nodes << ' '
                  << result.leaves << ' ' << result.bound << std::endl;
    }
}

void check_gate(unsigned k, const Big& absolute_lo, const Big& absolute_hi) {
    const Big odd_seeds[] = {absolute_lo, absolute_hi - 2};
    for (const Big& seed : odd_seeds) {
        State s = odd_header(seed - base);
        for (unsigned i = 0; i < k; ++i) {
            bulk(s);
            if (s.a <= 1) throw std::runtime_error("early gate return");
        }
        if (s.a > s.c || s.a.get_ui() % 2) throw std::runtime_error("gate return guard");
    }
}

struct Merger { std::size_t exits; Offset edges, seed; };
Merger merge_last(Offset edge, unsigned cap, Offset budget) {
    // Every first exit is the successor of a seed in the final cap slots.
    std::set<Offset> pending;
    for (Offset x = edge - cap; x < edge; ++x) {
        Offset dest = next_reset(x);
        if (dest >= edge) pending.insert(dest);
    }
    if (pending.empty()) throw std::runtime_error("empty exit set");
    const auto exits = pending.size();
    Offset edges = 0;
    while (pending.size() > 1) {
        if (++edges > budget) throw std::runtime_error("merger budget");
        Offset x = *pending.begin();
        pending.erase(pending.begin());
        pending.insert(next_reset(x));
    }
    return {exits, edges, *pending.begin()};
}

Merger merge_edge(unsigned k, Offset edge, Offset budget) {
    const unsigned cap = std::max(615U, (4 * 293 + 9 * (8 + k) + 5) / 2);
    return merge_last(edge, cap, budget);
}

void follow_edge_bands() {
    constexpr unsigned total_bulks = 733;
    constexpr Offset low = 53'719'288, end = 80'126'736;
    unsigned k, count = 0;
    Offset previous;
    Big edge;
    while (std::cin >> k >> edge >> previous) {
        if (k != 7 + 2 * count || k > total_bulks || edge < checkpoint ||
            !(edge.get_ui() & 1) || previous >= low)
            throw std::runtime_error("invalid edge-band input");
        base = edge;
        prepare();
        unsigned cap = 615;
        const auto suffix = "J" + std::string(total_bulks-k+1, 'L') + "R";
        for (Offset x : {low, end-2}) {
            const Probe test(x);
            if (!test.word.ordinary || test.word.opening_bulks != k-1 ||
                test.word.suffix != suffix)
                throw std::runtime_error("incorrect edge-band endpoint word");
            cap = std::max(cap, unsigned(test.bound));
        }
        if (cap != (4 * 294 + 9 * (8 + total_bulks) + 5) / 2)
            throw std::runtime_error("incorrect edge-band gain bound");
        auto seed = previous;
        Offset calls = 0;
        while (seed < low) {
            seed = next_reset(seed);
            ++calls;
        }
        if (seed >= end) throw std::runtime_error("missed edge band");
        const auto result = merge_last(end, cap, 400000);
        std::cout << k << ' ' << seed << ' ' << calls << ' ' << result.exits << ' '
                  << result.edges << ' ' << result.seed << std::endl;
        ++count;
    }
    if (count != 364) throw std::runtime_error("incomplete edge-band census");
}

constexpr Offset mixed_threshold = 30'000'000;
struct MixedInterval { Offset lo, hi; unsigned bound; };

void find_mixed_intervals(Offset lo, Offset hi, const Probe& left, const Probe& right,
                          std::vector<MixedInterval>& pieces) {
    if (left.word.ordinary && right.word.ordinary &&
        left.word.opening_bulks == right.word.opening_bulks &&
        left.word.suffix == right.word.suffix) {
        const unsigned bound = std::max(615U, unsigned(left.bound));
        if (!pieces.empty() && pieces.back().hi == lo) {
            pieces.back().hi = hi;
            pieces.back().bound = std::max(pieces.back().bound, bound);
        } else {
            pieces.push_back({lo, hi, bound});
        }
        return;
    }
    if (hi-lo < mixed_threshold) return;
    const Offset mid = lo + 2*((hi-lo)/4);
    find_mixed_intervals(lo, mid, left, Probe(mid-2), pieces);
    find_mixed_intervals(mid, hi, Probe(mid), right, pieces);
}

void mixed_bridges() {
    prepare();
    // The previous connected table ends here after the k=717 gate.
    Offset source = 158'145'479'878, low, high;
    unsigned k;
    for (unsigned expected = 715; std::cin >> k >> low >> high; expected -= 2) {
        const Offset start = source + source%2;
        if (k != expected || k < 7 || start+2 > low || low >= high ||
            high > limit || (low | high) % 2 || high-low < 8192)
            throw std::runtime_error("invalid mixed bridge");
        check_gate(k, checkpoint+low, checkpoint+high);
        std::vector<MixedInterval> pieces;
        // Odd absolute seeds have even offsets from Y.
        find_mixed_intervals(start, low, Probe(start), Probe(low-2), pieces);
        Offset direct = 0, mergers = 0, saved = 0, visited = 0, seed = source;
        for (const MixedInterval& p : pieces) {
            if (p.hi <= seed || p.hi-p.lo < mixed_threshold) continue;
            while (seed < p.lo) {
                seed = next_reset(seed);
                ++direct;
            }
            if (seed >= p.hi) continue;
            const auto merged = merge_last(p.hi, p.bound, 400000);
            visited += merged.edges + p.bound;
            saved += p.hi-seed;
            seed = merged.seed;
            ++mergers;
        }
        while (seed < low) {
            seed = next_reset(seed);
            ++direct;
        }
        if (seed >= high) throw std::runtime_error("missed destination gate");
        const auto terminal = merge_edge(k, high, 400000);
        std::cout << k << ' ' << source << ' ' << low << ' ' << high << ' ' << seed
                  << ' ' << terminal.seed << ' ' << direct << ' ' << mergers << ' '
                  << visited << ' ' << saved << ' ' << pieces.size() << std::endl;
        source = terminal.seed;
    }
}

void trace_chain() {
    prepare();
    Offset seed = 0, lo, hi;
    unsigned k;
    while (std::cin >> k >> lo >> hi) {
        if (lo >= hi || hi > limit || (lo | hi) % 2 || !(k % 2) || k > 1000 ||
            hi - lo < 8192)
            throw std::runtime_error("invalid gate");
        Offset calls = 0;
        while (seed < lo) {
            seed = next_reset(seed);
            ++calls;
        }
        if (seed >= hi) throw std::runtime_error("trajectory missed gate");
        const Offset arrival = seed;
        check_gate(k, checkpoint + lo, checkpoint + hi);
        auto result = merge_edge(k, hi, 3000000);
        seed = result.seed;
        std::cout << k << ' ' << lo << ' ' << hi << ' ' << arrival << ' ' << calls << ' '
                  << result.exits << ' ' << result.edges << ' ' << seed << std::endl;
    }
}

void census(bool follow = false) {
    constexpr unsigned horizon = 16384;
    unsigned k, count = 0;
    Offset minimum = std::numeric_limits<Offset>::max(), maximum = 0;
    Offset largest_gain = 0, total = 0;
    Big lo, hi;
    const Big target = (power * 14348907 - 8282708212L) / 13959275;
    while (std::cin >> k >> lo >> hi) {
        if (!(k % 2) || k > 1000 || lo < checkpoint || hi <= lo || !(lo.get_ui() & 1) ||
            !(hi.get_ui() & 1) || hi - lo < 8192 || hi + limit > target)
            throw std::runtime_error("invalid census input");
        // The source seeds can have 140 digits; all merger displacements
        // immediately around a single edge fit in a machine word.
        base = hi - 8192;
        prepare();
        check_gate(k, lo, hi);
        auto result = merge_edge(k, 8192, 250000);
        if (!follow) {
            std::cout << k << ' ' << result.exits << ' ' << result.edges << ' '
                      << result.seed - 8192 << std::endl;
            continue;
        }
        Offset current = result.seed;
        for (unsigned n = 0; n < horizon; ++n) {
            const Offset next = next_reset(current);
            largest_gain = std::max(largest_gain, next-current);
            current = next;
        }
        const Offset shift = current-result.seed;
        minimum = std::min(minimum,shift);
        maximum = std::max(maximum,shift);
        total += shift;
        ++count;
    }
    if (follow) {
        std::cout << count << " mergers, " << Offset(count)*horizon
                  << " returns, displacement " << minimum << ".." << maximum
                  << ", largest gain " << largest_gain << ", total " << total << '\n';
    }
}

int main(int argc, char** argv) {
    if (argc == 1) trace_chain();
    else if (argc == 2 && std::string(argv[1]) == "--census") census();
    else if (argc == 2 && std::string(argv[1]) == "--follow-mergers") census(true);
    else if (argc == 2 && std::string(argv[1]) == "--edge-bands") follow_edge_bands();
    else if (argc == 2 && std::string(argv[1]) == "--mixed") mixed_bridges();
    else if (argc == 2 && std::string(argv[1]) == "--cover") cover_gaps();
    else {
        std::cerr << "Usage: checkpoint_y [--census | --follow-mergers | --edge-bands | --mixed | --cover]\n";
        return 2;
    }
}
