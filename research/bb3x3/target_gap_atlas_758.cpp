// Sparse merge of reset-header residues with the shared exact dyadic atlas.
// c++ -O3 -std=c++17 -fopenmp target_gap_atlas_758.cpp -lgmpxx -lgmp -o target_gap_atlas
// ./target_gap_atlas --self-test
// ./target_gap_atlas --sample r p count groups directory-bits
// ./target_gap_atlas r p threads [first stop [groups directory-bits]]
// Every output row certifies a disjoint half-open interval of header indices.
// Defaults use all headers, twelve atlas groups and a 20-bit leaf directory.
#define main wider_even_worker_main
#include "wider_even_lattice_758.cpp"
#undef main

constexpr UInt RESIDUE_PERIOD=2*D;
std::vector<unsigned> reset_residues;
std::vector<unsigned> reset_index(RESIDUE_PERIOD/128+2);

struct TailFilter {
    const unsigned bits,size;
    unsigned depth=0;
    std::vector<UInt> marked;
    explicit TailFilter(unsigned bits):bits(bits),size(1u<<bits),marked((size+64)/64) {
        assert(bits<=24);
        build(0,1,0);
    }
    void build(Wide a,UInt four,unsigned used) {
        const UInt low=a*size/pow3[used],high=(a+four)*size/pow3[used];
        if(high<=low+1) {
            marked[low/64]|=UInt(1)<<(low%64);
            marked[high/64]|=UInt(1)<<(high%64);
            depth=std::max(depth,used);
            return;
        }
        build(3*a,four,used+1);
        build(9*a+5*four,4*four,used+2);
    }
    bool may_survive(Wide numerator,unsigned denominator_bits) const {
        const UInt bin=denominator_bits>=bits ? numerator>>(denominator_bits-bits)
                                             : numerator<<(bits-denominator_bits);
        assert(bin<size);
        return marked[bin/64]&(UInt(1)<<(bin%64));
    }
};

void make_reset_residues() {
    mpz_class power,target;
    mpz_ui_pow_ui(power.get_mpz_t(),3,292);
    mpz_ui_pow_ui(target.get_mpz_t(),3,307);
    target=(target-8282708212L)/D;
    for(unsigned offset=0;offset<32768;offset+=2) {
        mpz_class a=2*power-1,c=target-offset+585-power;
        for(unsigned k=0;k<14;++k) {
            if(k==8) { c-=a-1; a=3*a+2; }
            const mpz_class q=(c+1)/4;
            a-=4*q+3; c=6*q+5;
        }
        const mpz_class h=(a+1)/2;
        reset_residues.push_back(mpz_fdiv_ui(h.get_mpz_t(),RESIDUE_PERIOD));
    }
    std::sort(reset_residues.begin(),reset_residues.end());
    reset_residues.erase(std::unique(reset_residues.begin(),reset_residues.end()),reset_residues.end());
    assert(reset_residues.size()==8192);
    for(unsigned x:reset_residues) assert(x%2==0);
    for(size_t i=0;i<reset_index.size();++i)
        reset_index[i]=std::lower_bound(reset_residues.begin(),reset_residues.end(),128*i)-reset_residues.begin();
}

struct ResetCursor {
    const UInt step,modulus,residue;
    UInt block,n;
    unsigned index;
    ResetCursor(const Header& h):step(D*(h.m==h.r?1:3)),
        modulus(RESIDUE_PERIOD*step),residue(h.a%modulus) { jump(1); }
    void jump(UInt low) {
        const UInt z=low+residue;
        const UInt lower=(z%modulus+step-1)/step;
        block=z/modulus;
        index=reset_index[lower/128];
        while(index<reset_residues.size() && reset_residues[index]<lower) ++index;
        if(index==reset_residues.size()) { index=0; ++block; }
        n=block*modulus+step*reset_residues[index]-residue;
        assert(n>=low);
    }
    void advance() {
        ++index;
        if(index==reset_residues.size()) { index=0; ++block; }
        n=block*modulus+step*reset_residues[index]-residue;
    }
};

struct LeafDirectory {
    const std::vector<Leaf>& leaves;
    unsigned shift,max_depth=0;
    std::vector<unsigned> first;
    LeafDirectory(const std::vector<Leaf>& input,unsigned p,unsigned bits):
        leaves(input),shift(2*p-bits),first((size_t(1)<<bits)+1) {
        for(const auto& leaf:leaves) max_depth=std::max(max_depth,leaf.depth);
        unsigned index=0;
        for(size_t b=0;b<first.size();++b) {
            const UInt low=UInt(b)<<shift;
            while(index<leaves.size() && leaves[index].high<low) ++index;
            first[b]=index;
        }
    }
    unsigned lookup(UInt n) const {
        unsigned i=first[n>>shift];
        while(i<leaves.size() && leaves[i].high<n) ++i;
        return i;
    }
};

