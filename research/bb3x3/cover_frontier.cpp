// Check the earlier two-parity frontier.
#include "reset_cover_758.hpp"

int main(int argc, char** argv) {
    if (argc != 1 && argc != 3) {
        std::cerr << "Usage: cover_frontier [low high]\n";
        return 2;
    }
    Num lo = argc == 1 ? 1079817520208950LL : std::stoll(argv[1]);
    Num hi = argc == 1 ? 1080000000000000LL : std::stoll(argv[2]);
    // W starts at most 1+2*hi and grows by <=9 per branch. The 10,000
    // branch cap and hi<=10^17 keep even the intermediate 3*a inside int64.
    if (lo < 3 || hi < lo || hi > 100000000000000000LL) return 2;
    for (int p = 0; p < 2; ++p) {
        Cover check;
        Num first = lo % 2 == p ? lo : lo + 1;
        Num last = hi % 2 == p ? hi : hi - 1;
        if (!check.range(first, last)) return 1;
        std::cout << "parity " << p << ", leaves " << check.leaves
                  << ", maximum jump bound " << check.max_gain << std::endl;
        if (argc == 1 && (check.max_gain != (p ? 801 : 71) ||
                          check.leaves != (p ? 196904171 : 1)))
            return 1;
    }
}
