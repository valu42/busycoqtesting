// g++ -O3 -fopenmp -std=c++17 dyadic_tail_join_758.cpp -lgmpxx -lgmp -o dyadic_tail_join
#include <gmpxx.h>

#include <algorithm>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Word = std::uint64_t;
using Wide = unsigned __int128;

struct Prefix {
    Word angle;
    Word first_numerator;
};

struct Result {
    Word matches = 0;
    Word exact_replays = 0;
    std::vector<std::pair<Word, unsigned>> tails;
};

struct Search {
    unsigned power, half_length, threshold;
    Word denominator, grain, modulus;
    std::vector<std::vector<Prefix>> groups;
    std::vector<Result> results;

    Search(unsigned power, unsigned length, unsigned threshold, unsigned grain_bits)
        : power(power), half_length(length), threshold(threshold),
          denominator(Word(1) << (2*power)), grain(Word(1) << grain_bits),
          modulus(10*grain), groups(length+1), results(length+1) {}

    // Prepend inverse branches. The exact lower endpoint is in [a,a+2)
    // in units of 1/(denominator*grain).
    void build_first_halves(Wide a, unsigned depth, unsigned pairs) {
        if (depth == half_length) {
            const Word r = a % modulus;
            const Word angle = (5*grain + modulus - r) % modulus;
            const Word first = 10*static_cast<Word>(a/modulus) + 5 + 10*(r > 5*grain);
            groups[pairs].push_back({angle, first});
            return;
        }
        const Wide grid = Wide(denominator)*grain;
        build_first_halves(a/3, depth+1, pairs);
        build_first_halves((4*a+5*grid)/9, depth+1, pairs+1);
    }

    // Replay from the original numerator. The angle bounds in the join do
    // not influence the reported lengths.
    unsigned exact_length(Word numerator) const {
        Wide a = numerator, q = denominator;
        unsigned elapsed = 0;
        while (q < (Wide(1) << 123) && elapsed < 280) {
            if (3*a < q) {
                a *= 3;
                ++elapsed;
            } else if (9*a > 5*q) {
                a = 9*a - 5*q;
                q *= 4;
                elapsed += 2;
            } else {
                return elapsed;
            }
        }
        mpz_class x, d;
        mpz_import(x.get_mpz_t(), 1, 1, sizeof(a), 0, 0, &a);
        mpz_import(d.get_mpz_t(), 1, 1, sizeof(q), 0, 0, &q);
        while (elapsed < 280) {
            if (3*x < d) {
                x *= 3;
                ++elapsed;
            } else if (9*x > 5*d) {
                x = 9*x - 5*d;
                d *= 4;
                elapsed += 2;
            } else {
                return elapsed;
            }
        }
        throw std::overflow_error("Increase the exact replay limit beyond 280.");
    }

    // All first halves with j pairs have one width. Scan second intervals
    // against just this group of angular residues.
    struct Join {
        Search& search;
        unsigned pairs, bucket_shift = 0;
        const std::vector<Prefix>& keys;
        Result& result;
        Word scale;
        std::vector<unsigned> buckets;

        Join(Search& search, unsigned pairs)
            : search(search), pairs(pairs), keys(search.groups[pairs]),
              result(search.results[pairs]) {
            mpz_class value = mpz_class(search.denominator)*search.grain;
            mpz_mul_2exp(value.get_mpz_t(), value.get_mpz_t(), 2*pairs);
            mpz_class divisor;
            mpz_ui_pow_ui(divisor.get_mpz_t(), 3, search.half_length+pairs);
            value /= divisor;
            if (!value.fits_ulong_p() || value.get_ui() > UINT64_MAX/9)
                throw std::overflow_error("Choose smaller grain bits or longer half length.");
            scale = value.get_ui();

            while ((search.modulus >> bucket_shift) > keys.size()/4 + 1) ++bucket_shift;
            const unsigned count = (search.modulus >> bucket_shift) + 2;
            buckets.resize(count);
            unsigned index = 0;
            for (unsigned h=0; h<count; ++h) {
                while (index < keys.size() && (keys[index].angle >> bucket_shift) < h) ++index;
                buckets[h] = index;
            }
        }