struct ResetResult {
    Counts count;
    UInt probes=0,images=0;
    void add(const ResetResult& other) {
        count.tests+=other.count.tests; count.exact+=other.count.exact;
        count.survivors+=other.count.survivors;
        probes+=other.probes; images+=other.images;
    }
};

ResetResult sparse_check(const Header& h,const LeafDirectory& directory,
                         const TailFilter& filter,std::vector<UInt>* survivors=nullptr) {
    assert(h.m+directory.max_depth+filter.depth<=last_guard);
    ResetResult result;
    Counts& count=result.count;
    const UInt q=UInt(1)<<(2*h.p);
    ResetCursor cursor(h);
    while(cursor.n<q) {
        ++result.probes;
        const unsigned index=directory.lookup(cursor.n);
        if(index==directory.leaves.size()) break;
        const Leaf& leaf=directory.leaves[index];
        if(cursor.n<leaf.low) { cursor.jump(leaf.low); continue; }
        for(;cursor.n<=leaf.high;cursor.advance()) {
            const UInt n=cursor.n;
            ++count.tests;
            const Wide numerator=leaf.at_low+pow3[leaf.depth]*(n-leaf.low);
            if(!filter.may_survive(numerator,leaf.bits)) continue;
            ++result.images;
            if(!image_hole(n,h.p,h.m,h.m+leaf.depth,numerator,leaf.bits,count)) {
                ++count.survivors;
                if(survivors) survivors->push_back(n);
                else {
                    mpz_class a;
                    mpz_import(a.get_mpz_t(),1,1,sizeof(h.a),0,0,&h.a);
#pragma omp critical
                    gmp_printf("surviving r=%u m=%u p=%u N=%lu A=%Zd\n",h.r,h.m,h.p,n,a.get_mpz_t());
                }
            }
        }
    }
    return result;
}

std::vector<Header> reset_headers(unsigned r,unsigned p) {
    std::vector<Header> all,headers;
    headers_rec(all,5,2,1,4,r,p);
    for(const auto& h:all) if(h.p==p) headers.push_back(h);
    return headers;
}

UInt reference_next(const Header& h,UInt low) {
    const UInt step=D*(h.m==h.r?1:3),modulus=RESIDUE_PERIOD*step;
    const UInt residue=h.a%modulus;
    UInt next=~UInt(0);
    for(UInt r:reset_residues) {
        UInt n=(step*r+modulus-residue)%modulus;
        if(n<low) n+=((low-n+modulus-1)/modulus)*modulus;
        next=std::min(next,n);
    }
    return next;
}

void sparse_self_test() {
    UInt checked=0,remaining=0,queries=0;
    const TailFilter filter(8);
    for(unsigned p=18;p<=20;++p) {
        const unsigned r=2*p+3;
        const auto headers=reset_headers(r,p);
        const auto leaves=atlas(p,4);
        const LeafDirectory directory(leaves,p,12);
        last_guard=r+1+8+filter.depth;
        for(unsigned sample=0;sample<128;++sample) {
            const Header& h=headers[sample*headers.size()/128];
            const UInt q=UInt(1)<<(2*p),step=D*(h.m==h.r?1:3);
            const UInt modulus=RESIDUE_PERIOD*step,residue=h.a%modulus;
            std::vector<UInt> actual,expected;
            const ResetResult result=sparse_check(h,directory,filter,&actual);
            for(UInt x:reset_residues) {
                UInt n=(step*x+modulus-residue)%modulus;
                if(!n) n+=modulus;
                for(;n<q;n+=modulus) {
                    ++checked;
                    if(!direct_hole(n,p,h.m)) expected.push_back(n);
                }
            }
            std::sort(expected.begin(),expected.end());
            assert(actual==expected && result.count.survivors==expected.size());
            remaining+=expected.size();
            ResetCursor cursor(h);
            for(UInt low:{UInt(1),q/3,q-1,q+modulus-1}) {
                cursor.jump(low);
                assert(cursor.n==reference_next(h,low));
                const UInt previous=cursor.n;
                cursor.advance();
                assert(cursor.n==reference_next(h,previous+1));
                queries+=2;
            }
        }
    }
    assert(remaining>0);
    last_guard=filter.depth;
    UInt filtered=0;
    for(unsigned p=5;p<=8;++p) for(UInt n=5;n<(UInt(1)<<(2*p));n+=10)
        if(!filter.may_survive(n,2*p)) {
            assert(direct_hole(n,p,0));
            ++filtered;
        }
    std::printf("Checked %lu exact header-supported directions, including %lu budget survivors; %lu independent cursor queries; %lu filtered small-grid directions.\n",checked,remaining,queries,filtered);
}

