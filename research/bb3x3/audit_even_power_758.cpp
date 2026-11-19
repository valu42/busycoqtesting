#define AUDIT_EVEN_POWER
#include "cross_even_power_758.cpp"
#include <random>
#include <set>
#include <sstream>

// Independent implementation, using the original (a,c) rules one at a time.
static Num literal(Num seed) {
    State s = seed % 2 ? State{5,seed} : State{3,seed+3};
    for (int moves = 0; moves <= 11000; ++moves) {
        if (s.a == 1) return s.c;
        Num q = (s.c+1)/4;
        if (s.a >= 4*q+3) {
            s = {s.a-4*q-3, 6*q+5};
        } else if (s.a <= s.c) {
            if (s.a % 2 == 0) return s.c+s.a/2+2;
            s = {3*s.a+2, s.c-s.a+1};
        } else {
            if (s.a % 2 == 0) return -1;
            s = {3*s.c+8, 1};
        }
    }
    throw std::runtime_error("literal iteration limit");
}

static void audit_phases() {
    std::array<int,6> seen{};
    for (Num d = 0; d < 100; ++d) {
        for (Num a = 1; a <= 1501; a += 2) {
            Num c = 2*d+1;
            Ang p{(a+2*c-1)/2,d};
            State s{a,c};
            Phase expected;
            if (a == 1) {
                expected = at_reset;
            } else if (branch(s) == jump) {
                expected = jump_odd;
                s = advance(s, jump);
            } else if (branch(s) == exceptional) {
                expected = exceptional_odd;
                s = advance(s, exceptional);
            } else {
                s = advance(s, bulk);
                auto next = branch(s);
                if (next == bulk) {
                    expected = double_bulk;
                    s = advance(s, bulk);
                } else if (next == returned) {
                    expected = bulk_return;
                    if (s.c+s.a/2+2 != p.u+5+2*(p.d & 1))
                        throw std::logic_error("paired return");
                } else {
                    expected = terminal;
                }
            }
            if (phase(p) != expected) throw std::logic_error("phase");
            if (expected == jump_odd || expected == double_bulk || expected == exceptional_odd) {
                auto next = expected == exceptional_odd ? Ang{p.u+4,0} : advance_pair(p,expected);
                if (next.u != (s.a+2*s.c-1)/2 || next.d != (s.c-1)/2)
                    throw std::logic_error("paired successor");
            }
            ++seen[expected];
        }
    }
    for (auto count : seen)
        if (!count) throw std::logic_error("untested phase");
}

int main() {
    audit_phases();
    std::mt19937_64 rng(758);
    constexpr Num first = 2*power, last = 3*power-75000;
    std::uint64_t checked = 0, halting = 0;
    for (int i = 0; i < 768; ++i) {
        Num l = first+Num(rng()%(last-first-1048576));
        if (i < 2) l = i == 0 ? first : last-1048576;
        Num h = l+1048575;
        Packed table;
        table.reset(l,h);
        Num first_even = l+(l & 1);
        for (int k = 0; k < 1536; ++k) {
            Num seed = k < 1024 ? first_even+2*k
                                : (l+Num(rng()%std::uint64_t(h-l))+1) & ~Num{1};
            if (literal(seed+1) != normalize(seed+1)) throw std::logic_error("odd return");
            Num actual = literal(seed);
            if (actual > 0 && actual % 2) actual = literal(actual);
            Num got;
            try {
                got = table.get(seed);
            } catch (const std::runtime_error& e) {
                if (std::string(e.what()).find("possible halt") != 0) throw;
                got = -1;
            }
            if (actual != got) throw std::runtime_error("disagreement at "+std::to_string(seed));
            ++checked;
            halting += actual == -1;
        }
    }

    std::uint64_t covered = 0;
    for (int i = 0; i < 20; ++i) {
        auto l = first+Num(rng()%(last-first-2000000));
        Num h = l+250001+(rng()%1000000);
        Solver solver;
        std::ostringstream receipt;
        auto old = std::cout.rdbuf(receipt.rdbuf());
        solver.run(l,h);
        std::cout.rdbuf(old);

        std::set<Num> front;
        for (Num q = l; q <= l+5000; ++q) front.insert(q % 2 ? literal(q) : q);
        while (*front.begin() < h) {
            auto s = *front.begin();
            front.erase(front.begin());
            auto r = literal(s);
            if (r <= 0) throw std::runtime_error("sample orbit halts");
            if (r & 1) r = literal(r);
            if (r <= s) throw std::logic_error("literal progress");
            front.insert(r);
        }
        if (*front.begin() < solver.front.first() || *front.rbegin() > solver.front.last())
            throw std::logic_error("crossing");
        covered += 5001;
    }
    std::cout << checked << " even samples (" << halting << " halts), "
              << checked << " odd samples, " << covered << " crossing inputs\n";
}
