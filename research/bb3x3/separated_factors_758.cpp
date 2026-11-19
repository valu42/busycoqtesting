// Bound common ordinary words from nearby, distinct states of #758 or #153.
#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <vector>

constexpr int limit = 16384;
constexpr int gains[] = {5,9,7,7};
constexpr int offsets[] = {20,35,26,29};

struct Edge {
    int next;
    int cost;
};

Edge direction(int v, int k) {
    // Equality at the two guard boundaries is included. The next direction
    // can then be zero or one half, which is handled as a pure cycle.
    if (k%4 == 0 && 9*k <= 2*v) return {9*(k/4),2};
    if (3*k >= v) return {3*k-v,1};
    return {-1,0};
}

int error_transient(int q, const std::vector<int>& phases) {
    const int span = 7*q+1;
    const int count = span*static_cast<int>(phases.size());
    std::vector<int> distance(count,-1), path;
    std::vector<bool> active(count,false);
    auto advance = [&](int index) -> Edge {
        int phase = index/span, e = index%span-7*q;
        int next_phase = (phase+1)%phases.size();
        int k = phases[phase], k_next = phases[next_phase];
        const bool pair = 9*k < 2*q;
        if (pair) {
            int residue = ((e%4)*(q%4)%4+4)%4;
            int numerator = 9*e+q*offsets[residue];
            if (numerator%4) std::abort();
            e = numerator/4-k_next*gains[residue];
        } else {
            e = 3*e+q-2*k_next;
        }
        if (e < -7*q || e > 0) return {-1,0};
        return {next_phase*span+e+7*q, pair ? 2 : 1};
    };
    int largest = 0;
    for (int index=0; index<count; ++index) {
        if (distance[index] >= 0) continue;
        int x = index;
        path.clear();
        while (x >= 0 && distance[x] < 0) {
            if (active[x]) std::abort();  // a bounded deviation cycle would invalidate the bound
            active[x] = true;
            path.push_back(x);
            x = advance(x).next;
        }
        int tail = x < 0 ? 0 : distance[x];
        for (auto it=path.rbegin(); it!=path.rend(); ++it) {
            tail += advance(*it).cost;
            distance[*it] = tail;
            active[*it] = false;
            largest = std::max(largest,tail);
        }
    }
    return largest;
}

int main() {
    int longest_direction = 0, longest_error = 0, primitive = 0;
    for (int v=1; v<=limit; ++v) {
        int size = v/2+1;
        std::vector<int> mark(size), distance(size), path;
        for (int first=0; first<size; ++first) {
            if (mark[first]) continue;
            int k = first;
            path.clear();
            while (k >= 0 && mark[k] == 0) {
                mark[k] = 1;
                path.push_back(k);
                k = direction(v,k).next;
            }
            if (k >= 0 && mark[k] == 1) {
                std::vector<int> phases;
                int x = k;
                do {
                    phases.push_back(x);
                    mark[x] = 2;
                    distance[x] = 0;
                    x = direction(v,x).next;
                } while (x != k);
                if (k != 0 && 2*k != v && std::gcd(k,v) == 1) {
                    ++primitive;
                    if (std::gcd(v,6) != 1) std::abort();
                    longest_error = std::max(longest_error,error_transient(v,phases));
                }
            }
            for (auto it=path.rbegin(); it!=path.rend(); ++it) {
                int x = *it;
                if (mark[x] == 2) continue;
                Edge edge = direction(v,x);
                distance[x] = edge.next < 0 ? 0 : distance[edge.next]+edge.cost;
                mark[x] = 2;
                longest_direction = std::max(longest_direction,distance[x]);
            }
        }
    }
    if (longest_direction != 28 || primitive != 25 || longest_error != 22)
        return 1;
    std::cout << "Mass differences 1.." << limit << ": direction transient "
              << longest_direction << " calls, " << primitive
              << " mixed primitive cycles, bounded deviation transient "
              << longest_error << " calls.\n";
}