int main(int argc,char** argv) {
    pow3[0]=1;
    for(size_t i=1;i<pow3.size();++i) pow3[i]=3*pow3[i-1];
    make_reset_residues();
    if(argc==2 && std::strcmp(argv[1],"--self-test")==0) { sparse_self_test(); return 0; }
    const bool sample=argc>1 && std::strcmp(argv[1],"--sample")==0;
    if((sample && argc!=7) || (!sample && argc!=4 && argc!=6 && argc!=8)) return 2;
    const unsigned r=std::atoi(argv[1+sample]),p=std::atoi(argv[2+sample]);
    const unsigned threads=sample?1:std::atoi(argv[3]);
    const UInt sample_size=sample?std::strtoull(argv[4],nullptr,10):0;
    unsigned groups=12,bits=20;
    UInt first=0,stop=~UInt(0);
    if(sample) { groups=std::atoi(argv[5]); bits=std::atoi(argv[6]); }
    else {
        if(argc>=6) { first=std::strtoull(argv[4],nullptr,10); stop=std::strtoull(argv[5],nullptr,10); }
        if(argc==8) { groups=std::atoi(argv[6]); bits=std::atoi(argv[7]); }
    }
    if(r<57 || r>63 || p<29 || p>30 || groups<8 || groups>21 || bits<16 || bits>26 || threads<1 || threads>9) return 2;
    const auto start=std::chrono::steady_clock::now();
    const TailFilter filter(20);
    assert(r+1+2*groups+filter.depth<=last_guard);
    const auto leaves=atlas(p,groups);
    const LeafDirectory directory(leaves,p,bits);
    const auto headers=reset_headers(r,p);
    stop=std::min(stop,UInt(headers.size()));
    if((sample && (sample_size==0 || sample_size>headers.size())) || (!sample && first>=stop)) return 2;
    std::fprintf(stderr,"r=%u p=%u: %zu headers, %zu atlas leaves, filter depth %u, %u threads\n",r,p,headers.size(),leaves.size(),filter.depth,threads);
    if(sample) {
        ResetResult total;
        for(UInt i=0;i<sample_size;++i) total.add(sparse_check(headers[i*headers.size()/sample_size],directory,filter));
        const double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
        std::printf("Stratified sample: %lu/%zu headers, %lu probes, %lu atlas tests, %lu image tests, %lu exact fallbacks, %lu survivors, %.3f s\n",sample_size,headers.size(),total.probes,total.count.tests,total.images,total.count.exact,total.count.survivors,seconds);
        return total.count.survivors?1:0;
    }
    std::puts("r\tp\tlast_guard\tgroups\tdirectory_bits\tfilter_bits\tfirst\tstop\tcells\tprobes\tatlas_tests\timage_tests\texact_fallbacks\tsurvivors");
    UInt done=0,survivors=0;
    constexpr UInt CHUNK=4096;
    const UInt chunks=(stop-first+CHUNK-1)/CHUNK;
#pragma omp parallel for schedule(dynamic,1) num_threads(threads)
    for(UInt chunk=0;chunk<chunks;++chunk) {
        const UInt left=first+CHUNK*chunk,right=std::min(stop,left+CHUNK);
        ResetResult total;
        for(UInt i=left;i<right;++i) total.add(sparse_check(headers[i],directory,filter));
#pragma omp critical
        {
            done+=right-left; survivors+=total.count.survivors;
            std::printf("%u\t%u\t%u\t%u\t%u\t%u\t%lu\t%lu\t%lu\t%lu\t%lu\t%lu\t%lu\t%lu\n",r,p,last_guard,groups,bits,filter.bits,left,right,right-left,total.probes,total.count.tests,total.images,total.count.exact,total.count.survivors);
            std::fflush(stdout);
            const double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
            std::fprintf(stderr,"Completed %lu/%lu headers in %.3f s\n",done,stop-first,seconds);
        }
    }
    const double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
    std::fprintf(stderr,"Completed [%lu,%lu) in %.3f s; %lu budget survivors\n",first,stop,seconds,survivors);
    return survivors?1:0;
}
