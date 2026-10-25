// UNVERIFIED packet searches for supplied entries 405 and 482.
// The packet-cycle method is due to valu42's PacketHalt274 work and upstream
// PR #39. These two tables were learned independently and their finite laws
// are checked in ResearchPacketCoverage.v. See PACKET_STREAM.md.
// Reuses the SOC25 sliding binary representation for both tape and call count.
// AI-assisted by Codex. Counts below are complete boundary rounds, not TM steps.
#include "sliding_bits.hpp"
#include <algorithm>
#include <charconv>
#include <chrono>
#include <cmath>
#include <cstdio>
#include <fstream>
#include <iostream>
#include <limits>
#include <random>
#include <vector>
using u64=uint64_t;
using sliding::Bits;
using Clock=std::chrono::steady_clock;
struct Packet{unsigned width;std::vector<std::pair<u64,u64>> pre,cycle;};
std::vector<Packet> packets405={
{3,{},{{0,0},{1,1}}},
{3,{},{{1,1},{0,0}}},
{3,{{2,0},{3,1}},{{0,0},{1,1}}},
{4,{},{{5,2}}},
{4,{{4,0}},{{5,2}}},
// First needed after boundary 161210: the old catalogue stopped unknown.
{6,{{12,0},{13,0}},{{8,0},{9,1},{0,0},{1,0}}},
};
std::vector<Packet> packets482={
{3,{},{{0,0},{1,1}}},
{3,{},{{1,1},{0,0}}},
{4,{},{{5,2}}},
{4,{{4,0}},{{5,2}}},
{4,{{2,0},{3,0},{4,0}},{{5,2}}},
{6,{{10,0},{11,0},{12,0},{13,0}},{{8,0},{9,1},{0,0},{1,0}}},
{7,{{42,0},{43,0},{44,0},{45,0}},{{40,0},{41,2}}},
};
__attribute__((always_inline)) inline u64 peek(const Bits& x,u64 pos,unsigned width) {
 const u64 abs=x.base+pos,index=(abs>>6)-x.first,off=abs&63;
 if(index>=x.words.size())return 0;
 u64 v=x.words[index]>>off;
 if(off&&index+1<x.words.size())v|=x.words[index+1]<<(64-off);
 return width==64?v:v&((u64(1)<<width)-1);
}
__attribute__((always_inline)) inline void field(Bits& x,u64 pos,unsigned width,u64 value) {
 const u64 abs=x.base+pos,index=(abs>>6)-x.first,off=abs&63,mask=(u64(1)<<width)-1;
 if(index>=x.words.size()){if(!value)return;x.words.resize(index+1,0);}
 x.words[index]=(x.words[index]&~(mask<<off))|(value<<off);
 if(off+width>64) {
  u64 hi=value>>(64-off),hm=mask>>(64-off);
  if(index+1>=x.words.size()){if(hi)x.words.push_back(hi);}
  else x.words[index+1]=(x.words[index+1]&~hm)|hi;
 }
 x.trim();
}
template<class Binary> __attribute__((always_inline)) inline void smalladd(Binary& x,u64 n){while(n){unsigned p=static_cast<unsigned>(__builtin_ctzll(n));x.add_power(p);n&=n-1;}}
template<class Binary> __attribute__((always_inline)) inline void smallsub(Binary& x,u64 n){while(n){unsigned p=static_cast<unsigned>(__builtin_ctzll(n));x.subtract_power(p);x.trim();n&=n-1;}}

