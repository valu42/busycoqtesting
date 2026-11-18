#pragma once

// Lift one exported physical period without writing a second copy of its
// input. Cache the six-state action of each stripe during the first phase.
int virtual_lift(int argc,char** argv) {
    using namespace virtual17;
    namespace code=tiled::coded;
    if(argc!=5)throw std::runtime_error("lift SOURCE PHYSICAL_STATE THREADS OUTPUT");
    const B seed=number(argv[2]),workers=number(argv[3]);
    if(seed>=6||!workers||workers>64)throw std::runtime_error("invalid physical lift dimensions");
    code::Alphabet alphabet;
    std::vector<code::Map> maps;std::array<bool,6> seen{};
    std::ofstream dest(argv[4],std::ios::binary);
    if(!dest)throw std::runtime_error("cannot create lifted source");
    U state=seed,copies=0;B source_slots=0,source_marks=0;
    code::Counter total;
    do{
        if(seen[state])throw std::runtime_error("the physical lift has a nonzero preperiod");
        seen[state]=true;size_t cursor=0;
        read_source(argv[1],workers*6,[&](const Batch& jobs){
            std::vector<B> marks(jobs.size());
            if(!copies){
                maps.resize(cursor+jobs.size());
                #pragma omp parallel for num_threads(workers) schedule(static)
                for(size_t j=0;j<jobs.size();++j){
                    code::Map map=code::identity;
                    const auto& src=jobs[j];
                    for(auto [off,n]:src.frames){
                        for(U i=0;i<n/16;++i){
                            U symbol=src.bytes[off+i];const auto& step=alphabet.transitions[symbol];
                            for(auto& x:map)x=step[x];
                            marks[j]+=__builtin_popcount(alphabet.mask[symbol]);
                        }
                        if(n%16){
                            U word=alphabet.mask[src.bytes[off+n/16]]&((1u<<(n%16))-1);
                            code::Map step=code::identity;
                            for(U s=0;s<6;++s)step[s]=Packet::compile(s,word,n%16).state;
                            map=code::compose(map,step);marks[j]+=__builtin_popcount(word);
                        }
                    }
                    maps[cursor+j]=map;
                }
            }
            std::vector<U> entrance;
            for(size_t j=0;j<jobs.size();++j){
                if(!copies){source_slots+=jobs[j].slots;source_marks+=marks[j];}
                entrance.push_back(state);state=maps.at(cursor+j)[state];
                if(state==invalid)throw std::runtime_error("conflicting bursts in the physical lift");
            }
            std::vector<code::Image> results(jobs.size());std::exception_ptr failure;
            #pragma omp parallel for num_threads(workers) schedule(static)
            for(size_t j=0;j<jobs.size();++j)try {
                const auto& src=jobs[j];auto& out=results[j];
                out.block.bytes.reserve(src.bytes.size()+4);
                U s=entrance[j],shift=0;B acc=0;
                auto codeword=[&](U word){
                    auto symbol=alphabet.code[word];
                    if(symbol==255)throw std::runtime_error("lifted pulse gap below four");
                    out.block.bytes.push_back(symbol);
                };
                auto push=[&](const Packet& p){
                    if(p.state==invalid)throw std::runtime_error("conflicting marked bursts in stripe");
                    s=p.state;out.calls+=p.calls;out.inner+=p.interior;out.block.slots+=p.width;
                    acc|=B(p.bits)<<shift;shift+=p.width;
                    while(shift>=16){codeword(acc&65535);acc>>=16;shift-=16;}
                };
                for(auto [off,n]:src.frames){
                    for(U i=0;i<n/16;++i)push(alphabet.packets[src.bytes[off+i]][s]);
                    if(n%16)push(Packet::compile(s,alphabet.mask[src.bytes[off+n/16]],n%16));
                }
                if(shift)codeword(acc);
                if(s!=maps[cursor+j][entrance[j]])throw std::logic_error("incorrect lift stripe endpoint");
            }catch(...){
                #pragma omp critical(lift_file_error)
                {if(!failure)failure=std::current_exception();}
            }
            if(failure)std::rethrow_exception(failure);
            for(const auto& image:results){
                const auto& frame=image.block;total.add(image);
                if(!frame.slots)continue;
                if(frame.slots>(1u<<22))throw std::runtime_error("lifted frame too large");
                unsigned char bytes[4];for(U i=0;i<4;++i)bytes[i]=(frame.slots>>(8*i))&255;
                dest.write(reinterpret_cast<const char*>(bytes),4);
                dest.write(reinterpret_cast<const char*>(frame.bytes.data()),frame.bytes.size());
            }
            if(!dest)throw std::runtime_error("failed to write lifted pulse stream");
            cursor+=jobs.size();
        });
        if(cursor!=maps.size())throw std::runtime_error("source changed during physical lift");
        ++copies;
        std::cerr<<"completed source copy "<<copies<<", physical state "<<state<<std::endl;
    }while(state!=seed);
    dest.close();if(!dest)throw std::runtime_error("failed to close lifted period");
    std::cout<<"lift "<<copies<<' '<<source_slots<<' '<<source_marks<<' '<<state<<' '
             <<total.slots<<' '<<total.calls<<' '<<total.inner<<'\n';
    return 0;
}
