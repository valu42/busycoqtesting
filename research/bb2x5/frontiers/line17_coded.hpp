// Chronological, byte-coded pulse blocks for the pure period of line 17.
// Each complete 16-slot block with mark gaps >= 4 has one of 250 bit masks.
// A block's final symbol carries an explicit length, so concatenation never
// inserts padding pulses. The original packed reader handles the early pairs.
#pragma once
#include <chrono>
#include <limits>
#include <fstream>
#include <string>
#include <utility>

namespace tiled::coded {
using Map = std::array<unsigned char,7>;
constexpr Map identity = {0,1,2,3,4,5,6};
constexpr unsigned job_slots = 262144;
constexpr size_t extent_bytes = 64u<<20;

Map compose(const Map& first,const Map& second) {
    Map result;
    for(unsigned s=0;s<7;++s) result[s]=second[first[s]];
    return result;
}

struct Alphabet {
    std::array<unsigned char,65536> code;
    std::array<unsigned,250> mask{};
    std::array<std::array<Packet,6>,250> packets{};
    std::array<StateMap,250> transitions{};
    Alphabet() {
        code.fill(255);
        unsigned k=0;
        for(unsigned w=0;w<65536;++w) {
            if (w&((w>>1)|(w>>2)|(w>>3))) continue;
            if (k>=mask.size()) throw std::logic_error("pulse alphabet too large");
            code[w]=k; mask[k]=w;
            transitions[k].fill(invalid);
            for(unsigned s=0;s<6;++s) {
                packets[k][s]=Packet::compile(s,w,16);
                transitions[k][s]=packets[k][s].state;
            }
            ++k;
        }
        if(k!=mask.size()) throw std::logic_error("pulse alphabet size");
    }
    Map action(const std::vector<unsigned char>& bytes, unsigned slots) const {
        Map result=identity;
        unsigned full=slots/16;
#ifdef __SSSE3__
        __m128i m=_mm_setr_epi8(0,1,2,3,4,5,6,6,6,6,6,6,6,6,6,6);
        for(unsigned j=0;j<full;++j)
            m=_mm_shuffle_epi8(_mm_loadu_si128(reinterpret_cast<const __m128i*>(transitions[bytes[j]].data())),m);
        alignas(16) unsigned char out[16];
        _mm_store_si128(reinterpret_cast<__m128i*>(out),m);
        std::copy_n(out,7,result.begin());
#else
        for(unsigned j=0;j<full;++j)
            for(auto& s:result) s=transitions[bytes[j]][s];
#endif
        if(unsigned tail=slots%16) {
            Map tail_map=identity;
            for(unsigned s=0;s<6;++s) tail_map[s]=Packet::compile(s,mask[bytes.back()],tail).state;
            result=compose(result,tail_map);
        }
        return result;
    }
};

struct Block {
    unsigned slots=0;
    Map map=identity;
    std::vector<unsigned char> bytes;
};

struct DiskFile {
    FILE* file=nullptr;
    size_t size=0;
    struct Frame {unsigned slots; Map map;};
    std::vector<Frame> frames;
    DiskFile() {
        char name[]="line17-coded-XXXXXX";
        int fd=mkstemp(name);
        if(fd<0) throw std::runtime_error("cannot create coded spool");
        if(unlink(name)!=0) {close(fd); throw std::runtime_error("cannot unlink coded spool");}
        file=fdopen(fd,"w+b");
        if(!file) {close(fd); throw std::runtime_error("cannot open coded spool");}
    }
    ~DiskFile() {if(file) fclose(file);}
    DiskFile(const DiskFile&)=delete;
};

struct Word {
    std::vector<std::unique_ptr<DiskFile>> files;
    Map map=identity;
    Count slots=0;
    void append(const Block& b) {
        if(!b.slots) return;
        if(files.empty() || files.back()->size>=extent_bytes) files.emplace_back(std::make_unique<DiskFile>());
        auto& f=*files.back();
        if(fwrite(b.bytes.data(),1,b.bytes.size(),f.file)!=b.bytes.size())
            throw std::runtime_error("coded spool write failed");
        f.frames.push_back({b.slots,b.map}); f.size+=b.bytes.size();
        slots+=b.slots; map=compose(map,b.map);
    }
    void join(Word&& other) {
        slots+=other.slots; map=compose(map,other.map);
        for(auto& f:other.files) files.push_back(std::move(f));
    }
};

// One job can contain several framed inputs. Keep their partial last symbols
// separate. The output is encoded as a single, new frame.
struct Job {
    std::vector<Block> blocks;
    Map map=identity;
    unsigned slots=0;
    void add(Block&& b) {
        slots+=b.slots; map=compose(map,b.map);
        blocks.push_back(std::move(b));
    }
};
using Batch=std::vector<Job>;

template<class Visit>
void read(Word& word, bool release, unsigned batch_size, Visit visit) {
    Batch batch;
    Job job;
    for(auto& fp:word.files) {
        auto& f=*fp;
        if(fseeko(f.file,0,SEEK_SET)!=0) throw std::runtime_error("coded spool seek failed");
        for(const auto& frame:f.frames) {
            Block b;
            b.slots=frame.slots; b.map=frame.map; b.bytes.resize((b.slots+15)/16);
            if(fread(b.bytes.data(),1,b.bytes.size(),f.file)!=b.bytes.size())
                throw std::runtime_error("short coded spool read");
            job.add(std::move(b));
            if(job.slots>=job_slots) {batch.push_back(std::move(job));job=Job{};}
            if(batch.size()==batch_size) {visit(batch);batch.clear();}
        }
        // All phase images for this extent have now consumed the same bytes.
        if(release) fp.reset();
    }
    if(job.slots) batch.push_back(std::move(job));
    if(!batch.empty()) visit(batch);
}

struct Image {
    Block block;
    unsigned end=0;
    Count calls=0, inner=0;
};

Image transform(const Job& job,unsigned start,const Alphabet& alphabet) {
    Image out;
    out.block.bytes.reserve(job.slots/20+8);
    unsigned state=start,left=0,full=0;
    Count acc=0;
    auto put_code=[&](unsigned w) {
        auto code=alphabet.code[w];
        if(code==255) throw std::runtime_error("encountered a pulse mask outside the coded alphabet");
        out.block.bytes.push_back(code);
    };
    auto emit=[&](const Packet& p) {
        if(p.state==invalid) throw std::runtime_error("overlapping marked bursts");
        state=p.state; out.calls+=p.calls; out.inner+=p.interior;
        acc|=Count(p.bits)<<left; left+=p.width;
        if(left>=32) {
            put_code(acc&65535);put_code((acc>>16)&65535);
            left-=32;acc>>=32;full+=32;
        }
    };
    for(const auto& b:job.blocks) {
        for(unsigned j=0;j<b.slots/16;++j) emit(alphabet.packets[b.bytes[j]][state]);
        if(unsigned tail=b.slots%16) emit(Packet::compile(state,alphabet.mask[b.bytes.back()],tail));
    }
    out.block.slots=full+left;
    if(left>=16) {put_code(acc&65535);left-=16;acc>>=16;}
    if(left) put_code(acc&65535);
    out.end=state;
    out.block.map=alphabet.action(out.block.bytes,out.block.slots);
    return out;
}

struct Counter {
    Count slots=0, calls=0, inner=0;
    void add(const Image& image) {
        if(slots>UINT64_MAX-image.block.slots || calls>UINT64_MAX-image.calls || inner>UINT64_MAX-image.inner)
            throw std::overflow_error("coded count overflow");
        slots+=image.block.slots;calls+=image.calls;inner+=image.inner;
    }
};

// The action stored for each input frame gives its exact entering state in a
// short serial scan. All phase copies of the same batch then share one read.
std::vector<Image> images(const Batch& batch,std::vector<unsigned>& phases,
                          const Alphabet& a,int workers) {
    size_t n=batch.size(),count=n*phases.size();
    std::vector<unsigned char> starts(count);
    std::vector<Image> result(count);
    for(size_t p=0;p<phases.size();++p)
        for(size_t j=0;j<n;++j) {
            starts[p*n+j]=phases[p];
            phases[p]=batch[j].map[phases[p]];
            if(phases[p]==invalid) throw std::runtime_error("marked-burst conflict in coded input");
        }
    std::exception_ptr failure;
    #pragma omp parallel for if(count>=static_cast<size_t>(workers) && workers>1) num_threads(workers) schedule(static)
    for(size_t k=0;k<count;++k) {
        try {
            result[k]=transform(batch[k%n],starts[k],a);
            if(result[k].end!=batch[k%n].map[starts[k]]) throw std::logic_error("coded frame action mismatch");
        } catch(...) {
            #pragma omp critical(line17_coded_error)
            {if(!failure) failure=std::current_exception();}
        }
    }
    if(failure) std::rethrow_exception(failure);
    return result;
}

Word from_packed(const Segments& parts,const Alphabet& a) {
    Word word;
    for(const auto& part:parts) for(Count start=0;start<part->size;start+=job_slots) {
        Block b;b.slots=std::min<Count>(job_slots,part->size-start);
        for(unsigned i=0;i<b.slots;i+=16) {
            unsigned width=std::min(16u,b.slots-i);
            unsigned bits=(part->addr[(start+i)/64]>>((start+i)%64))&((1u<<width)-1);
            auto code=a.code[bits];
            if(code==255) throw std::runtime_error("packed period contains closely spaced marks");
            b.bytes.push_back(code);
        }
        b.map=a.action(b.bytes,b.slots);word.append(b);
    }
    return word;
}

std::vector<unsigned> cycle(const Map& map,unsigned start) {
    std::vector<unsigned> phases;
    unsigned s=start;
    do {
        if(s==invalid) throw std::runtime_error("invalid coded cycle");
        if(std::find(phases.begin(),phases.end(),s)!=phases.end()) return {};
        phases.push_back(s);s=map[s];
    } while(s!=start);
    return phases;
}

Word lift_word(Word& source,const std::vector<unsigned>& initial,Counter& count,
               const Alphabet& a,int workers) {
    auto states=initial;
    std::vector<Word> pieces(states.size());
    read(source,true,std::max(32,workers*12),[&](const Batch& batch) {
        auto res=images(batch,states,a,workers);
        for(size_t i=0;i<res.size();++i) {
            count.add(res[i]);pieces[i/batch.size()].append(res[i].block);
        }
    });
    Word output;
    for(size_t i=0;i<states.size();++i) {
        if(states[i]!=initial[(i+1)%initial.size()]) throw std::logic_error("coded period failed to close");
        output.join(std::move(pieces[i]));
    }
    return output;
}

struct Tail {
    std::vector<unsigned> states;
    std::vector<Counter> rows;
    const Alphabet& alphabet;
    int workers;
    Tail(const std::vector<unsigned>& initial,size_t cut,const Alphabet& a,int threads):
        states(initial.begin()+cut,initial.end()),rows(states.size()),alphabet(a),workers(threads) {}
    void write(std::ostream& out) const {
        for(size_t i=0;i<states.size();++i) {
            const auto& r=rows[i];
            write_row(states[i],r.slots,r.calls,r.inner,out);
        }
    }
    void feed(Batch batch) {
        for(size_t i=0;i<states.size() && !batch.empty();++i) {
            std::vector<unsigned> state{states[i]};
            auto out=images(batch,state,alphabet,workers);states[i]=state.front();
            Batch next;
            for(auto& image:out) {
                rows[i].add(image);
                if(image.block.slots) {next.emplace_back();next.back().add(std::move(image.block));}
            }
            batch=std::move(next);
        }
    }
};

bool trace() {return std::getenv("LINE17_TILES_TRACE")!=nullptr;}

bool read_frame_size(std::istream& input,unsigned& size) {
    unsigned char b[4];
    input.read(reinterpret_cast<char*>(b),4);
    if(input.gcount()==0 && input.eof()) return false;
    if(input.gcount()!=4) throw std::runtime_error("truncated coded frame size");
    size=unsigned(b[0])|(unsigned(b[1])<<8)|(unsigned(b[2])<<16)|(unsigned(b[3])<<24);
    if(!size || size>(1u<<22)) throw std::runtime_error("invalid coded frame size");
    return true;
}

// A portable frame has a little-endian 32-bit slot count and ceil(count/16)
// alphabet bytes. Frame padding has no effect on the source word.
void export_period(Word& word,const std::vector<Cycle>& history,Count marks,const char* path) {
    const auto& last=history.back();
    std::string tmp=std::string(path)+".tmp";
    std::ofstream out(tmp,std::ios::binary);
    read(word,true,64,[&](const Batch& batch){
        for(const auto& job:batch) for(const auto& b:job.blocks) {
            const unsigned n=b.slots;
            const unsigned char length[4]={static_cast<unsigned char>(n),static_cast<unsigned char>(n>>8),
                static_cast<unsigned char>(n>>16),static_cast<unsigned char>(n>>24)};
            out.write(reinterpret_cast<const char*>(length),4);
            out.write(reinterpret_cast<const char*>(b.bytes.data()),b.bytes.size());
        }
        if(!out) throw std::runtime_error("cannot write coded period");
    });
    out.close();
    if(!out || std::rename(tmp.c_str(),path)!=0) throw std::runtime_error("cannot install coded period");
    std::cout<<"period "<<history.size()<<' '<<last.origin<<' '<<last.root_period<<' '<<word.slots<<' '<<marks<<'\n';
    for(const auto& c:history) {
        if(last.root_period%c.root_period!=0) throw std::logic_error("incompatible coded export periods");
        mpz_class k=last.root_period/c.root_period;
        write_row(c.state,k*c.period_slots,k*c.period_calls,k*c.period_inner);
    }
}

void run(Word word,std::vector<Cycle> history,const std::vector<unsigned>& states,
         const mpz_class& minimum,Count limit,int workers,const Alphabet& a,
         size_t export_cut=0,const char* export_path=nullptr) {
    size_t cut=history.size();
    mpz_class origin=history.back().origin,root=history.back().root_period;
    Count marks=history.back().period_inner.get_ui()/2-word.slots;
    if(history.back().prefix_slots) throw std::runtime_error("expected a pure coded period");
    while(cut<(export_cut ? export_cut : states.size()) && origin+root<minimum) {
        auto phases=cycle(word.map,states[cut]);
        if(phases.empty()) break;
        // At a closed digit boundary, there are at most three compounds per
        // mark. Three distinct mark phases visit all trits once, for six
        // compounds per input mark across the three copies. This exact
        // identity lets a three-copy lift fit right up to the spool budget.
        Count bound=phases.size()==3 ? word.slots+8*marks :
            phases.size()*(word.slots+12*marks)/3;
        if(bound>limit) break;
        Counter counts;
        auto next=lift_word(word,phases,counts,a,workers);
        if(next.slots>bound || next.slots!=counts.slots)
            throw std::logic_error("coded lift size disagrees with digit bound");
        root*=phases.size();++cut;
        Cycle c;
        c.cycle=phases.size();c.state=states[cut-1];c.period_slots=counts.slots;
        c.period_calls=counts.calls;c.period_inner=counts.inner;c.origin=origin;c.root_period=root;
        history.push_back(c);word=std::move(next);marks=counts.inner/2-counts.slots;
        if(trace()) std::cerr<<"coded cut "<<cut<<" root "<<root<<" slots "<<word.slots<<" marks "<<marks<<std::endl;
    }
    if(export_cut) {
        if(cut!=export_cut) throw std::runtime_error("coded period budget or transient before requested export cut");
        export_period(word,history,marks,export_path);return;
    }
    mpz_class copies=0;
    if(minimum>origin) {
        mpz_class delta=minimum-origin;
        mpz_cdiv_q(copies.get_mpz_t(),delta.get_mpz_t(),root.get_mpz_t());
    }
    const mpz_class epochs=origin+copies*root;
    write_aligned_rows(history,epochs);
    if(cut==states.size()) return;
    if(!mpz_fits_ulong_p(copies.get_mpz_t())) throw std::overflow_error("too many finite coded periods");
    auto k=copies.get_ui();
    if(trace()) std::cerr<<"coded tail cut "<<cut<<" copies "<<k<<" epochs "<<epochs<<std::endl;
    Tail tail(states,cut,a,workers);
    for(Count j=0;j<k;++j) {
        read(word,j+1==k,std::max(96,workers*32),[&](Batch& b){tail.feed(std::move(b));});
        if(const char* path=std::getenv("LINE17_CODED_PROGRESS")) {
            std::string tmp=std::string(path)+".tmp";
            std::ofstream out(tmp);
            write_aligned_rows(history,origin+(j+1)*root,out);
            tail.write(out);out.close();
            if(!out || std::rename(tmp.c_str(),path)!=0) throw std::runtime_error("cannot save completed period");
        }
        if(trace() && (k<=100 || j+1==k || !((j+1)&j)))
            std::cerr<<"coded tail period "<<j+1<<" of "<<k<<std::endl;
    }
    tail.write(std::cout);
}
} // namespace tiled::coded
