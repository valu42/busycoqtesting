// Run the actual last 21 digit transducers on all supplied cyclic source phases.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <iterator>
#include <stdexcept>
#include <string>
#include <vector>

struct Suffix {
    static constexpr unsigned width = 21;
    std::array<unsigned,width> state;
    unsigned decision_count = 0;
    std::array<unsigned,2> late_marks{};
    explicit Suffix(const std::string& register_word) {
        for (unsigned i=0; i<width; ++i) {
            char v = register_word[2*i];
            unsigned pending = i && register_word[2*i-1]=='3';
            state[i] = 2*std::string("102").find(v) + pending;
        }
    }
    bool emit(unsigned i, unsigned bit) {
        if (i==width) return true;
        if (i==15 && decision_count<10) {
            ++decision_count;
            if (decision_count>=9) late_marks[decision_count-9]=bit;
        }
        unsigned v=state[i]/2, pending=state[i]%2;
        if (pending && bit) throw std::runtime_error("overlapping marks");
        if (pending || bit) {
            state[i]=2*((v+2)%3)+(v!=0);
            if (emit(i+1,0)) return true;
            return v && emit(i+1,v==1);
        }
        state[i]=2*((v+1)%3);
        return v==2 && emit(i+1,0);
    }
};

int main(int argc, char** argv) try {
    if (argc!=4 || (std::string(argv[3])!="4" && std::string(argv[3])!="5"))
        throw std::runtime_error("expected suffix, period file and prefix mark count (4 or 5)");
    std::string suffix=argv[1];
    if (suffix.size()!=42) throw std::runtime_error("expected 21 data pairs");
    for (size_t i=0;i<suffix.size();i+=2)
        if (std::string("102").find(suffix[i])==std::string::npos ||
            (suffix[i+1]!='2' && suffix[i+1]!='3'))
            throw std::runtime_error("invalid pair");
    if (suffix.back()!='2') throw std::runtime_error("expected clear terminal flag");
    std::ifstream src(argv[2],std::ios::binary);
    if(!src) throw std::runtime_error("period file unavailable");
    std::string word((std::istreambuf_iterator<char>(src)),{});
    unsigned count = argv[3][0]-'0';
    std::string lock(6*count+2,0);
    for (unsigned j=0;j<count;++j) lock[6*j+4]=1;
    if (word.size()<lock.size() || !std::all_of(word.begin(),word.end(),[](char c){return c==0 || c==1;}))
        throw std::runtime_error("expected period at least as long as the required binary prefix");
    std::string cyclic=word+word.substr(0,lock.size()-1);
    for(size_t phase=cyclic.find(lock);phase<word.size();phase=cyclic.find(lock,phase+1)) {
        Suffix run(suffix);
        size_t index=phase;
        for(unsigned rank=1;;++rank) {
            auto before=run.state;
            if(run.emit(0,word[index])) {
                unsigned symbol=run.late_marks[0]?1:run.late_marks[1]?0:4;
                if(run.decision_count<9 || (run.decision_count<10 && symbol!=1))
                    throw std::runtime_error("incomplete decision");
                std::string row;
                for(unsigned i=0;i<Suffix::width;++i) {
                    row+="102"[before[i]/2];
                    row+=(i+1<Suffix::width && before[i+1]%2)?'3':'2';
                }
                row+='2';
                std::cout<<phase<<' '<<rank<<' '<<symbol<<' '<<row<<' '<<(word[index]||before[0]%2)<<'\n';
                break;
            }
            if(++index==word.size()) index=0;
            if(rank>=81526541) throw std::runtime_error("published slot bound violated");
        }
    }
} catch(std::exception& e) {std::cerr<<e.what()<<'\n';return 1;}
