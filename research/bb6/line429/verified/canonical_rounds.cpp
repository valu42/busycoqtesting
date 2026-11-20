// Evaluate the two formal gate predicates only at actual full-phase returns.
// Tape orientation and states below are original, as in the ranking.
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
struct Run {
 vector<unsigned char> tape = vector<unsigned char>(1<<22);
 int p=1<<21,q=0;
 uint64_t t=0;
 int at(int x) const {return tape.at(x);}
 void advance(int n) {
  static const char* table[]={"1RB0LC","1RC1RA","1RD0RF","0LE---","1LA1LE","0RA0RF"};
  while(n--){const char*cmd=table[q]+3*at(p);if(*cmd=='-'){cout<<"halt t="<<t<<endl;exit(0);}
    tape.at(p)=cmd[0]-'0';p+=(cmd[1]=='R'?1:-1);q=cmd[2]-65;++t;}
 }
 bool gate() const {
  int h=0;bool a=true,b=true;
  for(int x=p-1;;--x){int d=at(x);
    if(!a && !b)return false;
    if(h==0){if(d){b=a;a=false;}else h=1;}
    else if(h==1){if(!d)return a;h=2;}
    else if(!d){h=0;b=a;}else{h=1;a=b;}
  }
 }
 bool parser() const {
  // States L,J,L0,L1,D,D0,E,N,Turn,Stop
  static const int step[8][2]={{2,3},{4,0},{4,0},{1,8},{5,6},{8,9},{7,6},{1,8}};
  int state=1;
  for(int x=p+2;state<8;++x)state=step[state][at(x)];
  return state==9;
 }
 void round(){
   while(true){
     if(q!=4)abort();
     if(at(p)){advance(1);continue;}
     if(!at(p-1)){advance(3);break;}
     advance(at(p-2)?8:5);
   }
   if(q!=0)abort();
   do advance(1);while(q!=4);
 }
};
int main(int argc,char**argv){
 if(argc!=2)return 2;
 uint64_t limit=stoull(argv[1]);Run s;
 s.advance(4);uint64_t table[4]{},n=0;
 while(s.t<limit){
  if(s.q!=4||s.at(s.p)!=1||s.at(s.p+1)!=0)abort();
  bool g=s.gate(),m=s.parser();int tag=int(g)+2*int(m);
  if(++table[tag]==1){cout<<"first round "<<n<<" time "<<s.t<<" gate="<<g<<" MJstop="<<m<<" pos="<<s.p-(1<<21)<<" u[0:60]=";
    for(int i=0;i<60;++i) cout<<s.at(s.p+2+i);cout<<" w[0:60]=";for(int i=0;i<60;++i)cout<<s.at(s.p-1-i);cout<<endl;}
  ++n;s.round();
 }
 cout<<"canonical rounds starting before "<<limit<<" next_t "<<s.t<<" n "<<n;
 for(int tag=0;tag<4;++tag)cout<<" class"<<tag<<"="<<table[tag];cout<<endl;
}
