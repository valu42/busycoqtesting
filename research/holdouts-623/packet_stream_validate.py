#!/usr/bin/env python3
"""Independent packet learning and tests for packet_stream.cpp.

The oracle executes an ordinary finite tape and treats a matching right exit
as an external call. Cycles are discovered, not copied from the native table.
Tests are not formal verification of the native executable.
"""
import sys,time,json,subprocess,tempfile,argparse,gzip
from pathlib import Path
class Budget(Exception):pass
class Explorer:
 def __init__(self,code,seconds=30,maxwidth=160,limit=1000000):
  flat=code.replace('_','');ops=[]
  for i in range(0,36,3):ops.extend([-1,0,0] if flat[i:i+3]=='---' else [int(flat[i]),1 if flat[i+1]=='R' else -1,ord(flat[i+2])-65])
  self.ops=[ops[i:i+3] for i in range(0,36,3)]
  self.cache={};self.batches={};self.decode_cache={};self.maxwidth=maxwidth;self.limit=limit;self.deadline=time.monotonic()+seconds
  self.bulk=True;self.bulk_events=0;self.qr=2;self.ql=0;self.marker=0;self.learned_raw=0;self.events=0;self.maxdepth=0
 def law(self,w,width):
  key=(w,width)
  if key in self.cache:return self.cache[key]
  if time.monotonic()>self.deadline:raise Budget('time_limit')
  tape=bytearray([self.marker]+[(w>>i)&1 for i in range(width)])
  q,h,calls=self.qr,1,0;result=None
  for steps in range(self.limit):
   if h<0:
    if q==self.ql and tape[0]==self.marker:
     result=('law',sum(tape[i+1]<<i for i in range(width)),calls)
    break
   if h>width:
    if q!=self.qr or tape[width]!=self.marker:break
    calls+=1;h=width-1;q=self.ql;continue
   wr,dr,qq=self.ops[2*q+tape[h]]
   if wr<0:
    # A halt after an unresolved external call is not an unconditional law.
    if calls==0:result=('halt',)
    break
   tape[h]=wr;h+=dr;q=qq
  self.learned_raw+=steps+1
  self.cache[key]=result;return result
 def batch(self,w,width):
  key=w,width
  if key in self.batches:return self.batches[key]
  chain=[];seen={};u=w
  while u not in seen and len(chain)<128:
   law=self.law(u,width)
   if law is None or law[0]=='halt':self.batches[key]=None;return None
   seen[u]=len(chain);chain.append((u,law[2]));u=law[1]
  if u not in seen:self.batches[key]=None;return None
  start=seen[u];result=chain[:start],chain[start:]
  self.batches[key]=result;return result
 def short_decode(self,w):
  first=None
  for width in range(1,15):
   u=w&((1<<width)-1);law=self.law(u,width)
   if law:
    if law[0]=='halt':
     if first is None:return ('halt',)
    else:
     batch=self.batch(u,width)
     if batch:return 'batch',width,batch
     if first is None:first=('law',width,law)
  return first
 def decode(self,w):
  key=w&16383
  if key not in self.decode_cache:self.decode_cache[key]=self.short_decode(key)
  result=self.decode_cache[key]
  if result:return result
  for width in range(15,self.maxwidth+1):
   u=w&((1<<width)-1);law=self.law(u,width)
   if law:
    if law[0]=='halt':return ('halt',)
    batch=self.batch(u,width)
    return ('batch',width,batch) if batch else ('law',width,law)
  raise Budget('window_limit')
 def eval(self,n,w):
  stack=[];fuel=0
  while True:
   self.events+=1;fuel+=1
   if fuel>1000000:raise Budget('event_limit')
   if (fuel&4095)==0 and time.monotonic()>self.deadline:raise Budget('time_limit')
   if n==0:
    if not stack:return w
    n,v,width=stack.pop();w=v|(w<<width);continue
   action=self.decode(w)
   if action[0]=='halt':return None
   width=action[1];tail=w>>width
   if action[0]=='batch':
    pre,cyc=action[2];p=len(pre)
    if self.bulk and not pre and len(cyc)==1 and cyc[0][1]==2:
     difference=w^(w>>width)
     repeat=1+((difference&-difference).bit_length()-1)//width if difference else 1
     if repeat>1:
      length=repeat*width;v=w&((1<<length)-1)
      stack.append((0,v,length));n<<=repeat;w>>=length;self.bulk_events+=1
      if n.bit_length()>2000000:raise Budget('integer_limit')
      continue
    if n<p:
     out=sum(k for _,k in pre[:n]);v=pre[n][0]
    else:
     q,r=divmod(n-p,len(cyc));out=sum(k for _,k in pre)+q*sum(k for _,k in cyc)+sum(k for _,k in cyc[:r]);v=cyc[r][0]
    stack.append((0,v,width));n=out;w=tail
   else:
    _,v,k=action[2]
    if k==0:n-=1;w=v|(tail<<width)
    else:stack.append((n-1,v,width));n=k;w=tail
   self.maxdepth=max(self.maxdepth,len(stack))
 def raw_seed(self):
  tape=set();q=h=0
  for steps in range(1000000):
   if q==0 and h in tape and h+1 not in tape and min(tape)>=h:
    return sum(1<<(p-h-2) for p in tape if p>=h+2),steps
   wr,dr,q1=self.ops[2*q+(h in tape)]
   if wr<0:raise Budget('raw_halt')
   if wr:tape.add(h)
   else:tape.discard(h)
   h+=dr;q=q1
  raise Budget('seed_limit')

