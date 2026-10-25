// UNVERIFIED native search using the existing CubicCap WF17/32/33/35/36
// certificates. Counts are certificate iterations, not ordinary TM steps.
// Guarded doubling and asymmetric blocks are unverified exploration.
// A halt candidate requires Coq replay.
// AI-assisted by Codex. See CUBIC_FAMILY.md for derivation and source mapping.
#include <algorithm>
#include <array>
#include <charconv>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <memory>
#include <random>
#include <stdexcept>
#include <string>
#include <vector>
using u64=uint64_t;
using i64=int64_t;
using u128=__uint128_t;
using i128=__int128_t;
using Clock=std::chrono::steady_clock;
constexpr u64 LIMIT=UINT64_MAX/16;
struct State {
    u64 a,b,c;
    bool operator==(const State& x)const{return a==x.a&&b==x.b&&c==x.c;}
};
struct Model {unsigned entry,lemma,left_b,left_add;const char* machine;State initial;};
constexpr Model MODELS[]={
 {35,17,0,0,"1RB0LE_1LC1RA_1RA1LD_0LC0LA_0RE1RF_0RC---",{3,0,0}},
 {269,32,1,2,"1LB1LD_0RC1LA_1LA1RC_0LB1RE_1LF0RD_---0LE",{0,1,0}},
 {494,33,2,2,"1LB1RE_1LC1LA_0RD1LB_1RE1RD_1LF0RA_---0LE",{2,2,1}},
 {138,35,0,4,"1LB1LD_0RC1LA_1RA1RC_1LA1RE_1LF0RD_---0LE",{0,1,1}},
 {409,36,0,2,"1LB1LD_0RC1LA_0LA1RC_1LA1RE_1LF0RD_---0LE",{0,0,1}}
};
const Model& model(unsigned entry) {
    for(const auto& m:MODELS)if(m.entry==entry)return m;
    throw std::runtime_error("unsupported entry");
}

// The scalar cases follow the nat certificate, including the decremented
// variables bound by Coq's S-patterns. false means the certificate says None.
__attribute__((always_inline)) inline bool scalar(const Model& m,State& s) {
    const u64 i=std::min(s.a/(m.lemma==17?3:2),s.c);
    u64 a=s.a-i*(m.lemma==17?3:2),b=s.b+2*i,c=s.c-i;
    if(m.lemma==17) {
        if(a==0) {
            if(b==0) {if(c==0){s={a,b,c};return true;}if(c==1)s={3,0,4};else return false;}
            else if(b==1) {if(c==0)s={3,0,4};else return false;}
            else {if(c==0)s={2*b-1,1,1};else s={2*b+1,0,c-1};}
        } else if(a==1) {
            if(c==0)s={3,0,4+2*b};else if(c==1)s={3+2*b,1,1};else s={5+2*b,0,c-2};
        } else if(a==2) {
            if(c==0)s={0,1,3+2*b};else s={0,3+b,c-1};
        } else {if(c==0)s={a-2,1,3+2*b};else s={a,b,c};}
        return true;
    }
    if(a==1 && c==0)return false;
    if(a>=4) {s={a-4,2,1+b};return true;} // c=0 after the bouncer
    if(m.lemma==32) {
        if(a==0)s=c==0?State{1+2*b,1,0}:State{2+2*b,1,c-1};
        else if(a==1)s=c==1?State{3+2*b,1,0}:State{4+2*b,1,c-2};
        else s={a==2?u64(2):u64(4),1,b};
    } else if(m.lemma==33) {
        if(a==0) {
            if(c==0)s={b==0?u64(2):2*b-1,2,1};
            else if(c==1)s={2*b,2,1};else s={2+2*b,2,c-2};
        } else if(a==1) {
            if(c==1)s={1+2*b,2,1};else if(c==2)s={2+2*b,2,1};else s={4+2*b,2,c-3};
        } else if(a==2)s=b==0?State{0,2,1}:State{2,2,b-1};
        else s=b==0?State{2,2,1}:State{4,2,b-1};
    } else if(m.lemma==35) {
        if(a==0) {
            if(c==0)s={1+2*b,1,1};else if(c==1)s={2+2*b,1,1};else s={4+2*b,0,c-1};
        } else if(a==1) {
            if(c==1)s={3+2*b,1,1};else if(c==2)s={4+2*b,1,1};else s={6+2*b,0,c-2};
        } else if(a==2)s=b==0?State{2,1,1}:State{4,0,b};
        else s=b==0?State{4,1,1}:State{6,0,b};
    } else {
        if(a==0)s=c==0?State{1+2*b,0,1}:State{2+2*b,0,c};
        else if(a==1)s=c==1?State{3+2*b,0,1}:State{4+2*b,0,c-1};
        else s={a==2?u64(2):u64(4),0,1+b};
    }
    return true;
}

