#include <gmpxx.h>
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

// Compile with g++ -O3 -fopenmp -std=c++17 dyadic_survival_758.cpp -lgmpxx -lgmp.
// Each normalized J costs one elementary move and P costs two. The final
// single bulk returning out of the ordinary branches is excluded.
using U = unsigned __int128;
using Big = mpz_class;
Big big(U value) {
    Big result;
    mpz_import(result.get_mpz_t(), 1, 1, sizeof(value), 0, 0, &value);
    return result;
}
using Count = std::uint64_t;

struct Subtree {
    U a, q, step;
    Count n;
    unsigned e;
};

struct Scan {
    unsigned power, limit, high = 0, deepest_split = 0;
    Count witness = 0, examined = 0, longest_count = 0, censored = 0;
    std::vector<Count> survivors;
    std::vector<std::pair<Count, unsigned>> long_tails;
    Count original_step = 10;  // spacing of the root numerators

    // p/q is in (0,1), with p odd and q a positive power of 2.
    // The large-integer fallback covers even a long tail without rounding.
    unsigned finish(Big p, Big q, unsigned e) const {
        while (e < limit) {
            if (3*p < q) {
                p *= 3;
                ++e;
            } else if (9*p > 5*q) {
                p = 9*p - 5*q;
                q *= 4;
                e += 2;
            } else break;
        }
        return e;
    }

    unsigned finish(U p, U q, unsigned e) const {
        while (e < limit) {
            if (q > (U(1) << 123)) return finish(big(p), big(q), e);
            if (3*p < q) {
                p *= 3;
                ++e;
            } else if (9*p > 5*q) {
                p = 9*p - 5*q;
                q *= 4;
                e += 2;
            } else break;
        }
        return e;
    }

    void record(Count n, unsigned e) {
        ++examined;
        if (e >= 189) long_tails.emplace_back(n,e);
        if (e >= limit) {
            if (survivors.size() < 20) survivors.push_back(n);
            ++censored;
        }
        if (e > high) {
            high = e;
            witness = n;
            longest_count = 1;
        } else if (e == high) {
            if (!longest_count || n < witness) witness = n;
            ++longest_count;
        }
    }

    // Surviving candidates form an arithmetic progression from a/q with
    // initial numerator n and spacing step/q. The original numerators
    // increase by original_step and remain odd multiples of five.
    void visit(U a, U q, U step, Count n, unsigned e,
               std::vector<Subtree>* frontier=nullptr, unsigned depth=0) {
        if (a > q) return;
        if (frontier && depth == 9) {
            frontier->push_back({a, q, step, n, e});
            return;
        }
        if (q > (U(1) << 123) || step > (U(1) << 123))
            throw std::overflow_error("prefix exceeds uint128");
        // A very deep node near a pure-P path may reach the safe division
        // bound before its cardinality drops to eight. Enumerate it directly.
        if (q > (U(1) << 120) || step > (U(1) << 120) ||
            q-a < 8*step || e >= limit) {
            for (; a <= q; a += step, n += original_step) record(n, finish(a, q, e));
            return;
        }
        deepest_split = std::max(deepest_split, e);
        visit(3*a, q, 3*step, n, e+1, frontier, depth+1);
        const U advance = 9*step;
        const U base = 9*a;
        const U cutoff = 5*q;
        // First point on the P side. Subtract the cutoff only after adding
        // the exact number of forward grid spacings, to stay unsigned.
        const U i = base >= cutoff ? 0 : (cutoff-base+advance-1)/advance;
        const U new_a = base + i*advance - cutoff;
        visit(new_a, 4*q, advance, n + original_step*static_cast<Count>(i), e+2, frontier, depth+1);
    }

