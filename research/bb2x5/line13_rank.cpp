// Locate the root pulse of each new even cell on line 13.
// Compile with C++20. BMI2 and carryless multiply are optional fast paths.
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>
#if defined(__BMI2__) || defined(__PCLMUL__)
#include <immintrin.h>
#endif

using Bits = std::uint64_t;
using std::size_t;
constexpr Bits odd_slots = 0xaaaaaaaaaaaaaaaaULL;

struct Packed {
    Bits length = 0;
    std::vector<Bits> words;

    void append(Bits value, unsigned count) {
        if (!count) return;
        unsigned used = length % 64;
        if (used == 0) words.push_back(value);
        else {
            words.back() |= value << used;
            if (used + count > 64) words.push_back(value >> (64 - used));
        }
        length += count;
    }

    void clear() {
        words.clear();
        length = 0;
    }
};

// A or C sets a toggle bit. C alone sets a compound bit. No silent slots
// are stored in a packet word.
struct Word {
    Packed toggle, compound;
    void clear() { toggle.clear(); compound.clear(); }
};

struct Selector {
    Packed emitted;
    Bits count = 0;
    std::vector<Bits> prefix_counts;

    void add(Bits mask, unsigned n) {
        emitted.append(mask, n);
        count += std::popcount(mask);
    }
    void index() {
        Bits total = 0;
        for (size_t j = 0; j < emitted.words.size(); ++j) {
            if (j % 512 == 0) prefix_counts.push_back(total);
            total += std::popcount(emitted.words[j]);
        }
        if (total != count) throw std::logic_error("inconsistent selector");
    }
    Bits select(Bits rank) const {
        if (rank >= count) throw std::logic_error("missing output packet");
        size_t j = 0;
        if (!prefix_counts.empty()) {
            auto upper = std::upper_bound(prefix_counts.begin(), prefix_counts.end(), rank);
            size_t block = size_t(upper - prefix_counts.begin() - 1);
            j = 512*block;
            rank -= prefix_counts[block];
        }
        while (rank >= Bits(std::popcount(emitted.words[j])))
            rank -= std::popcount(emitted.words[j++]);
        Bits bits = emitted.words[j];
        while (rank) { bits &= bits - 1; --rank; }
        return 64*j + std::countr_zero(bits);
    }
    void clear() { emitted.clear(); count = 0; prefix_counts.clear(); }
};

Bits inclusive_parity(Bits bits) {
#ifdef __PCLMUL__
    auto x = _mm_cvtsi64_si128(bits);
    return Bits(_mm_cvtsi128_si64(_mm_clmulepi64_si128(x, _mm_set1_epi64x(-1), 0)));
#else
    for (unsigned shift = 1; shift < 64; shift *= 2) bits ^= bits << shift;
    return bits;
#endif
}

Bits extract(Bits bits, Bits mask) {
#ifdef __BMI2__
    return _pext_u64(bits, mask);
#else
    Bits result = 0, dest = 1;
    while (mask) {
        if (bits & (mask & -mask)) result |= dest;
        mask &= mask - 1;
        dest <<= 1;
    }
    return result;
#endif
}

// Apply the published three-by-three cell table to up to 64 ordered inputs.
// On a non-4 toggle, the digit is 2 exactly when the preceding B run is odd.
void transform(const Word& input, size_t first_word, Bits length, int& digit,
               Word& output, Selector& selector, bool drop_first = false) {
    for (Bits offset = 0; offset < length; offset += 64) {
        size_t j = first_word + offset/64;
        unsigned n = std::min<Bits>(64, length - offset);
        Bits mask = ~Bits(0) >> (64 - n);
        Bits h = input.toggle.words[j] & mask;
        Bits c = input.compound.words[j] & mask;
        bool skip = drop_first && !offset;
        if (skip) {
            // The first A was consumed when the new pair became 21.
            h >>= 1; c >>= 1; --n;
            selector.add(0, 1);
            if (!n) continue;
            mask >>= 1;
        }
        Bits four = (inclusive_parity(h) << 1) ^ -Bits(digit == 4);
        // A carry records that the preceding toggle was in an odd slot.
        Bits odd = h & odd_slots, even = h & ~odd_slots;
        Bits previous_odd = (odd + ~even + (digit != 2)) ^ odd ^ ~even;
        Bits gap_odd = ~(previous_odd ^ odd_slots);
        Bits single = h & ~four;
        Bits doubled = four & (~h | c) & mask;
        Bits active = single | doubled;
        Bits out_toggle = (single & ~(gap_odd ^ c)) | doubled;
        unsigned size = std::popcount(active);
        output.toggle.append(extract(out_toggle, active), size);
        output.compound.append(extract(doubled, active), size);
        selector.add(active, n);

        if ((digit == 4) ^ (std::popcount(h) % 2)) digit = 4;
        else if (h) digit = 1 + (n - std::bit_width(h)) % 2;
        else digit = 1 + ((digit == 2) + n) % 2;
    }
}