struct Table {
    unsigned bits;u64 radix;const Model& m;
    std::array<std::vector<int32_t>,6> corrections;
    Table(unsigned k,const Model& mm):bits(k),radix(u64(1)<<k),m(mm) {
        if(k<1||k>24||m.lemma==17)throw std::runtime_error("invalid table setting");
        for(unsigned q=0;q<6;++q){corrections[q].resize(radix);build(q,0,0,0,0,q/2,q&1);}
    }
    void build(unsigned seed,unsigned depth,u64 word,i64 C,i64 D,unsigned b,unsigned parity) {
        if(depth==bits) {
            if(C<INT32_MIN||C>INT32_MAX)throw std::runtime_error("correction overflow");
            corrections[seed][word]=static_cast<int32_t>(C);return;
        }
        build(seed,depth+1,2*word,2*C+2*b+m.left_add,D+2-parity,m.left_b,0);
        build(seed,depth+1,2*word+1,2*C-D+2*b-4,D+2,2,parity);
    }
    bool jump(State& s)const {
        if(s.b>2)return false;
        const u64 n=s.a+2*s.b+2*s.c;
        if(!n)return false;
        u64 word,r;
        if(s.a<=UINT64_MAX/radix){const u64 x=s.a*radix;word=x/n;r=x%n;}
        else {const u128 x=u128(s.a)*radix;word=static_cast<u64>(x/n);r=static_cast<u64>(x%n);}
        if(r<6*radix||n-r<8*radix)return false;
        const i128 a=i128(r)+corrections[2*s.b+(s.a&1)][word];
        const u64 b=(word&1)?2:m.left_b;
        const u64 next_n=n+2*bits-((s.a&1)&&word!=radix-1);
        if(a<0||a+2*b>next_n||((next_n-static_cast<u64>(a)-2*b)&1))
            throw std::runtime_error("invalid jump result");
        s={static_cast<u64>(a),b,(next_n-static_cast<u64>(a)-2*b)/2};return true;
    }
};

