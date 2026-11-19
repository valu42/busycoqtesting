// Optional 128-bit endpoint comparator for the scale-10 universal replay.
// Compile beside the exact reference: c++ -O3 -std=c++17 outer_wall_fast_758.cpp -lgmpxx -lgmp -o outer_wall_fast_758
#define main gateway_reference_cli
#include "gateway_758.cpp"
#undef main

using Wide = __int128_t;
using Word = __uint128_t;

struct Signature {
    int jumps, length, bound;
    Word bits;
    std::string long_word;
    bool matches(const Signature& other) const {
        return jumps==other.jumps && length==other.length && bits==other.bits &&
               (length>=0 || long_word==other.long_word);
    }
};

class AngularCover {
    LocalMap exact;
    std::array<Distance,period> counter{};
    std::array<Wide,308> mass{};
    std::array<unsigned long,308> cutoff{};
    std::array<int,64> from_bits{};
    Distance slope, nodes=0, leaves=0;
    static constexpr Distance basin_near=543249654390404L;

    Signature reference(Distance d) const {
        Ending t=exact.probe(d);
        if(t.word.size()>127 || t.word.find('E')!=std::string::npos)
            return {t.jumps,-1,t.bound,0,t.word};
        Word bits=0;
        for(char move:t.word) bits=2*bits+(move=='J');
        return {t.jumps,int(t.word.size()),t.bound,bits,{}};
    }

    Signature signature(Distance d) const {
        Distance u=counter[d%period]+slope*(d/period);
        int k=from_bits[63-__builtin_clzl(u)];
        if(static_cast<unsigned long>(u)>cutoff[k]) --k;
        // The ratio at the top of a binary octave is <2, so it crosses
        // at most one factor-of-three threshold.
        require(k>=0,"invalid batch index");
        if(static_cast<unsigned long>(u)>=cutoff[k] || !mass[k]) return reference(d);
        Wide m=mass[k], a=Wide(13959275)*u, error=1;
        int bound=4*(293+k)+9*14;
        Word bits=0;
        for(int length=0;length<125;){
            if(error>=m) return reference(d);
            Wide first=3*a-m, margin=3*error+3;
            if(first < -margin){
                a*=3; error=3*error+1; bits=2*bits+1; bound+=4;
                ++length; continue;
            }
            if(first<=margin) return reference(d);
            Wide second=3*first-2*m, margin2=9*error+15;
            if(second < -margin2)
                return {k,length+1,(bound+9+5)/2,2*bits,{}};
            if(second<=margin2) return reference(d);
            a=second/4; error=(9*error+3)/4+3; bits*=4; bound+=18;
            length+=2;
        }
        return reference(d);
    }

    void visit(Distance lo,Distance hi,const Signature& l,const Signature& r){
        ++nodes;
        if(l.matches(r)){
            require(l.bound<=lo-basin_near,"return beyond scale-10 inner edge");
            ++leaves;
            return;
        }
        require(lo<hi,"inconsistent singleton");
        Distance mid=lo+2*((hi-lo)/4);
        Signature m=mid==lo?l:signature(mid);
        visit(lo,mid,l,m);
        m=mid+2==hi?r:signature(mid+2);
        visit(mid+2,hi,m,r);
    }

public:
    AngularCover(Distance lo,Distance hi):exact(lo,hi){
        require(905416090650670L<=lo && lo<=hi && hi<=1000000000000000L,
                "outside scale-10 extension");
        std::array<Big,308> power;
        power[0]=1;
        for(int k=1;k<=307;++k) power[k]=3*power[k-1];
        Big H=(power[307]-8282708212L)/13959275;
        auto prefix_counter=[&](Distance d){
            State s{2*power[292]-1,H-d-power[292]+585};
            int gain=4*292;
            for(int i=0;i<14;++i){
                if(i==8) jump(s,gain,false);
                bulk(s,gain,false);
            }
            Big u=s.a+1;
            require(mpz_fits_slong_p(u.get_mpz_t()),"counter overflow");
            return u.get_si();
        };
        for(int r=0;r<period;r+=2) counter[r]=prefix_counter(r);
        slope=prefix_counter(period)-counter[0];
        for(int r=0;r<period;r+=2){
            Big largest=Big(slope)*(hi/period)+counter[r];
            require(largest>0 && mpz_fits_slong_p(largest.get_mpz_t()),"positive LP64 counter");
        }
        for(int k=0;k<=307;++k){
            Big m=2*power[307-k],limit=2*H/power[k];
            cutoff[k]=mpz_fits_ulong_p(limit.get_mpz_t())?limit.get_ui():~0UL;
            if(mpz_sizeinbase(m.get_mpz_t(),2)>110 || power[k]<=2*Big(hi)+100000) continue;
            require(m*(2*Big(hi)+100100)<2*H,"normalized mass error");
            require(2*Big(8282708212L)*(Big(1)<<63)+m<2*H,"normalized initial error");
            unsigned long bottom=m.get_ui();
            Big top=m>>64;
            mass[k]=(Wide(top.get_ui())<<64)+bottom;
        }
        for(int e=0;e<64;++e){
            unsigned long low=1UL<<e;
            int k=0;
            while(k+1<=307 && cutoff[k+1]>=low) ++k;
            from_bits[e]=k;
        }
        Distance left=lo+lo%2,right=hi-hi%2;
        require(left<=right && lo-615>=basin_near,"unsupported band");
        visit(left,right,signature(left),signature(right));
        std::cout<<lo<<' '<<hi<<' '<<nodes<<' '<<leaves<<'\n';
    }
};

int main(int argc,char** argv){
    if(argc!=4 || std::string(argv[1])!="--universal") return 2;
    try{
        Distance hi=std::stoll(argv[2]),lo=std::stoll(argv[3]);
        AngularCover verify(lo,hi);
    }catch(const std::exception& e){
        std::cerr<<e.what()<<'\n'; return 1;
    }
}