        template<class Integer>
        static bool interval_may_survive(Integer& lo, Integer& hi, Integer& q,
                                         unsigned& elapsed, unsigned threshold,
                                         Integer safe_limit) {
            while (elapsed < threshold && q < safe_limit) {
                if (3*hi < q) {
                    lo *= 3;
                    hi *= 3;
                    ++elapsed;
                } else if (9*lo > 5*q) {
                    lo = 9*lo - 5*q;
                    hi = 9*hi - 5*q;
                    q *= 4;
                    elapsed += 2;
                } else {
                    return !(3*lo > q && 9*hi < 5*q);
                }
            }
            return true;
        }

        bool may_survive(Word z, Word width, unsigned elapsed) const {
            if (width < 64) return true;
            Word lo = z > 20 ? z-20 : 0;
            Word hi = std::min(width, z+20);
            Word q = width;
            if (lo > hi) return true;
            if (!interval_may_survive(lo,hi,q,elapsed,search.threshold,UINT64_MAX/9))
                return false;
            if (q < UINT64_MAX/9 || elapsed >= search.threshold) return true;
            Wide low=lo, high=hi, d=q;
            return interval_may_survive(low,high,d,elapsed,search.threshold,Wide(1)<<123);
        }

        void inspect_range(Word left, Word right, Word period, Word start,
                           Word width, unsigned second_pairs) {
            const auto first = keys.begin() + buckets[left >> bucket_shift];
            const auto last = keys.begin() + buckets[(right >> bucket_shift)+1];
            auto it = std::lower_bound(first, last, left,
                [](const Prefix& prefix, Word value) { return prefix.angle < value; });
            for (; it != last && it->angle <= right; ++it) {
                ++result.matches;
                const Word z = period*search.modulus + it->angle - start;
                const unsigned elapsed = 2*search.half_length + pairs + second_pairs;
                if (!may_survive(z,width,elapsed)) continue;
                const Word n = it->first_numerator + 10*period;
                if (n >= search.denominator) continue;
                ++result.exact_replays;
                const unsigned length = search.exact_length(n);
                if (length >= search.threshold) result.tails.emplace_back(n,length);
            }
        }

        void visit_second_halves(Word lo, Word hi, unsigned depth, unsigned pairs_so_far) {
            if (depth != search.half_length) {
                visit_second_halves(lo/3,hi/3,depth+1,pairs_so_far);
                visit_second_halves((4*lo+5*scale)/9,(4*hi+5*scale)/9,
                                    depth+1,pairs_so_far+1);
                return;
            }
            const Word modulus=search.modulus;
            const Word first_period=lo/modulus, last_period=(hi+5)/modulus;
            for (Word i=first_period; i<=last_period; ++i) {
                const Word left = i==first_period ? lo%modulus : 0;
                const Word right = i==last_period ? (hi+5)%modulus : modulus-1;
                inspect_range(left,right,i,lo,hi-lo,pairs_so_far);
            }
        }
    };

    void run() {
        std::size_t count = 1;
        for (unsigned j=0; j<=half_length; ++j) {
            groups[j].reserve(count);
            count = count*(half_length-j)/(j+1);
        }
        build_first_halves(0,0,0);
        #pragma omp parallel for schedule(dynamic,1)
        for (unsigned j=0; j<=half_length; ++j) {
            auto& prefixes = groups[j];
            std::sort(prefixes.begin(), prefixes.end(),
                [](const Prefix& x, const Prefix& y) { return x.angle < y.angle; });
            Join group(*this,j);
            group.visit_second_halves(0,group.scale,0,0);
        }
        Result total;
        for (const auto& group : results) {
            total.matches += group.matches;
            total.exact_replays += group.exact_replays;
            total.tails.insert(total.tails.end(), group.tails.begin(), group.tails.end());
        }
        std::sort(total.tails.begin(), total.tails.end());
        total.tails.erase(std::unique(total.tails.begin(),total.tails.end()),total.tails.end());
        std::cout << "matches " << total.matches << " exact " << total.exact_replays
                  << " long " << total.tails.size() << '\n';
        for (auto [n,e] : total.tails)
            std::cout << "long_tail " << power << " " << n << " " << e << '\n';
    }
};

int main(int argc, char** argv) {
    if (argc < 4 || argc > 5) {
        std::cerr << "usage: dyadic_tail_join power half_length threshold [grain_bits=32]\n";
        return 2;
    }
    const unsigned p=std::stoul(argv[1]), b=std::stoul(argv[2]), t=std::stoul(argv[3]);
    const unsigned bits = argc==5 ? std::stoul(argv[4]) : 32;
    if (p<2 || p>28 || b<3 || b>26 || t<=4*b || t>=280 || bits<12 || bits>40) return 2;
    Search search(p,b,t,bits);
    search.run();
}
