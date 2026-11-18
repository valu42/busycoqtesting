// Invert a one-based output slot through the finite words used by the packed worker.
// Included after Word, Transfer and Stream. The ordinary clock worker needs no spool.
#pragma once
#include <cstdio>
#include <cerrno>
#include <cstdlib>
#include <cstring>
#include <memory>
#include <optional>
#include <unistd.h>

struct SavedWord {
    std::fpos_t position{};
    Count bits=0;
};

class SlotOrigins {
    struct Layer {
        SavedWord prefix,period,suffix;
        mpz_class copies;
        unsigned initial;
    };
    struct CloseFile { void operator()(std::FILE* f) const { std::fclose(f); } };
    std::unique_ptr<std::FILE,CloseFile> file;
    std::vector<Layer> layers;

    SavedWord save(const Word& word) {
        SavedWord ref;
        ref.bits=word.size;
        if (std::fgetpos(file.get(),&ref.position)!=0 ||
            (!word.data.empty() && std::fwrite(word.data.data(),sizeof(Count),word.data.size(),file.get())!=word.data.size()))
            throw std::runtime_error("cannot write the slot-origin temporary file");
        return ref;
    }

    // Consume one word unless it contains the requested output. In that case
    // return its exact parent input slot, including when a slot emits two bits.
    std::optional<mpz_class> seek_word(const Transfer& tr,const SavedWord& word,unsigned& state,
                                       mpz_class& rank,mpz_class& consumed) {
        if (!word.bits) return {};
        if (std::fsetpos(file.get(),&word.position)!=0)
            throw std::runtime_error("cannot seek in the slot-origin temporary file");
        Count wanted=rank<=2*word.bits ? rank.get_ui() : std::numeric_limits<Count>::max();
        Count emitted=0;
        std::array<Count,2048> block;
        for (Count pos=0;pos<word.bits;) {
            Count bits=std::min<Count>(word.bits-pos,64*block.size());
            size_t words=(bits+63)/64;
            if (std::fread(block.data(),sizeof(Count),words,file.get())!=words)
                throw std::runtime_error("cannot read the slot-origin temporary file");
            for (Count j=0;j<bits;j+=8) {
                unsigned width=static_cast<unsigned>(std::min<Count>(8,bits-j));
                unsigned byte=(block[j/64]>>(j%64))&255;
                const Packet p=width==8 ? tr.table[state][byte] : Transfer::compile(state,byte,width);
                if (p.state==invalid) throw std::runtime_error("overlapping marked bursts");
                if (wanted-emitted<=p.width) {
                    for (unsigned b=0;b<width;++b) {
                        const auto one=Transfer::compile(state,(byte>>b)&1,1);
                        emitted+=one.width;
                        if (emitted>=wanted) return consumed+pos+j+b+1;
                        state=one.state;
                    }
                    throw std::logic_error("byte and single-slot ranks differ");
                }
                emitted+=p.width;
                state=p.state;
            }
            pos+=bits;
        }
        rank-=emitted;
        consumed+=word.bits;
        return {};
    }

    mpz_class parent(const Transfer& tr,const Layer& layer,mpz_class rank) {
        unsigned state=layer.initial;
        mpz_class consumed=0;
        if (auto hit=seek_word(tr,layer.prefix,state,rank,consumed)) return *hit;
        // The first repeat of the full digit state closes a cycle. Skip only
        // repetitions strictly before the occurrence, including silent cycles.
        struct Boundary { int copy=-1; mpz_class rank=0; };
        std::array<Boundary,6> seen;
        mpz_class remaining=layer.copies;
        int copy=0;
        bool skipped=false;
        while (remaining>0 && layer.period.bits) {
            if (!skipped && seen[state].copy>=0) {
                int cycle=copy-seen[state].copy;
                mpz_class width=seen[state].rank-rank;
                mpz_class skip=remaining/cycle;
                if (width>0) {
                    mpz_class before=(rank-1)/width;
                    if (before<skip) skip=before;
                }
                consumed+=skip*cycle*layer.period.bits;
                remaining-=skip*cycle;
                rank-=skip*width;
                skipped=true;
                if (!remaining) break;
            }
            if (!skipped) seen[state]={copy,rank};
            if (auto hit=seek_word(tr,layer.period,state,rank,consumed)) return *hit;
            --remaining;
            ++copy;
        }
        if (auto hit=seek_word(tr,layer.suffix,state,rank,consumed)) return *hit;
        throw std::logic_error("selected output is outside its finite stream");
    }
public:
    SlotOrigins() {
        const char* tmp=std::getenv("TMPDIR");
        std::string path;
        int fd=-1;
        for (const char* dir : {tmp,"/tmp","."}) {
            if (!dir || !*dir) continue;
            path=std::string(dir)+"/line17-ranks-XXXXXX";
            fd=::mkstemp(path.data());
            if (fd>=0) break;
        }
        if (fd<0) throw std::runtime_error(std::string("cannot create slot-origin temporary file: ")+std::strerror(errno));
        if (::unlink(path.c_str())!=0) {
            ::close(fd);
            throw std::runtime_error("cannot unlink slot-origin temporary file");
        }
        file.reset(::fdopen(fd,"w+b"));
        if (!file) { ::close(fd); throw std::runtime_error("cannot open slot-origin temporary stream"); }
    }
    void remember(const Stream& input,unsigned initial) {
        layers.push_back({save(input.prefix),save(input.period),save(input.suffix),input.copies,initial});
    }
    mpz_class root(const Transfer& tr,mpz_class rank) {
        if (std::fflush(file.get())!=0) throw std::runtime_error("cannot flush slot-origin temporary file");
        for (auto i=layers.rbegin();i!=layers.rend();++i) rank=parent(tr,*i,rank);
        return rank;
    }
};
