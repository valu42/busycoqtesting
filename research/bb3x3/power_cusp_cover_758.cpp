// Verify all odd reset seeds P+d in an inclusive interval of even offsets d.
// c++ -O3 -std=c++17 power_cusp_cover_758.cpp -lgmpxx -lgmp -o power_cusp_cover
#include <algorithm>
#include <cstdint>
#include <gmpxx.h>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>

using Big = mpz_class;
using Offset = std::uint64_t;
constexpr unsigned bits = 18;
constexpr unsigned mask = (1u << bits)-1;
const Big power = [] { Big p; mpz_ui_pow_ui(p.get_mpz_t(),3,292); return p; }();

struct Block { Offset y; unsigned gain; };
struct Trace { std::string word; unsigned bound,actual; };
struct Window { Offset low,high; unsigned cap; };
struct Result { Offset nodes=0, probes=0; unsigned cap=0; };

class Shell {
    std::vector<Block> table = std::vector<Block>(1u<<bits);
    Offset factor=1;
    unsigned initial=0;
    Result stats;

    Trace probe(Offset d) {
        ++stats.probes;
        // The 292 jumps leave c=d+585, with y=(c+7)/2 and mass gain 1168.
        Big y=(d+592)/2;
        unsigned gain=1168;
        for (unsigned j=0;j<initial/bits;++j) {
            const auto& block=table[y.get_ui()&mask];
            mpz_fdiv_q_2exp(y.get_mpz_t(),y.get_mpz_t(),bits);
            mpz_mul_ui(y.get_mpz_t(),y.get_mpz_t(),factor);
            mpz_add_ui(y.get_mpz_t(),y.get_mpz_t(),block.y);
            gain+=block.gain;
        }
        for (unsigned j=0;j<initial%bits;++j) {
            const auto low=y.get_ui()&1;
            gain+=5+4*low;
            y+=low;
            y/=2;
            y*=3;
        }
        Big c=2*y-7, a=2*(power+d-c)+gain+1;
        if (a<=1 || mpz_even_p(a.get_mpz_t())) throw std::runtime_error("initial bulk guard");
        unsigned bound=1168+9*initial;
        std::string word;
        word.reserve(50);
        for (unsigned i=0;i<5000;++i) {
            if (a==1) {
                word+='Z';
                return {word,bound/2,gain/2};
            }
            if (a<=c) {
                if (mpz_even_p(a.get_mpz_t())) {
                    word+='R';
                    return {word,(bound+5)/2,(gain+5)/2};
                }
                c-=a-1;
                a=3*a+2;
                bound+=4;
                gain+=4;
                word+='J';
                continue;
            }
            const bool small_residue=c.get_ui()%4==1;
            const unsigned correction=small_residue?2:4;
            if (a-c>=correction) {
                a-=c+correction;
                c=3*(c/2)+(small_residue?5:8);
                bound+=9;
                gain+=small_residue?5:9;
                word+='L';
            } else if (a-c==2 && !small_residue) {
                a=3*c+8;
                c=1;
                bound+=8;
                gain+=8;
                word+='E';
            } else {
                throw std::runtime_error("halting origin at offset "+std::to_string(d));
            }
        }
        throw std::runtime_error("tail budget at offset "+std::to_string(d));
    }

    void cover(Offset low,Offset high,const Trace& first,const Trace& last) {
        ++stats.nodes;
        if (first.word==last.word) {
            stats.cap=std::max(stats.cap,first.bound);
            return;
        }
        const Offset mid=low+2*((high-low)/4);
        cover(low,mid,first,mid==low?first:probe(mid));
        cover(mid+2,high,mid+2==high?last:probe(mid+2),last);
    }

    void windows(Offset low,Offset high,Offset threshold,const Trace& first,const Trace& last,
                 std::vector<Window>& out) {
        if (first.word==last.word) {
            const unsigned cap=std::max(620u,first.bound);
            if (!out.empty() && out.back().high==low) {
                out.back().high=high+2;
                out.back().cap=std::max(out.back().cap,cap);
            } else out.push_back({low,high+2,cap});
            return;
        }
        if (high-low<threshold) return;
        const Offset mid=low+2*((high-low)/4);
        windows(low,mid,threshold,first,mid==low?first:probe(mid),out);
        windows(mid+2,high,threshold,mid+2==high?last:probe(mid+2),last,out);
    }

public:
    explicit Shell(Offset high) {
        // c_i+13 <= (3/2)^i (high+598) bounds the right counter of the whole interval.
        Big lhs=4*(Big(high)+598),rhs=power;
        while (9*lhs<=4*rhs) { lhs*=9; rhs*=4; initial+=2; }
        for (unsigned j=0;j<bits;++j) factor*=3;
        for (unsigned i=0;i<=mask;++i) {
            Offset y=i;
            unsigned gain=0;
            for (unsigned j=0;j<bits;++j) {
                gain+=5+4*(y&1);
                y=3*((y+1)/2);
            }
            table[i]={y,gain};
        }
    }

