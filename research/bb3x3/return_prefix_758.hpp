#pragma once

#include "reset_cover_758.hpp"
#include <array>

// Use the smaller same-parity endpoint to batch J's valid for every larger seed.
inline State reset_after_common_j(Num seed, Num first, const Cover& proof) {
    Num u = first % 2 ? 6 : 4;
    Num offset = first % 2 ? 0 : 3;
    Num threshold = (2*(first+offset)+u)/u;
    auto it = std::upper_bound(proof.powers.begin(), proof.powers.end(), threshold);
    int k = int(it-proof.powers.begin())-1;
    Num power = proof.powers[k];
    return {u*power-1, seed+offset+2*k-u*((power-1)/2)};
}

// Translate a shared guarded prefix along each residue class of the reset seed.
class ResetResidues {
    static constexpr int region_bits = 31;
    static constexpr Num region_size = Num{1} << region_bits;
    static constexpr int max_bulk = 9;

    struct Table {
        Num first = 0;
        int shift = 0;
        State stride{0, 0};
        bool returns = false;
        std::vector<State> values;
    };

    std::array<Table, 2> tables;
    Num region = -1;
    Num lower = 0, upper = 0;

    static void make(Table& table, Num first, Num last, const Cover& proof) {
        table = {};
        if (first > last) return;
        State entry = reset_after_common_j(first, first, proof);
        Num initial_a = entry.a, offset = entry.c-first;
        State left{initial_a, first+offset}, right{initial_a, last+offset};

        int bulks = 0;
        std::vector<Branch> prefix;
        // Along a shared J/L word a is nonincreasing as the seed increases.
        // Recheck the smallest a before each call to preserve the first reset.
        while (right.a > 1 && prefix.size() < 128) {
            Branch op = branch(left);
            if (op != branch(right)) break;
            if (op == returned) {
                table.returns = true;
                break;
            }
            if (op != bulk && op != jump) break;
            if (op == bulk) {
                if (bulks == max_bulk) break;
                ++bulks;
            }
            prefix.push_back(op);
            left = advance(left, op);
            right = advance(right, op);
        }
        table.first = first;
        table.shift = bulks+1;
        Num period = Num{1} << table.shift;
        if (last-first >= period) {
            // Before the ith bulk, a shift of 2^(bulks+1) at the seed still
            // leaves c unchanged modulo four. The floor in q therefore
            // translates exactly. J preserves binary precision, L loses one bit.
            State delta{0, period};
            for (Branch op : prefix) {
                if (op == bulk) delta = {delta.a-delta.c, 3*(delta.c/2)};
                else delta = {3*delta.a, delta.c-delta.a};
            }
            table.stride = delta;
        }
        for (Num r = 0; r <= std::min(period-1, last-first); r += 2) {
            State s{initial_a, first+r+offset};
            for (Branch op : prefix) s = advance(s, op);
            if (table.returns) s = {1, s.a/2+s.c+2};
            table.values.push_back(s);
        }
    }

public:
    void reset(Num lo, Num hi) {
        lower = lo;
        upper = hi;
        region = -1;
    }

    State get(Num seed, const Cover& proof) {
        Num key = seed >> region_bits;
        if (region != key) {
            region = key;
            Num lo = std::max(lower, key*region_size);
            Num hi = std::min(upper, (key+1)*region_size-1);
            for (int p = 0; p < 2; ++p)
                make(tables[p], lo+(lo%2!=p), hi-(hi%2!=p), proof);
        }
        const Table& t = tables[seed%2];
        Num offset = seed-t.first;
        Num r = offset & ((Num{1} << t.shift)-1);
        State s = t.values[r/2];
        // All branch shifts preserve delta_a + 2*delta_c = 2*period.
        if (t.returns) return {1, s.c+offset-r};
        Num n = offset >> t.shift;
        return {s.a+n*t.stride.a, s.c+n*t.stride.c};
    }
};

// Execute a further shared prefix on smaller seed intervals, grouping runs.
class ReturnPrefix {
    static constexpr int region_bits = 19;
    static constexpr int largest_bulk_run = 7;
    struct Run {
        Branch op;
        int count;
        Num power;
    };
    struct Plan {
        Num key = -1;
        bool returns = false;
        std::vector<Run> runs;
    };
    struct BulkEffect {
        Num cost;
        Num right;
    };

