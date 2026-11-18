#pragma once
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
    Index(const std::string& path,const ternary17::Tables& t,unsigned threads){
        
        whole.resize(t.count);std::iota(whole.begin(),whole.end(),0);
        std::deque<Token> tail;
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
};
struct Stats {std::array<unsigned char,7> slots{},marks{};};
struct EmitTable {
    const ternary17::Tables& t;
    std::vector<B> packet;std::vector<Stats> stats;
    std::array<U,250> full{};
    explicit EmitTable(const ternary17::Tables& tbl):t(tbl){
        packet.resize(t.count*t.rows.size());stats.resize(packet.size());
        for(unsigned c=0;c<250;++c)full[c]=t.token[16][c]*t.count;
        for(unsigned n=1;n<=16;++n)for(unsigned c=0;c<250;++c){
            if(t.mask[c]>=(1u<<n))continue;
            unsigned id=t.token[n][c];
            for(U state=0;state<t.count;++state){
                B w=t.mask[c];unsigned width=n;U v=state,finish=0;
                auto& costs=stats[id*t.count+state];
                for(unsigned d=0;d<t.depth;++d){
                    auto out=ternary17::stepword(v%3,w,width);v/=3;
                    finish+=t.powers[d]*out.state;w=out.bits;width=out.n;
                    costs.slots[d]=width;costs.marks[d]=__builtin_popcountll(w);
                }
                if(width>42||finish!=t.rows[id][state])throw std::logic_error("virtual packet disagrees with index");
                packet[id*t.count+state]=(w<<22)|(B(width)<<16)|finish;
            }
        }
    }
};
struct Raw {unsigned n=0;std::vector<B> data;};
Raw emit(const Source& in,U start,U end,std::vector<B>& hist,const EmitTable& table) {
    Raw out;out.data.reserve(in.slots/192+3);U state=start;B acc=0;unsigned shift=0;
    auto push=[&](U row){
        auto id=row+state;auto p=table.packet[id];++hist[id];
        state=p&65535;unsigned n=(p>>16)&63;B bits=p>>22;
        acc|=bits<<shift;shift+=n;
        if(shift>=64){out.data.push_back(acc);shift-=64;acc=shift?bits>>(n-shift):0;}
    };
    for(auto [off,n]:in.frames){
        for(unsigned i=0;i<n/16;++i) push(table.full[in.bytes[off+i]]);
        if(n%16)push(table.t.token[n%16][in.bytes[off+n/16]]*table.t.count);
    }
    out.n=64*out.data.size()+shift;if(shift)out.data.push_back(acc);
    if(state!=end)throw std::logic_error("virtual stripe end");
    return out;
}
struct Pipe {
    using Output=std::vector<Raw>;
    std::mutex lock;std::condition_variable cv;std::deque<Output> queue;bool done=false;std::exception_ptr error;
    std::vector<tiled::TailDigit>& digits;const tiled::Tables& tables;std::thread thread;
    Pipe(std::vector<tiled::TailDigit>& d,const tiled::Tables& t):digits(d),tables(t),thread([this]{consume();}){}
    void consume()try {
        while(true){Output out;{
            std::unique_lock<std::mutex> lk(lock);cv.wait(lk,[&]{return done||!queue.empty();});
            if(queue.empty())return;out=std::move(queue.front());queue.pop_front();cv.notify_one();
        }
        for(const auto& frame:out)if(frame.n)tiled::feed_tail(digits,0,frame.data.data(),frame.n,tables);}
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
    if(argc!=8 && argc!=9)throw std::runtime_error("vrun FILE CUT DEPTH START_BASE_INDEX COPIES THREADS OUTPUT_PREFIX [PHASE_BATCH] < seed_register");
    std::string path=argv[1],outbase=argv[7],reg;
    const B base_cut=number(argv[2]), depth=number(argv[3]), workers=number(argv[6]);
    if(base_cut>424||!depth||depth>7||!workers||workers>64)
        throw std::runtime_error("invalid runner dimensions");
    const unsigned cut=base_cut,d=depth,threads=workers;
    B begin=number(argv[4]),copies=number(argv[5]),batch=argc==9?number(argv[8]):1;
    if(copies>UINT32_MAX || begin>UINT64_MAX-copies)throw std::runtime_error("invalid finite copy range");
    if(!batch||batch>32)throw std::runtime_error("invalid phase batch");
    std::cin>>reg;std::vector<U> states;U flag=0;
    if(reg.empty()||reg.size()%2||reg.size()>848) throw std::runtime_error("invalid register size");
    for(size_t i=0;i<reg.size();i+=2){
        if((reg[i]!='0'&&reg[i]!='1'&&reg[i]!='2')||(reg[i+1]!='2'&&reg[i+1]!='3')) throw std::runtime_error("invalid register encoding");
        states.push_back(2*(reg[i]=='1'?0:reg[i]=='0'?1:2)+flag);flag=reg[i+1]=='3';}
    if(cut+d>states.size())throw std::runtime_error("short seed register");
    ternary17::Tables vt(d);EmitTable emitters(vt);Index index(path,vt,threads);
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
    std::vector<tiled::TailDigit> tail(states.size()-cut-d);
    for(size_t i=0;i<tail.size();++i)tail[i].state=states[cut+d+i];
    tiled::Tables plain;
    std::array<B,7> slots{},marks{};const auto seed_debt=drain(s0,vt);
    for(B first=0;first<copies;){
        U g=std::min<B>(batch,copies-first);std::vector<Phase> phases(g);
        for(U q=0;q<g;++q){
            auto& p=phases[q];p.state=p.start=state;p.before=drain(index.inverse[state],vt);
            state=index.whole[state];p.after=drain(index.inverse[state],vt);
            if(q)p.spool=std::make_unique<Spool>();
            p.hist.assign(threads,std::vector<B>(emitters.packet.size()));
        }
        auto started=std::chrono::steady_clock::now();size_t cursor=0;
        Pipe pipe(tail,plain);Trim direct(pipe,phases[0].before.bits[d-1],phases[0].after.bits[d-1]);
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
            for(size_t v=0;v<count;++v)try{
                U q=v/b.size();output[v]=emit(b[v%b.size()],enter[v],end[v],phases[q].hist[worker_id()],emitters);
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
                Pipe delayed(tail,plain);Trim trim(delayed,p.before.bits[d-1],p.after.bits[d-1]);
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
            for(const auto& row:tail)tiled::write_row(row.state,row.slots,row.calls,row.interior,out);
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
