// Prove all inputs leading up to the fifth candidate enter its local bypass.
#include "reset_cover_758.hpp"
#include <stdexcept>

constexpr Num K = 40486323621582648;

void check(Num far, Num near, std::uint64_t leaves, int gain) {
    Cover cover;
    Num lower=K-far, upper=K-near;
    for (int parity=0; parity<=1; ++parity) {
        Num first=lower+(lower%2!=parity), last=upper-(upper%2!=parity);
        if (!cover.range(first,last)) throw std::runtime_error("uncertified reset");
    }
    if (cover.leaves!=leaves || cover.max_gain!=gain || gain>=near-73)
        throw std::runtime_error("unexpected bound");
    std::cout << lower << ' ' << upper << ' ' << leaves << ' ' << gain << '\n';
}

int main() {
    check(100000000000,100000000,83292670,763);
    check(100000000,10000,861226,672);
}
