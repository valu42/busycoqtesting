#include <array>
#include <gmpxx.h>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>
using u32 = std::uint32_t;
using u64 = std::uint64_t;

constexpr unsigned b = 27, m = 35, first = 14;
constexpr u32 period = 1u << (b-1), mask = period-1;
constexpr u32 C = m + 5*(b+1)/4;
std::array<u32,1 << first> carries, weights;
std::array<u32,1 << (b-first)> remaining;
u32 pow3 = 1;
void init() {
    for (unsigned i=0; i<first; ++i) pow3 *= 3;
    for (u32 i=0; i<carries.size(); ++i) {
        u32 y=i;
        for (unsigned j=0; j<first; ++j) {
            weights[i] += y&1;
            y = 3*((y+1)/2);
        }
        carries[i] = y;
    }
    for (u32 i=0; i<remaining.size(); ++i) {
        u32 y=i;
        for (unsigned j=0; j<b-first; ++j) {
            remaining[i] += y&1;
            y = 3*((y+1)/2);
        }
    }
}
u32 successor_y(u32 n) {
    const u32 y = 2*n, low = y & (carries.size()-1);
    const u32 high = (pow3*(y>>first)+carries[low]) & (remaining.size()-1);
    return y+C+weights[low]+remaining[high];
}
u32 step(u32 n) {
    return (successor_y(n)-2*n+1)/2;
}
struct Marks {
    std::vector<u64> words = std::vector<u64>(period/64);
    bool has(u32 x) const {return (words[x>>6]>>(x&63)) & 1;}
    void add(u32 x) {words[x>>6] |= u64(1) << (x&63);}
    void erase(u32 x) {words[x>>6] &= ~(u64(1) << (x&63));}
};
using Integer = mpz_class;
__extension__ typedef unsigned __int128 u128;
constexpr u64 power = 50031545098999707ULL, cut = 50032132174230649ULL;
constexpr u64 stride = u64(1) << (b+1);
constexpr u64 source = 50032132179190025ULL, copies = 1093, period_returns = 1606408;

u128 timed_return(u64 seed, u64& destination) {
    // Sum branch J on a geometric progression, then replay the proven bulks.
    const u128 p = power;
    u128 clock = (24*((p*p-1)/8) - 34*((p-1)/2)
                  + m*(23+5*(u128(2)*seed+1)) + 10*m*(m-1))/2;
    u64 a = 2*power-1, c = seed-power+2*m+1;
    for (unsigned i=0; i<b; ++i) {
        const u128 x=c;
        const u64 q=(c+1)/4;
        assert((c&1) && a>=4*q+3);
        clock += (c%4 == 1) ? (6*x*x+31*x+37)/2 : (3*x*x+29*x+65);
        a -= 4*q+3;
        c = 6*q+5;
    }
    assert(!(a&1) && a<=c);
    clock += 3*u128(a)*a+3*a+5*c+11;
    destination=a/2+c+2;
    return clock;
}

Integer timed_cycle(u64 start) {
    Integer total=0, value;
    u64 seed=start;
    for (u64 i=0; i<period_returns; ++i) {
        u64 next;
        const u128 dt=timed_return(seed,next);
        mpz_import(value.get_mpz_t(),1,1,sizeof(dt),0,0,&dt);
        total+=value;
        const u64 y=(seed-power+2*m+8)/2;
        const u32 n=((y+1)/2)&mask;
        const u64 predicted_y=2*((y+1)/2)+(successor_y(n)-2*n);
        assert(next == 2*predicted_y+power-2*m-8);
        seed=next;
    }
    assert(seed==start+stride);
    return total;
}

void timed_flight() {
    const Integer a=timed_cycle(source), b=timed_cycle(source+stride);
    const Integer c=timed_cycle(source+2*stride);
    const Integer d1=b-a, d2=c-2*b+a;
    const u64 last=copies-1;
    assert(timed_cycle(source+last*stride) == a+last*d1+last*(last-1)/2*d2);
    const Integer elapsed=copies*a+copies*(copies-1)/2*d1
                          +copies*(copies-1)*(copies-2)/6*d2;
    assert(elapsed == Integer("15968388026771997073986594690949338871473882"));
    u64 next;
    const u128 raw=timed_return(source,next);
    Integer initial;
    mpz_import(initial.get_mpz_t(),1,1,sizeof(raw),0,0,&raw);
    assert(next == 50032132179190191ULL && initial == Integer("9762379791435097453128986287146657"));
    std::cout << "cycle clock " << a << ", first difference " << d1
              << ", second difference " << d2 << "\n";
    std::cout << "flight from " << source << " to " << source+copies*stride
              << " costs " << elapsed << " raw transitions\n";
}

int main() {
    init();
    Marks visited, active;
    u64 cycles=0, count=0, max_tail=0, total_paths=0;
    for (u64 seed=cut; seed<=cut+100101; seed+=2) {
        const u64 y=(seed-power+2*m+8)/2;
        u32 start = ((y+1)/2) & mask, n=start;
        u64 path=0;
        while (!visited.has(n) && !active.has(n)) {
            active.add(n);
            n=(n+step(n))&mask;
            ++path;
        }
        if (active.has(n)) {
            u32 j=n; u64 length=0, drift=0;
            constexpr u64 safe_cut = cut+100101+194*25047+1;
            constexpr u64 seed_mask = (u64(1) << (b+1))-1;
            u64 earliest = safe_cut+seed_mask;
            do {
                u32 gain=step(j);
                // S(2j) recovers the actual successor y from the quotient.
                const u64 seed = 2*u64(successor_y(j))+power-2*m-8;
                const u64 arrival = safe_cut + ((seed-safe_cut)&seed_mask);
                if (arrival < earliest) earliest=arrival;
                j=(j+gain)&mask;
                drift+=gain;
                ++length;
            } while (j!=n);
            assert(length == 1606408 && drift == period);
            std::cout << "cycle length " << length << ", winding " << drift/period
                      << ", representative quotient residue " << n << "\n";
            std::cout << "first blank reset at or above " << safe_cut << " is " << earliest
                      << ", and after 1093 periods reaches " << earliest+1093*(seed_mask+1) << "\n";
            assert(earliest == source);
            ++cycles;
        }
        n=start;
        while (active.has(n)) {
            visited.add(n);
            active.erase(n);
            n=(n+step(n))&mask;
        }
        count+=path;
        if(path>max_tail) max_tail=path;
        total_paths+=path>0;
    }
    assert(cycles == 1 && count == 1631454);
    std::cout << "cycles " << cycles << ", quotient residues scanned " << count
              << ", maximum new path " << max_tail << ", nonempty paths "
              << total_paths << "\n";
    timed_flight();
}
