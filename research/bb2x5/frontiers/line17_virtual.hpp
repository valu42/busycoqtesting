#pragma once
#include <map>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <condition_variable>
#include <deque>
#include <mutex>
#include <thread>

namespace virtual17 {
using U=uint32_t;
using B=uint64_t;
unsigned worker_id() {
#ifdef _OPENMP
    return omp_get_thread_num();
#else
    return 0;
#endif
}

struct Physical {U state=0;B bits=0;unsigned n=0;};
Physical physical(U s,B w,unsigned n,unsigned depth) {
    Physical group;U mul=1;
    for(unsigned d=0;d<depth;++d){
        U dig=s%6;s/=6;U v=dig/2,p=dig%2;
        B next=0;unsigned len=0;
        for(unsigned i=0;i<n;++i){
            bool bit=(w>>i)&1;
            if(p&&bit)return {UINT32_MAX,0,0};
            if(p||bit){
                if(v==1)next|=B(2)<<len;
                len+=v?2:1;p=v!=0;v=(v+2)%3;
            }else{if(v==2)++len;v=(v+1)%3;}
            if(len>61)throw std::runtime_error("physical token width");
        }
        group.state+=mul*(2*v+p);mul*=6;w=next;n=len;
    }
    group.bits=w;group.n=n;return group;
}
int clear_value(U s,unsigned d) {
    U sum=0,mul=1;
    for(unsigned i=0;i<d;++i){
        if(s%2)return -1;
        sum+=mul*((s%6)/2);mul*=3;s/=6;
    }
    return sum;
}
struct Token {unsigned mask,width;};
std::vector<U> boundary(const std::deque<Token>& tail,const ternary17::Tables& t) {
    U dim=1;for(unsigned i=0;i<t.depth;++i)dim*=6;
    std::vector<U> live(dim);std::iota(live.begin(),live.end(),0);
    for(auto a:tail){
        for(auto& x:live)x=physical(x,a.mask,a.width,t.depth).state;
        std::sort(live.begin(),live.end());live.erase(std::unique(live.begin(),live.end()),live.end());
        if(!live.empty()&&live.back()==UINT32_MAX)live.pop_back();
    }
    std::vector<U> inverse(t.count,UINT32_MAX);
    for(auto s:live){
        U x=s,n=0;int value=0;
        while((value=clear_value(x,t.depth))<0){
            x=physical(x,0,1,t.depth).state;++n;
            if(x==UINT32_MAX || n>dim)throw std::runtime_error("end state has no clear completion");
        }
        U v=(value+t.count-(n%t.count))%t.count;
        if(inverse[v]!=UINT32_MAX)throw std::runtime_error("ambiguous physical endpoint");
        inverse[v]=s;
    }
    if(std::find(inverse.begin(),inverse.end(),UINT32_MAX)!=inverse.end())
        throw std::runtime_error("incomplete physical suffix image");
    return inverse;
}
struct Source {
    unsigned slots=0;
    std::vector<unsigned char> bytes;
    std::vector<std::pair<unsigned,unsigned>> frames;
    void add(unsigned n,const std::vector<unsigned char>& data){
        frames.emplace_back(bytes.size(),n);bytes.insert(bytes.end(),data.begin(),data.end());slots+=n;
    }
};
using Batch=std::vector<Source>;
template<class Func>void read_source(const std::string& path,unsigned batch_size,Func visit) {
    std::ifstream file(path,std::ios::binary);if(!file)throw std::runtime_error("cannot open coded source");
    unsigned n;std::vector<unsigned char> bytes;Batch jobs;Source job;
    while(tiled::coded::read_frame_size(file,n)){
        if(!n||n>(1u<<22))throw std::runtime_error("invalid coded frame");
        bytes.resize((n+15)/16);
        if(!file.read((char*)bytes.data(),bytes.size()))throw std::runtime_error("short frame");
        if(std::any_of(bytes.begin(),bytes.end(),[](unsigned char c){return c>=250;})) throw std::runtime_error("invalid coded symbol");
        job.add(n,bytes);
        if(job.slots>=1048576){jobs.push_back(std::move(job));job=Source{};}
        if(jobs.size()>=batch_size){visit(jobs);jobs.clear();}
    }
    if(!file.eof())throw std::runtime_error("bad source file");
    if(job.slots)jobs.push_back(std::move(job));if(!jobs.empty())visit(jobs);
}
struct StripeAction {
    std::vector<unsigned char> coordinates;
    void assign(const std::vector<U>& action) {
        if(action.size()<=256) {
            coordinates.assign(action.begin(),action.end());
            return;
        }
        unsigned fields=action.size()==729?2:5;
        coordinates.resize(243*fields);
        for(unsigned v=0;v<243;++v){
            auto high=[&](unsigned s){return action[v+243*s]/243;};
            coordinates[v*fields]=action[v]%243;
            coordinates[v*fields+1]=ternary17::Tables::action_code(high(0)%3,high(1)%3);
            if(fields==5)for(unsigned a=0;a<3;++a)
                coordinates[v*fields+2+a]=ternary17::Tables::action_code(high(a)/3,high(a+3)/3);
        }
    }
    U operator[](U s) const {
        if(coordinates.size()<=256) return coordinates[s];
        const unsigned fields=coordinates.size()/243,v=s%243,a=s/243%3,b=s/729;
        const auto* data=coordinates.data()+v*fields;
        auto eval=[](unsigned g,unsigned x){return (g%3+(g>=3?2*x:x))%3;};
        U out=data[0]+243*eval(data[1],a);
        if(fields==5)out+=729*eval(data[2+a],b);
        return out;
    }
};
struct Index{
    std::vector<StripeAction> maps;
    std::vector<U> whole,inverse;
    B slots=0,marks=0;
    std::deque<Token> tail;
    Index(const std::string& path,const ternary17::Tables& t,unsigned threads){
        
        whole.resize(t.count);std::iota(whole.begin(),whole.end(),0);
        read_source(path,threads*5,[&](const Batch& jobs){
            size_t first=maps.size();maps.resize(first+jobs.size());
            std::vector<B> ms(jobs.size());
            #pragma omp parallel for num_threads(threads) schedule(static)
            for(size_t j=0;j<jobs.size();++j){
                const auto& b=jobs[j];ternary17::Tokens tok;tok.reserve(b.bytes.size());
                for(auto [off,n]:b.frames)for(unsigned i=0;i<(n+15)/16;++i){
                    unsigned c=b.bytes[off+i];
                    unsigned width=std::min(16u,n-16*i);
                    tok.push_back(t.token[width][c]);ms[j]+=__builtin_popcount(t.mask[c]&((1u<<width)-1));
                }
                auto act=ternary17::act(t,tok);maps[first+j].assign(act);
            }
            for(size_t j=0;j<jobs.size();++j){
                const auto& b=jobs[j];const auto& m=maps[first+j];
                slots+=b.slots;marks+=ms[j];for(auto& x:whole)x=m[x];
                // Only the final 128 input tokens are needed to check the phase.
                if(b.bytes.size()>128)tail.clear();
                for(auto [off,n]:b.frames)for(unsigned i=0;i<(n+15)/16;++i){
                    if(off+i+128<b.bytes.size())continue;
                    tail.push_back({t.mask[b.bytes[off+i]],std::min(16u,n-16*i)});
                    if(tail.size()>128)tail.pop_front();
                }
            }
        });
        inverse=boundary(tail,t);
    }
    // The cache contains only stripe actions and the original trailing
    // tokens. Recompose the full period and recover physical endpoints on
    // reload. The driver binds this file to the exact source bytes by SHA-256.
    void save(const std::string& path,const ternary17::Tables& t) const {
        std::ofstream out(path,std::ios::binary);
        out<<"BB25-L17-PHASE-1\n"<<t.depth<<' '<<slots<<' '<<marks<<' '<<maps.size()<<' '<<tail.size()<<'\n';
        for(auto token:tail)out<<token.mask<<' '<<token.width<<'\n';
        for(const auto& map:maps)out.write(reinterpret_cast<const char*>(map.coordinates.data()),map.coordinates.size());
        out.close();
        if(!out)throw std::runtime_error("failed to write phase index");
    }
    Index(std::istream& input,const ternary17::Tables& t){
        std::string magic;
        std::getline(input,magic);
        U depth=0,count_tail=0;B rows=0;
        if(magic!="BB25-L17-PHASE-1" || !(input>>depth>>slots>>marks>>rows>>count_tail)
            || depth!=t.depth || !rows || !slots || marks>slots || count_tail>128 || !count_tail)
            throw std::runtime_error("invalid phase index header");
        for(U i=0;i<count_tail;++i){
            Token a{};
            if(!(input>>a.mask>>a.width)||!a.width||a.width>16||a.mask>=65536||t.code[a.mask]==255)
                throw std::runtime_error("invalid phase index suffix");
            tail.push_back(a);
        }
        if(input.get()!='\n')throw std::runtime_error("invalid phase index separator");
        const auto offset=input.tellg();
        input.seekg(0,std::ios::end);
        const auto remaining=input.tellg()-offset;
        const U fields=t.count<=256?1:t.count==729?2:5;
        const U size=fields==1?t.count:243*fields;
        if(remaining<=0 || B(remaining)%size || B(remaining)/size!=rows)
            throw std::runtime_error("invalid phase index extent");
        input.seekg(offset);
        whole.resize(t.count);std::iota(whole.begin(),whole.end(),0);
        maps.resize(rows);
        for(auto& map:maps){
            map.coordinates.resize(size);
            if(!input.read(reinterpret_cast<char*>(map.coordinates.data()),size))
                throw std::runtime_error("truncated phase index");
            for(U i=0;i<size;++i){
                const U limit=fields==1?t.count:(i%fields?6:243);
                if(map.coordinates[i]>=limit)throw std::runtime_error("invalid phase coordinates");
            }
            for(auto& s:whole)s=map[s];
        }
        inverse=boundary(tail,t);
    }

};
struct Stats {std::array<unsigned char,7> slots{},marks{};};
// Split each token action at the third trit. A complete sixteen-slot token
// has only 160 possible emitted words there, across all symbols and states.
// The upper table is shared by every occurrence of each distinct word.
struct EmitTable {
    const ternary17::Tables& t;
    struct Word {
        B bits;
        unsigned width;
        bool operator<(const Word& rhs) const {
            return width<rhs.width || (width==rhs.width && bits<rhs.bits);
        }
    };
    struct Partial {
        U end=0;
        Word word{};
        Stats costs{};
    };
    U lower_depth,lower_states,upper_states,upper_offset;
    std::vector<U> lower;
    std::vector<B> upper;
    std::vector<Stats> stats;
    std::array<U,250> full{};
    static Partial act(U state,Word in,unsigned first,unsigned last) {
        Partial out;out.word=in;U multiplier=1;
        for(unsigned i=first;i<last;++i) {
            auto step=ternary17::stepword(state%3,out.word.bits,out.word.width);
            state/=3;out.end+=multiplier*step.state;multiplier*=3;
            out.word={step.bits,step.n};
            out.costs.slots[i]=step.n;out.costs.marks[i]=__builtin_popcountll(step.bits);
        }
        return out;
    }
    explicit EmitTable(const ternary17::Tables& table):t(table) {
        lower_depth=std::min<U>(3,t.depth);
        lower_states=t.powers[lower_depth];upper_states=t.count/lower_states;
        upper_offset=lower_states*t.rows.size();
        lower.resize(upper_offset);stats.resize(upper_offset);
        std::map<Word,U> unique;
        for(unsigned i=0;i<250;++i)full[i]=t.token[16][i]*lower_states;
        for(unsigned n=1;n<=16;++n)for(unsigned c=0;c<250;++c){
            if(t.mask[c]>=(1u<<n))continue;
            U index=t.token[n][c]*lower_states;
            for(U state=0;state<lower_states;++state){
                auto partial=act(state,{t.mask[c],n},0,lower_depth);
                const auto [it,inserted]=unique.emplace(partial.word,unique.size());
                lower[index+state]=((it->second*upper_states)<<5)|partial.end;
                stats[index+state]=partial.costs;
            }
        }
        upper.resize(unique.size()*upper_states);
        stats.resize(upper_offset+upper.size());
        for(auto [word,id]:unique)for(U state=0;state<upper_states;++state){
            U index=id*upper_states+state;
            auto partial=act(state,word,lower_depth,t.depth);
            if(partial.word.width>42||partial.end>=128)throw std::logic_error("split emission packet too wide");
            upper[index]=(partial.word.bits<<16)|(B(partial.word.width)<<8)|partial.end;
            stats[upper_offset+index]=partial.costs;
        }
        for(U row=0;row<t.rows.size();++row)for(U state=0;state<t.count;++state) {
            U lo=lower[row*lower_states+state%lower_states];
            B hi=upper[(lo>>5)+state/lower_states];
            if((lo&31)+lower_states*(hi&127)!=t.rows[row][state])
                throw std::logic_error("split tables disagree with exact phase action");
        }
    }
};
struct Raw {unsigned n=0;std::vector<B> data;};
template<unsigned Width>
void emit_together(const Source& source, const std::array<U,Width>& begin,
                   const std::array<U,Width>& expected_end, const std::array<B*,Width>& hist,
                   std::array<Raw*,Width>& output, const EmitTable& table) {
    std::array<U,Width> lower{},upper{},shift{};
    std::array<B,Width> accumulator{};
    for(unsigned j=0;j<Width;++j){
        lower[j]=begin[j]%table.lower_states;
        upper[j]=begin[j]/table.lower_states;
        output[j]->data.reserve(source.slots/192+3);
    }
    auto push=[&](U row){
        std::array<U,Width> upper_row{};
        for(unsigned j=0;j<Width;++j){
            U id=row+lower[j],action=table.lower[id];
            ++hist[j][id];lower[j]=action&31;upper_row[j]=(action>>5)+upper[j];
        }
        for(unsigned j=0;j<Width;++j){
            U id=upper_row[j];
            B p=table.upper[id];
            ++hist[j][table.upper_offset+id];upper[j]=p&127;
            unsigned width=(p>>8)&63;B bits=p>>16;
            accumulator[j]|=bits<<shift[j];shift[j]+=width;
            if(shift[j]>=64){
                output[j]->data.push_back(accumulator[j]);shift[j]-=64;
                accumulator[j]=shift[j]?bits>>(width-shift[j]):0;
            }
        }
    };
    for(auto [off,n]:source.frames){
        for(unsigned i=0;i<n/16;++i)push(table.full[source.bytes[off+i]]);
        if(n%16)push(table.t.token[n%16][source.bytes[off+n/16]]*table.lower_states);
    }
    for(unsigned j=0;j<Width;++j){
        auto& out=*output[j];out.n=64*out.data.size()+shift[j];
        if(shift[j])out.data.push_back(accumulator[j]);
        if(lower[j]+table.lower_states*upper[j]!=expected_end[j])
            throw std::logic_error("split phase endpoint disagrees with the index");
    }
}

// Three physical digits share a byte transfer. The cost packet has one
// ten-bit slot field and one ten-bit mark field per digit. Bounded local
// chunks can add packets directly without carries between fields.
struct TailPackets {
    struct Packet { B word=0,cost=0; };
    struct Level {
        unsigned depth,states;
        std::vector<Packet> packets;
        explicit Level(unsigned size):depth(size),states(1){
            for(unsigned i=0;i<size;++i)states*=6;
            packets.resize(511*states);
            for(unsigned n=1;n<=8;++n)for(unsigned word=0;word<(1u<<n);++word){
                unsigned token=(1u<<n)-1+word;
                for(unsigned start=0;start<states;++start){
                    unsigned state=start,length=n,finish=0,mul=1;
                    B bits=word,cost=0;bool valid=true;
                    for(unsigned digit=0;digit<depth;++digit){
                        auto x=physical(state%6,bits,length,1);
                        if(x.state==UINT32_MAX){valid=false;break;}
                        state/=6;finish+=mul*x.state;mul*=6;
                        bits=x.bits;length=x.n;
                        if(length>31)throw std::logic_error("physical byte cost field");
                        cost|=B(length)<<(20*digit);
                        cost|=B(__builtin_popcountll(bits))<<(20*digit+10);
                    }
                    auto& p=packets[token*states+start];
                    if(valid){p.word=(bits<<16)|(B(length)<<8)|finish;p.cost=cost;}
                    else p.word=255;
                }
            }
        }
    };
    std::array<Level,3> levels{Level(1),Level(2),Level(3)};
};
struct PhysicalTail {
    struct Block {
        unsigned state=0;
        std::array<B,3> slots{},marks{};
        Raw buffer;
    };
    const TailPackets& tables;
    std::vector<U> initial;
    std::vector<Block> blocks;
    PhysicalTail(const std::vector<U>& states,const TailPackets& tab):tables(tab),initial(states) {
        blocks.resize((states.size()+2)/3);
        for(size_t j=0;j<states.size();++j)blocks[j/3].state+=states[j]*(j%3==0?1:j%3==1?6:36);
    }
    void feed(const Raw& source){
        const Raw* input=&source;
        for(size_t k=0;k<blocks.size()&&input->n;++k){
            auto& b=blocks[k];auto& out=b.buffer;
            const unsigned d=std::min<size_t>(3,initial.size()-3*k);
            const auto& tab=tables.levels[d-1];
            const auto* full=tab.packets.data()+255*tab.states;
            out.data.clear();out.data.reserve(input->n/64+2);
            B acc=0,cost=0;unsigned shift=0;U state=b.state;
            auto push=[&](const TailPackets::Packet* row){
                auto p=row[state];state=p.word&255;
                if(state==255)throw std::runtime_error("overlapping marked bursts in physical suffix");
                unsigned width=(p.word>>8)&31;B bits=p.word>>16;
                acc|=bits<<shift;cost+=p.cost;shift+=width;
                if(shift>=64){out.data.push_back(acc);shift-=64;acc=shift?bits>>(width-shift):0;}
            };
            auto collect=[&]{
                for(unsigned j=0;j<d;++j){b.slots[j]+=cost&1023;cost>>=10;b.marks[j]+=cost&1023;cost>>=10;}
                cost=0;
            };
            unsigned bytes=input->n/8,at=0;
            for(;at<bytes;){
                unsigned stop=std::min(at+32,bytes);
                for(;at<stop;++at){auto word=(input->data[at/8]>>(8*(at%8)))&255;push(full+word*tab.states);}
                collect();
            }
            if(auto rem=input->n%8){
                auto word=(input->data[at/8]>>(8*(at%8)))&((1u<<rem)-1);
                push(tab.packets.data()+((1u<<rem)-1+word)*tab.states);collect();
            }
            out.n=64*out.data.size()+shift;if(shift)out.data.push_back(acc);
            b.state=state;input=&out;
        }
    }
    void write(std::ostream& stream,B inputs,B input_marks) const {
        for(size_t j=0;j<initial.size();++j){
            const auto& block=blocks[j/3];unsigned pos=j%3;
            U state=block.state/(pos==0?1:pos==1?6:36)%6,old=initial[j];
            B slots=block.slots[pos],marks=block.marks[pos];
            if(3*slots+state/2<inputs+old/2)throw std::logic_error("negative physical burst count");
            B scaled=3*slots+state/2-inputs-old/2;
            if(scaled%4)throw std::logic_error("physical suffix trit balance");
            B calls=inputs+2*(scaled/4)+input_marks+old%2-state%2;
            tiled::write_row(state,slots,calls,2*(slots+marks),stream);
            inputs=slots;input_marks=marks;
        }
    }
};

struct Pipe {
    using Output=std::vector<Raw>;
    std::mutex lock;std::condition_variable cv;std::deque<Output> queue;bool done=false;std::exception_ptr error;
    PhysicalTail& digits;std::thread thread;
    explicit Pipe(PhysicalTail& d):digits(d),thread([this]{consume();}){}
    void consume()try {
        while(true){Output out;{
            std::unique_lock<std::mutex> lk(lock);cv.wait(lk,[&]{return done||!queue.empty();});
            if(queue.empty())return;out=std::move(queue.front());queue.pop_front();cv.notify_one();
        }
        for(const auto& frame:out)if(frame.n)digits.feed(frame);}
    }catch(...){std::lock_guard<std::mutex> lk(lock);error=std::current_exception();done=true;cv.notify_all();}
    void send(Output&& out){
        std::unique_lock<std::mutex> lk(lock);cv.wait(lk,[&]{return done||queue.size()<4;});
        if(error)std::rethrow_exception(error);queue.push_back(std::move(out));cv.notify_one();
    }
    void finish(){{std::lock_guard<std::mutex> lk(lock);done=true;cv.notify_all();}thread.join();if(error)std::rethrow_exception(error);}
    ~Pipe(){if(thread.joinable()){{std::lock_guard<std::mutex> lk(lock);done=true;cv.notify_all();}thread.join();}}
};
// Pending bursts have already emitted a short suffix in the virtual stream.
// With no new marks the physical machine emits that debt, then only zeros.
struct Debt {
    U virtual_state=0;
    std::array<std::vector<unsigned char>,7> bits;
};
Debt drain(U physical_state,const ternary17::Tables& t) {
    Debt debt;U s=physical_state,elapsed=0;
    while(clear_value(s,t.depth)<0){
        U input=0,n=1,newstate=0,power=1;
        for(unsigned j=0;j<t.depth;++j){
            auto step=physical(s%6,input,n,1);s/=6;
            if(step.state==UINT32_MAX)throw std::logic_error("conflicting boundary debt");
            newstate+=power*step.state;power*=6;input=step.bits;n=step.n;
            for(unsigned i=0;i<n;++i)debt.bits[j].push_back((step.bits>>i)&1);
        }
        s=newstate;
        if(++elapsed>6*t.count)throw std::runtime_error("unresolved virtual burst");
    }
    debt.virtual_state=(U(clear_value(s,t.depth))+t.count-elapsed%t.count)%t.count;
    for(unsigned j=0;j<t.depth;++j){
        U q=t.powers[j+1],zeros=(debt.virtual_state%q+elapsed)/q;
        auto& bits=debt.bits[j];
        if(zeros>bits.size()||std::find(bits.end()-zeros,bits.end(),1)!=bits.end())
            throw std::logic_error("invalid ordinary continuation of virtual burst");
        bits.resize(bits.size()-zeros);
    }
    return debt;
}
Raw raw_bits(const std::vector<unsigned char>& bits) {
    Raw frame;frame.n=bits.size();frame.data.resize((frame.n+63)/64);
    for(size_t i=0;i<bits.size();++i)frame.data[i/64]|=B(bits[i])<<(i%64);
    return frame;
}
struct Trim {
    Pipe& pipe;const std::vector<unsigned char>& owed;std::deque<Raw> guard;B slots=0;
    Trim(Pipe& target,const std::vector<unsigned char>& before,const std::vector<unsigned char>& after):
        pipe(target),owed(after) {if(!before.empty()){Pipe::Output p;p.push_back(raw_bits(before));pipe.send(std::move(p));}}
    void feed(Pipe::Output&& frames){
        if(owed.empty()){pipe.send(std::move(frames));return;}
        Pipe::Output out;
        for(auto& f:frames)if(f.n){
            slots+=f.n;guard.push_back(std::move(f));
            while(!guard.empty()&&slots-guard.front().n>=owed.size()){
                slots-=guard.front().n;out.push_back(std::move(guard.front()));guard.pop_front();
            }
        }
        if(!out.empty())pipe.send(std::move(out));
    }
    void finish(){
        if(owed.empty())return;
        if(slots<owed.size())throw std::runtime_error("virtual period shorter than pending suffix");
        auto keep=slots-owed.size();B pos=0;Pipe::Output out;
        for(auto& frame:guard){
            for(B j=keep>pos?keep-pos:0;j<frame.n;++j)
                if(((frame.data[j/64]>>(j%64))&1)!=owed.at(pos+j-keep))throw std::logic_error("pending suffix disagrees with emitted word");
            auto old=frame.n;frame.n=pos<keep?std::min<B>(frame.n,keep-pos):0;pos+=old;
            if(frame.n)out.push_back(std::move(frame));
        }
        if(!out.empty())pipe.send(std::move(out));
    }
};
struct Spool {
    FILE* f=nullptr;
    explicit Spool() {
        char file[]="line17-phase-XXXXXX";int fd=mkstemp(file);
        if(fd<0)throw std::runtime_error("cannot open temporary phase file");
        if(unlink(file)!=0){close(fd);throw std::runtime_error("cannot unlink phase file");}
        f=fdopen(fd,"w+b");if(!f){close(fd);throw std::runtime_error("cannot open phase stream");}
    }
    ~Spool(){if(f)fclose(f);}
    void write(const Raw& r,const ternary17::Tables& t){
        if(!r.n)return;std::vector<unsigned char> b((r.n+15)/16);
        for(unsigned i=0;i<b.size();++i){
            unsigned width=std::min(16u,r.n-16*i);
            unsigned word=(r.data[i/4]>>(16*(i%4)))&((1u<<width)-1);
            b[i]=t.code[word];if(b[i]==255)throw std::logic_error("phase spool mark gap");
        }
        if(fwrite(&r.n,4,1,f)!=1||fwrite(b.data(),1,b.size(),f)!=b.size())throw std::runtime_error("phase spool write failed");
    }
    void replay(Trim& dest,const ternary17::Tables& t){
        if(fseeko(f,0,SEEK_SET)!=0)throw std::runtime_error("phase spool rewind failed");
        std::vector<unsigned char>b;Pipe::Output batch;unsigned n;
        while(fread(&n,4,1,f)==1){
            Raw r;r.n=n;b.resize((n+15)/16);r.data.resize((n+63)/64);
            if(fread(b.data(),1,b.size(),f)!=b.size())throw std::runtime_error("short phase spool");
            for(unsigned i=0;i<b.size();++i){if(b[i]>=250)throw std::runtime_error("invalid spool code");r.data[i/4]|=B(t.mask[b[i]])<<(16*(i%4));}
            batch.push_back(std::move(r));if(batch.size()==128){dest.feed(std::move(batch));batch.clear();}
        }
        if(ferror(f))throw std::runtime_error("phase spool read failed");
        if(!batch.empty())dest.feed(std::move(batch));
    }
};
using Histogram=std::vector<std::vector<B>>;
struct Phase {
    U start=0,state=0;
    Histogram hist;
    std::unique_ptr<Spool> spool;
    Debt before,after;
};
}
int virtual_advance(int argc,char**argv){
    using namespace virtual17;
    if(argc<8 || argc>10)throw std::runtime_error("vrun FILE CUT DEPTH START_BASE_INDEX COPIES THREADS OUTPUT_PREFIX [PHASE_BATCH [INDEX_FILE]] < seed_register");
    std::string path=argv[1],outbase=argv[7],reg;
    const B base_cut=number(argv[2]), depth=number(argv[3]), workers=number(argv[6]);
    if(base_cut>424||!depth||depth>7||!workers||workers>64)
        throw std::runtime_error("invalid runner dimensions");
    const unsigned cut=base_cut,d=depth,threads=workers;
    B begin=number(argv[4]),copies=number(argv[5]),batch=argc>=9?number(argv[8]):1;
    if(copies>UINT32_MAX || begin>UINT64_MAX-copies)throw std::runtime_error("invalid finite copy range");
    if(!batch||batch>32)throw std::runtime_error("invalid phase batch");
    std::cin>>reg;std::vector<U> states;U flag=0;
    if(reg.empty()||reg.size()%2||reg.size()>848) throw std::runtime_error("invalid register size");
    for(size_t i=0;i<reg.size();i+=2){
        if((reg[i]!='0'&&reg[i]!='1'&&reg[i]!='2')||(reg[i+1]!='2'&&reg[i+1]!='3')) throw std::runtime_error("invalid register encoding");
        states.push_back(2*(reg[i]=='1'?0:reg[i]=='0'?1:2)+flag);flag=reg[i+1]=='3';}
    if(cut+d>states.size())throw std::runtime_error("short seed register");
    ternary17::Tables vt(d);EmitTable emitters(vt);
    std::ifstream cache;
    if(argc==10){cache.open(argv[9],std::ios::binary);if(!cache)throw std::runtime_error("cannot open phase index");}
    Index index=argc==10?Index(cache,vt):Index(path,vt,threads);
    U state=(vt.count-1)/2;
    std::vector<U> orbit;
    do {
        if(orbit.size()>=vt.count)throw std::runtime_error("invalid source period orbit");
        orbit.push_back(state);state=index.whole[state];
    } while(state!=orbit.front());
    state=orbit[begin%orbit.size()];
    U s0=0,mul=1;for(U i=0;i<d;++i){s0+=mul*states[cut+i];mul*=6;}
    if(index.inverse[state]!=s0)throw std::runtime_error("seed is not the specified physical phase");
    if(index.slots && copies>(UINT64_MAX/32)/index.slots) throw std::overflow_error("finite pulse count limit");
    std::cerr<<"indexed "<<index.slots<<" slots and "<<index.marks<<" marks at "<<cut<<" from phase "<<begin<<std::endl;
    TailPackets physical_tables;
    PhysicalTail tail(std::vector<U>(states.begin()+cut+d,states.end()),physical_tables);
    std::array<B,7> slots{},marks{};const auto seed_debt=drain(s0,vt);
    for(B first=0;first<copies;){
        U g=std::min<B>(batch,copies-first);std::vector<Phase> phases(g);
        for(U q=0;q<g;++q){
            auto& p=phases[q];p.state=p.start=state;p.before=drain(index.inverse[state],vt);
            state=index.whole[state];p.after=drain(index.inverse[state],vt);
            if(q)p.spool=std::make_unique<Spool>();
            p.hist.assign(threads,std::vector<B>(emitters.stats.size()));
        }
        auto started=std::chrono::steady_clock::now();size_t cursor=0;
        Pipe pipe(tail);Trim direct(pipe,phases[0].before.bits[d-1],phases[0].after.bits[d-1]);
        read_source(path,threads*6,[&](const Batch& b){
            size_t count=g*b.size();std::vector<U> enter(count),end(count);
            std::vector<Raw> output(count);std::exception_ptr failure;
            for(U q=0;q<g;++q){
                auto& p=phases[q];
                for(size_t j=0;j<b.size();++j){
                    size_t v=q*b.size()+j;enter[v]=p.state;
                    p.state=index.maps.at(cursor+j)[p.state];end[v]=p.state;
                }
            }
            #pragma omp parallel for num_threads(threads) schedule(static)
            for(size_t j=0;j<b.size();++j)try{
                const unsigned lane=worker_id();
                auto group=[&](auto width,U first_phase) {
                    constexpr unsigned W=decltype(width)::value;
                    std::array<U,W> inputs,ends;std::array<B*,W> hist;
                    std::array<Raw*,W> outputs;
                    for(U i=0;i<W;++i){
                        size_t at=(first_phase+i)*b.size()+j;
                        inputs[i]=enter[at];ends[i]=end[at];outputs[i]=&output[at];
                        hist[i]=phases[first_phase+i].hist[lane].data();
                    }
                    emit_together<W>(b[j],inputs,ends,hist,outputs,emitters);
                };
                U q=0;
                for(;q+4<=g;q+=4)group(std::integral_constant<unsigned,4>{},q);
                if(q+2<=g){group(std::integral_constant<unsigned,2>{},q);q+=2;}
                if(q<g)group(std::integral_constant<unsigned,1>{},q);
            }catch(...){
                #pragma omp critical(virtual_emit_error)
                {if(!failure)failure=std::current_exception();}
            }
            if(failure)std::rethrow_exception(failure);
            Pipe::Output now;
            for(size_t j=0;j<b.size();++j)now.push_back(std::move(output[j]));
            direct.feed(std::move(now));
            for(U q=1;q<g;++q)for(size_t j=0;j<b.size();++j)phases[q].spool->write(output[q*b.size()+j],vt);
            cursor+=b.size();
        });
        direct.finish();pipe.finish();
        if(cursor!=index.maps.size())throw std::runtime_error("changed coded source");
        for(U q=0;q<g;++q){
            auto& p=phases[q];
            if(p.state!=index.whole[p.start])throw std::logic_error("phase return disagrees with index");
            if(q){
                Pipe delayed(tail);Trim trim(delayed,p.before.bits[d-1],p.after.bits[d-1]);
                p.spool->replay(trim,vt);trim.finish();delayed.finish();p.spool.reset();
            }
            B elapsed=first+q+1;
            for(const auto& h:p.hist)for(size_t id=0;id<h.size();++id)if(h[id]){
                const auto& c=emitters.stats[id];
                for(U i=0;i<d;++i){slots[i]+=h[id]*c.slots[i];marks[i]+=h[id]*c.marks[i];}
            }
            std::string name=outbase+std::to_string(begin+elapsed)+".counts",tmp=name+".tmp";std::ofstream out(tmp);
            out<<"base "<<begin<<' '<<begin+elapsed<<' '<<index.slots<<' '<<index.marks<<'\n';
            B n=index.slots*elapsed,m=index.marks*elapsed;U e=index.inverse[p.state];
            for(U j=0;j<d;++j){
                U end=e%6;e/=6;
                B physical_slots=slots[j]+seed_debt.bits[j].size()-p.after.bits[j].size();
                B physical_marks=marks[j]+std::count(seed_debt.bits[j].begin(),seed_debt.bits[j].end(),1)-
                    std::count(p.after.bits[j].begin(),p.after.bits[j].end(),1);
                B scaled=3*physical_slots+end/2-n-states[cut+j]/2;
                if(scaled%4)throw std::logic_error("virtual endpoint trit balance");
                tiled::write_row(end,physical_slots,n+2*(scaled/4)+m+states[cut+j]%2-end%2,2*(physical_slots+physical_marks),out);
                n=physical_slots;m=physical_marks;
            }
            tail.write(out,n,m);
            out.close();if(!out||std::rename(tmp.c_str(),name.c_str())!=0)throw std::runtime_error("interval output failed");
            std::cerr<<"base "<<begin+elapsed<<" physical "<<index.inverse[p.state]<<" group seconds "<<std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count()<<std::endl;
        }
        first+=g;
    }
    return 0;
}


