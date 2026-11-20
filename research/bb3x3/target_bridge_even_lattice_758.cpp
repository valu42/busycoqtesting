// Exact high-pair lattice check for arbitrary even left coordinates.
// Build: c++ -O3 -std=c++17 target_bridge_even_lattice_758.cpp -lgmpxx -lgmp -o even_lattice
// Run: ./even_lattice [first-r last-r] (defaults 57 57).
// Reuse the archived inverse-cylinder and outward-rounding primitives.
#define main archived_header_main
#include "high_pair_headers_758.cpp"
#undef main
#include <cassert>
#include <cstring>

bool direct_hole(UInt n,unsigned p,unsigned last) {
    mpz_class a=n,b=mpz_class(1)<<(2*p);
    for(unsigned depth=0;depth<=last;) {
        if(3*a>b && 9*a<5*b) return true;
        if(3*a<b) { a*=3; ++depth; }
        else if(9*a>5*b) { a=9*a-5*b; b*=4; depth+=2; }
        else return false;
    }
    return false;
}

void verify_lattice_skip() {
    UInt checked=0;
    for(unsigned pairs=12;pairs<=14;++pairs) {
        const UInt four=UInt(1)<<(2*pairs),step=10000;
        for(UInt residue : {UInt(1235),UInt(5675),UInt(9995)}) {
            const UInt first=(step-residue)%step;
            std::vector<UInt> brute,fast;
            for(UInt n=first;n<four;n+=step) {
                const unsigned bin=n>>(2*pairs-bin_bits);
                const bool escaped=direct_hole(n,pairs,40);
                if(next_bin[bin]==bin) brute.push_back(n);
                else assert(escaped);
                ++checked;
            }
            UInt n=first;
            while(n<four) {
                const unsigned bin=n>>(2*pairs-bin_bits);
                if(next_bin[bin]!=bin) {
                    if(next_bin[bin]>bin_count) break;
                    const UInt lower=UInt(next_bin[bin])<<(2*pairs-bin_bits);
                    n=lower+(step-((lower+residue)%step))%step;
                } else { fast.push_back(n); n+=step; }
            }
            assert(fast==brute);
        }
    }
    std::printf("Compared lattice skipping with %lu direct rational checks.\n",checked);
}

// N+A=3^(m-r)*D*h0 with h0 ANY even integer. The resulting
// lattice contains every physically possible header at that exponent.
template<unsigned scale>
void even_cell(Wide a,unsigned pairs) {
    ++counts[pairs].cells;
    constexpr UInt step=2*divisor*scale;
    const UInt residue=a%step;
    const UInt four=UInt(1)<<(2*pairs);
    UInt n=(step-residue)%step;
    while(n<=four) {
        ++counts[pairs].probes;
        const unsigned bin=n>>(2*pairs-bin_bits);
        if(next_bin[bin]!=bin) {
            if(next_bin[bin]>bin_count) break;
            const UInt lower=UInt(next_bin[bin])<<(2*pairs-bin_bits);
            n=lower+(step-((lower+residue)%step))%step;
            continue;
        }
        ++counts[pairs].tests;
        if(!escapes(n,pairs,cutoff+(scale==3))) {
            ++counts[pairs].survivors;
            mpz_class origin;
            mpz_import(origin.get_mpz_t(),1,1,sizeof(a),0,0,&a);
            gmp_printf("surviving r=%u p=%u N=%lu scale=%u A=%Zd\n",cutoff,pairs,n,scale,origin.get_mpz_t());
        }
        n+=step;
    }
}

void even_prefixes(Wide a,unsigned m,unsigned p,Wide four) {
    if(p+(cutoff+1-m)/2<minimum_pairs) return;
    if(m>=cutoff) {
        if(p>=minimum_pairs) {
            if(m==cutoff) even_cell<1>(a,p);
            else even_cell<3>(a,p);
        }
        return;
    }
    even_prefixes(3*a,m+1,p,four);
    even_prefixes(9*a+5*four,m+2,p+1,4*four);
}

int main(int argc,char **argv) {
    unsigned first=57,last=57;
    const bool self_test=argc==2 && std::strcmp(argv[1],"--self-test")==0;
    if(argc==3) { first=std::atoi(argv[1]); last=std::atoi(argv[2]); }
    else if(self_test) {}
    else if(argc!=1) return 2;
    if(first<57 || first>last || last>58) return 2;
    minimum_pairs=29;
    limit=248;
    powers[0]=1;
    for(size_t i=1;i<powers.size();++i) powers[i]=3*powers[i-1];
    mark_bins(0,1,0);
    unsigned next=bin_count+1;
    for(int i=bin_count;i>=0;--i) {
        if(next_bin[i]) next=i;
        next_bin[i]=next;
    }
    if(self_test) { verify_lattice_skip(); return 0; }
    std::puts("r\tp\tlast_guard\tcells\tprobes\tangular_tests\texact_fallbacks\tsurvivors");
    bool ok=true;
    for(cutoff=first;cutoff<=last;++cutoff) {
        counts.fill({});
        even_prefixes(5,2,1,4);
        for(unsigned p=minimum_pairs;p<counts.size();++p) {
            const Counts &c=counts[p];
            if(!c.cells) continue;
            std::printf("%u\t%u\t%u\t%lu\t%lu\t%lu\t%lu\t%lu\n",cutoff,p,limit,c.cells,c.probes,c.tests,c.exact,c.survivors);
            ok &= c.survivors==0;
        }
        std::fflush(stdout);
    }
    return ok?0:1;
}
