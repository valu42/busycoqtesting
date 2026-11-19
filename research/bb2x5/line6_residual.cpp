// Replay the physical table and compare header-stripped words at new leftmost blanks.
#include <algorithm>
#include <array>
#include <cstdint>
#include <deque>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>

namespace {
constexpr int K=5, codes=3125;
constexpr std::array<int,K> place{1,5,25,125,625};
struct Rule { int write, direction, state; };
constexpr Rule rules[2][5]={
    {{1,1,1},{-1,0,0},{3,-1,1},{4,1,1},{0,-1,0}},
    {{2,-1,1},{3,-1,0},{3,1,1},{4,1,0},{0,1,0}}};
struct Crossings {
    std::uint64_t length=0, hash=0, power=1;
    void append(int state) { ++length; hash=131*hash+state+1; power*=131; }
    void append(const Crossings& rhs) {
        length+=rhs.length; hash=hash*rhs.power+rhs.hash; power*=rhs.power;
    }
};
struct Exit { int word, pos, state, steps; std::array<Crossings,K+1> edges{}; };
Exit cache[codes][2][2]{};
int floor_index(int x) { return x>=0 ? x/K : -1-((-1-x)/K); }
int digit(int word,int i) { return (word/place[i])%5; }
const Exit& block(int initial,int state,int side) {
    auto& saved=cache[initial][state][side];
    if (saved.steps) return saved;
    int word=initial, pos=side ? K-1 : 0, steps=0;
    std::array<Crossings,K+1> edges{};
    while (0<=pos && pos<K) {
        const int old=digit(word,pos);
        const Rule r=rules[state][old];
        // Replay this block literally when it contains the first undefined instruction.
        if (r.write<0) return saved={-1,pos,state,-1,{}};
        word+=(r.write-old)*place[pos];
        edges[pos+(r.direction>0)].append(r.state);
        pos+=r.direction; state=r.state;
        if (++steps>2*K*codes) throw std::runtime_error("closed block cycle");
    }
    return saved={word,pos,state,steps,edges};
}
class Tape {
    std::deque<int> data{0};
    int first=0;
public:
    int& at(int index) {
        while (index<first) { data.push_front(0); --first; }
        while (index-first>=int(data.size())) data.push_back(0);
        return data[index-first];
    }
    int read(int x) const {
        const int i=floor_index(x);
        return i<first || i-first>=int(data.size()) ? 0 : digit(data[i-first],x-K*i);
    }
};
// Start a fresh B probe at each offset in the checkpoint word. The source
// tape stays immutable. A per-run stamp initializes blocks on first touch.
void scan_suffixes(const std::string& source) {
    std::vector<int> originals(source.size()/K+1);
    for (std::size_t i=0;i<source.size();++i)
        originals[i/K]+=(source[i]-'0')*place[i%K];
    std::vector<int> words(originals.size()), stamp(originals.size(),-1);
    // Both 32 and 33 preserve the returned tag. U 30 U 0 forces A,
    // where U is any sequence of these two pairs.
    const std::string padded=source+"0000";
    std::vector<int> skip(padded.size()+1);
    for (int i=int(padded.size())-1;i>=0;--i)
        skip[i]=(padded[i]=='3' && (padded[i+1]=='2' || padded[i+1]=='3')) ? skip[i+2] : i;
    std::array<int,3> outcomes{};
    int unexpected=0;
    std::uint64_t longest=0;
    int longest_at=-1;
    for (int start=0;start<int(source.size());++start) {
        int head=start, state=1;
        std::uint64_t steps=0;
        while (head>=start) {
            const int index=head/K, pos=head%K;
            if (index>=int(words.size())) {
                words.resize(index+1);
                stamp.resize(index+1,-1);
            }
            if (stamp[index]!=start) {
                words[index]=index<int(originals.size()) ? originals[index] : 0;
                stamp[index]=start;
            }
            int& word=words[index];
            if (index*K>=start && (pos==0 || pos==K-1)) {
                const Exit& result=block(word,state,pos!=0);
                if (result.word>=0) {
                    word=result.word; state=result.state;
                    steps+=result.steps; head=index*K+result.pos;
                    continue;
                }
            }
            const int old=digit(word,pos);
            const Rule r=rules[state][old];
            if (r.write<0) {
                state=2;
                if (!outcomes[2]) std::cout<<"first_halt_offset "<<start<<" steps "<<steps<<"\n";
                break;
            }
            word+=(r.write-old)*place[pos];
            head+=r.direction; state=r.state; ++steps;
        }
        const int first=skip[start];
        const bool visible=padded.compare(first,2,"30")==0 && padded[skip[first+2]]=='0';
        if (state!=int(!visible)) {
            if (!unexpected) std::cout<<"first_unexpected_offset "<<start<<" steps "<<steps<<"\n";
            ++unexpected;
        }
        ++outcomes[state];
        if (steps>longest) {longest=steps;longest_at=start;}
    }
    std::cout<<"suffixes_A "<<outcomes[0]<<" B "<<outcomes[1]<<" H "<<outcomes[2]
             <<" unexpected "<<unexpected<<" longest_steps "<<longest<<" at_offset "<<longest_at<<"\n";
}

}
int main(int argc,char** argv) {
    if (argc!=2 && argc!=3) return 2;
    const bool dump=argc==3 && std::string(argv[2])=="--histories";
    const bool suffixes=argc==3 && std::string(argv[2])=="--suffixes";
    if (argc==3 && !dump && !suffixes) return 2;
    const int limit=std::stoi(argv[1]);
    if (limit<1) return 2;
    const std::string header="322323300";
    Tape tape;
    std::vector<Crossings> cuts(limit+1);
    std::size_t capacity=1;
    while (capacity<2*cuts.size()) capacity*=2;
    std::vector<int> stamps(capacity), indices(capacity);
    std::uint64_t cut_pairs=0;
    int x=0,state=0,epoch=0,top=0,headers=0;
    std::uint64_t time=0,ambiguous=0;
    std::set<std::tuple<int,int,std::uint64_t>> seen{{0,0,0}};
    std::map<std::pair<int,int>,std::pair<int,unsigned>> counts{{{0,0},{0,1}}};
    while (epoch<limit) {
        const int i=floor_index(x), left=K*i, pos=x-left;
        int& word=tape.at(i);
        // Keep the first new negative coordinate visible, including when it is a block edge.
        if (left > -epoch && (pos==0 || pos==K-1)) {
            const Exit& result=block(word,state,pos!=0);
            if (result.word>=0) {
                for (int edge=0;edge<=K && left+edge<=1;++edge)
                    cuts[1-(left+edge)].append(result.edges[edge]);
                word=result.word; x=left+result.pos; state=result.state;
                top=std::max(top,left+K-1); time+=result.steps;
                continue;
            }
        }
        const int old=digit(word,pos);
        const Rule r=rules[state][old];
        if (r.write<0) {
            std::cout<<"halt "<<time<<" "<<x<<" "<<state<<" "<<old<<"\n";return 0;
        }
        const int edge=x+(r.direction>0);
        if (edge<=1) cuts[1-edge].append(r.state);
        word+=(r.write-old)*place[pos];state=r.state;
        top=std::max(top,x);x+=r.direction;++time;
        if (x>=-epoch) continue;
        ++epoch;
        if (state!=0 || x!=-epoch || tape.read(x)!=0) throw std::logic_error("blank checkpoint");
        // F(2^n) contains F(2^(n-1)); only the blank epoch's new
        // crossings are appended to the inherited interior cuts. The new root
        // has one conceptual B entry and one physical B exit.
        const int n=epoch-1;
        cuts[n]={}; cuts[n].append(1); cuts[n].append(1);
        for (int i=0;i<=n;++i) {
            const auto& a=cuts[n-i];
            if (a.length%2) throw std::logic_error("unfinished crossing pair");
            if (dump) std::cout<<"cut "<<n<<" "<<i<<" "<<a.length<<" "<<a.hash<<"\n";
            std::uint64_t mix=a.hash^(a.length*11400714819323198485ULL);
            mix^=mix>>33; mix*=0xff51afd7ed558ccdULL; mix^=mix>>33;
            std::size_t slot=mix&(capacity-1);
            while (stamps[slot]==epoch) {
                const int j=indices[slot];
                if (a.hash==cuts[n-j].hash && a.length==cuts[n-j].length) {
                    std::cout<<"pump_candidate "<<n<<" "<<j<<" "<<i<<"\n";
                    return 4;
                }
                slot=(slot+1)&(capacity-1);
            }
            stamps[slot]=epoch; indices[slot]=i;
        }
        cut_pairs+=std::uint64_t(n)*(n+1)/2;
        int start=x+1+9*headers;
        for (;;) {
            unsigned j=0;
            while (j<header.size() && tape.read(start+j)==header[j]-'0') ++j;
            if (j!=header.size()) break;
            start+=header.size();++headers;
        }
        // Previously verified full headers persist by the literal header lemma.
        while (top>=x+1 && tape.read(top)==0) --top;
        const int length=std::max(0,top-start+1);
        const int twos=epoch-3*headers;
        auto& group=counts[{twos,length}];
        if (group.second) {
            ambiguous+=group.second;
            std::cout<<"same_size "<<group.first<<" "<<epoch<<" "<<twos<<" "<<length<<"\n";
        } else group.first=epoch;
        ++group.second;
        std::uint64_t hash=0;
        for (int c=start;c<=top;++c) hash=hash*131+tape.read(c)+1;
        if (!seen.emplace(twos,length,hash).second) {
            std::cout<<"candidate "<<epoch<<" "<<twos<<" "<<length<<" "<<hash<<"\n";
            return 3;
        }
        if (epoch==5 || epoch==329 || epoch==376 || epoch==limit) {
            std::cout<<"epoch "<<epoch<<" steps "<<time<<" headers "<<headers<<" residual_twos "
                     <<twos<<" residual_length "<<length<<" coordinate "<<top<<"\n";
        }
    }
    std::cout<<"distinct "<<seen.size()<<" pairs_equal_in_length_and_twos "<<ambiguous<<"\n";
    std::cout<<"unary_cut_pairs "<<cut_pairs<<"\n";
    std::string final_word;
    for (int c=x+1;c<=top;++c) final_word.push_back(char('0'+tape.read(c)));
    std::cout<<"word "<<final_word<<"\n";
    if (suffixes) scan_suffixes(final_word);
}