// Entry 35: a fixed branch word has ideal map (4^k*a-B*N)/3^L.
// Corrections depend only on b, a mod 3^L, and N mod 3^(L-1).
// A final margin excludes exceptional branches at every prefix.
struct MixedTable {
 struct Value{int32_t correction;uint8_t increment,steps;};
 struct Leaf{u64 B,P,inverse,den,mu_a,mu_n;unsigned L,word;size_t offset;};
 unsigned bits;u64 radix;std::vector<unsigned> lookup;std::vector<Leaf> leaves;std::vector<Value> values;
 MixedTable(unsigned k):bits(k),radix(u64(1)<<(2*k)),lookup(radix) {
  if(k<1||k>8)throw std::runtime_error("invalid event width");
  build(0,0,1,0,0);
 }
 void build(unsigned depth,u64 B,u64 P,unsigned L,unsigned word) {
  if(depth<bits){build(depth+1,4*B,3*P,L+1,2*word);build(depth+1,4*B+3*P,P,L,2*word+1);return;}
  unsigned id=static_cast<unsigned>(leaves.size());for(u64 i=B;i<B+P;++i)lookup[i]=id;
  u64 inverse=P;for(unsigned j=0;j<6;++j)inverse*=2-P*inverse;
  leaves.push_back({B,P,inverse,L?P/3:1,UINT64_MAX/P,UINT64_MAX/(L?P/3:1),L,word,values.size()});
  for(unsigned b0=0;b0<2;++b0)for(u64 n0=0;n0<(L?P/3:1);++n0)for(u64 a0=0;a0<P;++a0){
   i64 a=static_cast<i64>(a0),n=static_cast<i64>(n0);unsigned b=b0,steps=0;
   for(unsigned j=bits;j-->0;){
    if((word>>j)&1){a=4*a-3*n+6*b-2;n+=3;b=1;++steps;}
    else{const i64 r=(a%3+3)%3;a=4*((a-r)/3)+2*b+(r==0?1:r==1?5:7);n+=r==0?0:r==1?2:3;b=0;steps+=r==2?2:1;}
   }
   const i64 C=static_cast<i64>(P)*a-static_cast<i64>(radix*a0)+static_cast<i64>(B*n0);
   if(C<INT32_MIN||C>INT32_MAX)throw std::runtime_error("mixed overflow");
   values.push_back({static_cast<int32_t>(C),static_cast<uint8_t>(n-n0),static_cast<uint8_t>(steps)});
  }
 }
 unsigned jump(State& s,u64 remaining)const {
  if(s.b>1)return 0;
  const u64 n=s.a+2*s.b+s.c;
  if(n<4*radix||s.a>=n)return 0;
  if(n>UINT64_MAX/radix)return 0;
  const u64 scaled=radix*s.a,index=scaled/n;
  const auto& l=leaves[lookup[index]];const u64 X=scaled-l.B*n;
  if(X<3*l.P*radix||l.P*n-X<l.P*radix)return 0;
  auto mod=[](u64 x,u64 p,u64 mu){u64 r=x-static_cast<u64>((u128(x)*mu)>>64)*p;return r>=p?r-p:r;};
  const auto& v=values[l.offset+(s.b*l.den+mod(n,l.den,l.mu_n))*l.P+mod(s.a,l.P,l.mu_a)];
  if(v.steps>remaining)return 0;
  const u64 numerator=X+static_cast<u64>(v.correction);
  const u64 a=numerator*l.inverse,b=l.word&1,newn=n+v.increment;
  if(a*l.P!=numerator||a+2*b>newn)throw std::runtime_error("mixed result");
  s={a,b,newn-a-2*b};return v.steps;
 }
};
u64 integer(const std::string& v) {
    u64 n;auto r=std::from_chars(v.data(),v.data()+v.size(),n);
    if(r.ec!=std::errc()||r.ptr!=v.data()+v.size())throw std::runtime_error("invalid unsigned integer");
    return n;
}
struct Checkpoint {State s;u64 iterations=0,jumps=0,scalar_steps=0;};
void save(const std::string& path,const Model& m,const Checkpoint& c) {
    if(path.empty())return;
    std::ofstream out(path+".tmp");
    out<<"cubic-family-v1\n"<<m.entry<<' '<<m.machine<<'\n'<<c.s.a<<' '<<c.s.b<<' '<<c.s.c<<' '
       <<c.iterations<<' '<<c.jumps<<' '<<c.scalar_steps<<'\n';out.close();
    if(!out||std::rename((path+".tmp").c_str(),path.c_str()))throw std::runtime_error("checkpoint write failed");
}
Checkpoint resume(const std::string& path,const Model& m) {
    std::ifstream in(path);std::string tag,table,tok;unsigned entry=0;
    if(!std::getline(in,tag)||tag!="cubic-family-v1"||!(in>>entry>>table)||entry!=m.entry||table!=m.machine)
        throw std::runtime_error("checkpoint identity mismatch");
    Checkpoint c{};
    for(auto p:{&c.s.a,&c.s.b,&c.s.c,&c.iterations,&c.jumps,&c.scalar_steps}) {
        if(!(in>>tok))throw std::runtime_error("truncated checkpoint");
        *p=integer(tok);
    }
    if(in>>tok)throw std::runtime_error("trailing checkpoint data");
    if(c.s.a>LIMIT||c.s.b>LIMIT||c.s.c>LIMIT||c.jumps>c.iterations||c.scalar_steps>c.iterations-c.jumps||
       u128(c.iterations-c.scalar_steps)>u128(24)*c.jumps)
        throw std::runtime_error("invalid checkpoint");
    return c;
}