std::vector<Packet> expand_catalogue(const std::vector<Packet>& source) {
    std::vector<Packet> result=source;
    for(const auto& p:source) {
        for(size_t j=1;j<p.pre.size();++j)
            result.push_back({p.width,{p.pre.begin()+static_cast<std::ptrdiff_t>(j),p.pre.end()},p.cycle});
        for(size_t j=1;j<p.cycle.size();++j) {
            auto cycle=p.cycle;std::rotate(cycle.begin(),cycle.begin()+static_cast<std::ptrdiff_t>(j),cycle.end());
            result.push_back({p.width,{},std::move(cycle)});
        }
    }
    return result;
}
const char* machine(unsigned entry) {
    if(entry==405)return "1RB0LB_0RC0LF_1LD1RE_0LA0RB_0RD0RF_0LA---";
    if(entry==482)return "1RB0LB_0RC0LD_1LD1RE_0LA0RB_0RD1RF_1LA---";
    throw std::runtime_error("unsupported entry");
}
u64 integer(const std::string& s,int base=10) {
    u64 n;const auto r=std::from_chars(s.data(),s.data()+s.size(),n,base);
    if(r.ec!=std::errc()||r.ptr!=s.data()+s.size())throw std::runtime_error("invalid integer");
    return n;
}
Bits from_hex(const std::string& s) {
    if(s.empty()||s.size()>25000000)throw std::runtime_error("invalid hex size");
    Bits x;
    for(size_t end=s.size();end;) {
        const size_t start=end>16?end-16:0;
        x.words.push_back(integer(s.substr(start,end-start),16));end=start;
    }
    x.trim();return x;
}
struct Checkpoint {
    Bits word{1};u64 rounds=0,events=0;
    // A proven unchanged prefix of (1010)^prefix packets. Not serialized:
    // a resumed checkpoint starts at zero and rediscovers it from the tape.
    u64 prefix=0;
};
void save(const std::string& path,unsigned entry,const Checkpoint& c) {
    if(path.empty())return;
    std::ofstream out(path+".tmp");
    out<<"packet-stream-v1\n"<<entry<<' '<<machine(entry)<<'\n'
       <<c.rounds<<' '<<c.events<<'\n'<<c.word.hex()<<'\n';out.close();
    if(!out||std::rename((path+".tmp").c_str(),path.c_str()))throw std::runtime_error("checkpoint write failed");
}
Checkpoint resume(const std::string& path,unsigned entry) {
    std::ifstream in(path);std::string tag,id,tm,rounds,events,hex,extra;
    if(!std::getline(in,tag)||tag!="packet-stream-v1"||!(in>>id>>tm>>rounds>>events>>hex)||in>>extra)
        throw std::runtime_error("invalid checkpoint");
    if(integer(id)!=entry||tm!=machine(entry))throw std::runtime_error("checkpoint identity mismatch");
    Checkpoint c{from_hex(hex),integer(rounds),integer(events)};
    if(c.rounds>c.events)throw std::runtime_error("invalid checkpoint counts");
    return c;
}
// N = 16*H+r, H>=1. Each window keeps N = 2^exponent*H+bias.
// A packet is composed only if its branch and residue hold for EVERY H>=1.
struct Window {
    uint16_t output=0;
    int16_t bias=0;
    uint8_t width=0,exponent=4,events=0;
};
__attribute__((always_inline)) inline void left(Bits& x,u64 count) {
    if(!x.length())return;
    if(count>x.base){const u64 words=(count-x.base+63)/64;x.base+=64*words;x.first+=words;}
    x.base-=count;
    while(x.first>(x.base>>6)){x.words.push_front(0);--x.first;}
}
// Exact sparse call counter: 2^exponent + offset. Long powers and borrows
// remain symbolic. If the signed offset grows, fall back to the dense deque.
// The offset is kept below 2^100; each window shifts by at most eight bits.
struct Counter {
    using i128=__int128_t;using u128=__uint128_t;
    inline static u64 fallbacks=0;
    bool sparse;u64 exponent=0;i128 offset=0;Bits dense;
    explicit Counter(u64 value=0,bool use_sparse=true):sparse(use_sparse),offset(i128(value)-1),dense(use_sparse?0:value){}
    u64 length() const {
        if(!sparse)return dense.length();
        if(exponent>110)return exponent+(offset>=0?1:0);
        const i128 v=(i128(1)<<exponent)+offset;
        if(v<0)throw std::runtime_error("negative sparse counter");
        if(!v)return 0;
        const u64 hi=static_cast<u64>(u128(v)>>64),lo=static_cast<u64>(v);
        return hi?128-static_cast<u64>(__builtin_clzll(hi)):64-static_cast<u64>(__builtin_clzll(lo));
    }
    void materialize() {
        if(!sparse)return;
        dense=Bits(1);left(dense,exponent);
        u128 rest=offset<0?u128(-offset):u128(offset);
        while(rest) {
            const u64 lo=static_cast<u64>(rest);
            const unsigned p=lo?static_cast<unsigned>(__builtin_ctzll(lo)):64+static_cast<unsigned>(__builtin_ctzll(static_cast<u64>(rest>>64)));
            if(offset<0)dense.subtract_power(p);else dense.add_power(p);
            rest&=rest-1;
        }
        dense.trim();sparse=false;++fallbacks;
    }
    void trim() {
        if(!sparse){dense.trim();return;}
        if(offset>=(i128(1)<<100)||offset<=-(i128(1)<<100))materialize();
    }
    void right(u64 count) {
        if(!sparse){dense.right(count);return;}
        if(count>8)throw std::runtime_error("sparse shift range");
        const i128 divisor=i128(1)<<count;
        if(exponent>=count) {
            exponent-=count;
            offset=offset>=0?offset/divisor:-((-offset+divisor-1)/divisor);
        } else {
            const i128 value=(i128(1)<<exponent)+offset;
            if(value<0)throw std::runtime_error("negative sparse shift");
            exponent=0;offset=value/divisor-1;
        }
    }
    void shift_left(u64 count) {
        if(!sparse){left(dense,count);return;}
        if(count>8)throw std::runtime_error("sparse shift range");
        exponent+=count;offset*=i128(1)<<count;trim();
    }
    void left_one(){shift_left(1);}
    void add_power(u64 p) {
        if(!sparse){dense.add_power(p);return;}
        if(p>8)throw std::runtime_error("sparse add range");
        offset+=i128(1)<<p;trim();
    }
    void subtract_power(u64 p) {
        if(!sparse){dense.subtract_power(p);return;}
        if(p>8)throw std::runtime_error("sparse subtract range");
        offset-=i128(1)<<p;trim();
    }
};
__attribute__((always_inline)) inline u64 peek(const Counter& x,u64 pos,unsigned width) {
    if(!x.sparse)return peek(x.dense,pos,width);
    if(pos!=0)throw std::runtime_error("sparse field position");
    const Counter::u128 value=Counter::u128(x.offset)+(x.exponent<width?(Counter::u128(1)<<x.exponent):0);
    return static_cast<u64>(value)&((u64(1)<<width)-1);
}
__attribute__((always_inline)) inline void left(Counter& x,u64 count){x.shift_left(count);}
void initial_power(Bits& x,u64 exponent){left(x,exponent);}
void initial_power(Counter& x,u64 exponent){x.exponent=exponent;}
struct Engine {
    const std::vector<Packet> packets;
    std::vector<int> decode;
    std::vector<Window> windows;
    bool sparse_counter,skip_prefix;
    explicit Engine(unsigned entry,bool single=false,bool dense_counter=false,bool no_prefix=false):packets(expand_catalogue(entry==405?packets405:packets482)),decode(16384,-1),sparse_counter(!dense_counter),skip_prefix(!no_prefix) {
        for(unsigned v=0;v<16384;++v)for(unsigned i=0;i<packets.size();++i) {
            const auto& p=packets[i];const u64 u=p.pre.empty()?p.cycle[0].first:p.pre[0].first;
            if((v&((1u<<p.width)-1))==u){decode[v]=static_cast<int>(i);break;}
        }
        if(!single) {
            windows.resize(1<<20);
            for(unsigned word=0;word<65536;++word)for(unsigned residue=0;residue<16;++residue) {
                Window w;w.bias=static_cast<int16_t>(residue);
                while(w.width<16) {
                    const int id=decode[(word>>w.width)&16383];
                    if(id<0)break;
                    const auto& p=packets[static_cast<unsigned>(id)];
                    if(w.width+p.width>16)break;
                    const int pre=static_cast<int>(p.pre.size()),period=static_cast<int>(p.cycle.size());
                    const unsigned down=static_cast<unsigned>(__builtin_ctz(static_cast<unsigned>(period)));
                    if(w.exponent<down || (1<<w.exponent)+w.bias<std::max(1,pre))break;
                    int total=0,constant=0;
                    for(auto x:p.cycle)total+=static_cast<int>(x.second);
                    for(auto x:p.pre)constant+=static_cast<int>(x.second);
                    const int r=((w.bias-pre)%period+period)%period;
                    for(int j=0;j<r;++j)constant+=static_cast<int>(p.cycle[static_cast<unsigned>(j)].second);
                    const int bias=((w.bias-pre-r)/period)*total+constant;
                    if(bias<INT16_MIN||bias>INT16_MAX)throw std::runtime_error("window bias overflow");
                    w.bias=static_cast<int16_t>(bias);
                    w.exponent=static_cast<uint8_t>(w.exponent-down+static_cast<unsigned>(__builtin_ctz(static_cast<unsigned>(total))));
                    w.output|=static_cast<uint16_t>(p.cycle[static_cast<unsigned>(r)].first<<w.width);
                    w.width=static_cast<uint8_t>(w.width+p.width);++w.events;
                }
                windows[(word<<4)|residue]=w;
            }
        }
    }
    // Any interrupted/unknown round is rolled back by the caller. The local
    // word is partially rewritten while its yet-unprocessed tail is scanned.
    template<class Binary> std::string round_impl(Checkpoint& c,u64 max_bits,Clock::time_point deadline)const {
        c.word.left_one();c.word.left_one();c.word.add_power(0);
        Binary n(1);u64 cursor=0,next_check=c.events;
        if(skip_prefix) {
            // Prepending 10 preserves at least the previous whole packets.
            // The skipped packets are unchanged for every incoming call count.
            u64 repeat=c.prefix,blocks=0;
            while(true) {
                const u64 difference=peek(c.word,4*repeat,64)^0x5555555555555555ULL;
                if(difference){repeat+=static_cast<u64>(__builtin_ctzll(difference))/4;break;}
                repeat+=16;
                if((++blocks&4095)==0&&Clock::now()>=deadline)return "time_limit";
            }
            initial_power(n,repeat);cursor=4*repeat;c.prefix=repeat;
            if(c.events>UINT64_MAX-repeat)throw std::runtime_error("event overflow");
            c.events+=repeat;
            if(n.length()>max_bits)return "space_limit";
        }
        while(n.length()) {
            if(c.events>=next_check) {
                if(Clock::now()>=deadline)return "time_limit";
                next_check=c.events>UINT64_MAX-4096?UINT64_MAX:c.events+4096;
            }
            if(!windows.empty()&&n.length()>4&&n.length()+5<=max_bits) {
                const auto& w=windows[(peek(c.word,cursor,16)<<4)|peek(n,0,4)];
                if(w.events>1) {
                    n.right(4);left(n,w.exponent);
                    if(w.bias<0)smallsub(n,static_cast<u64>(-w.bias));else smalladd(n,static_cast<u64>(w.bias));
                    field(c.word,cursor,w.width,w.output);cursor+=w.width;
                    if(c.events>UINT64_MAX-w.events)throw std::runtime_error("event overflow");
                    c.events+=w.events;
                    if(c.word.length()>max_bits||n.length()>max_bits)return "space_limit";
                    continue;
                }
            }
            const int id=decode[peek(c.word,cursor,14)];
            if(id<0) {
                // The unconditional C/0 call returns immediately with 0 -> 1.
                // It is a transient rule, so a cycle-only catalogue omits it.
                if(peek(c.word,cursor,1)==0) {
                    field(c.word,cursor,1,1);smallsub(n,1);
                    if(c.events==UINT64_MAX)throw std::runtime_error("event overflow");
                    ++c.events;continue;
                }
                return peek(c.word,cursor,3)==7?"halt_candidate":"unknown_packet";
            }
            const auto& p=packets[static_cast<unsigned>(id)];
            const u64 small=n.length()<=8?peek(n,0,8):256;
            u64 v;
            if(small<p.pre.size()) {
                u64 out=0;for(u64 j=0;j<small;++j)out+=p.pre[j].second;
                v=p.pre[small].first;n=Binary(out);
            } else {
                u64 sumpre=0,sumcyc=0;
                for(auto x:p.pre)sumpre+=x.second;
                for(auto x:p.cycle)sumcyc+=x.second;
                if((p.cycle.size()&(p.cycle.size()-1))||sumcyc==0||(sumcyc&(sumcyc-1)))
                    throw std::runtime_error("unsupported packet multiplier");
                smallsub(n,p.pre.size());
                const unsigned shift=static_cast<unsigned>(__builtin_ctzll(p.cycle.size()));
                const u64 r=shift?peek(n,0,shift):0;v=p.cycle[r].first;
                n.right(shift);for(u64 j=sumcyc;j>1;j>>=1)n.left_one();
                u64 add=sumpre;for(u64 j=0;j<r;++j)add+=p.cycle[j].second;
                smalladd(n,add);
            }
            field(c.word,cursor,p.width,v);cursor+=p.width;
            if(c.events==UINT64_MAX)throw std::runtime_error("event overflow");
            ++c.events;
            if(c.word.length()>max_bits||n.length()>max_bits)return "space_limit";
        }
        ++c.rounds;return "complete";
    }
    std::string round(Checkpoint& c,u64 max_bits,Clock::time_point deadline)const {
        return sparse_counter?round_impl<Counter>(c,max_bits,deadline):round_impl<Bits>(c,max_bits,deadline);
    }
};
void selftest() {
    std::mt19937_64 rng(405482);
    using u128=__uint128_t;
    for(unsigned trial=0;trial<1000;++trial) {
        Bits x(rng());u128 ref=x.words[0];
        for(unsigned j=0;j<100;++j) {
            unsigned width=static_cast<unsigned>(1+rng()%14),pos=static_cast<unsigned>(rng()%100);
            u64 value=rng()&((u64(1)<<width)-1);
            field(x,pos,width,value);
            ref=(ref&~(((u128(1)<<width)-1)<<pos))|(u128(value)<<pos);
            unsigned shift=static_cast<unsigned>(rng()%4);x.right(shift);ref>>=shift;
            const unsigned up=static_cast<unsigned>(rng()%4);if(x.length()+up<=128){left(x,up);ref<<=up;}
            for(unsigned p=0;p<128;p+=7)if(peek(x,p,14)!=static_cast<u64>((ref>>p)&16383))
                throw std::runtime_error("bit-field mismatch");
            if(peek(x,0,64)!=static_cast<u64>(ref)||peek(x,64,64)!=static_cast<u64>(ref>>64))
                throw std::runtime_error("wide field mismatch");
            if(from_hex(x.hex()).hex()!=x.hex())throw std::runtime_error("hex mismatch");
        }
    }
    u64 counter_cases=0;
    for(unsigned trial=0;trial<200;++trial) {
        Counter c(1);Bits reference(1);
        const u64 initial_power=trial%2?512+rng()%10000:rng()%64;
        c.exponent=initial_power;left(reference,initial_power);
        for(unsigned j=0;j<1000;++j) {
            const unsigned operation=static_cast<unsigned>(rng()%4);
            if(operation==0) {const u64 shift=rng()%9;left(c,shift);left(reference,shift);}
            else if(operation==1){const u64 shift=rng()%9;c.right(shift);reference.right(shift);}
            else if(operation==2){const u64 value=rng()%256;smalladd(c,value);smalladd(reference,value);}
            else if(reference.length()>8){const u64 value=rng()%256;smallsub(c,value);smallsub(reference,value);}
            if(c.length()!=reference.length()||peek(c,0,16)!=peek(reference,0,16))
                throw std::runtime_error("sparse counter mismatch");
            if(j%40==0) {Counter copy=c;copy.materialize();if(copy.dense.hex()!=reference.hex())throw std::runtime_error("sparse materialization mismatch");}
            ++counter_cases;
        }
    }
    u64 window_cases=0;
    for(unsigned entry:{405u,482u}) {
        Engine engine(entry);
        for(unsigned key=0;key<engine.windows.size();++key) {
            const auto& w=engine.windows[key];
            if(w.events<2)continue;
            for(u64 h:{u64(1),u64(2),u64(1)+(rng()&((u64(1)<<48)-1))}) {
                u128 n=u128(h)*16+(key&15);unsigned cursor=0,output=0;
                for(unsigned j=0;j<w.events;++j) {
                    const int id=engine.decode[((key>>4)>>cursor)&16383];
                    if(id<0)throw std::runtime_error("window decoder mismatch");
                    const auto& p=engine.packets[static_cast<unsigned>(id)];
                    if(n<p.pre.size()||!n)throw std::runtime_error("window branch mismatch");
                    n-=p.pre.size();const u64 r=static_cast<u64>(n%p.cycle.size());n/=p.cycle.size();
                    u64 total=0,add=0;
                    for(auto x:p.cycle)total+=x.second;
                    for(auto x:p.pre)add+=x.second;
                    for(u64 i=0;i<r;++i)add+=p.cycle[i].second;
                    n=n*total+add;output|=static_cast<unsigned>(p.cycle[r].first<<cursor);cursor+=p.width;
                }
                const u128 expected=w.bias<0?(u128(h)<<w.exponent)-static_cast<unsigned>(-w.bias)
                                                :(u128(h)<<w.exponent)+static_cast<unsigned>(w.bias);
                if(n!=expected||output!=w.output||cursor!=w.width)throw std::runtime_error("window composition mismatch");
                ++window_cases;
            }
        }
    }
    std::cout<<"{\"selftest\":\"passed\",\"field_operations\":100000,\"window_cases\":"<<window_cases<<",\"counter_operations\":"<<counter_cases<<"}\n";
}
int main(int argc,char**argv)try {
    unsigned entry=405;u64 budget=100000,max_bits=2000000;double seconds=60;
    std::string input,output;bool hex=false,single=false,no_prefix=false;int counter_mode=0;
    for(int i=1;i<argc;++i) {
        const std::string o=argv[i];
        if(o=="--selftest"){selftest();return 0;}
        if(o=="--hex"){hex=true;continue;}
        if(o=="--single"){single=true;continue;}
        if(o=="--no-prefix"){no_prefix=true;continue;}
        if(o=="--dense-counter"){if(counter_mode==1)throw std::runtime_error("conflicting counter modes");counter_mode=-1;continue;}
        if(o=="--sparse-counter"){if(counter_mode==-1)throw std::runtime_error("conflicting counter modes");counter_mode=1;continue;}
        if(o=="--help"){std::cout<<"--entry 405|482 --rounds N --seconds S --max-bits N --resume PATH --checkpoint PATH --hex --single --no-prefix --dense-counter --sparse-counter --selftest\n";return 0;}
        if(++i==argc)throw std::runtime_error("missing argument");
        const std::string v=argv[i];
        if(o=="--entry"){u64 n=integer(v);if(n!=405&&n!=482)throw std::runtime_error("unsupported entry");entry=static_cast<unsigned>(n);}
        else if(o=="--rounds")budget=integer(v);
        else if(o=="--seconds"){size_t end;seconds=std::stod(v,&end);if(end!=v.size())throw std::runtime_error("invalid time");}
        else if(o=="--max-bits")max_bits=integer(v);
        else if(o=="--resume")input=v;else if(o=="--checkpoint")output=v;else throw std::runtime_error("unknown argument");
    }
    if(!std::isfinite(seconds)||seconds<=0||seconds>1e7||max_bits<8||max_bits>100000000)
        throw std::runtime_error("invalid budget");
    Checkpoint c=input.empty()?Checkpoint{}:resume(input,entry);
    if(c.word.length()>max_bits)throw std::runtime_error("checkpoint exceeds bit budget");
    const u64 base=c.rounds;if(budget>UINT64_MAX-base)throw std::runtime_error("round overflow");
    const bool dense_counter=counter_mode==-1||(counter_mode==0&&entry==482);
    Engine engine(entry,single,dense_counter,no_prefix);auto start=Clock::now();
    auto deadline=start+std::chrono::duration_cast<Clock::duration>(std::chrono::duration<double>(seconds));
    double saved=0;std::string status="round_limit";
    while(c.rounds<base+budget) {
        if(Clock::now()>=deadline){status="time_limit";break;}
        Checkpoint previous=c;std::string result=engine.round(c,max_bits,deadline);
        if(result!="complete"){c=std::move(previous);status=result;break;}
        double elapsed=std::chrono::duration<double>(Clock::now()-start).count();
        if(elapsed-saved>=30){save(output,entry,c);saved=elapsed;}
    }
    save(output,entry,c);
    std::cout<<std::setprecision(17)<<"{\"verified\":false,\"entry\":"<<entry<<",\"status\":\""<<status
       <<"\",\"rounds\":"<<c.rounds<<",\"prefix_skip\":"<<(no_prefix?"false":"true")<<",\"counter_fallbacks\":"<<Counter::fallbacks<<",\"sparse_counter\":"<<(dense_counter?"false":"true")<<",\"window_bits\":"<<(single?0:16)<<",\"new_rounds\":"<<c.rounds-base<<",\"events\":"<<c.events
       <<",\"word_bits\":"<<c.word.length()<<",\"seconds\":"<<std::chrono::duration<double>(Clock::now()-start).count();
    if(hex)std::cout<<",\"word_hex\":\""<<c.word.hex()<<"\"";
    std::cout<<"}\n";return 0;
}catch(const std::exception& e){std::cerr<<"error: "<<e.what()<<'\n';return 1;}