void check_transform(const std::vector<unsigned>& letters, int initial) {
    // Entries are (new digit, outgoing packet). 1=A, 2=B and 3=C.
    constexpr int next[][4] = {{}, {1,4,2,4}, {2,4,1,4}, {}, {4,1,4,1}};
    constexpr int emitted[][4] = {{}, {0,1,0,2}, {0,2,0,1}, {}, {0,0,3,3}};
    Word input, expected;
    std::vector<Bits> positions;
    int scalar = initial;
    for (size_t i = 0; i < letters.size(); ++i) {
        unsigned in = letters[i];
        input.toggle.append(in != 2, 1);
        input.compound.append(in == 3, 1);
        int out = emitted[scalar][in];
        scalar = next[scalar][in];
        if (out) {
            expected.toggle.append(out != 2, 1);
            expected.compound.append(out == 3, 1);
            positions.push_back(i);
        }
    }
    int digit = initial;
    Word actual;
    Selector indices;
    transform(input, 0, letters.size(), digit, actual, indices);
    indices.index();
    if (digit != scalar || expected.toggle.length != actual.toggle.length ||
        actual.toggle.words != expected.toggle.words ||
        actual.compound.words != expected.compound.words || indices.count != positions.size())
        throw std::logic_error("packet comparison failed");
    for (size_t i = 0; i < positions.size(); ++i)
        if (positions[i] != indices.select(i)) throw std::logic_error("packet rank comparison failed");
}

void self_test() {
    unsigned count = 1;
    for (unsigned n = 0; n <= 7; ++n, count *= 3) {
        for (unsigned number = 0; number < count; ++number) {
            std::vector<unsigned> letters(n);
            unsigned digits = number;
            for (auto& q : letters) { q = 1 + digits % 3; digits /= 3; }
            for (int s : {1, 2, 4}) check_transform(letters, s);
        }
    }
    Bits seed = 13;
    for (unsigned n : {63, 64, 65, 127, 128, 129, 511, 32769}) {
        std::vector<unsigned> letters(n);
        for (auto& q : letters) {
            seed = seed * 6364136223846793005ULL + 1;
            q = 1 + (seed >> 32) % 3;
        }
        for (int s : {1, 2, 4}) check_transform(letters, s);
    }
}

struct Layer {
    // At depth d startup covers 2^d-1 root pulses, the period covers 2^d.
    // Each new startup is the old startup and one old period. Each new
    // period is two old periods. Selectors preserve the parent slot.
    std::array<Selector, 4> part;
};

Bits timestamp(const std::vector<Layer>& layers, bool periodic, Bits rank) {
    Bits offset = 0;
    for (size_t d = layers.size(); d > 0; --d) {
        const auto& part = layers[d-1].part;
        unsigned i = periodic ? 2 : 0;
        if (rank >= part[i].count) {
            rank -= part[i].count;
            offset += (Bits(1) << (d-1)) - !periodic;
            periodic = true;
            ++i;
        }
        rank = part[i].select(rank);
    }
    if (!periodic || rank != 0) throw std::logic_error("invalid root rank");
    return offset;
}

void prepare(const std::vector<int>& digits, std::vector<Layer>& layers,
             Word& startup, Word& period) {
    period.toggle.append(1, 1);
    period.compound.append(1, 1);
    for (size_t d = 0; d < layers.size(); ++d) {
        auto& part = layers[d].part;
        Word prefix_out, period_out;
        int digit = digits[d];
        transform(startup, 0, startup.toggle.length, digit, prefix_out, part[0]);
        transform(period, 0, period.toggle.length, digit, prefix_out, part[1]);
        int entering_cycle = digit;
        for (unsigned i : {2U, 3U})
            transform(period, 0, period.toggle.length, digit, period_out, part[i]);
        if (digit != entering_cycle || period_out.toggle.length == 0)
            throw std::logic_error("dyadic cycle failed");
        for (auto& selector : part) selector.index();
        startup = std::move(prefix_out);
        period = std::move(period_out);
    }
}

