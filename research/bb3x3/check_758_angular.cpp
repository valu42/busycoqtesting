// Build with c++ -O3 -std=c++17 check_758_angular.cpp -o check_758_angular
#include <cassert>
#include <cstdint>
#include <iostream>
#include <utility>

using U = std::uint64_t;
using Wide = __int128_t;
using State = std::pair<U, U>;

static constexpr U origin = 1'080'000'000'055'450;
static constexpr U steps = 771'519'141;
static constexpr U mod_limit = 32'000'000'000;
static constexpr U cells = 1024;

static State step(State s) {
    const auto [a, c] = s;
    if (a <= c) {
        if (a % 2 == 0) return {1, c + a/2 + 2};
        if (c % 2 == 1) return {3*a + 2, c - a + 1};
        assert(a == 1 && c >= 2);
        return {3, c + 3};
    }
    assert(c % 2 == 1);
    const U q = (c + 1)/4;
    if (a >= 4*q + 3) return {a - 4*q - 3, 6*q + 5};
    assert(c % 4 == 3 && a == c + 2);  // All other live-domain cases halt.
    return {3*c + 8, 1};
}

int main() {
#ifdef NDEBUG
    std::cerr << "Compile without -DNDEBUG to run the checks.\n";
    return 2;
#endif
    // Each call increases mass by at most nine, so intermediate products in
    // the replay fit in 64 bits. Signed 128-bit products below are explicit.
    State point{1, origin};
    for (U i = 0; i < steps; ++i) point = step(point);
    const auto [a, c] = point;
    assert(a == 1'408'855'846'243'751 && c == 375'573'977'278'745);
    const U u = (a + 2*c - 1)/2;
    const U d = (c - 1)/2;
    const Wide z = Wide(529)*d - Wide(92)*u + 900;
    assert(z == -20'857'846'628'352LL && z % (1<<17) == 0 && z % (1<<18) != 0);
    assert(Wide(cells)*d/u == 178);
    // Interval endpoint checks in the proof. Here q <= mod_limit and
    // t = (92u-900)/529. Compensate exact rational rounding algebraically.
    // t/u lies strictly between bins 178 and 179; t+27q is still in bin 178.
    assert(Wide(cells)*(92*Wide(u)-900) > 178*Wide(529)*u);
    assert(Wide(cells)*(92*Wide(u)-900+27*Wide(529)*mod_limit) < 179*Wide(529)*u);
    // Monotone in u as verified by the leading coefficients.
    static_assert(cells*92 > 178*529 && cells*92 < 179*529);
    // 9d <= 2u-12 gives the first two B moves when d is 0 modulo 4.
    assert(9*(92*Wide(u)-900+4*Wide(529)*mod_limit) <= (2*Wide(u)-12)*529);
    // After them d1=(9d+20)/4; the next J guard is (u+4)/3<=d1<=(u+4)/2.
    assert(3*(9*(92*Wide(u)-900)+20*529) > 4*529*(Wide(u)+4));
    assert(2*(9*(92*Wide(u)-900+4*Wide(529)*mod_limit)+20*529) < 4*529*(Wide(u)+4));
    static_assert(9*92 < 2*529 && 3*9*92 > 4*529 && 2*9*92 < 4*529);
    // The actual deterministic continuation reaches its first reset in 22 calls.
    for (int i = 1; i <= 22; ++i) {
        point = step(point);
        if (i != 22) assert(point.first != 1);
    }
    assert(point.first == 1 && point.second == 1'080'001'900'400'671);
    std::cout << "Blank checkpoint replayed. Matched angular bin 178 and 17 binary digits.\n"
              << "Actual continuation reaches reset " << point.second << " in 22 calls.\n";
}