void selftest(unsigned bits,unsigned events) {
    std::mt19937_64 rng(62332333536ULL);u64 checked=0;
    for(const auto& m:MODELS)if(m.lemma!=17) {
        Table table(bits,m);
        auto compare=[&](State s){State ref=s;if(!table.jump(s))return;
            for(unsigned j=0;j<bits;++j)if(!scalar(m,ref))throw std::runtime_error("skipped halt");
            if(!(s==ref))throw std::runtime_error("batch mismatch");
            ++checked;};
        for(unsigned i=0;i<250000;++i)compare({rng()%(LIMIT/8),rng()%3,rng()%(LIMIT/8)});
        State fast=m.initial,slow=fast;u64 done=0;
        while(done<1000000) {
            if(1000000-done>=bits&&table.jump(fast))done+=bits;
            else {if(!scalar(m,fast))throw std::runtime_error("early halt");++done;}
        }
        for(u64 i=0;i<done;++i)if(!scalar(m,slow))throw std::runtime_error("early halt");
        if(!(fast==slow))throw std::runtime_error("orbit mismatch");
    }
    MixedTable mixed(events);u64 mixed_checked=0;
    auto compare=[&](State s) {
        State reference=s;const unsigned count=mixed.jump(s,1000);if(!count)return;
        for(unsigned j=0;j<count;++j)if(!scalar(MODELS[0],reference))throw std::runtime_error("mixed block skipped halt");
        if(!(s==reference))throw std::runtime_error("mixed block mismatch");
        ++mixed_checked;
    };
    for(unsigned i=0;i<1000000;++i) {
        const u64 range=i<500000?1000000000000ULL:200000;
        compare({rng()%range,rng()%3,rng()%range});
    }
    for(u64 n:{u64(0),u64(1),u64(100000),LIMIT/16}) {
        compare({n,0,0});compare({0,0,n});compare({n,1,1});
        compare({n/4,0,n-n/4});compare({3*(n/4),1,n/4});
    }
    std::cout<<"{\"selftest\":\"passed\",\"accepted_jumps\":"<<checked
             <<",\"mixed_jumps\":"<<mixed_checked<<",\"orbits\":4}\n";
}

