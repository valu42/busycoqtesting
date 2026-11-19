// Exact four-step Bigfoot evaluator in Ligocki's unshifted coordinates.
#include <gmpxx.h>
#include <algorithm>
#include <array>
#include <cstdint>
#include <charconv>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

struct Walk {
    int64_t gain = 0;
    int64_t minimum = 0;

    void append(const Walk &other) {
        minimum = std::min(minimum, gain + other.minimum);
        gain += other.gain;
    }
};

struct Block {
    unsigned length;
    Walk walk;
};

Block direct_block(unsigned x) {
    static constexpr int gain[] = {0, 1, -1, 0, 1, 0};
    static constexpr int offset[] = {-1, -1, 3, 1, 3, 5};
    static constexpr unsigned mode[] = {2, 3, 2, 5, 2, 3};
    unsigned b = 2*x + 1, c = 2;
    Walk walk;
    for (unsigned j = 0; j < 4; ++j) {
        unsigned r = b % 6;
        if ((b % 2 == 1) != (j < 2)) throw std::logic_error("length parity mismatch");
        b = 8*(b/6) + c + offset[r];
        c = mode[r];
        walk.append({gain[r], std::min(0, gain[r])});
    }
    if (!(b % 2) || c != 2) throw std::logic_error("phase mismatch");
    return {(b-1)/2, walk};
}

class Evaluator {
    static constexpr unsigned radix = 81*81;
    std::array<Block, radix> pair;
    // At level k the length is 4 * 2^k four-step blocks.
    std::vector<mpz_class> divisors = {mpz_class(radix)*radix};

public:
    explicit Evaluator(unsigned top) {
        for (unsigned i = 0; i < radix; ++i) {
            auto first = direct_block(i);
            if (i < 81 && 81*first.length <= 256*i)
                throw std::logic_error("length growth bound failed");
            auto second = direct_block(first.length);
            first.walk.append(second.walk);
            pair[i] = {second.length, first.walk};
        }
        for (unsigned i = 0; i < top; ++i)
            divisors.push_back(divisors.back()*divisors.back());
    }

    Walk run(mpz_class &x, unsigned level) const {
        mpz_class high;
        if (x >= divisors[level])
            mpz_tdiv_qr(high.get_mpz_t(), x.get_mpz_t(), x.get_mpz_t(), divisors[level].get_mpz_t());
        Walk walk;
        if (level == 0) {
            uint64_t low = x.get_ui();
            for (unsigned i = 0; i < 2; ++i) {
                const Block &b = pair[low % radix];
                low = (low/radix << 16) + b.length;
                walk.append(b.walk);
            }
            x = low;
        } else {
            walk = run(x, level-1);
            walk.append(run(x, level-1));
        }
        if (high != 0) x += high << (32UL << level);
        return walk;
    }
};

int main(int argc, char **argv) {
    if (argc != 2) {
        std::cerr << "usage: bigfoot_blank_829 MACRO_STEPS (a positive multiple of 16)\n";
        return 2;
    }
    std::string argument = argv[1];
    uint64_t steps = 0;
    const char *end = argument.data() + argument.size();
    auto parsed = std::from_chars(argument.data(), end, steps);
    if (parsed.ec != std::errc{} || parsed.ptr != end) return 2;
    if (!steps || steps % 16 || steps > (uint64_t{1} << 40)) return 2;
    uint64_t chunks = steps / 16;
    unsigned top = 0;
    while ((uint64_t{2} << top) <= chunks) ++top;
    Evaluator evaluator(top);
    mpz_class x = 0;
    Walk walk;
    for (int k = static_cast<int>(top); k >= 0; --k) {
        if ((chunks >> k) & 1)
            walk.append(evaluator.run(x, k));
    }
    std::cout << "steps=" << steps << " counter=" << 2+walk.gain
              << " minimum=" << 2+walk.minimum
              << " x_bits=" << mpz_sizeinbase(x.get_mpz_t(), 2)
              << " x_mod_1000000007=" << mpz_fdiv_ui(x.get_mpz_t(), 1000000007)
              << " x_mod_1000000009=" << mpz_fdiv_ui(x.get_mpz_t(), 1000000009) << '\n';
    return 2+walk.minimum < 0;
}
