#pragma once
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>

using Num = std::int64_t;
struct State {
    Num a;
    Num c;
};

enum Branch { bulk, jump, exceptional, returned, halted };

Branch branch(State s) {
    Num q = (s.c + 1) / 4;
    if (s.a >= 4*q + 3) return bulk;
    if (s.a <= s.c) return s.a % 2 == 0 ? returned : jump;
    return s.a % 2 == 0 ? halted : exceptional;
}

State advance(State s, Branch action) {
    if (action == bulk) {
        Num q = (s.c + 1) / 4;
        return {s.a - 4*q - 3, 6*q + 5};
    }
    if (action == jump) return {3*s.a + 2, s.c - s.a + 1};
    return {3*s.c + 8, 1};   // exceptional
}

struct Cover {
    std::vector<Num> powers{1};
    std::uint64_t leaves = 0;
    int max_gain = 0;

    Cover() {
        while (powers.back() < 100000000000000000LL)
            powers.push_back(3 * powers.back());
    }

    // Return 0 when this one interval cannot certify a return for all seeds.
    int bound(Num lo, Num hi) const {
        bool odd = lo % 2 != 0;
        State left{odd ? 5 : 3, odd ? lo : lo + 3};
        State right{left.a, odd ? hi : hi + 3};
        int cost = odd ? 4 : 8;  // growth in a + 2c

        // Batch k common J's.  u*3^k <= 2c+u suffices at the lower
        // endpoint and all larger seeds. Additional J's use the loop.
        Num u = left.a + 1;
        Num threshold = (2*left.c + u) / u;
        int k = int(std::upper_bound(powers.begin(), powers.end(), threshold)
                    - powers.begin()) - 1;
        Num delta = -u*((powers[k] - 1)/2) + 2*k;
        left = {u*powers[k] - 1, left.c + delta};
        right = {left.a, right.c + delta};
        cost += 4*k;

        for (int i = 0; i < 10000; ++i) {
            Branch action = branch(left);
            if (action != branch(right) || action == halted) return 0;
            if (action == returned) return (cost + 5)/2;
            // At a common exceptional endpoint state, monotonicity forces
            // each intermediate state to equal it before the exceptional move.
            if (action == exceptional && (left.a != right.a || left.c != right.c))
                return 0;
            left = advance(left, action);
            right = advance(right, action);
            cost += action == bulk ? 9 : action == jump ? 4 : 8;
        }
        return 0;
    }

    bool range(Num lo, Num hi) {
        if (lo > hi) return true;
        int gain = bound(lo, hi);
        if (gain > 0) {
            ++leaves;
            max_gain = std::max(max_gain, gain);
            return true;
        }
        if (lo == hi) {
            std::cerr << "Uncertified seed " << lo << '\n';
            return false;
        }
        Num mid = lo + 2*((hi - lo)/4);
        return range(lo, mid) && range(mid + 2, hi);
    }
};

