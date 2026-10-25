// Unverified implementation of SOC25Iter.F from upstream PR #40, pinned at
// 069dc1eb72df69dfa595f491b5c315c3ce424ac6. See SOC25_DEQUE.md for attribution.
// The acceleration is the sliding binary representation, not a new round map.
// A budget is UNKNOWN; a native halt is only a candidate. AI-assisted by Codex.
#include <algorithm>
#include <charconv>
#include <chrono>
#include <cstdint>
#include <deque>
#include <iomanip>
#include <iostream>
#include <random>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

using u64=uint64_t;
using i64=int64_t;
constexpr u64 POSITION_LIMIT=u64(1)<<58;

// Stored positions are absolute; changing the logical low end does not shift
// or copy the remaining words. Bits below base are always zero.
struct Bits {
    std::deque<u64> words;
    u64 base=64, first=1;
    explicit Bits(u64 x=0) {if (x) words.push_back(x);}
    void clear() {words.clear();base=64;first=1;}
    void trim() {while (!words.empty() && words.back()==0) words.pop_back();}
    u64 length() const {
        if (words.empty()) return 0;
        return (first+words.size()-1)*64+64-static_cast<u64>(__builtin_clzll(words.back()))-base;
    }
    u64 block(u64& cursor) const {
        const u64 absolute=base+cursor;
        u64 index=(absolute>>6)-first;
        if (index>=words.size()) throw std::runtime_error("read past binary counter");
        u64 w=words[index] & (UINT64_MAX<<(absolute&63));
        while (!w) {
            if (++index>=words.size()) throw std::runtime_error("missing low block");
            w=words[index];
        }
        const u64 position=(first+index)*64+static_cast<u64>(__builtin_ctzll(w))-base;
        const u64 gap=position-cursor;
        cursor=position+1;
        return gap;
    }
    void right(u64 count) {
        if (count>=length()) {clear();return;}
        base+=count;
        while (first<(base>>6)) {words.pop_front();++first;}
        words.front() &= UINT64_MAX<<(base&63);
    }
    void left_one() {
        if (words.empty()) return;
        if (base==0) {base=64;++first;}
        --base;
        if ((base>>6)<first) {words.push_front(0);--first;}
    }
    void add_power(u64 p) {
        const u64 absolute=base+p;
        u64 index=(absolute>>6)-first;
        if (index>=words.size()) words.resize(index+1,0);
        const u64 old=words[index], value=u64(1)<<(absolute&63);
        words[index]+=value;
        if (words[index]>=old) return;
        while (true) {
            if (++index==words.size()) words.push_back(0);
            if (++words[index]) return;
        }
    }
    void subtract_power(u64 p) {
        const u64 absolute=base+p;
        u64 index=(absolute>>6)-first;
        if (index>=words.size()) throw std::runtime_error("negative counter");
        const u64 old=words[index], value=u64(1)<<(absolute&63);
        words[index]-=value;
        if (old>=value) return;
        while (true) {
            if (++index==words.size()) throw std::runtime_error("negative counter");
            const u64 before=words[index];--words[index];
            if (before) return;
        }
    }
    std::string hex() const {
        const u64 count=(length()+63)/64, offset=base&63;
        if (!count) return "0";
        std::ostringstream out;out<<std::hex<<std::setfill('0');
        for (u64 j=count;j-->0;) {
            u64 w=words[j]>>offset;
            if (offset && j+1<words.size()) w|=words[j+1]<<(64-offset);
            out<<std::setw(16)<<w;
        }
        return out.str();
    }
    u64 fingerprint() const {
        // Reproducibility aid, not a cryptographic certificate. Independent
        // validation compares the complete hexadecimal integer instead.
        u64 h=14695981039346656037ULL;
        const u64 count=(length()+63)/64,offset=base&63;
        for (u64 j=0;j<count;++j) {
            u64 w=words[j]>>offset;
            if (offset && j+1<words.size()) w|=words[j+1]<<(64-offset);
            for (unsigned b=0;b<8;++b) {h^=(w>>(8*b))&255;h*=1099511628211ULL;}
        }
        return h;
    }
};