int virtual_probe(int argc,char** argv) {
    using namespace virtual17;
    if(argc!=5)throw std::runtime_error("probe FILE BASE_CUT DEPTH THREADS");
    const auto cut=number(argv[2]),d=number(argv[3]),threads=number(argv[4]);
    if(d<1||d>7||threads<1||threads>64||cut>424-d)throw std::runtime_error("invalid probe dimensions");
    ternary17::Tables t(d);
    std::deque<std::pair<unsigned,unsigned>> suffix;
    auto start=std::chrono::steady_clock::now();
    const auto total=ternary17::scan(argv[1],t,threads,suffix);
    std::deque<Token> bits;
    for(auto [w,n]:suffix)bits.push_back({w,n});
    const auto physical_end=boundary(bits,t);
    const U s0=(t.count-1)/2;
    std::vector<U> orbit;
    for(U v=s0;;v=total[v]){
        if(!orbit.empty()&&v==s0)break;
        if(orbit.size()>=t.count)throw std::logic_error("nonpermuting virtual orbit");
        orbit.push_back(v);
    }
    U initial=0,scale=1;
    for(unsigned j=0;j<d;++j) {
        initial+=2*scale;scale*=6;
        if(physical_end[s0]%scale!=initial) throw std::runtime_error("nonzero physical preperiod at this source seam");
        size_t h=1;
        while(h<orbit.size()&&physical_end[orbit[h]]%scale!=initial)++h;
        std::cout<<cut+j+1<<" source-copies "<<h<<'\n';
    }
    std::cout<<"virtual-orbit";
    for(auto v:orbit)std::cout<<' '<<v;
    std::cout<<'\n';
    std::cerr<<"verified physical suffix of "<<suffix.size()<<" tokens in "
             <<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<" seconds\n";
    return 0;
}


int virtual_index(int argc,char** argv){
    if(argc!=5)throw std::runtime_error("index SOURCE DEPTH THREADS OUTPUT");
    auto d=number(argv[2]),threads=number(argv[3]);
    if(d<1||d>7||threads<1||threads>64)throw std::runtime_error("invalid index dimensions");
    ternary17::Tables t(d);
    virtual17::Index index(argv[1],t,threads);
    index.save(argv[4],t);
    return 0;
}
