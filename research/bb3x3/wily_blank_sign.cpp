// Certify the Wily blank sign interval using packed run lengths.
// g++ -std=c++17 -O3 wily_blank_sign.cpp -lgmpxx -lgmp -o wily_blank_sign
// ./wily_blank_sign 256 > suffix.txt
#include <cstdint>
#include <deque>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

#include <gmpxx.h>

namespace {
using Word = std::uint64_t;
using Length = unsigned __int128;
using Runs = std::vector<Word>;

unsigned mode(Word run) { return run & 3; }
Word count(Word run) { return run >> 2; }
bool alternating(unsigned carry) { return carry == 0 || carry == 3; }

Word pack(unsigned carry, Word size) {
    if (size > (UINT64_MAX >> 2)) {
        throw std::overflow_error("one run needs more than 62 count bits");
    }
    return (size << 2) | carry;
}

unsigned following(unsigned carry, Word size) {
    return alternating(carry) && (size & 1) ? 3 - carry : carry;
}

void append(Runs& result, unsigned carry, Word size) {
    if (!size) return;
    if (!result.empty()) {
        const Word last = result.back();
        if (following(mode(last), count(last)) == carry) {
            result.back() = pack(mode(last), count(last) + size);
            return;
        }
    }
    result.push_back(pack(carry, size));
}

// The two constant runs use carries 1 and 2. The other two start an
// alternating 0,3 run. This implements the four original Wily bit rules.
void through(const Runs& input, bool& bit, Runs& output) {
    for (const Word run : input) {
        const unsigned carry = mode(run);
        const Word size = count(run);
        if (carry == 1) {
            append(output, bit ? 0 : 3, size);
            bit ^= size & 1;
        } else if (carry == 2) {
            append(output, bit ? 1 : 2, size);
        } else {
            const Word zeros = (size + (carry == 0)) / 2;
            append(output, 1 + (bit ^ (carry == 3)), zeros);
            bit ^= size & 1;
        }
    }
}

Length length(const Runs& runs) {
    // Each count is at most 62 bits, and a vector cannot have 2^64 elements.
    Length total = 0;
    for (const Word run : runs) total += count(run);
    return total;
}

mpz_class integer(Length value) {
    mpz_class result;
    mpz_import(result.get_mpz_t(), 1, 1, sizeof(value), 0, 0, &value);
    return result;
}

Length fixed_length(const mpz_class& value) {
    if (value < 0 || mpz_sizeinbase(value.get_mpz_t(), 2) > 128) {
        throw std::overflow_error("partial period exceeds 128 bits");
    }
    Length result = 0;
    std::size_t words;
    mpz_export(&result, &words, 1, sizeof(result), 0, 0, value.get_mpz_t());
    return result;
}

Runs prefix(const Runs& input, Length wanted) {
    Runs result;
    for (const Word run : input) {
        if (wanted <= count(run)) {
            append(result, mode(run), static_cast<Word>(wanted));
            break;
        }
        result.push_back(run);
        wanted -= count(run);
    }
    return result;
}

void consume_first(Runs& runs, bool cyclic) {
    const Word first = runs.front();
    if (count(first) == 1) {
        runs.erase(runs.begin());
    } else {
        runs.front() = pack(following(mode(first), 1), count(first) - 1);
    }
    if (cyclic) append(runs, mode(first), 1);
}

void through_period(const Runs& input, bool& bit, mpz_class& remaining,
                    const mpz_class& period, Runs& output) {
    mpz_class whole, extra;
    mpz_fdiv_qr(whole.get_mpz_t(), extra.get_mpz_t(), remaining.get_mpz_t(), period.get_mpz_t());
    bool after_one = bit;
    through(input, after_one, output);
    const Length events = length(output);
    bool final_bit = mpz_odd_p(whole.get_mpz_t()) ? after_one : bit;
    Runs tail;
    through(prefix(input, fixed_length(extra)), final_bit, tail);
    remaining = whole * integer(events) + integer(length(tail));
    if (after_one != bit) through(input, after_one, output);
    bit = final_bit;
}

void verify(unsigned power) {
    mpz_class remaining = mpz_class(1) << power;
    Runs runs{pack(0, 1), pack(1, 1)};
    std::deque<bool> pending{false, false};
    std::string suffix;
    std::size_t extensions = 0;
    bool periodic = true;

    while (remaining > 0) {
        if (pending.empty()) {
            const unsigned carry = mode(runs.front());
            if (carry == 1) throw std::runtime_error("physical halting carry reached the edge");
            if (carry == 2) {
                pending.push_back(true);
                pending.push_back(true);
            }
            pending.push_back(false);
            if (carry != 0) pending.push_back(false);
            consume_first(runs, periodic);
            --remaining;

            if (suffix.size() >= 69) {
                if (suffix.size() != 69 + 2*extensions || carry != 3 ||
                    (remaining > 0 && mode(runs.front()) != 0)) {
                    throw std::runtime_error("upper zero-pair sign certificate failed");
                }
                ++extensions;
            }
        }
        bool bit = pending.front();
        pending.pop_front();
        const mpz_class period = periodic ? integer(length(runs)) : mpz_class(0);
        if (periodic && remaining <= period) {
            runs = prefix(runs, fixed_length(remaining));
            periodic = false;
        }
        Runs output;
        output.reserve(runs.size());
        if (periodic) {
            through_period(runs, bit, remaining, period, output);
        } else {
            through(runs, bit, output);
            remaining = integer(length(output));
        }
        runs.swap(output);
        suffix.push_back(bit ? '1' : '0');
    }
    for (const bool bit : pending) suffix.push_back(bit ? '1' : '0');
    if (suffix.size() != 69 + 2*extensions || suffix.substr(suffix.size()-2) != "00") {
        throw std::runtime_error("unexpected final width or upper pair");
    }
    std::cerr << "2^" << power << " sweeps, " << suffix.size() << " bits, "
              << extensions << " verified late extensions\n";
    std::cout << suffix << '\n';
}
}  // namespace

int main(int argc, char** argv) {
    try {
        if (argc != 2) throw std::invalid_argument("supply a single sweep exponent, at least 22");
        std::size_t used;
        const std::string argument(argv[1]);
        const int power = std::stoi(argument, &used);
        if (used != argument.size() || power < 22) throw std::invalid_argument("invalid sweep exponent");
        verify(static_cast<unsigned>(power));
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
    return 0;
}
