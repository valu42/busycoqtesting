#!/usr/bin/env python3
"""Extract exact fresh-cell tests and audit full finite request histories.
No random input model is used to infer blank behavior.
"""
from collections import deque,Counter
from itertools import product
from pathlib import Path
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'frontiers'),str(ROOT)]
from longitudinal import Driver
from prior_sweeps import TapeMachine,parse

PATTERNS={8:r'BB',11:r'BA{2}(?:AAA)*B',12:r'BA',31:r'BA'}

def cell(driver,word):
    rules=parse(driver.machine);symbol=0;virgin=True;output=[];cost=0;answer=None
    for index,entry in enumerate(word):
        state=entry;seen=set()
        while (symbol,state,virgin) not in seen:
            seen.add((symbol,state,virgin))
            instruction=rules.get((state,symbol))
            if instruction is None:return dict(halt=True,at_input=index,output=''.join(output),cost=cost)
            symbol,direction,state=instruction;cost+=1
            if direction<0:
                answer=state;break
            output.append(state)
            state=driver.first['AB'.index(state)] if virgin else driver.usual
            virgin=False
        else:raise RuntimeError('local loop')
    return dict(halt=False,symbol=symbol,virgin_neighbor=virgin,answer=answer,output=''.join(output),cost=cost)

def network(driver,word):
    tape={};cost=0;answer=None;depth=0
    while word:
        c=cell(driver,word)
        if c['halt']:return {'halt':True}
        if depth==0:answer=c['answer']
        if c['symbol']:tape[depth]=c['symbol']
        cost+=c['cost'];word=c['output'];depth+=1
        if depth>1000:raise RuntimeError('depth budget')
    return dict(halt=False,tape=tape,steps=cost,head=-1,state=answer)

def literal(driver,word):
    tm=TapeMachine(driver.machine)
    for entry in word:
        tm.head=0;tm.state=entry
        while tm.head>=0:
            if not tm.step():return dict(halt=True)
            if tm.steps>1000000:raise RuntimeError('literal budget')
    return dict(halt=False,tape=tm.tape,steps=tm.steps,head=tm.head,state=tm.state)

def blank(driver,steps=1000000):
    tm=TapeMachine(driver.machine);histories={};first_visits={}
    # An entry is a rightward crossing into a nonnegative cell, plus the initial A.
    histories[0]='A';first_visits[0]=0
    for _ in range(steps):
        previous=tm.head
        assert tm.step()
        if tm.head>previous and tm.head>=0:
            histories[tm.head]=histories.get(tm.head,'')+tm.state if len(histories.get(tm.head,''))<30 else histories[tm.head]
            first_visits.setdefault(tm.head,tm.steps)
    for h in histories.values():assert not re.match(PATTERNS[driver.line],h)
    return {'raw_steps':tm.steps,'head':tm.head,'state':tm.state,'occupied_cells':len(tm.tape),
            'tape_sha256':hashlib.sha256(json.dumps(sorted(tm.tape.items())).encode()).hexdigest(),
            'tape_sparse':sorted(tm.tape.items()),
            'fresh_cell_count':len(histories),'prefixes':dict(sorted(Counter(h[:6] for h in histories.values()).items())),
            'first_entry_raw_steps':first_visits,'first_inputs':histories}

def main():
    result={}
    for line,pattern in PATTERNS.items():
        driver=Driver(line);local_cases=full_cases=halts=0
        for length in range(1,9):
            for letters in product('AB',repeat=length):
                word=''.join(letters)
                c=cell(driver,word)
                assert c['halt']==bool(re.match(pattern,word)),(line,word,c)
                local_cases+=1
                predicted=network(driver,word);actual=literal(driver,word)
                assert predicted==actual,(line,word,predicted,actual)
                full_cases+=1;halts+=actual['halt']
        result[line]={'machine':driver.machine,'fresh_halt_regex':pattern,'literal_first_returns':driver.first,
                      'ordinary_return':driver.usual,'local_histories_checked':local_cases,
                      'full_configuration_histories_checked':full_cases-halts,'halting_status_histories_checked':halts,
                      'blank_sample':blank(driver)}
        print(line,local_cases,'local words;',full_cases-halts,'full safe configurations;',halts,'halt outcomes')
    out=Path(__file__).with_name('remaining-stream-triggers.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(out)
if __name__=='__main__':main()
