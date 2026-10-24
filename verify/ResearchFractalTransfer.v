(* Arithmetic return rules for the machine in ResearchFractalSweep.v.
   transfer moves two cells from each of two right-hand runs into the
   leading left-hand run and the middle right-hand run. transfers repeats
   it an arbitrary number of times, preserving arbitrary untouched tails.
   The transfer proof assumes an even middle run. odd_middle_can_halt
   exhibits a halting configuration of the same shape with an odd middle
   run, so the block layout alone is not a nonhalting invariant.

   These rules do not cover every configuration of the blank run.
   AI-assisted research by Codex, using the BusyCoq authors' execution
   tactics and tape algebra. *)
From BusyCoq Require Import Individual62 ES_v2 ES_v3 ResearchFractalSweep.
From Coq Require Import List Lia.
Import ListNotations FractalSweep.
Open Scope sym_scope.
Notation "c -->* c'" := (c -[tm]->* c') (at level 40).
Notation "c -->+ c'" := (c -[tm]->+ c') (at level 40).
Lemma transfer l r a b c m :
  l <* [0] <* [1]^^(a+1) {{B}}>
    [1;0] *> [1]^^(b*2+2) *> [0] *> [1]^^(c*2) *>
    [0;0] *> [1]^^(m+2) *> r -->+
  l <* [0] <* [1]^^(a+3) {{B}}>
    [1;0] *> [1]^^(b*2) *> [0] *> [1]^^(c*2+2) *>
    [0;0] *> [1]^^m *> r.
Proof. first_step; es. Qed.

Lemma transfers n : forall l r a b c m,
  l <* [0] <* [1]^^(a+1) {{B}}>
    [1;0] *> [1]^^((b+n)*2) *> [0] *> [1]^^(c*2) *>
    [0;0] *> [1]^^(m+n*2) *> r -->*
  l <* [0] <* [1]^^(a+1+n*2) {{B}}>
    [1;0] *> [1]^^(b*2) *> [0] *> [1]^^((c+n)*2) *>
    [0;0] *> [1]^^m *> r.
Proof.
  induction n; intros l r a b c m.
  - simpl_tape; finish.
  - mid (l <* [0] <* [1]^^(a+3) {{B}}>
      [1;0] *> [1]^^((b+n)*2) *> [0] *> [1]^^(c*2+2) *>
      [0;0] *> [1]^^(m+n*2) *> r).
    + apply progress_evstep.
      applys_eq (transfer l r a (b+n) c (m+n*2)); flia.
    + applys_eq (IHn l r (a+2) b (c+1) m); flia.
Qed.

Lemma reset l r a m :
  l <* [0] <* [1]^^a {{B}}> [1;0;0] *> [1]^^(m+1) *> r -->+
  l {{E}}> [0] *> [0]^^a *> [1;1;0;0] *> [1]^^m *> r.
Proof. first_step; es. Qed.

Lemma odd_middle_can_halt :
  halts tm (0inf <* [1] {{B}}> [1;0;1;1;0;1;0;0;1;1] *> 0inf).
Proof. esx. Qed.

Print Assumptions transfer.
Print Assumptions transfers.
Print Assumptions reset.
Print Assumptions odd_middle_can_halt.