    void run(bool brute) {
        const U q = U(1) << (2*power);
        if (brute) {
            for (Count n = 5; n < q; n += 10) record(n, finish(U(n), q, 0));
        } else {
            std::vector<Subtree> nodes;
            visit(5,q,10,5,0,&nodes);
            std::vector<Scan> shards(nodes.size(), Scan{power,limit});
            #pragma omp parallel for schedule(dynamic,1)
            for (std::size_t i=0; i<nodes.size(); ++i) {
                const auto& t = nodes[i];
                shards[i].visit(t.a,t.q,t.step,t.n,t.e);
            }
            for (const auto& shard : shards) {
                examined += shard.examined;
                long_tails.insert(long_tails.end(), shard.long_tails.begin(), shard.long_tails.end());
                censored += shard.censored;
                deepest_split = std::max(deepest_split, shard.deepest_split);
                for (Count n : shard.survivors)
                    if (survivors.size()<20) survivors.push_back(n);
                if (shard.longest_count==0 || shard.high<high) continue;
                if (shard.high>high || longest_count==0) {
                    high=shard.high;
                    witness=shard.witness;
                    longest_count=0;
                }
                witness = std::min(witness, shard.witness);
                longest_count += shard.longest_count;
            }
        }
    }
};

int main(int argc, char** argv) {
    if (argc == 2 && (std::string(argv[1]) == "--progressions" || std::string(argv[1]) == "--bit-progressions")) {
        const bool bits_mode = std::string(argv[1]) == "--bit-progressions";
        unsigned r, m, p;
        Count residue, modulus;
        while (std::cin >> r >> m >> p >> residue >> modulus) {
            if ((bits_mode ? p>62 : p>31) || !modulus || residue >= modulus || residue%10 != 5 || modulus%10)
                throw std::invalid_argument("invalid dyadic numerator progression");
            Scan scan{p,400};
            scan.original_step = modulus;
            scan.visit(residue,U(1)<<(bits_mode ? p : 2*p),modulus,residue,0);
            if (scan.censored || !scan.longest_count || scan.deepest_split >= 189 ||
                    scan.deepest_split >= scan.high)
                throw std::logic_error("inconclusive progression search");
            for (const auto& hit : scan.long_tails)
                std::cout << "late " << hit.first << ' ' << hit.second << '\n';
            std::cout << r << ' ' << m << ' ' << p << ' ' << residue << ' ' << modulus
                      << ' ' << scan.witness << ' ' << scan.high << '\n';
        }
        return 0;
    }
    if (argc < 3 || argc > 5) {
        std::cerr << "usage: dyadic_scan min_p max_p [limit=220] [--brute]\n";
        return 2;
    }
    const unsigned lo=std::stoul(argv[1]), hi=std::stoul(argv[2]);
    const unsigned limit=argc>=4? std::stoul(argv[3]):220;
    const bool brute=argc==5 && std::string(argv[4])=="--brute";
    if (!lo || hi>27 || lo>hi || !limit) return 2;
    for (unsigned p=lo; p<=hi; ++p) {
        const auto start=std::chrono::steady_clock::now();
        Scan scan{p,limit};
        scan.run(brute);
        if (!brute && scan.deepest_split >= 189)
            throw std::logic_error("A pruned gap could be missing from the long-tail ledger");
        if (!brute && scan.longest_count && scan.high <= scan.deepest_split)
            throw std::logic_error("pruned gap could affect maximum");
        const auto elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-start);
        std::cout << "p=" << p << " max=" << scan.high << " first=" << scan.witness
                  << " ties=" << scan.longest_count << " censored=" << scan.censored
                  << " deepest_split=" << scan.deepest_split << " replayed=" << scan.examined << " seconds=" << elapsed.count() << '\n';
        std::sort(scan.long_tails.begin(), scan.long_tails.end());
        for (const auto& item : scan.long_tails)
            std::cout << "long_tail " << p << " " << item.first << " " << item.second << '\n';
        if (scan.censored) {
            std::cout << "sample";
            for (const auto n : scan.survivors) std::cout << " " << n;
            std::cout << '\n';
        }
        std::cout.flush();
    }
}
