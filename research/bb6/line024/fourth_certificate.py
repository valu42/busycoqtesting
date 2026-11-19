from marker_certificate import GuardedCertificate, term

def main():
    first = (1,2,2,3,3,2,2,3,1,9,1)
    after_open = (2,)*11 + (5,)
    last = (2,2,2,3,2,2,3,1,3,3,2,0,1,1,0)
    c = GuardedCertificate()
    print("import GuardedPhase\nimport Entry\nnamespace H7846.Line24\nopen Word")
    theorems = []
    for name, start, count, stop, g in [
        ("fourthPhaseA",first,9795372,(1,0,1)+after_open,33554532),
        ("fourthPhaseB",after_open,1389299,last,4168407),
    ]:
        end,cost,reach,pf=c.prefix(start,count)
        assert end==stop and reach<=g
        theorems.append(f"theorem {name} : GuardSeries {term(start)} {term(end)} {count} {cost} {reach} := {pf}")
    print("\n\n".join(c.lines+theorems))
    print("end H7846.Line24")

if __name__=="__main__":
    main()