struct Term {i64 position; bool positive;};
struct Plan {
    u64 length=0, consumed=0;
    bool halted=false, append_one=false;
    i64 shift=0;
    std::vector<Term> terms;
    void add(u64 p,bool positive=true) {terms.push_back({static_cast<i64>(p)-shift,positive});}
    void move(u64 n) {shift+=static_cast<i64>(n);}
};

// Read-only planning keeps a space-limited result at the last complete round.
// Signed powers represent the auxiliary counter; positive terms are applied
// before negative terms, so an intermediate borrow cannot make it negative.
Plan plan(u64 L,const Bits& X) {
    Plan p;
    const u64 size=X.length();
    if (L<1 || size<2 || size>L+1) throw std::runtime_error("invalid round domain");
    u64 cursor=0;
    const u64 h=X.block(cursor);
    if (cursor==size && h==L) {
        const u64 l=L-1,a=l/2,t=5*a+((l&1)?4:2);
        p.length=l+3+t;p.consumed=size;
        p.add(l+2+t);p.add(t);if(l&1)p.add(0);
        return p;
    }
    const u64 a=h/2;
    if (h&1) {
        if (cursor<size) {p.halted=true;return p;}
        const u64 t=5*a+3;
        p.length=L+1+t;p.consumed=size;
        p.add(L+1+t);p.add(h+2+t,false);p.add(t);p.add(t+1);
        return p;
    }
    u64 L1=L+1+5*a;
    p.add(L1);p.add(h+2+5*a,false);p.add(5*a);p.add(5*a+1);p.add(0,false);
    if (cursor==size) {
        p.length=L1;p.consumed=size;p.add(1);return p;
    }
    u64 i=X.block(cursor);
    p.add(i+1,false);p.add(1);
    while (true) {
        const u64 half=i/2;
        if (!(i&1)) {
            const u64 t=5*half+1;
            p.length=L1+1+t;p.consumed=cursor;p.append_one=true;
            p.move(t+1);p.add(t);return p;
        }
        const u64 t=5*half+4;
        L1+=1+t;p.move(t+1);p.add(t);p.add(0,false);
        if (cursor==size) {
            p.length=L1;p.consumed=size;p.add(0);return p;
        }
        i=X.block(cursor);p.add(i+1,false);p.add(0);
    }
}

void commit(Bits& X,const Plan& p) {
    X.right(p.consumed);
    if (p.append_one) {X.left_one();X.add_power(0);}
    for (bool positive : {true,false})
        for (const Term& term:p.terms) if(term.positive==positive) {
            const i64 exponent=term.position+p.shift;
            if (exponent<0 || static_cast<u64>(exponent)>p.length+2)
                throw std::runtime_error("invalid planned power");
            if (positive) X.add_power(static_cast<u64>(exponent));
            else X.subtract_power(static_cast<u64>(exponent));
        }
    X.trim();
    if (!X.length() || X.length()>p.length+1)
        throw std::runtime_error("round domain lost");
}

u64 integer(const std::string& text) {
    u64 value;auto r=std::from_chars(text.data(),text.data()+text.size(),value);
    if(r.ec!=std::errc() || r.ptr!=text.data()+text.size()) throw std::runtime_error("invalid integer");
    return value;
}

void arithmetic_selftest() {
    using u128=__uint128_t;
    std::mt19937_64 random(250040);
    for (unsigned trial=0;trial<100;++trial) {
        const u64 initial=random();Bits X(initial);u128 reference=initial;
        for(unsigned j=0;j<1000;++j) {
            const unsigned operation=static_cast<unsigned>(random()%4);
            const u64 p=random()%112;const u128 power=u128(1)<<p;
            if(operation==0) {const u64 n=random()%130;X.right(n);reference=n>=128?0:reference>>n;}
            if(operation==1 && reference<(u128(1)<<119)) {X.left_one();reference<<=1;}
            if(operation==2 && reference<(u128(1)<<120)-power) {X.add_power(p);reference+=power;}
            if(operation==3 && reference>=power) {X.subtract_power(p);reference-=power;}
            X.trim();
            std::ostringstream expected;expected<<std::hex<<std::setfill('0');
            if(!reference) expected<<'0';
            else {
                if(reference>>64)expected<<std::setw(16)<<static_cast<u64>(reference>>64);
                expected<<std::setw(16)<<static_cast<u64>(reference);
            }
            if(X.hex()!=expected.str())throw std::runtime_error("arithmetic comparison failed");
        }
    }
    std::cout<<"{\"arithmetic_selftest\":\"passed\",\"operations\":100000}\n";
}

