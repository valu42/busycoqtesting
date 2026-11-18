// Literal raw-instruction replay of the 47-cell insertion in back34.md.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

constexpr char machine[] = "1RB2LA4RA1LA3LA_0LA2RB3RB2LB---";
constexpr char period[] = "21112212211221111212121112211122211121112111112";

struct Instruction { int write, move, state; };

int main(int argc, char** argv) {
    int extra = argc == 1 ? 0 : std::stoi(argv[1]);
    if (argc > 2 || extra < 0 || extra > 1000) return 2;
    std::array<Instruction,10> instructions;
    std::string encoding(machine);
    encoding.erase(encoding.find('_'),1);
    for (int i = 0; i < 10; ++i) {
        auto s = encoding.substr(3*i,3);
        instructions[i] = s == "---" ? Instruction{0,0,2}
            : Instruction{s[0]-'0', s[1]=='L' ? -1 : 1, s[2]-'A'};
    }
    constexpr int origin = 12000;
    const int copies = 3600 + extra;
    std::vector<unsigned char> tape(origin + 47*copies + 16000);
    int head = origin, state = 0;
    auto step = [&]() {
        if (head < 0 || head >= int(tape.size()))
            throw std::runtime_error("literal tape budget exhausted");
        auto cmd = instructions[5*state + tape[head]];
        if (cmd.state == 2) return false;
        tape[head] = cmd.write;
        head += cmd.move;
        state = cmd.state;
        return true;
    };
    for (int t = 0; t < 5924; ++t)
        if (!step()) throw std::runtime_error("early blank halt");
    assert(head-origin == -52 && state == 0);
    int cut = head + 51; // after the first 50 cells following the head
    std::copy_backward(tape.begin()+cut, tape.begin()+cut+15,
                       tape.begin()+cut+15+47*copies);
    for (int i = 0; i < 47*copies; ++i) tape[cut+i] = period[i%47]-'0';
    std::uint64_t ticks = 0;
    const std::uint64_t boundary = 1816430783ULL + 498942ULL * extra;
    while (ticks < boundary && step()) ++ticks;
    if (ticks != boundary) throw std::runtime_error("early altered halt");
    auto left = std::find_if(tape.begin(),tape.end(),[](auto x){return x!=0;});
    auto last = std::find_if(tape.rbegin(),tape.rend(),[](auto x){return x!=0;}).base();
    std::cout << ticks << ' ' << head-origin << ' ' << state << ' '
              << left-tape.begin()-origin << '\n';
    for (auto i = left; i != last; ++i) std::cout.put(char('0'+*i));
    std::cout << '\n';
    int rightmost = head;
    while (step()) {
        ++ticks;
        rightmost = std::max(rightmost, head);
        if (ticks > boundary + 5000000000ULL)
            throw std::runtime_error("terminal budget exhausted");
    }
    std::cout << ticks << ' ' << head-origin << ' ' << state << ' ' << int(tape[head])
              << ' ' << rightmost-origin << '\n';
}
