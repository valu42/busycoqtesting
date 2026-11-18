// Timed A/B normal-form replay. Python independently certifies the local TM rules.
#include <charconv>
#include <exception>
#include <gmpxx.h>
#include <iostream>
#include <string>

int main(int argc, char** argv) try {
    if (argc != 2) return 2;
    unsigned long target;
    std::string argument(argv[1]);
    auto end = argument.data() + argument.size();
    auto parsed = std::from_chars(argument.data(), end, target);
    if (parsed.ec != std::errc{} || parsed.ptr != end) return 2;
    mpz_class b = 4, raw = 136, events = 0;
    unsigned long completed = 0;
    auto report = [&](const char* status, const mpz_class& guard_a) {
        std::cout << status << ' ' << completed << ' ' << guard_a.get_str(16) << ' ' << b.get_str(16)
                  << ' ' << raw.get_str(16) << ' ' << events.get_str(16) << '\n';
    };
    while (completed < target) {
        // Every round starts at A(4,b). After k consecutive A doublings we
        // have x=8*2^k, a=x-4, b'=b-(x-8)+k. Choose the last b' >= 0.
        mpz_class estimate = (b >> 3) + 1;
        unsigned long k = mpz_sizeinbase(estimate.get_mpz_t(),2)-1;
        mpz_class x = mpz_class(8) << k;
        while ((x << 1)-8-(k+1) <= b) { x <<= 1; ++k; }
        if (x-8-k > b) return 3;
        // 2*(x^2-64)/3 - 3*(x-8) + 3k; x is a power of two.
        mpz_class doubling = (mpz_class(1) << (2*k+6)) - 64;
        mpz_divexact_ui(doubling.get_mpz_t(),doubling.get_mpz_t(),3);
        raw += 2*doubling - 3*(x-8) + 3*k;
        events += k;
        mpz_class a = x-4;
        b -= x-8-k;
        mpz_class j = a < b ? a : b;
        raw += j*(2*j+9);
        ++events;
        if (b == a+1) { raw += 4*a+13; report("halt",a); return 0; }
        if (b == a+2) { raw += 4*a+47; a = 2*a+2; b = 3; }
        else { ++raw; a -= b; b <<= 1; }
        // Each B event strips exactly floor(a/3) local triples. Keep the
        // formal event count independent of the length of those triple sweeps.
        for (;;) {
            mpz_class q;
            unsigned long r = mpz_fdiv_q_ui(q.get_mpz_t(),a.get_mpz_t(),3);
            raw += q*(15*q + 6*b + 27);
            mpz_class tail = b+5*q;
            ++events;
            if (r == 1) { raw += 5*tail+72; b = tail+2; break; }
            if (r == 2) { raw += 6*tail+68; a = tail+5; b = 2; }
            else { raw += 2*tail+24; a = tail+3; b = 0; }
        }
        ++completed;
    }
    report("unknown",4);
    return 0;
} catch (const std::exception& e) { std::cerr << e.what() << '\n'; return 2; }
