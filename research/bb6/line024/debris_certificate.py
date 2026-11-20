"""Prove the bounded-reach counter phase before the remote debris is read."""
from marker_certificate import GuardedCertificate, term


def main():
    start = (2,2,2,1,3,2,1,4,2,1,5,2,3,4,4,4,4,4,3,1,0,1,0,0)
    cert = GuardedCertificate()
    count = 6132216374138
    end, cost, reach, proof = cert.prefix(start, count)
    assert end == (2,2,2,1,3,5,1,4,2,1,2,1,5,2,2,1,1,2,5,3,1,4,1,2,0,0)
    assert reach <= 18396649123346 and cost+15*count == 5717374479265554
    print("import GuardedPhase\nimport Entry\nnamespace H7846.Line24\nopen Word")
    print("\n\n".join(cert.lines))
    print(f"def postStackWord := {term(start)}")
    print(f"def lastDebrisWord := {term(end)}")
    print(f"theorem debrisPhase : GuardSeries postStackWord lastDebrisWord "
          f"{count} {cost} {reach} := {proof}")
    print("end H7846.Line24")


if __name__ == "__main__":
    main()
