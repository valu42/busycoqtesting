// Independent, deliberately direct big-integer transcription of SOC25Iter.F.
// Used to validate and benchmark soc25_deque.cpp; not a verified simulator.
// Source: upstream busycoq PR #40 at 069dc1eb72df69dfa595f491b5c315c3ce424ac6.
// Requires Boost.Multiprecision headers. AI-assisted by Codex.
#include <boost/multiprecision/cpp_int.hpp>
#include <chrono>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
using Big=boost::multiprecision::cpp_int;
using u64=uint64_t;
Big power(u64 n) {return Big(1)<<n;}
Big sub(const Big& a,const Big& b) {return a>=b?Big(a-b):Big(0);}
std::pair<Big,u64> split(const Big& x) {
    if(x==0)return {0,0};
    const u64 h=boost::multiprecision::lsb(x);return {x>>(h+1),h};
}
struct State {u64 L;Big X;};
bool step(State& s) {
    const u64 L=s.L;const Big& X=s.X;
    if(X==power(L)) {
        const u64 l=L-1,a=l/2,t=5*a+((l&1)?4:2);
        s={l+3+t,((power(l+2)+1)<<t)+((l&1)?1:0)};return true;
    }
    auto [m,h]=split(X);const u64 a=h/2;
    Big k=sub(power(L)-1,(power(h)-1)*2);
    if(h&1) {
        if(m!=0)return false;
        s={L+1+5*a+3,(2*k+1)<<(5*a+3)};return true;
    }
    u64 L1=L+1+5*a;Big k1=sub((2*k+1)<<(5*a),1);
    if(m==0) {s={L1,k1+2};return true;}
    auto [x,i]=split(m);k1=sub(k1,2*(power(i)-1));
    while(true) {
        const u64 half=i/2;
        if(!(i&1)) {s={L1+1+5*half+1,((2*k1+1)<<(5*half+1))+(2*x+1)};return true;}
        L1+=1+5*half+4;k1=sub((2*k1+1)<<(5*half+4),1);
        if(x==0) {s={L1,k1+1};return true;}
        auto next=split(x);x=next.first;i=next.second;k1=sub(k1,2*(power(i)-1)+1);
    }
}
int main(int argc,char** argv) try {
    u64 start=1,rounds=100000;bool hex=false;
    for(int i=1;i<argc;++i) {
        std::string arg=argv[i];
        if(arg=="--hex") {hex=true;continue;}
        if(++i==argc)throw std::runtime_error("missing value");
        std::size_t end;std::string text=argv[i];
        if(text.empty() || text[0]=='-')throw std::runtime_error("invalid integer");
        const u64 n=std::stoull(text,&end);
        if(end!=text.size())throw std::runtime_error("invalid integer");
        if(arg=="--start")start=n;else if(arg=="--rounds")rounds=n;
        else throw std::runtime_error("unknown option");
    }
    if(start<1 || start>3 || rounds>1000000)throw std::runtime_error("reference budget exceeded");
    State s{start==2?u64(2):u64(1),Big(start==1?2:start==2?4:3)};u64 done=0;
    const auto begin=std::chrono::steady_clock::now();
    for(;done<rounds;++done)if(!step(s))break;
    const double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count();
    std::cout<<std::setprecision(17)<<"{\"verified\":false,\"status\":\""
             <<(done<rounds?"halt_candidate":"round_limit")<<"\",\"start\":"<<start<<",\"rounds\":"<<done
             <<",\"L\":"<<s.L<<",\"bits\":"<<boost::multiprecision::msb(s.X)+1
             <<",\"seconds\":"<<seconds;
    if(hex)std::cout<<",\"X_hex\":\""<<std::hex<<s.X<<std::dec<<'"';
    std::cout<<"}\n";
} catch(const std::exception& e) {std::cerr<<"error: "<<e.what()<<'\n';return 1;}
