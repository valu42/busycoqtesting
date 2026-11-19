#pragma once
#include <map>
#include <string>
#include <vector>

using Word = std::uint64_t;
struct Ang { Num u, d; };
enum Phase { jump_odd, double_bulk, bulk_return, exceptional_odd, at_reset, terminal };
struct Pair { int gain, add, limit; };
constexpr Pair pairs[] = {{5,20,11}, {9,35,18}, {7,26,13}, {7,29,16}};

// Here a=2u-4d-1 and c=2d+1. With a odd, a first L makes it
// even. Classify that following move at the same time.
inline Phase phase(Ang p) {
    Num j = p.u - 3*p.d;
    if (p.u-2*p.d == 1) return at_reset;
    if (j <= 1) return jump_odd;
    Num t = 2*p.u - 9*p.d;
    if (t >= pairs[p.d & 3].limit) return double_bulk;
    if (j == 2 && (p.d & 1)) return exceptional_odd;
    return t <= 9+5*(p.d & 1) ? bulk_return : terminal;
}

inline Ang advance_pair(Ang s, Phase action) {
    if (action == jump_odd) return {s.u+2, 3*s.d-s.u+1};
    auto effect = pairs[s.d & 3];
    return {s.u+effect.gain, (9*s.d+effect.add)/4};
}

// A common J/LL word has d'=(A*d+B*u+e)/2^k, u'=u+g. Corrections
// (e,g) depend only on the single residue (A*d+B*u) modulo 2^k.
// Unsigned products retain the low 64 numerator bits. The exact final
// 2^k*d' is positive and smaller than 2^64 at the two supported scales.
class Packed {
    static constexpr int region_bits = 19;
    static constexpr int max_pairs = 5, max_ops = 16;
    struct Adjustment { Num additive; int gain; };
    struct Op {
        int bits = 0, mask = 0;
        Num mult = 1, mass = 0;
        Word launch_coef = 0, launch_constant = 0;
        std::vector<Adjustment> deltas;

        Ang start(Num seed) const {
            Word linear = launch_coef*Word(seed >> 1) + launch_constant;
            auto v = deltas[linear & mask];
            return {seed+launch_mass+v.gain, Num((linear+Word(v.additive)) >> bits)};
        }

        Ang advance(Ang s) const {
            Word linear = Word(mult)*s.d + Word(mass)*s.u;
            auto v = deltas[linear & mask];
            Word num = linear + Word(v.additive);
            return {s.u+v.gain, Num(num >> bits)};
        }
    };
    struct Plan {
        Num region = -1;
        bool returns = false;
        const Op* first = nullptr;
        std::vector<const Op*> stages;
    };
    Plan plan;
    Num low = 0, high = 0;
    std::map<std::string, Op> stages;

    static Ang replay(Ang s, const std::string& word) {
        for (char c : word) s = advance_pair(s, c == 'J' ? jump_odd : double_bulk);
        return s;
    }

    const Op* stage(const std::string& word) {
        auto found = stages.find(word);
        if (found != stages.end()) return &found->second;
        Op op;
        int den = 1;
        for (char c : word) {
            if (c == 'J') {
                op.mult *= 3;
                op.mass = 3*op.mass-den;
            } else {
                op.mult *= 9;
                op.mass *= 9;
                op.bits += 2;
                den *= 4;
            }
        }
        op.mask = den-1;
        op.launch_coef = Word(op.mult+2*op.mass);
        op.launch_constant = Word(op.mult)*Word(launch_offset-power)+Word(op.mass)*launch_mass;
        // mult is odd. At fixed mult*d+mass*u mod den every LL consumes
        // the same residue. Choosing u=0 enumerates the entire quotient.
        op.deltas.resize(den);
        for (int d = 0; d < den; ++d) {
            Ang end = replay({0,d}, word);
            op.deltas[(op.mult*d)&op.mask] = {den*end.d-op.mult*d, int(end.u)};
        }
        return &stages.emplace(word, std::move(op)).first->second;
    }

    static Ang enter(Num seed) {
        return {seed+launch_mass, seed/2-power+launch_offset};
    }

    void build(Num key) {
        Num l = std::max(low, key << region_bits);
        Num h = std::min(high, ((key+1) << region_bits)-1);
        Ang left = enter(l+(l & 1)), right = enter(h-(h & 1));
        plan.region = key;
        plan.returns = false;
        plan.stages.clear();
        std::string path;
        for (int i = 0; i < 256; ++i) {
            // In the underlying (a,c) cells a is nonincreasing and c
            // nondecreasing. At the right endpoint a is therefore smallest.
            if (right.u-2*right.d <= 1) break;
            Phase action = phase(left);
            if (action != phase(right)) break;
            if (action == bulk_return) {
                plan.returns = true;
                break;
            }
            if (action != jump_odd && action != double_bulk) break;
            left = advance_pair(left, action);
            right = advance_pair(right, action);
            path += action == jump_odd ? 'J' : 'B';
        }

        plan.first = nullptr;
        int pending = 0;
        std::string word;
        auto emit = [&] {
            const Op* op = stage(word);
            if (!plan.first) plan.first = op;
            else plan.stages.push_back(op);
            word.clear();
            pending = 0;
        };
        for (char c : path) {
            word += c;
            pending += c == 'B';
            if (pending == max_pairs || int(word.size()) == max_ops) emit();
        }
        if (!word.empty() || !plan.first) emit();
    }

public:
    void reset(Num l, Num h) { low = l; high = h; plan.region = -1; }

    Num get(Num seed) {
        auto key = seed >> region_bits;
        if (plan.region != key) build(key);
        Ang p = plan.first->start(seed);
        for (const Op* op : plan.stages) p = op->advance(p);
        if (plan.returns) return normalize(p.u+5+2*(p.d & 1));
        for (int i = 0; i < 5000; ++i) {
            auto action = phase(p);
            if (action == jump_odd || action == double_bulk) p = advance_pair(p, action);
            else if (action == bulk_return) return normalize(p.u+5+2*(p.d & 1));
            else if (action == at_reset) return normalize(2*p.d+1);
            else if (action == exceptional_odd) p = {p.u+4, 0};
            else throw std::runtime_error("possible halt at "+std::to_string(seed));
        }
        throw std::runtime_error("paired continuation limit");
    }
};
