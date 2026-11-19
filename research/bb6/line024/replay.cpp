// Literal checks on the two sides of the certified long phase.
// Build with c++ -O3 -std=c++17 replay.cpp -o replay.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Runs = std::vector<std::pair<int, int>>;

class Machine {
    std::vector<unsigned char> cells;
    int origin;
    int head;
    int state = 0;
    static constexpr std::array<const char*, 6> table = {
        "1RB0LA", "1RC---", "0LD1RD", "0RA0RE", "0RF1RC", "1LF0LA"
    };

    Runs read(int start, int finish, int direction) const {
        Runs result;
        for (int p = start; p != finish; p += direction) {
            int b = cells.at(p);
            if (result.empty() || result.back().first != b) result.emplace_back(b, 0);
            ++result.back().second;
        }
        return result;
    }

public:
    int low, high;
    std::uint64_t d_zero = 0;

    Machine(int left, int right)
        : cells(left + right + 1), origin(left), head(left), low(left), high(left) {}

    void mark(int position) {
        cells.at(origin + position) = 1;
        low = std::min(low, origin + position);
        high = std::max(high, origin + position);
    }

    void move(std::uint64_t count) {
        for (std::uint64_t i = 0; i < count; ++i) {
            const int b = cells[head];
            if (state == 3 && b == 0) ++d_zero;
            const char* rule = table[state] + 3 * b;
            if (*rule == '-') throw std::runtime_error("reached B1 after " + std::to_string(i) + " moves");
            cells[head] = rule[0] - '0';
            head += rule[1] == 'R' ? 1 : -1;
            if (head < 0 || head >= static_cast<int>(cells.size())) throw std::runtime_error("tape bound");
            state = rule[2] - 'A';
            low = std::min(low, head);
            high = std::max(high, head);
        }
    }

    void checkEntry() const {
        Runs left = {{0,1},{1,82430},{0,1},{1,2},{0,1},{1,1322},{0,1},{1,5},{0,1},{1,2},{0,1},{1,3}};
        Runs right = {{1,1},{0,1},{1,12},{0,1},{1,6},{0,1},{1,3},{0,1},{1,3},{0,1},
                      {1,3},{0,1},{1,6},{0,1},{1,3},{0,1},{1,3},{0,1},{1,24},{0,1},
                      {1,3},{0,1},{1,3},{0,1},{1,24},{0,1},{1,12},{0,1},{1,12},{0,1},
                      {1,9},{0,1},{1,3},{0,2},{1,3},{0,2},{1,7}};
        if (head-origin != 83689 || state != 3 || read(head-1,low-1,-1) != left ||
            read(head,high+1,1) != right) throw std::runtime_error("blank entry differs");
    }

    void checkLanding() const {
        if (head-origin != 152745948 || state != 3 || cells.at(head) ||
            cells.at(head+1) || cells.at(head+2)) throw std::runtime_error("landing differs");
    }

    void checkSecondRestart() const {
        if (head-origin != -48 || state != 0) throw std::runtime_error("restart head or state differs");
        const std::string outer = "111110110111";
        for (int p = 0; p < head; ++p) {
            int j = head-1-p;
            int bit = j < static_cast<int>(outer.size()) ? outer[j]-'0' : 0;
            if (cells[p] != bit) throw std::runtime_error("left exterior differs");
        }
        int p = head;
        auto expect = [&](int count, int bit) {
            for (int i = 0; i < count; ++i)
                if (cells.at(p++) != bit) throw std::runtime_error("right tape differs");
        };
        expect(4,0);
        for (int gap : {1320,8628,107996733,33554430,8388606,2097150,524286,
                        131070,32766,8190,2046,510,126,30,6,0}) {
            expect(gap,0);
            expect(6,1);
        }
        expect(2,0);
        expect(4,1);
        expect(static_cast<int>(cells.size())-p,0);
        std::cout << "Full regenerated local tape matches at +22751521280. Head "
                  << head-origin << ", visited [" << low-origin << ", " << high-origin << "].\n";
    }

    void checkMarkerTest(bool thirdMarker) const {
        if (head-origin != 18590 || state != 1 || cells.at(head) != thirdMarker)
            throw std::runtime_error("third-marker test differs");
    }

    void reportRestart() const {
        std::cout << "After one billion further moves: head " << head-origin << ", state " << char('A'+state)
                  << ", interval [" << low-origin << ", " << high-origin << "], D0 reads " << d_zero << '\n';
    }
};

void replayMarkerTest() {
    for (bool additional : {false,true}) {
        Machine m(1000,50000);
        const std::string outer = "111110110111";
        for (int i=0; i<static_cast<int>(outer.size()); ++i)
            if (outer[i]=='1') m.mark(-1-i);
        for (int i=0; i<6; ++i) {
            m.mark(1324+i);
            m.mark(9958+i);
            if (additional) m.mark(18590+i);
        }
        m.move(1394298);
        m.checkMarkerTest(additional);
    }
    std::cout << "B0 on the actual tape and B1 on the six-cell variant at +1394298.\n";
}

int main(int argc, char** argv) {
    replayMarkerTest();
    if (argc == 2 && std::string(argv[1]) == "--marker-test") return 0;
    Machine blank(1000, 100000);
    blank.move(20656445);
    blank.checkEntry();
    std::cout << "Both complete half-tapes match at move 20656445.\n";

    Machine restart(1000, 153000000);
    std::string left = "111110110111";  // Nearest first, at the certified restart.
    for (int i = 0; i < static_cast<int>(left.size()); ++i)
        if (left[i] == '1') restart.mark(-1-i);
    for (int i = 1324; i < 1330; ++i) restart.mark(i);
    // The next marked cell is more than 18 trillion cells away.
    restart.move(1000000000);
    restart.reportRestart();
    restart.move(22598775004ULL - 1000000000);
    restart.checkLanding();
    restart.move(22751521280ULL - 22598775004ULL);
    restart.checkSecondRestart();
}
