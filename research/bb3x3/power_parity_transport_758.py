"""Transport a reset through two successive macroscopic parity corridors."""
from argparse import ArgumentParser
from check_bb33 import first_return
from scale_clauses_758 import check_word
from power_gates_758 import coalesce


def endpoints(lo,hi,parity,word,output_parity):
    for seed in (lo+(parity-lo)%2,hi-(hi-parity)%2):
        gain=check_word(seed,word)
        assert 0 < gain and (seed+gain)%2==output_parity


def handoff(m, merge=False):
    p=3**m
    start=24*p//23
    cusp=2187*p//2059-2*m-500
    end=54*p//49-2*m-504
    # An ordinary return with at most seven bulks and one interior J
    # gains no more than this on either preserving corridor.
    max_gain=2*m+40
    assert start+100_000+2*m+100 < cusp and cusp+max_gain < end
    even_open='I'+'J'*(m-1)
    endpoints(start,start+100_000,0,even_open+'LLJLLJJJLR',1)
    endpoints(start,cusp-1,1,'J'*m+'LLLLLLLR',1)
    endpoints(cusp,end-1,0,even_open+'LLJLR',0)
    good=set()
    furthest=0
    for seed in range(cusp+(1-cusp)%2,cusp+max_gain+1,2):
        path=[]
        while seed%2 and seed not in good:
            assert len(path)<100_000
            path.append(seed)
            nxt=first_return(seed)
            assert nxt is not None and nxt>seed
            seed=nxt
        assert seed < end
        furthest=max(furthest,seed-cusp)
        good.update(path)
    row=(m,len(good),furthest)
    if merge:
        stop,edges=coalesce(range(end+end%2,end+max_gain+1,2),1_000_000)
        row+=(stop-end,edges)
    return row


def timed_flight(m, goal_offset):
    from target_clock_758 import first_pass,timed_return
    p=3**m
    seed=start=24*p//23
    cusp=2187*p//2059-2*m-500
    end=54*p//49-2*m-504
    count=clock=0
    if not seed%2:
        seed,cost=timed_return(seed)
        assert seed%2
        count,clock=1,cost
    seed,n,cost=first_pass(seed,start+(1-start)%2,cusp-1,256,2*m+40)
    count,clock=count+n,clock+cost
    while seed%2:
        seed,cost=timed_return(seed)
        count,clock=count+1,clock+cost
    seed,n,cost=first_pass(seed,cusp+cusp%2,end-1,16,2*m+40)
    count,clock=count+n,clock+cost
    while seed<end+goal_offset:
        seed,cost=timed_return(seed)
        count,clock=count+1,clock+cost
    assert seed==end+goal_offset
    return count,clock


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('exponents',type=int,nargs='*')
    parser.add_argument('--all',action='store_true')
    parser.add_argument('--merge',action='store_true')
    parser.add_argument('--clock',action='store_true',help='time the entrance at floor(24P/23) exactly')
    args=parser.parse_args()
    if not __debug__:parser.error('enable assertions')
    for m in (range(20,293) if args.all else args.exponents or (35,292)):
        if m<20:parser.error('require exponent at least 20')
        row=handoff(m,args.merge or args.clock)
        if args.clock:row+=timed_flight(m,row[-2])
        print(*row,sep='\t',flush=True)