int main(int argc,char** argv)try {
    unsigned entry=269,bits=10,events=5;u64 budget=1000000000;double seconds=30;
    bool test=false,only_scalar=false,batch=false;std::string input,output;
    for(int i=1;i<argc;++i) {
        std::string o=argv[i];
        if(o=="--selftest"){test=true;continue;}if(o=="--scalar"){only_scalar=true;continue;}
        if(o=="--batch"){batch=true;continue;}
        if(o=="--help"){std::cout<<"--entry 35|138|269|409|494 --bits 1..24 --events 1..8 --iterations N --seconds S --scalar --selftest --batch --resume PATH --checkpoint PATH\n";return 0;}
        if(++i==argc)throw std::runtime_error("missing argument");
        const std::string v=argv[i];
        if(o=="--entry"){const u64 n=integer(v);if(n>623)throw std::runtime_error("entry out of range");entry=static_cast<unsigned>(n);}
        else if(o=="--bits"){const u64 n=integer(v);if(n<1||n>24)throw std::runtime_error("invalid width");bits=static_cast<unsigned>(n);}
        else if(o=="--events"){const u64 n=integer(v);if(n<1||n>8)throw std::runtime_error("invalid event width");events=static_cast<unsigned>(n);}
        else if(o=="--iterations")budget=integer(v);
        else if(o=="--seconds"){size_t end;seconds=std::stod(v,&end);if(end!=v.size())throw std::runtime_error("invalid time");}
        else if(o=="--resume")input=v;else if(o=="--checkpoint")output=v;else throw std::runtime_error("unknown option");
    }
    if(!std::isfinite(seconds)||seconds<=0)throw std::runtime_error("invalid time");
    if(test){selftest(bits,events);return 0;}const Model& m=model(entry);
    if(batch) {
        std::string first,second,third;
        while(std::cin>>first) {
            if(!(std::cin>>second>>third))throw std::runtime_error("truncated batch input");
            State s{integer(first),integer(second),integer(third)};
            if(s.a>10000||s.b>10000||s.c>10000)throw std::runtime_error("batch range");
            if(scalar(m,s))std::cout<<s.a<<' '<<s.b<<' '<<s.c<<'\n';else std::cout<<"HALT\n";
        }
        if(!std::cin.eof())throw std::runtime_error("invalid batch input");
        return 0;
    }
    Checkpoint c=input.empty()?Checkpoint{m.initial}:resume(input,m);const u64 base=c.iterations;
    if(budget>UINT64_MAX-base)throw std::runtime_error("iteration overflow");
    std::unique_ptr<Table> table;if(!only_scalar&&m.lemma!=17)table=std::make_unique<Table>(bits,m);
    std::unique_ptr<MixedTable> mixed;if(!only_scalar&&m.lemma==17)mixed=std::make_unique<MixedTable>(events);
    const auto start=Clock::now();double last=0;std::string status="iteration_limit";
    while(c.iterations<base+budget) {
        if(((c.jumps+c.scalar_steps)&65535)==0){double elapsed=std::chrono::duration<double>(Clock::now()-start).count();
            if(elapsed-last>=30){save(output,m,c);last=elapsed;}if(elapsed>=seconds){status="time_limit";break;}}
        if(c.s.a>LIMIT/16||c.s.b>LIMIT/16||c.s.c>LIMIT/16){status="integer_limit";break;}
        const unsigned swept=mixed?mixed->jump(c.s,base+budget-c.iterations):0;
        if(swept){c.iterations+=swept;++c.jumps;}
        else if(table&&base+budget-c.iterations>=bits&&table->jump(c.s)){c.iterations+=bits;++c.jumps;}
        else {State next=c.s;if(!(m.lemma==17?scalar(MODELS[0],next):scalar(m,next))){status="halt_candidate";break;}c.s=next;++c.iterations;++c.scalar_steps;}
    }
    State probe=c.s;if(!scalar(m,probe))status="halt_candidate";
    const double elapsed=std::chrono::duration<double>(Clock::now()-start).count();save(output,m,c);
    std::cout<<std::setprecision(17)<<"{\"verified\":false,\"entry\":"<<entry<<",\"lemma\":\"CubicCap.WF"<<m.lemma
       <<"\",\"backend\":\""<<(only_scalar?"scalar":entry==35?"asymmetric_table":"doubling_table")
       <<"\",\"bits\":"<<bits<<",\"events\":"<<events<<",\"status\":\""<<status<<"\",\"iterations\":"<<c.iterations<<",\"new_iterations\":"<<c.iterations-base
       <<",\"a\":"<<c.s.a<<",\"b\":"<<c.s.b<<",\"c\":"<<c.s.c<<",\"jumps\":"<<c.jumps
       <<",\"scalar_steps\":"<<c.scalar_steps<<",\"seconds\":"<<elapsed<<"}\n";
    return 0;
}catch(const std::exception& e){std::cerr<<"error: "<<e.what()<<'\n';return 1;}