    ResetResidues initial;
    std::array<Plan, 2> plans;
    std::array<std::array<BulkEffect, 128>, 8> effects{};
    std::array<int, 8> cost_stride{}, right_stride{};
    Num lower = 0, upper = 0;

    void make(Plan& plan, Num first, Num last, const Cover& proof) {
        State left = initial.get(first, proof), right = initial.get(last, proof);
        plan.runs.clear();
        plan.returns = false;
        for (int i = 0; right.a > 1 && i < 256; ++i) {
            Branch op = branch(left);
            if (op != branch(right)) break;
            if (op == returned) {
                plan.returns = true;
                break;
            }
            if (op != bulk && op != jump) break;
            if (plan.runs.empty() || plan.runs.back().op != op ||
                (op == bulk && plan.runs.back().count == largest_bulk_run))
                plan.runs.push_back({op, 0, 1});
            Run& run = plan.runs.back();
            ++run.count;
            if (op == jump) run.power *= 3;
            left = advance(left, op);
            right = advance(right, op);
        }
    }

public:
    ReturnPrefix() {
        // x=floor((c+1)/4)+3 satisfies x'=floor(3x/2) under every L.
        // For n moves the decrement of a is
        // 8(x_n-x_0)-9n+4*(number of odd x_i for 0 <= i < n).
        // The final c is 6*x_(n-1)-13. Lifting x_0 by 2^n translates
        // x_n by 3^n and x_(n-1) by 2*3^(n-1).
        int power = 1;
        for (int n = 1; n <= largest_bulk_run; ++n) {
            power *= 3;
            cost_stride[n] = 8*(power-(1<<n));
            right_stride[n] = 4*power;
            for (int r = 0; r < (1<<n); ++r) {
                int x = r, previous = 0, odds = 0;
                for (int i = 0; i < n; ++i) {
                    previous = x;
                    odds += x%2;
                    x = 3*x/2;
                }
                effects[n][r] = {8*(x-r)-9*n+4*odds, 6*previous-13};
            }
        }
    }

    void reset(Num lo, Num hi) {
        lower = lo;
        upper = hi;
        for (Plan& p : plans) p.key = -1;
        initial.reset(lo, hi);
    }

    State get(Num seed, const Cover& proof) {
        Plan& plan = plans[seed%2];
        Num key = seed >> region_bits;
        if (plan.key != key) {
            plan.key = key;
            Num lo = std::max(lower, key<<region_bits);
            Num hi = std::min(upper, ((key+1)<<region_bits)-1);
            make(plan, lo+(lo%2!=seed%2), hi-(hi%2!=seed%2), proof);
        }
        State s = initial.get(seed, proof);
        for (const Run& run : plan.runs) {
            if (run.op == jump) {
                Num u = s.a+1;
                s = {u*run.power-1, s.c-u*((run.power-1)/2)+2*run.count};
            } else {
                Num x = ((s.c+1)>>2)+3;
                Num high = x >> run.count;
                auto row = effects[run.count][x&((1<<run.count)-1)];
                s = {s.a-cost_stride[run.count]*high-row.cost,
                     right_stride[run.count]*high+row.right};
            }
        }
        if (plan.returns) return {1, s.a/2+s.c+2};
        return s;
    }
    // Return -1 at a halt, -2 if the reference checker's original budget expires.
    Num first_return(Num seed, const Cover& proof) {
        auto finish = [](State s, int limit) -> Num {
            for (int i = 0; i < limit; ++i) {
                if (s.a == 1) return s.c;
                Branch op = branch(s);
                if (op == returned) return s.a/2+s.c+2;
                if (op == halted) return -1;
                s = advance(s, op);
            }
            return -2;
        };
        // After the initial J batch the two cache levels skip at most 128+256
        // moves and one return. The specific seed's reference J batch is at
        // least as long. Replay rare long paths to preserve the precise cap.
        Num result = finish(get(seed, proof), 4500);
        if (result == -2)
            result = finish(reset_after_common_j(seed, seed, proof), 5000);
        return result;
    }

};
