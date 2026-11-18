// Untimed blank-tape return computation for formal BB(2,5) holdout 4.
// Build with: c++ -O2 -std=c++17 line4_scalar.cpp -lgmpxx -lgmp -o line4_scalar
#include <gmpxx.h>

#include <array>
#include <charconv>
#include <cstdint>
#include <iostream>
#include <string_view>
#include <system_error>

constexpr unsigned block_digits = 7;
constexpr unsigned long block_modulus = 2187;  // 3^7
constexpr unsigned long output_modulus = 1000000007;

struct Block {
    unsigned long multiplier;
    long offset;
    bool returned_to_a;
};

using BlockTable = std::array<Block, block_modulus>;

BlockTable build_table() {
    BlockTable table{};
    for (unsigned long residue = 0; residue < block_modulus; ++residue) {
        // For input 3^7*q + residue, the current value is multiplier*q + offset.
        unsigned long multiplier = block_modulus;
        long offset = static_cast<long>(residue);
        bool returned_to_a = false;
        for (unsigned i = 0; i < block_digits; ++i) {
            const long digit = offset % 3;
            multiplier /= 3;
            offset /= 3;
            if (digit == 2) {
                offset -= 6;
                returned_to_a = true;
                break;
            }
            multiplier *= 7;
            offset = 7 * offset + digit + 1;
        }
        table[residue] = {multiplier, offset, returned_to_a};
    }
    return table;
}

void finish_b_excursion(mpz_class& value, mpz_class& quotient, const BlockTable& table) {
    for (;;) {
        const unsigned long residue =
            mpz_fdiv_q_ui(quotient.get_mpz_t(), value.get_mpz_t(), block_modulus);
        const Block& block = table[residue];
        value = quotient * block.multiplier + block.offset;
        if (block.returned_to_a) {
            return;
        }
    }
}

void show_return(std::uint64_t index, const mpz_class& width, const mpz_class& right_run) {
    std::cout << "return=" << index << " width=" << width
              << " b_bits=" << mpz_sizeinbase(right_run.get_mpz_t(), 2)
              << " b_mod_1000000007=" << mpz_fdiv_ui(right_run.get_mpz_t(), output_modulus)
              << '\n' << std::flush;
}

int main(int argc, char** argv) {
    std::uint64_t requested = 1024;
    if (argc > 2) {
        std::cerr << "Usage: line4_scalar [positive-return-number]\n";
        return 2;
    }
    if (argc == 2) {
        const std::string_view argument(argv[1]);
        const char* end = argument.data() + argument.size();
        const auto parsed = std::from_chars(argument.data(), end, requested);
        if (parsed.ec != std::errc{} || parsed.ptr != end || requested == 0) {
            std::cerr << "Return number must be a positive unsigned 64-bit decimal integer.\n";
            return 2;
        }
    }

    const BlockTable table = build_table();
    mpz_class right_run = 71;  // First B-to-A return from blank, at step 6,393.
    mpz_class width = 0;
    mpz_class level = 24;     // 24*3^width.
    mpz_class position, scalar, quotient;
    for (std::uint64_t index = 1;; ++index) {
        // Widths never decrease along the blank orbit.
        position = right_run + width + 9;
        while (position >= level) {
            ++width;
            ++position;
            level *= 3;
        }
        if (index == requested || index % 100000 == 0) {
            show_return(index, width, right_run);
        }
        if (index == requested) {
            return 0;
        }
        position += 2;  // position == level iff b == H_width.
        if (position == level) {
            std::cout << "halt_from_return=" << index << " width=" << width << '\n';
            return 0;
        }
        if (position > level) {
            scalar = 7 * level;  // b == H_width + 1.
        } else {
            scalar = 2 * level + right_run + width + 9;
        }
        finish_b_excursion(scalar, quotient, table);
        right_run.swap(scalar);
    }
}
