// Complete high-pair part of the dyadic header survey. Uses C++17 and GMP.
// c++ -O3 -std=c++17 high_pair_headers_758.cpp -lgmpxx -lgmp -o high_pair_headers
// ./high_pair_headers [first-r last-r minimum-p [last-guard]] (defaults: 45 53 23 257)
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <stdexcept>
#include <vector>
#include <gmpxx.h>

using UInt = std::uint64_t;
using Wide = unsigned __int128;
constexpr UInt divisor = 13959275;
constexpr UInt period = 2*divisor;
constexpr unsigned bin_bits = 22, bin_count = 1u << bin_bits;
unsigned limit = 257;

std::array<Wide,80> powers;
std::vector<int> residues;
std::vector<unsigned> next_bin(bin_count+1);
std::vector<unsigned> residue_index(period/128 + 2);
struct Counts { UInt cells=0, probes=0, tests=0, exact=0, survivors=0; };
std::array<Counts,33> counts;
unsigned cutoff, minimum_pairs;

void make_residues() {
    mpz_class p, target;
    mpz_ui_pow_ui(p.get_mpz_t(), 3, 292);
    mpz_ui_pow_ui(target.get_mpz_t(), 3, 307);
    target=(target-8282708212L)/divisor;
    for (int offset=0; offset<32768; offset+=2) {
        mpz_class a=2*p-1, c=target-offset+585-p;
        for (int k=0; k<14; ++k) {
            if (k==8) { c-=a-1; a=3*a+2; }
            mpz_class q=(c+1)/4;
            a-=4*q+3; c=6*q+5;
        }
        const mpz_class h=(a+1)/2;
        residues.push_back(mpz_fdiv_ui(h.get_mpz_t(),period));
    }
    std::sort(residues.begin(),residues.end());
    residues.erase(std::unique(residues.begin(),residues.end()),residues.end());
    if (residues.size()!=8192 || std::any_of(residues.begin(),residues.end(),
            [](int value) { return value%2!=0; }))
        throw std::logic_error("wrong header residues");
    for (size_t i=0; i<residue_index.size(); ++i)
        residue_index[i]=std::lower_bound(residues.begin(),residues.end(),128*i)-residues.begin();
}

// A surviving tail must lie in an inverse cylinder [A,A+4^p]/3^m.
// Mark a superset of possible cells on the 2^22 grid, including endpoints.
void mark_bins(Wide a, UInt four, unsigned m) {
    UInt lo=a*bin_count/powers[m], hi=(a+four)*bin_count/powers[m];
    if (hi<=lo+1) { next_bin[lo]=1; next_bin[hi]=1; return; }
    mark_bins(3*a,four,m+1);
    mark_bins(9*a+5*four,4*four,m+2);
}

// All uint64_t inputs through p=31 follow the original arithmetic. At p=32
// the numerator and the right endpoint 4^32 require an extra bit.
template<class Number>
bool escapes(Number n,unsigned pairs,unsigned depth) {
    // Lower and upper endpoints, in units of 2^-60, always enclose the orbit.
    constexpr UInt unit=UInt(1)<<60;
    UInt lo, hi;
    if (pairs == 32) {
        lo = n/16;
        hi = (n+15)/16;
    } else if (pairs == 31) {
        // A numerator on the 2^-62 grid can lie between two working-grid points.
        lo = n/4;
        hi = (n+3)/4;
    } else {
        lo = hi = n<<(60-2*pairs);
    }
    for (unsigned m=depth; m<=limit;) {
        if (3*hi<unit) { lo*=3; hi*=3; ++m; }
        else if (9*lo>5*unit) {
            lo=(9*lo-5*unit)/4; hi=(9*hi-5*unit+3)/4; m+=2;
        } else if (3*lo>unit && 9*hi<5*unit) return true;
        else break;
    }
    ++counts[pairs].exact;
    mpz_class a, b=mpz_class(1)<<(2*pairs);
    mpz_import(a.get_mpz_t(),1,1,sizeof(n),0,0,&n);
    for (unsigned m=depth; m<=limit;) {
        if (3*a<b) { a*=3; ++m; }
        else if (9*a>5*b) { a=9*a-5*b; b*=4; m+=2; }
        else if (3*a>b && 9*a<5*b) return true;
        else break;
    }
    return false;
}

