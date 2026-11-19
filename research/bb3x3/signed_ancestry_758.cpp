// Certify terminal-free mass residues by searching a signed inverse tree.
// c++ -O3 -std=c++17 signed_ancestry_758.cpp -o signed_ancestry_758
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>

using Integer = std::int64_t;

struct Survey {
    unsigned cap = 292;
    unsigned greatest = 0;
    Integer targets = 0;
    Integer nodes = 0;

    bool reaches_cap(Integer a, Integer c, unsigned depth) {
        if (a < -4 || c < -13 || a+2*c < 0) return false;
        ++nodes;
        greatest = std::max(greatest, depth);
        if (depth == cap) return true;
        if ((a+1)%6 == 0) {
            const Integer b = (a-2)/3;
            if (reaches_cap(b, c+b-1, depth+1)) return true;
        }
        if ((c+1)%6 == 0) {
            const Integer q = (c-5)/6;
            if (reaches_cap(a+4*q+3, 4*q-1, depth+1)) return true;
            if (reaches_cap(a+4*q+3, 4*q+1, depth+1)) return true;
        }
        return false;
    }
};

int main(int argc, char** argv) {
    const Integer width = argc == 2 ? std::atoll(argv[1]) : 1000000000;
    if (argc > 2 || width < 1 || width > 1000000000) {
        std::cerr << "usage: signed_ancestry_758 [width in 1..1000000000]\n";
        return 2;
    }
    Survey survey;
    for (Integer c=-1; c <= width/3+1; c+=2) {
        for (Integer gap=1; gap<=3; ++gap) {
            const Integer a = c+gap, mass = a+2*c;
            if (mass < 0 || mass > width) continue;
            ++survey.targets;
            if (survey.reaches_cap(a,c,0)) {
                std::cerr << "depth budget reached at " << a << ", " << c << '\n';
                return 1;
            }
        }
    }
    std::cout << "width " << width << ", targets " << survey.targets
              << ", signed nodes " << survey.nodes << ", greatest depth "
              << survey.greatest << '\n';
}
