// Exact shared-cylinder exhaustion for the remaining even-coordinate headers.
// c++ -O3 -std=c++17 -fopenmp wider_even_lattice_758.cpp -lgmpxx -lgmp -o wider_even
// ./wider_even [first-r last-r [prefix-groups [threads [last-guard]]]]
// Defaults: 58 59 21 3 248. To extend: ./wider_even 60 60 21 3 249
// ./wider_even --self-test
#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <stdexcept>
#include <vector>
#include <gmpxx.h>
#ifdef _OPENMP
#include <omp.h>
#endif

using UInt=std::uint64_t;
using Wide=unsigned __int128;
constexpr UInt D=13959275, UNIT=UInt(1)<<60;
std::array<Wide,80> pow3;
unsigned last_guard=248;

struct Leaf { Wide at_low; UInt low,high; unsigned depth,bits; };
struct Header { Wide a; unsigned r,m,p; };
struct Counts { UInt eligible=0,tests=0,exact=0,survivors=0; };

void atlas_rec(std::vector<Leaf>& out,Wide a,UInt four,unsigned depth,
               unsigned pairs,unsigned blocks,unsigned target,unsigned p) {
    if(blocks==target) {
        const Wide q=Wide(1)<<(2*p), den=pow3[depth];
        const UInt low=UInt(a*q/den)+1;
        const UInt high=UInt(((a+four)*q-1)/den);
        if(low<=high) out.push_back({den*low-a*q,low,high,depth,2*(p+pairs)});
        return;
    }
    atlas_rec(out,3*a,four,depth+1,pairs,blocks+1,target,p);
    atlas_rec(out,9*a+5*four,4*four,depth+2,pairs+1,blocks+1,target,p);
}

std::vector<Leaf> atlas(unsigned p,unsigned groups) {
    if(p>30 || groups>21) throw std::logic_error("128-bit atlas bound exceeded");
    std::vector<Leaf> out;
    out.reserve(size_t(1)<<groups);
    atlas_rec(out,0,1,0,0,0,groups,p);
    UInt previous=0;
    for(const auto& leaf:out) {
        assert(leaf.low>previous && leaf.high<(UInt(1)<<(2*p)));
        assert(leaf.bits<=102 && leaf.depth<=42);
        previous=leaf.high;
    }
    return out;
}

bool direct_hole(UInt n,unsigned p,unsigned depth) {
    mpz_class a=n,b=mpz_class(1)<<(2*p);
    for(;depth<=last_guard;) {
        if(3*a>b && 9*a<5*b) return true;
        if(3*a<b) { a*=3; ++depth; }
        else if(9*a>5*b) { a=9*a-5*b; b*=4; depth+=2; }
        else return false;
    }
    return false;
}

bool image_hole(UInt original,unsigned p,unsigned cut,unsigned depth,
                Wide numerator,unsigned bits,Counts& count) {
    UInt lo,hi;
    if(bits>60) {
        const unsigned shift=bits-60;
        lo=UInt(numerator>>shift);
        hi=UInt((numerator+((Wide(1)<<shift)-1))>>shift);
    } else lo=hi=UInt(numerator<<(60-bits));
    for(;depth<=last_guard;) {
        if(3*hi<UNIT) { lo*=3; hi*=3; ++depth; }
        else if(9*lo>5*UNIT) {
            lo=(9*lo-5*UNIT)/4; hi=(9*hi-5*UNIT+3)/4; depth+=2;
        } else if(3*lo>UNIT && 9*hi<5*UNIT) return true;
        else break;
    }
    ++count.exact;
    return direct_hole(original,p,cut);
}

Counts check(const Header& h,const std::vector<Leaf>& leaves,
             UInt custom_step=0,std::vector<unsigned char>* answers=nullptr) {
    Counts count;
    const UInt scale=h.m==h.r?1:3,step=custom_step?custom_step:2*D*scale;
    const UInt residue=UInt(h.a%step),q=UInt(1)<<(2*h.p);
    const UInt first=(step-residue)%step;
    assert(first>0 && first<q && first%10==5 && step%10==0);
    count.eligible=(q-1-first)/step+1;
    if(answers) answers->assign(count.eligible,1);
    for(const auto& leaf:leaves) {
        UInt n=leaf.low+(step-(leaf.low+residue)%step)%step;
        if(n>leaf.high) continue;
        Wide numerator=leaf.at_low+pow3[leaf.depth]*(n-leaf.low);
        const Wide increment=pow3[leaf.depth]*step;
        for(;n<=leaf.high;n+=step,numerator+=increment) {
            ++count.tests;
            const bool returned=image_hole(n,h.p,h.m,h.m+leaf.depth,
                                           numerator,leaf.bits,count);
            if(answers) (*answers)[(n-first)/step]=returned;
            if(!returned) {
                ++count.survivors;
                if(!answers) {
                    mpz_class a;
                    mpz_import(a.get_mpz_t(),1,1,sizeof(h.a),0,0,&h.a);
#pragma omp critical
                    gmp_printf("surviving r=%u m=%u p=%u N=%lu A=%Zd\n",h.r,h.m,h.p,n,a.get_mpz_t());
                }
            }
        }
    }
    assert(count.tests<=count.eligible);
    return count;
}

