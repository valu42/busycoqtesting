// Enumerate all ordinary rational directions up to a limit and exclude affine cycles.
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <vector>

using Integer = std::int64_t;
using Cycle = std::vector<int>;
constexpr int default_limit = 1000000;
constexpr int gain[] = {5, 9, 7, 7};
constexpr int offset[] = {20, 35, 26, 29};

int next_direction(int q, int k) {
    if (9*k < 2*q && k%4 == 0) return 9*(k/4);
    if (3*k > q && 2*k < q) return 3*k-q;
    return -1;
}

std::vector<Cycle> directions(int q, bool reduced_scan) {
    std::vector<Cycle> found;
    // At a cyclic minimum the incoming move is J and the outgoing move P.
    const int first = reduced_scan ? (q%3 == 1 ? 8 : 4) : 1;
    const int stride = reduced_scan ? 12 : 1;
    for (int seed = first; reduced_scan ? 9*seed < 2*q : 2*seed < q; seed += stride) {
        int k = seed;
        do {
            k = next_direction(q,k);
        } while (k > seed);
        if (k == seed && std::gcd(k,q) == 1) {
            Cycle cycle;
            do {
                cycle.push_back(k);
                k = next_direction(q,k);
            } while (k != seed);
            found.push_back(cycle);
        }
    }
    return found;
}

bool exclude_deviations(int q, const Cycle& cycle, Integer& visited) {
    // At the reference phase, one stamp per bounded deviation suffices.
    // Leaving the finite interval at an intermediate phase excludes an infinite orbit.
    std::vector<int> stamp(7*q+1);
    for (int initial = -7*q; initial <= 0; ++initial) {
        const int id = initial+7*q+1;
        Integer e = initial;
        for (;;) {
            if (stamp[e+7*q] != 0) {
                if (stamp[e+7*q] == id) {
                    std::cout << "Cyclic deviation q=" << q << " e=" << e << " direction";
                    for (int k : cycle) std::cout << " " << k;
                    std::cout << "\n";
                    return false;
                }
                break;
            }
            stamp[e+7*q] = id;
            ++visited;
            for (std::size_t i=0; i<cycle.size(); ++i) {
                const int k = cycle[i], next = cycle[(i+1)%cycle.size()];
                if (9*k < 2*q) {
                    const int r = int((((e%4)*(q%4))%4+4)%4);
                    const Integer num = 9*e+Integer(q)*offset[r];
                    if (num%4 != 0) std::abort();
                    e = num/4-Integer(next)*gain[r];
                } else {
                    e = 3*e+q-2*next;
                }
                if (e < -7*q || e > 0) break;
            }
            if (e < -7*q || e > 0) break;
        }
    }
    return true;
}

int main(int argc, char** argv) {
    const int limit = argc < 2 ? default_limit : std::atoi(argv[1]);
    // This upper bound preserves the int arithmetic used for direction and stamp indices.
    if (argc > 2 || limit < 5 || limit > 10000000) return 2;
    Integer primitive = 0, visited = 0;
    int largest = 0;
    for (int q=5; q<=limit; q+=2) {
        if (q%3 == 0) continue;
        auto cycles = directions(q,true);
        if (q <= 999 && cycles != directions(q,false)) std::abort();
        for (const auto& cycle : cycles) {
            ++primitive;
            largest = q;
            if (!exclude_deviations(q,cycle,visited)) return 1;
        }
    }
    if (limit == default_limit && (primitive != 128 || visited != 343738502 || largest != 961331))
        std::abort();
    std::cout << "Through q=" << limit << ": " << primitive << " primitive cycles, "
              << visited << " reference deviations, largest direction denominator "
              << largest << ", no affine cycle.\n";
}
