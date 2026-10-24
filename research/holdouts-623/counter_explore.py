#!/usr/bin/env python3
"""Exploratory acceleration for the public CounterClass3 table.

Rules: verify/ResearchCounterBatch.v and ResearchCounterRecurrence.v.
This program is NOT verified by Rocq and does not emit proof certificates.
Its iteration count combines raw steps and shortcuts; it is not a TM runtime.
Counts are unbounded Python integers. A checkpoint records an exact finite tape
in this implementation, so the next run can resume without starting over.

Examples (from the repository root):
  python research/holdouts-623/counter_explore.py --selftest
  python research/holdouts-623/counter_explore.py --d0 F --start A --iterations 1000000
  python research/holdouts-623/counter_explore.py --d0 F --start F --seconds 120 --output checkpoint.json
  python research/holdouts-623/counter_explore.py --d0 F --start F --resume checkpoint.json --output checkpoint.json

P0_n is adapted from the existing CounterClass3v1.v induction. This is
AI-assisted research by Codex using the repository authors' counter rules.
"""
import argparse,hashlib,json,random,sys,time
from pathlib import Path
INF=float('inf')
class Side:
 def __init__(self):self.words=[];self.part=0;self.length=0
 def copy(self):
  s=Side();s.words=self.words.copy();s.part=self.part;s.length=self.length;return s
 def norm(self):
  if not self.words and not self.part:self.length=0
 def word(self,w,n):
  if not n or (not self.words and not w):return
  if self.words and self.words[-1][0]==w:self.words[-1]=(w,self.words[-1][1]+n)
  else:self.words.append((w,n))
 def push(self,b,n=1):
  if not n or (not self.words and not self.length and not b):return
  if self.length:
   k=min(3-self.length,n);self.part=(self.part<<k)|((1<<k)-1 if b else 0);self.length+=k;n-=k
   if self.length==3:self.word(self.part,1);self.part=self.length=0
  if n>=3:self.word(7 if b else 0,n//3);n%=3
  if n:self.part=(1<<n)-1 if b else 0;self.length=n
  self.norm()
 def pop(self):
  if not self.length:
   if not self.words:return 0
   w,n=self.words[-1];self.part=w;self.length=3
   if n==1:self.words.pop()
   else:self.words[-1]=(w,n-1)
  b=self.part&1;self.part>>=1;self.length-=1;self.norm();return b
 def drop(self,n):
  while n:
   if self.length:
    k=min(self.length,n);self.part>>=k;self.length-=k;n-=k;self.norm()
   elif not self.words:return
   elif n>=3:
    w,count=self.words[-1];k=min(n//3,count);n-=3*k
    if count==k:self.words.pop()
    else:self.words[-1]=(w,count-k)
   else:
    w,count=self.words[-1];self.part=w;self.length=3
    if count==1:self.words.pop()
    else:self.words[-1]=(w,count-1)
 def prefix(self,b):
  total=0;p=self.part
  for _ in range(self.length):
   if p&1!=b:return total
   total+=1;p>>=1
  for w,n in reversed(self.words):
   if w==(7 if b else 0):total+=3*n;continue
   for _ in range(3):
    if w&1!=b:return total
    total+=1;w>>=1
  return total if b else INF
 def prefix110(self):
  bits=(1,1,0);total=0;p=self.part
  for _ in range(self.length):
   if p&1!=bits[total%3]:return total//3
   total+=1;p>>=1
  expected=sum(bits[(total+i)%3]<<i for i in range(3))
  for w,n in reversed(self.words):
   if w==expected:total+=3*n;continue
   for _ in range(3):
    if w&1!=bits[total%3]:return total//3
    total+=1;w>>=1
  if bits[total%3]==0:total+=1
  return total//3
 def pattern(self,w,n):
  if not n:return
  if not self.length:self.word(w,n);return
  for i in (2,1,0):self.push((w>>i)&1)
  rotation=(self.part<<(3-self.length))|(w>>self.length)
  self.word(rotation,n-1)
 def data(self):return [self.part,self.length,self.words]

def recurrence(variant,q,c,l,r):
 if c or q not in (0,5):return None
 if q==0:
  m=r.prefix(1);k=l.prefix(1)
  if k:
   l.drop(k+1);r.drop(m+1);r.push(1);r.push(0);r.push(1,k+m);return 0,0,1
  if l.prefix(0)>=2:
   if m==1:
    rr=r.copy();rr.drop(2)
    if rr.prefix(1):return None
   l.drop(2);l.push(0);l.push(1,2);l.push(0,m);r.drop(m+1);return 5,0,2
  l.drop(1);k=l.prefix(1);assert k;l.drop(k+1);r.drop(m+1)
  r.push(0);r.push(1,m+2);r.push(0);r.push(1,k-1);return 0,0,3
 n=r.prefix(1)
 if n:
  k=l.prefix(1);l.drop(k+1);r.drop(n+1)
  r.push(0);r.push(1,n-1);r.push(0);r.push(1,k+1);return 0,0,4
 rr=r.copy();rr.drop(1);n=rr.prefix(1)
 if n>=2:
  r.drop(n+2);l.push(1);l.push(0);l.push(1,2);l.push(0,n-2);return 5,0,5
 if n==1:return -1,0,-1
 r.drop(2)
 if variant==5:l.push(1);r.push(1);return 5,0,6
 k=l.prefix(1);l.drop(k+1);r.push(1,2);r.push(0);r.push(1,k);return 0,0,7

def run(variant,limit,start,seconds=120,checkpoint=None,output=None):
 code=('1LB1LA_1LC1RB_0RD0LA_1L'+chr(65+variant)+'1RE_---1RF_1RC0RF').replace('_','')
 tm=[None if code[i:i+3]=='---' else (int(code[i]),1 if code[i+1]=='R' else -1,ord(code[i+2])-65) for i in range(0,36,3)]
 q=start;c=0;l=Side();r=Side();stats=dict(p0=0,frontier=0,back=0,sweep=0,raw=0,recurrence=0);base=0;maxbits=0
 if checkpoint:
  v=json.loads(Path(checkpoint).read_text());
  if v['variant']!=variant or v['start']!=start:raise ValueError('checkpoint uses a different table or starting state')
  if v['status'] not in ('limit','time'):raise ValueError('cannot resume a terminal checkpoint')
  q,c=v['q'],v['c'];base=v['iterations'];stats=v['stats'];maxbits=v['maxbits']
  for side,name in [(l,'l'),(r,'r')]:side.part,side.length,side.words=v[name];side.words=[tuple(x) for x in side.words]
 t0=time.monotonic();status='limit';i=0
 for i in range(limit):
  if i%10000==0:
   maxbits=max(maxbits,max((n.bit_length() for side in (l,r) for w,n in side.words),default=0))
   if time.monotonic()-t0>seconds:status='time';break
  if q==0 and c==0:
   n=l.prefix110()
   if n:
    m=r.prefix(1);l.drop(3*n);r.drop(m+1);r.push(1,n);r.push(0);r.push(1,m+2*n);stats['back']+=1;continue
  if q==5 and c==0:
   n=r.prefix(1)
   if n and l.prefix(0)>=2*n+1:
    l.drop(2*n);l.pattern(6,n);r.drop(n);stats['frontier']+=1;continue
  if q==1 and c==0 and r.prefix(1)==2:
   rr=r.copy();rr.drop(2)
   if rr.prefix(0)==1:
    rr.drop(1);z=l.prefix(0);n=rr.prefix(1) if z==INF else min((z+1)//2,rr.prefix(1))
    if n:l.drop(2*n-1);c=l.pop();r.push(1,2*n);stats['p0']+=1;continue
  rec=recurrence(tm[6][2],q,c,l,r)
  if rec:
   nq,nc,rule=rec
   if nq<0:status='HALT_RULE';break
   q,c=nq,nc;stats['recurrence']+=1;continue
  op=tm[2*q+c]
  if op is None:status='HALT';break
  b,d,qq=op;src,dst=(r,l) if d==1 else (l,r)
  if qq==q:
   n=src.prefix(c)
   if n==INF:status='selfloop';break
   if n:src.drop(n);c=src.pop();dst.push(b,n+1);stats['sweep']+=1;continue
  dst.push(b);c=src.pop();q=qq;stats['raw']+=1
 else:i=limit
 maxbits=max(maxbits,max((n.bit_length() for side in (l,r) for w,n in side.words),default=0))
 result=dict(variant=variant,start=start,iterations=base+i,q=q,c=c,l=l.data(),r=r.data(),stats=stats,status=status,maxbits=maxbits,seconds=time.monotonic()-t0)
 if output:Path(output).write_text(json.dumps(result)+'\n')
 digest=hashlib.sha256(json.dumps([q,c,l.data(),r.data()]).encode()).hexdigest()
 print(json.dumps({k:result[k] for k in ['variant','start','iterations','status','stats','seconds','maxbits']}|{'runs':len(l.words)+len(r.words),'digest':digest}),flush=True)
 return result

def selftest():
 rng=random.Random(47813);cases=0
 for variant in (1,5):
  code=('1LB1LA_1LC1RB_0RD0LA_1L'+chr(65+variant)+'1RE_---1RF_1RC0RF').replace('_','')
  tm=[None if code[i:i+3]=='---' else (int(code[i]),1 if code[i+1]=='R' else -1,ord(code[i+2])-65) for i in range(0,36,3)]
  for i in range(500):
   q=rng.choice((0,5));c=0;l=Side();r=Side()
   for _ in range(12):l.push(rng.randrange(2));r.push(rng.randrange(2))
   if i%3==0:
    l.push(0);l.push(1,rng.randrange(10));r.push(0);r.push(1,rng.randrange(10))
   if i%3==1:
    l.push(1);l.push(0,1+rng.randrange(20));r.push(0);r.push(1,rng.randrange(20));r.push(0,rng.randrange(3))
   ll,rr=l.copy(),r.copy();result=recurrence(variant,q,c,ll,rr)
   if result is None:continue
   qq,cc,rule=result;found=False
   for _ in range(1000000):
    op=tm[2*q+c]
    if op is None:
     assert rule==-1;found=True;break
    b,d,q=op;src,dst=(r,l) if d==1 else (l,r);dst.push(b);c=src.pop()
    if rule!=-1 and (q,c,l.data(),r.data())==(qq,cc,ll.data(),rr.data()):found=True;break
   assert found, (variant,i,rule)
   cases+=1
 print(json.dumps(dict(selftest='passed',return_rule_cases=cases)))

if __name__=='__main__':
 sys.set_int_max_str_digits(0)
 ap=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
 ap.add_argument('--d0',choices=('B','F'),default='F')
 ap.add_argument('--start',choices=tuple('ABCDEF'),default='A')
 ap.add_argument('--iterations',type=int,default=50000000)
 ap.add_argument('--seconds',type=float,default=120)
 ap.add_argument('--resume',type=Path)
 ap.add_argument('--output',type=Path)
 ap.add_argument('--selftest',action='store_true')
 args=ap.parse_args()
 if args.selftest:selftest()
 else:
  if args.iterations<0 or args.seconds<0:ap.error('budgets must be nonnegative')
  run(ord(args.d0)-65,args.iterations,ord(args.start)-65,args.seconds,args.resume,args.output)