int main(int argc,char** argv) try {
    u64 start=1,rounds=1000000,max_bits=256000000;
    double seconds=30;bool output_hex=false,batch=false;
    for(int i=1;i<argc;++i) {
        std::string arg=argv[i];
        if(arg=="--hex") {output_hex=true;continue;}
        if(arg=="--batch") {batch=true;continue;}
        if(arg=="--selftest") {arithmetic_selftest();return 0;}
        if(arg=="--help") {
            std::cout<<"--start 1|2|3 --rounds N --seconds S --max-bits N --hex --batch --selftest\n";return 0;
        }
        if(++i==argc)throw std::runtime_error("missing value");
        if(arg=="--start")start=integer(argv[i]);
        else if(arg=="--rounds")rounds=integer(argv[i]);
        else if(arg=="--max-bits")max_bits=integer(argv[i]);
        else if(arg=="--seconds") {std::size_t end;std::string s=argv[i];seconds=std::stod(s,&end);
            if(end!=s.size() || !(seconds>0 && seconds<1e9)) throw std::runtime_error("invalid seconds");}
        else throw std::runtime_error("unknown option");
    }
    if(start<1 || start>3 || max_bits<8 || max_bits>POSITION_LIMIT)
        throw std::runtime_error("unsupported start or bit limit");
    if(batch) {
        u64 L,x,n;
        while(std::cin>>L>>x>>n) {
            if(L<1 || L>60 || x<2 || x>=(u64(1)<<(L+1)) || n>100000)
                throw std::runtime_error("invalid batch input");
            Bits X(x);bool halt=false;
            for(u64 j=0;j<n;++j) {
                auto p=plan(L,X);if(p.halted){halt=true;break;}
                if(p.length+1>max_bits)throw std::runtime_error("batch bit limit");
                commit(X,p);L=p.length;
            }
            if(halt)std::cout<<"HALT\n";else std::cout<<L<<' '<<X.hex()<<'\n';
        }
        if(!std::cin.eof())throw std::runtime_error("invalid batch text");
        return 0;
    }
    u64 L=start==2?2:1,done=0;Bits X(start==1?2:start==2?4:3);
    std::string status="round_limit";
    const auto begin=std::chrono::steady_clock::now();
    for(;done<rounds;++done) {
        if((done&4095)==0 && std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count()>=seconds)
            {status="time_limit";break;}
        if(L>POSITION_LIMIT/8 || X.base>POSITION_LIMIT) {status="integer_limit";break;}
        const auto p=plan(L,X);
        if(p.halted) {status="halt_candidate";break;}
        if(p.length+1>max_bits) {status="space_limit";break;}
        commit(X,p);L=p.length;
    }
    if(plan(L,X).halted)status="halt_candidate";
    const double elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count();
    std::cout<<std::setprecision(17)<<"{\"verified\":false,\"status\":\""<<status
             <<"\",\"start\":"<<start<<",\"rounds\":"<<done<<",\"L\":"<<L
             <<",\"bits\":"<<X.length()<<",\"stored_words\":"<<X.words.size()
             <<",\"fnv1a64\":\""<<std::hex<<X.fingerprint()<<std::dec<<"\",\"seconds\":"<<elapsed;
    if(output_hex)std::cout<<",\"X_hex\":\""<<X.hex()<<'"';
    std::cout<<"}\n";
} catch(const std::exception& e) {std::cerr<<"error: "<<e.what()<<'\n';return 1;}