void headers_rec(std::vector<Header>& out,Wide a,unsigned m,unsigned p,
                 Wide four,unsigned r,unsigned minimum) {
    if(p+(r+1-m)/2<minimum) return;
    if(m>=r) { if(p>=minimum) out.push_back({a,r,m,p}); return; }
    headers_rec(out,3*a,m+1,p,four,r,minimum);
    headers_rec(out,9*a+5*four,m+2,p+1,4*four,r,minimum);
}

void self_test() {
    last_guard=40;
    UInt points=0,remaining=0;
    for(unsigned p=8;p<=10;++p) {
        const auto leaves=atlas(p,7);
        const Header h{5,10,10,p};
        std::vector<unsigned char> answers;
        const Counts counts=check(h,leaves,10,&answers);
        for(size_t i=0;i<answers.size();++i) {
            const bool actual=direct_hole(5+10*i,p,10);
            assert(bool(answers[i])==actual);
            remaining+=!actual;
        }
        points+=answers.size();
        assert(counts.survivors<=counts.tests);
    }
    assert(remaining>0);
    std::printf("Compared atlas exhaustion with %lu exact rational trajectories; %lu correctly survive the shortened budget.\n",points,remaining);
}

int main(int argc,char** argv) {
    pow3[0]=1;
    for(size_t i=1;i<pow3.size();++i) pow3[i]=3*pow3[i-1];
    if(argc==2 && std::strcmp(argv[1],"--self-test")==0) { self_test(); return 0; }
    unsigned first=58,last=59,groups=21,threads=3;
    if(argc>=3 && argc<=6) {
        first=std::atoi(argv[1]); last=std::atoi(argv[2]);
        if(argc>=4) groups=std::atoi(argv[3]);
        if(argc>=5) threads=std::atoi(argv[4]);
        if(argc==6) last_guard=std::atoi(argv[5]);
    } else if(argc!=1) return 2;
    if(first<57 || first>last || last>60 || groups<4 || groups>21 || threads<1 || threads>3 || last_guard<last+42 || last_guard>1000) return 2;
    const auto start=std::chrono::steady_clock::now();
    std::vector<Header> headers;
    for(unsigned r=first;r<=last;++r) headers_rec(headers,5,2,1,4,r,29);
    std::vector<Counts> results(headers.size());
    for(unsigned p=29;p<=30;++p) {
        std::vector<size_t> indices;
        for(size_t i=0;i<headers.size();++i) if(headers[i].p==p) indices.push_back(i);
        if(indices.empty()) continue;
        const auto leaves=atlas(p,groups);
        std::fprintf(stderr,"p=%u: %zu exact atlas cylinders, %zu headers, %u threads\n",p,leaves.size(),indices.size(),threads);
        UInt finished=0;
#pragma omp parallel for schedule(dynamic,1) num_threads(threads)
        for(size_t j=0;j<indices.size();++j) {
            const size_t i=indices[j];
            results[i]=check(headers[i],leaves);
#pragma omp critical
            {
                ++finished;
                const UInt progress_interval=indices.size()<100?10:100;
                if(finished%progress_interval==0 || finished==indices.size()) {
                    const double elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
                    std::fprintf(stderr,"p=%u completed %lu/%zu headers in %.3f s\n",p,finished,indices.size(),elapsed);
                }
            }
        }
    }
    std::puts("r\tp\tlast_guard\tcells\teligible\tatlas_tests\texact_fallbacks\tsurvivors");
    bool ok=true;
    for(unsigned r=first;r<=last;++r) for(unsigned p=29;p<=30;++p) {
        Counts total;
        UInt cells=0;
        for(size_t i=0;i<headers.size();++i) if(headers[i].r==r && headers[i].p==p) {
            ++cells;
            total.eligible+=results[i].eligible; total.tests+=results[i].tests;
            total.exact+=results[i].exact; total.survivors+=results[i].survivors;
        }
        if(!cells) continue;
        std::printf("%u\t%u\t%u\t%lu\t%lu\t%lu\t%lu\t%lu\n",r,p,last_guard,cells,total.eligible,total.tests,total.exact,total.survivors);
        ok &= total.survivors==0;
    }
    const double elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
    std::fprintf(stderr,"Completed in %.3f s\n",elapsed);
    return ok?0:1;
}