MACHINES = {
 405: '1RB0LB_0RC0LF_1LD1RE_0LA0RB_0RD0RF_0LA---',
 482: '1RB0LB_0RC0LD_1LD1RE_0LA0RB_0RD1RF_1LA---',
}

def raw_boundaries(e, count=10):
 w,_=e.raw_seed();q=h=steps=matches=0;tape=set()
 for _ in range(count):
  while steps<1000000:
   if q==0 and h in tape and h+1 not in tape and min(tape)>=h:
    actual=sum(1<<(p-h-2) for p in tape if p>=h+2)
    if actual==w:matches+=1;break
   wr,dr,qq=e.ops[2*q+(h in tape)];assert wr>=0
   if wr:tape.add(h)
   else:tape.discard(h)
   h+=dr;q=qq;steps+=1
  else:break
  w=e.eval(1,1|(w<<2));assert w is not None
  wr,dr,qq=e.ops[2*q+(h in tape)];assert wr>=0
  if wr:tape.add(h)
  else:tape.discard(h)
  h+=dr;q=qq;steps+=1
 return matches,steps

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('binary',type=Path);args=parser.parse_args()
 binary=str(args.binary.resolve())
 def run(entry,*opts):
  r=subprocess.run([binary,'--entry',str(entry),*map(str,opts)],check=True,capture_output=True,text=True,timeout=120)
  return json.loads(r.stdout)
 def state(r):return r['rounds'],r['events'],int(r['word_hex'],16)
 report={'verified':False,'models':[]}
 for entry,machine in MACHINES.items():
  e=Explorer(machine,seconds=120);w,seed=e.raw_seed();small=None
  for n in range(1000):
   w=e.eval(1,1|(w<<2));assert w is not None
   if n==99:small=w
  full=run(entry,'--rounds',1000,'--seconds',30,'--hex');assert state(full)[2]==w
  assert state(run(entry,'--rounds',100,'--hex'))[2]==small
  assert state(run(entry,'--rounds',1000,'--single','--hex'))==state(full)
  assert state(run(entry,'--rounds',1000,'--single','--no-prefix','--hex'))==state(full)
  assert state(run(entry,'--rounds',1000,'--no-prefix','--hex'))==state(full)
  assert state(run(entry,'--rounds',1000,'--dense-counter','--hex'))==state(full)
  assert state(run(entry,'--rounds',1000,'--sparse-counter','--hex'))==state(full)
  plain=Explorer(machine,seconds=120);plain.bulk=False;v,_=plain.raw_seed()
  for _ in range(100):v=plain.eval(1,1|(v<<2))
  assert v==small
  matches,rawsteps=raw_boundaries(Explorer(machine,seconds=120))
  assert matches==10
  with tempfile.TemporaryDirectory(prefix='packet-test-',dir=Path.cwd()) as directory:
   cp=Path(directory)/'state'
   run(entry,'--rounds',321,'--checkpoint',cp)
   split=run(entry,'--resume',cp,'--rounds',679,'--checkpoint',cp,'--hex')
   assert state(split)==state(full)
   assert state(run(entry,'--resume',cp,'--rounds',0,'--hex'))==state(full)
   for seconds,maxbits in ((1e-6,2000000),(30,16)):
    limited=run(entry,'--rounds',10000,'--seconds',seconds,'--max-bits',maxbits,'--hex','--checkpoint',cp)
    assert limited['status'] in ('time_limit','space_limit')
    replay=run(entry,'--rounds',limited['rounds'],'--hex')
    assert state(limited)==state(replay),limited
    assert state(run(entry,'--resume',cp,'--rounds',0,'--hex'))==state(limited)
   # A supplied artificial boundary outside the packet table stays unknown;
   # stopping during a round must preserve the previous full boundary word.
   cp.write_text(f'packet-stream-v1\n{entry} {machine}\n0 0\nffff\n')
   unknown=run(entry,'--resume',cp,'--rounds',1,'--hex')
   assert unknown['status']=='unknown_packet' and state(unknown)==(0,0,65535)
   cp.write_text(f'packet-stream-v1\n{entry} {machine}\n0 0\n1d\n')
   candidate=run(entry,'--resume',cp,'--rounds',1,'--hex')
   assert candidate['status']=='halt_candidate' and state(candidate)==(0,0,29)
   assert Explorer(machine,seconds=30).eval(1,1|(29<<2)) is None
   cp.write_text(f'packet-stream-v1\n{entry} {machine}\n0 0\n19\n')
   transient=run(entry,'--resume',cp,'--rounds',1,'--hex')
   assert transient['status']=='halt_candidate' and state(transient)==(0,0,25)
   assert Explorer(machine,seconds=30).eval(1,1|(25<<2)) is None
   for text in ('broken\n',f'packet-stream-v1\n{entry} {machine}\n1 0\n1\n',
                f'packet-stream-v1\n{entry} {machine}\n0 0\n-1\n'):
    cp.write_text(text);r=subprocess.run([binary,'--entry',str(entry),'--resume',str(cp)],capture_output=True)
    assert r.returncode!=0
  report['models'].append(dict(entry=entry,python_rounds=1000,unbatched_rounds=100,
   ordinary_tm_boundaries=matches,ordinary_tm_steps=rawsteps,blank_seed_steps=seed,
   learned_packet_inputs=len(e.cache),packet_oracle_steps=e.learned_raw,
   native_seconds=full['seconds'],checkpoint_resume='passed',rollback_controls='passed'))
 fixture=Path(__file__).with_name('packet405_frontier.checkpoint.gz')
 with tempfile.TemporaryDirectory(prefix='packet-frontier-',dir=Path.cwd()) as directory:
  cp=Path(directory)/'frontier'
  cp.write_bytes(gzip.decompress(fixture.read_bytes()))
  lines=cp.read_text().splitlines();assert lines[2].split()[0]=='161210'
  original=int(lines[3],16)
  explorer=Explorer(MACHINES[405],seconds=120)
  expected=explorer.eval(1,1|(original<<2));assert expected is not None
  advanced=run(405,'--resume',cp,'--rounds',1,'--max-bits',4000000,'--hex')
  assert advanced['rounds']==161211 and int(advanced['word_hex'],16)==expected
  for options in (('--dense-counter',),('--single',),('--no-prefix',)):
   comparison=run(405,'--resume',cp,'--rounds',1,'--max-bits',4000000,'--hex',*options)
   assert state(comparison)==state(advanced)
  report['frontier_regression']=dict(entry=405,from_round=161210,to_round=161211,
   word_bits=expected.bit_length(),packet_oracle_steps=explorer.learned_raw,full_word_match=True)
 report['native_selftest']=json.loads(subprocess.run([binary,'--selftest'],check=True,capture_output=True,text=True).stdout)
 print(json.dumps(report,indent=2))

if __name__=='__main__':main()