    unsigned even_gain(Offset d) const {
        // I J^291 from even seed P+d. Here d is odd.
        Big a=4*(power/3)-1, c=power-2*(power/3)+d+587;
        unsigned gain=8+4*291;
        for (char op:std::string("LLJLLL")) {
            if (op=='J') {
                if (a>c || mpz_even_p(a.get_mpz_t())) throw std::runtime_error("even jump guard");
                c-=a-1;
                a=3*a+2;
                gain+=4;
            } else {
                const bool small=c.get_ui()%4==1;
                const unsigned j=small?2:4;
                if (a<c+j) throw std::runtime_error("even bulk guard");
                a-=c+j;
                c=3*(c/2)+(small?5:8);
                gain+=small?5:9;
            }
            if (a==1) throw std::runtime_error("early return in the even word");
        }
        if (a>c || mpz_odd_p(a.get_mpz_t())) throw std::runtime_error("even reset guard");
        return (gain+5)/2;
    }

    std::vector<unsigned> even_phases(Offset high) const {
        std::vector<unsigned> gains(64);
        for (unsigned d=1;d<64;d+=2) {
            gains[d]=even_gain(d);
            const Offset near=high-(high-d)%64;
            if (gains[d]!=even_gain(near)) throw std::runtime_error("even phase mismatch");
        }
        return gains;
    }

    Offset next(Offset d,const std::vector<unsigned>& gains) {
        return d+(d%2?gains[d%64]:probe(d).actual);
    }

    void link(Offset low,Offset high) {
        const auto gains=even_phases(high);
        Offset s=low,count=0;
        while (s<high) { s=next(s,gains); ++count; }
        std::cout<<low<<' '<<high<<' '<<s<<' '<<count<<'\n';
    }

    void stitch(Offset low,Offset high,Offset threshold) {
        const auto gains=even_phases(high);
        const Offset odd_first=low+low%2, odd_last=high-high%2;
        std::vector<Window> candidates;
        if (odd_first<=odd_last)
            windows(odd_first,odd_last,threshold,probe(odd_first),probe(odd_last),candidates);
        Offset seed=low,literal=0,joins=0,saved_width=0;
        for (const auto& w:candidates) {
            if (seed>=w.high || w.high-w.low<threshold || w.high>=high) continue;
            while (seed<w.low) { seed=next(seed,gains); ++literal; }
            if (seed>=w.high) continue;
            std::set<Offset> live;
            for (unsigned i=0;i<w.cap;++i) live.insert(w.high+i);
            for (unsigned i=0;i<200000 && live.size()>1 && *live.begin()<high;++i) {
                const Offset current=*live.begin();
                live.erase(live.begin());
                live.insert(next(current,gains));
                ++literal;
            }
            if (live.size()==1 && *live.begin()<high) {
                saved_width+=w.high-seed;
                seed=*live.begin();
                ++joins;
            }
        }
        while (seed<high) { seed=next(seed,gains); ++literal; }
        std::cout<<low<<' '<<high<<' '<<seed<<' '<<threshold<<' '<<literal<<' '
                 <<joins<<' '<<saved_width<<'\n';
    }

    void verify(Offset low,Offset high) {
        cover(low,high,probe(low),probe(high));
        std::cout<<low<<' '<<high<<' '<<initial<<' '<<stats.nodes<<' '
                 <<stats.probes<<' '<<stats.cap<<'\n';
    }
};

int main(int argc,char** argv) {
    bool link=argc==4 && std::string(argv[3])=="--link";
    bool stitch=argc==5 && std::string(argv[3])=="--stitch";
    if (argc!=3 && !link && !stitch) { std::cerr<<"Usage: power_cusp_cover LOW HIGH [--link | --stitch WIDTH]\n"; return 2; }
    try {
        const Offset low=std::stoull(argv[1]),high=std::stoull(argv[2]);
        if (high>1'000'000'000'000'000'000ULL || low>high || (!link && !stitch && (low%2 || high%2)) || ((link || stitch) && high<64))
            throw std::runtime_error("use ordered even offsets from zero through 10^18");
        Shell map(high);
        if (stitch) {
            const Offset width=std::stoull(argv[4]);
            if (width<4) throw std::runtime_error("use a window width of at least four");
            map.stitch(low,high,width);
        } else if (link) map.link(low,high);
        else map.verify(low,high);
    } catch (const std::exception& e) { std::cerr<<e.what()<<'\n'; return 1; }
}
