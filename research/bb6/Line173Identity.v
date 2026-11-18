From BusyCoq Require Import Individual62 FIBv7.
Definition row173 (p : Q * Sym) : option (Sym * dir * Q) :=
  match p with
  | (A,S0) => Some (S1,R,B) | (A,S1) => Some (S0,L,E)
  | (B,S0) => Some (S1,R,C) | (B,S1) => Some (S1,R,E)
  | (C,S0) => Some (S0,R,D) | (C,S1) => Some (S1,R,C)
  | (D,S0) => Some (S1,L,A) | (D,S1) => Some (S0,L,B)
  | (E,S0) => Some (S1,L,F) | (E,S1) => Some (S0,R,B)
  | (F,S0) => None           | (F,S1) => Some (S1,L,D)
  end.
Example literal_nonhalt : ~ halts row173 c0 := TM3.nonhalt.
Print Assumptions literal_nonhalt.
