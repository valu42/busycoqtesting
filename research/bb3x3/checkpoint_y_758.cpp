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

State odd_header(Offset x) {
    State s{2 * power - 1, checkpoint + x - power + 585};
    if (s.c <= 0) throw std::runtime_error("illegal initial jumps");
    for (unsigned i = 0; i < 8; ++i) {
        bulk(s);
        if (s.a <= 1) throw std::runtime_error("early header return");
    }
    jump(s);
    return s;
}

unsigned even_gain(Offset x) {
    State s{4 * (power / 3) - 1, checkpoint + x - 2 * (power / 3) + 587};
    if (s.c <= 0) throw std::runtime_error("illegal even launch");
    for (char op : std::string("LLJLLJL")) {
        if (op == 'J') jump(s); else bulk(s);
        if (s.a <= 1) throw std::runtime_error("early even return");
    }
    if (s.a > s.c || s.a.get_ui() % 2) throw std::runtime_error("even return guard");
    Big gain = s.a / 2 + s.c + 2 - checkpoint - x;
    return gain.get_ui();
}

void prepare() {
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
    // Keep c+13 below checkpoint/4. The formal mass never decreases,
    // so every formal intermediate state still satisfies a>c+4.
    for (unsigned j = 0; j < initial_packs.size(); ++j) {
        Big bound = max_c + 13 + 38342 * ((Big(1) << j) / 512);
        for (;;) {
            bound = (bound * factor + mask) >> bits;
            if (4 * bound > checkpoint) break;
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
    Big x = c - checkpoint;
    if (!x.fits_ulong_p() || x <= from || x > limit)
        throw std::runtime_error("exit outside verifier range");
    return x.get_ui();
}

Offset next_reset(Offset x) {
    if (x & 1) return x + even_gains[x % 64];

    State s = lanes[(x % 512) / 2];
    const Offset periods = x / 512;
    s.c += Big(38342) * periods;
    s.a -= Big(75660) * periods;
    Big y = (s.c + 7) / 2;
    unsigned gain = 0;
    unsigned bucket = x == 0 ? 0 : std::numeric_limits<Offset>::digits - __builtin_clzl(x);
    for (unsigned i = 0; i < initial_packs.at(bucket); ++i) gain += apply_block(y);
    Big nc = 2 * y - 7;
    s.a += 2 * (s.c - nc) + gain;
    s.c = nc;

    for (unsigned step = 0; step < 5000; ++step) {
        if (s.a == 1) return checked_exit(s.c, x);
        if (s.a <= s.c) {
            if (s.a.get_ui() & 1) jump(s);
            else return checked_exit(s.a / 2 + s.c + 2, x);
            continue;
        }
        y = (s.c + 7) / 2;
        const unsigned block_gain = apply_block(y);
        nc = 2 * y - 7;
        Big na = s.a + 2 * (s.c - nc) + block_gain;
        if (na > 1) {
            s = {na, nc};
            continue;
        }
        const bool low = (s.c.get_ui() & 3) == 1;
        const Big difference = s.a - s.c;
        if (difference >= (low ? 2 : 4)) bulk(s);
        else if (difference == 2 && !low) s = {3 * s.c + 8, 1};
        else throw std::runtime_error("direct halt at offset " + std::to_string(x));
    }
    throw std::runtime_error("individual return exceeded budget");
}

int main() {
    prepare();
    Offset seed = 0, lo, hi;
    unsigned k;
    while (std::cin >> k >> lo >> hi) {
        if (lo >= hi || hi > limit || (lo | hi) % 2 || !(k % 2) || k > 1000)
            throw std::runtime_error("invalid gate");
        Offset calls = 0;
        while (seed < lo) {
            seed = next_reset(seed);
            ++calls;
        }
        if (seed >= hi) throw std::runtime_error("trajectory missed gate");
        const Offset arrival = seed;
        for (Offset x : {lo, hi - 2}) {
            State s = odd_header(x);
            for (unsigned i = 0; i < k; ++i) {
                bulk(s);
                if (s.a <= 1) throw std::runtime_error("early gate return");
            }
            if (s.a > s.c || s.a.get_ui() % 2) throw std::runtime_error("gate return guard");
        }

        // Every possible first exit is the successor of a seed in the final cap slots.
        const unsigned cap = std::max(615U, (4 * 293 + 9 * (8 + k) + 5) / 2);
        if (hi - lo <= cap) throw std::runtime_error("gate too narrow");
        std::set<Offset> pending;
        for (Offset x = hi - cap; x < hi; ++x) {
            Offset dest = next_reset(x);
            if (dest >= hi) pending.insert(dest);
        }
        if (pending.empty()) throw std::runtime_error("empty exit set");
        const auto exits = pending.size();
        Offset edges = 0;
        while (pending.size() > 1) {
            if (++edges > 3000000) throw std::runtime_error("merger budget");
            Offset x = *pending.begin();
            pending.erase(pending.begin());
            pending.insert(next_reset(x));
        }
        seed = *pending.begin();
        std::cout << k << ' ' << lo << ' ' << hi << ' ' << arrival << ' '
                  << calls << ' ' << exits << ' ' << edges << ' ' << seed << std::endl;
    }
    return 0;
}