// Number of packets strictly before a specified root-time offset.
Bits before(const std::vector<Layer>& layers, bool periodic, Bits count, Bits limit) {
    Bits lo = 0, hi = count;
    while (lo < hi) {
        Bits mid = lo + (hi-lo)/2;
        if (timestamp(layers, periodic, mid) < limit) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}

bool run(Bits groups, Bits additional, unsigned depth, const std::string& tape) {
    if (!groups || depth > 60 || groups > std::numeric_limits<Bits>::max() - additional ||
        !tape.starts_with("1144") || tape.size() % 2 || tape.size() < 6 ||
        tape.find_first_not_of("124") != std::string::npos ||
        (tape.back() != '1' && tape.back() != '2') || depth >= tape.size()-4)
        throw std::invalid_argument("expected a canonical line-13 tape and a mature lower strip");
    std::vector<int> digits;
    for (size_t i = 4; i < tape.size(); ++i) digits.push_back(tape[i] - '0');
    std::vector<Layer> layers(depth);
    Word startup, period;
    prepare(digits, layers, startup, period);
    Bits cycle = Bits(1) << depth, onset = cycle-1;
    std::vector<Selector> history;
    std::array<Word,2> work;
    auto feed = [&](const Word& word, Bits slots, bool periodic, Bits base) {
        constexpr size_t chunk_words = 2048;
        for (Bits start = 0; start < slots; start += 64*chunk_words) {
            const Word* src = &word;
            size_t first = start/64;
            Bits n = std::min<Bits>(64*chunk_words, slots-start);
            for (size_t d = depth; n; ++d) {
                bool born = d == digits.size();
                if (born) {
                    Bits rank = 0;
                    for (size_t k = d-depth; k > 0; --k) rank = history[k-1].select(rank);
                    Bits pulse = groups + base + timestamp(layers, periodic, start+rank);
                    bool first_A = (src->toggle.words[first] & 1) && !(src->compound.words[first] & 1);
                    if (!first_A) {
                        std::cout << "B3 " << d+3 << " " << pulse << std::endl;
                        return false;
                    }
                    std::cout << "A " << d+4 << " " << pulse << std::endl;
                    digits.push_back(2);
                    digits.push_back(1);
                }
                size_t level = d-depth;
                if (level == history.size()) history.emplace_back();
                auto& selector = history[level];
                selector.clear();
                auto& out = work[level%2];
                out.clear();
                transform(*src, first, n, digits[d], out, selector, born);
                src = &out;
                first = 0;
                n = out.toggle.length;
            }
        }
        return true;
    };

    Bits first_count = startup.toggle.length;
    if (additional < onset) first_count = before(layers, false, first_count, additional);
    if (!feed(startup, first_count, false, 0)) return false;
    if (additional > onset) {
        Bits left = additional-onset;
        Bits base = onset;
        while (left >= cycle) {
            if (!feed(period, period.toggle.length, true, base)) return false;
            base += cycle;
            left -= cycle;
        }
        if (left && !feed(period, before(layers, true, period.toggle.length, left), true, base))
            return false;
    }
    std::cout << "last_visited " << digits.size()+3 << std::endl;
    return true;
}

int main(int argc, char** argv) try {
    if (argc == 2 && std::string(argv[1]) == "--check") {
        self_test();
        std::cout << "Checked packet outputs, digits and original positions." << std::endl;
        return 0;
    }
    if (argc != 5) throw std::invalid_argument("usage: line13-rank START_GROUPS ADDITIONAL_GROUPS SHALLOW_CELLS POSITIVE_TAPE");
    auto depth = std::stoul(argv[3]);
    if (depth > 60) throw std::invalid_argument("shallow strip exceeds 60 cells");
    run(std::stoull(argv[1]), std::stoull(argv[2]), unsigned(depth), argv[4]);
    return 0;
} catch (const std::exception& e) {
    std::cerr << e.what() << '\n';
    return 2;
}