template<unsigned scale, class Number>
void check_cell(Wide a, unsigned pairs) {
    ++counts[pairs].cells;
    constexpr UInt step=divisor*scale, modulus=period*step;
    const UInt residue=a%modulus;
    const Number four=Number(1)<<(2*pairs);
    Number n=0;
    while (n<=four) {
        // N+A = scale*D*h0. Find the next supported header residue.
        const Number z=residue+n;
        const UInt h=(z%modulus+step-1)/step;
        Number block=z/modulus;
        unsigned i=residue_index[h/128];
        while (i<residues.size() && UInt(residues[i])<h) ++i;
        if (i==residues.size()) { i=0; ++block; }
        n=block*modulus+residues[i]*step-residue;
        if (n>four) break;
        ++counts[pairs].probes;
        unsigned bin=n>>(2*pairs-bin_bits);
        if (next_bin[bin]!=bin) {
            if (next_bin[bin]>bin_count) break;
            n=Number(next_bin[bin])<<(2*pairs-bin_bits);
            continue;
        }
        ++counts[pairs].tests;
        if (!escapes(n,pairs,cutoff+(scale==3))) {
            ++counts[pairs].survivors;
            mpz_class origin, numerator;
            mpz_import(numerator.get_mpz_t(),1,1,sizeof(n),0,0,&n);
            mpz_import(origin.get_mpz_t(),1,1,sizeof(a),0,0,&a);
            gmp_printf("surviving r=%u p=%u N=%Zd scale=%u A=%Zd\n",
                       cutoff,pairs,numerator.get_mpz_t(),scale,origin.get_mpz_t());
        }
        ++n;
    }
}

void prefixes(Wide a,unsigned m,unsigned p,Wide four) {
    if (p+(cutoff+1-m)/2<minimum_pairs) return;
    if (m>=cutoff) {
        if (p>=minimum_pairs) {
            if (p==32) {
                if (m==cutoff) check_cell<1,Wide>(a,p);
                else check_cell<3,Wide>(a,p);
            } else {
                if (m==cutoff) check_cell<1,UInt>(a,p);
                else check_cell<3,UInt>(a,p);
            }
        }
        return;
    }
    prefixes(3*a,m+1,p,four);
    prefixes(9*a+5*four,m+2,p+1,4*four);
}

int main(int argc,char **argv) {
    unsigned first=45,last=53;
    minimum_pairs=23;
    unsigned forced_jumps=0;
    if (argc==4 || argc==5 || argc==6) {
        first=std::atoi(argv[1]); last=std::atoi(argv[2]); minimum_pairs=std::atoi(argv[3]);
        if (argc>=5) limit=std::atoi(argv[4]);
        if (argc==6) forced_jumps=std::atoi(argv[5]);
    } else if (argc!=1) return 2;
    if (forced_jumps+2>first || first<2 || first>last || last>63 || limit<last+42 || limit>1000 || minimum_pairs<12 || minimum_pairs>32) return 2;
    powers[0]=1;
    for (size_t i=1; i<powers.size(); ++i) powers[i]=3*powers[i-1];
    make_residues();
    mark_bins(0,1,0);
    unsigned next=bin_count+1;
    for (int i=bin_count; i>=0; --i) {
        if (next_bin[i]) next=i;
        next_bin[i]=next;
    }
    std::puts("r\tp\tlast_guard\tcells\tprobes\tangular_tests\texact_fallbacks\tsurvivors");
    bool ok=true;
    for (cutoff=first; cutoff<=last; ++cutoff) {
        counts.fill({});
        prefixes(5*powers[forced_jumps],2+forced_jumps,1,4); // P followed by any requested forced jumps.
        for (unsigned p=minimum_pairs; p<counts.size(); ++p) {
            const Counts &c=counts[p];
            if (!c.cells) continue;
            std::printf("%u\t%u\t%u\t%lu\t%lu\t%lu\t%lu\t%lu\n",cutoff,p,limit,c.cells,c.probes,c.tests,c.exact,c.survivors);
            ok &= c.survivors==0;
        }
        std::fflush(stdout);
    }
    return ok?0:1;
}
