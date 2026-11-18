#!/usr/bin/env python3
"""Bounded blank-orbit audit using inherited, timed line6.probe.
Run from any directory; Python 3.10+, assertions enabled.
"""
import argparse, hashlib, json, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from line6 import MACHINE,HEADER,probe,literal_probe
from prior_sweeps import TapeMachine

def run(epochs, literal_epochs):
    tm=TapeMachine(MACHINE)
    residual=''; headers=0; total=0; events=[]; samples=[]; last_total=0
    min_cost=None; max_cost=0
    for epoch in range(1,epochs+1):
        result=probe(residual)
        assert result.state=='B', (epoch,result)
        cost=2+result.steps+48*headers
        total+=cost
        min_cost=cost if min_cost is None else min(min_cost,cost)
        max_cost=max(max_cost,cost)
        residual='32'+result.word
        while residual.startswith(HEADER):
            headers+=1; residual=residual[len(HEADER):]
            events.append({'epoch':epoch,'steps':total,'headers':headers})
        word=HEADER*headers+residual
        assert word.count('2')==epoch
        assert '02' not in word and '222' not in word
        if epoch<=literal_epochs:
            while tm.head>-epoch:
                assert tm.step()
            assert (tm.head,tm.state,tm.steps)==(-epoch,'A',total)
            assert tm.tape=={tm.head+i:int(c) for i,c in enumerate(word,1) if c!='0'}
        if epoch%100==0 or epoch==epochs:
            samples.append({'epoch':epoch,'steps':total,'interval_steps':total-last_total,'headers':headers,'width':len(word),'residual_width':len(residual),'epoch_cost':cost})
            last_total=total
    # Tractable continuation of the final exact residual is tested separately,
    # including sparse tape, physical head, state and instruction count.
    local=literal_probe(residual,limit=100000000)
    accelerated=probe(residual)
    assert local==accelerated
    word=HEADER*headers+residual
    return {'machine':MACHINE,'epochs':epochs,'steps':total,'head':-epochs,'state':'A',
            'headers':headers,'residual':residual,'word_sha256':hashlib.sha256(word.encode()).hexdigest(),
            'width':len(word),'header_events':events,'samples':samples,
            'minimum_epoch_steps':min_cost,'maximum_epoch_steps':max_cost,
            'verification':{'literal_blank_epochs':literal_epochs,'complete_configurations_compared':literal_epochs,
                            'final_residual_probe_steps':local.steps,'final_residual_probe_result':local.state,
                            'final_residual_full_return_matches':True}}

if __name__=='__main__':
    assert __debug__
    ap=argparse.ArgumentParser(); ap.add_argument('--epochs',type=int,default=2000); ap.add_argument('--literal-epochs',type=int,default=376); ap.add_argument('--output',type=Path,default=Path(__file__).with_name('remaining-line6.json'))
    args=ap.parse_args(); start=time.monotonic(); result=run(args.epochs,min(args.literal_epochs,args.epochs)); result['elapsed_seconds']=time.monotonic()-start
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('residual','samples','header_events')},indent=2))
    print('header events:',result['header_events'])
