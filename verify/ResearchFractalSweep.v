(* Exact whole-sweep reduction for the public chaotic-fractal table below.
   This is NOT a proof that its blank run halts or does not halt.

   turn is defined on every pair of finite binary words. Both scans terminate
   structurally. The theorem blank_halts_iff_turns transfers the blank-run
   halting question, in both directions, to iteration of this recurrence.

   Words are nearest-cell first; the right word includes the scanned cell.
   Missing cells are zero. AI-assisted research by Codex, using the BusyCoq
   authors' TM semantics, execution tactics and general halts_iff theorem. *)
From BusyCoq Require Import Individual62 ES_v2.
From Coq Require Import List String Lia.
Import ListNotations.
Open Scope sym_scope.

Module FractalSweep.
Definition tm := Eval compute in
  (TM_from_str "1RB1LE_0RC1RC_0RD0RB_1RE0RF_1LA0LE_---1RB").
Notation "c -->* c'" := (c -[tm]->* c') (at level 40).
Notation "c -->+ c'" := (c -[tm]->+ c') (at level 40).

Definition word := list sym.
Definition pair := (word * word)%type.
Definition side_of (w : word) : side := w *> 0inf.
Definition config (q : Q) (p : pair) :=
  side_of (fst p) {{q}}> side_of (snd p).

(* The right scan reads a prefix code:
     a1   -> a0,   continue B
     a011 -> a001, continue B
     a00  -> a01,  switch to E
     a010 -> halt (F reading zero).
   The output is pushed onto the left word in reverse order. *)
Fixpoint right_scan (l r : word) {struct r} : option pair :=
  match r with
  | a :: S1 :: rest => right_scan (S0 :: a :: l) rest
  | a :: S0 :: S1 :: S1 :: rest =>
      right_scan (S1 :: S0 :: S0 :: a :: l) rest
  | a :: S0 :: S1 :: _ => None
  | a :: S0 :: S0 :: rest => Some (S1 :: S0 :: a :: l, rest)
  | a :: _ => Some (S1 :: S0 :: a :: l, [])
  | [] => Some ([S1;S0;S0] ++ l, [])
  end.

(* E erases 1s while moving left; 0 followed by a left-hand 1
   becomes 11; a pair of zeros ends the sweep and returns to B.
   All recursive calls consume at least one cell of l. The empty
   cases explicitly execute the final one or two blank cells. *)
Fixpoint left_scan (l r : word) {struct l} : pair :=
  let rest := tl r in
  match l with
  | [] => match hd S0 r with
          | S1 => ([S1], S1 :: S0 :: rest)
          | S0 => ([S1], S1 :: rest)
          end
  | a :: more =>
      match hd S0 r with
      | S1 => left_scan more (a :: S0 :: rest)
      | S0 => match a with
              | S0 => (S1 :: more, S1 :: rest)
              | S1 => match more with
                      | [] => ([S1], S1 :: S1 :: S1 :: rest)
                      | b :: more' => left_scan more' (b :: S1 :: S1 :: rest)
                      end
              end
      end
  end.

Definition turn (p : pair) : option pair :=
  match right_scan (fst p) (snd p) with
  | None => None
  | Some (l,r) => Some (left_scan l r)
  end.

Ltac first_step := eapply progress_intro; [prove_step | simpl_tape].

Lemma B_pair l r a :
  l {{B}}> [a;1] *> r -->+ l <* [0;a] {{B}}> r.
Proof. destruct a; first_step; es. Qed.
Lemma B_four l r a :
  l {{B}}> [a;0;1;1] *> r -->+ l <* [1;0;0;a] {{B}}> r.
Proof. destruct a; first_step; es. Qed.
Lemma B_exit l r a :
  l {{B}}> [a;0;0] *> r -->+ l <* [1;0;a] {{E}}> r.
Proof. destruct a; first_step; es. Qed.
Lemma B_stop l r a : halts tm (l {{B}}> [a;0;1;0] *> r).
Proof. destruct a; esx. Qed.

Lemma right_scan_spec l r :
  match right_scan l r with
  | Some p => config B (l,r) -->+ config E p
  | None => halts tm (config B (l,r))
  end.
Proof.
  revert l r; fix IH 2; intros l r.
  destruct r as [|a [|b r]].
  - cbn [right_scan config fst snd side_of]; first_step; es.
  - cbn [right_scan config fst snd side_of]; destruct a; first_step; es.
  - destruct b.
    + destruct r as [|c r].
      * cbn [right_scan config fst snd side_of]; destruct a; first_step; es.
      * destruct c.
        -- cbn [right_scan config fst snd side_of]; apply B_exit.
        -- destruct r as [|d r].
           ++ cbn [right_scan config fst snd side_of]; destruct a; esx.
           ++ destruct d.
              ** cbn [right_scan config fst snd side_of]; apply B_stop.
              ** cbn [right_scan].
                 specialize (IH (S1::S0::S0::a::l) r).
                 destruct (right_scan (S1::S0::S0::a::l) r) as [p|].
                 --- eapply progress_trans; [|exact IH].
                     unfold config,side_of; cbn; apply B_four.
                 --- eapply halts_evstep; [exact IH|].
                     apply progress_evstep; unfold config,side_of; cbn; apply B_four.
    + cbn [right_scan]. specialize (IH (S0::a::l) r).
      destruct (right_scan (S0::a::l) r) as [p|].
      * eapply progress_trans; [|exact IH].
        unfold config,side_of; cbn; apply B_pair.
      * eapply halts_evstep; [exact IH|].
        apply progress_evstep; unfold config,side_of; cbn; apply B_pair.
Qed.

Lemma left_scan_spec l r : config E (l,r) -->+ config B (left_scan l r).
Proof.
  revert l r; fix IH 1; intros l r.
  destruct l as [|a l].
  - destruct r as [|b r]; [|destruct b];
      cbn [left_scan config fst snd side_of hd tl]; first_step; es.
  - destruct r as [|b r].
    + destruct a.
      * cbn [left_scan config fst snd side_of hd tl]; first_step; es.
      * destruct l as [|a l].
        -- cbn [left_scan config fst snd side_of hd tl]; first_step; es.
        -- cbn [left_scan hd tl]. eapply progress_evstep_trans.
           2: apply progress_evstep, IH.
           unfold config,side_of; cbn; destruct a; first_step; es.
    + destruct b.
      * destruct a.
        -- cbn [left_scan config fst snd side_of hd tl]; first_step; es.
        -- destruct l as [|a l].
           ++ cbn [left_scan config fst snd side_of hd tl]; first_step; es.
           ++ cbn [left_scan hd tl]. eapply progress_evstep_trans.
              2: apply progress_evstep, IH.
              unfold config,side_of; cbn; destruct a; first_step; es.
      * cbn [left_scan hd tl]. eapply progress_evstep_trans.
        2: apply progress_evstep, IH.
        unfold config,side_of; cbn; destruct a; first_step; es.
Qed.

Lemma turn_spec p :
  match turn p with
  | Some p' => config B p -->+ config B p'
  | None => halts tm (config B p)
  end.
Proof.
  destruct p as [l r]; unfold turn; cbn [fst snd].
  pose proof (right_scan_spec l r) as H.
  destruct (right_scan l r) as [[l' r']|]; [|exact H].
  eapply progress_trans; [exact H|apply left_scan_spec].
Qed.

Theorem halts_iff_turns p : halts tm (config B p) <-> iter_halts turn p.
Proof.
  eapply (halts_iff tm pair p turn (config B) (fun _ => True)).
  - intros i _; pose proof (turn_spec i) as H.
    destruct (turn i); [split; [exact H|exact I]|exact H].
  - exact I.
Qed.

Definition initial : pair := ([S1], []).
Lemma blank_to_initial : c0 -->+ config B initial.
Proof. unfold initial,config,side_of; cbn; first_step; es. Qed.

Theorem blank_halts_iff_turns : halts tm c0 <-> iter_halts turn initial.
Proof.
  rewrite <-halts_iff_turns.
  apply halts_evstep_iff, progress_evstep, blank_to_initial.
Qed.

(* A short counterexample to the tempting invariant that the right word
   has no isolated 1 after its leading cell. 10011 has that property,
   but its next sweep leaves 1011001, which the next right scan halts on. *)
Lemma no_isolated_one_is_insufficient : halts tm (config B ([S1],[S1;S0;S0;S1;S1])).
Proof. unfold config,side_of; cbn; esx. Qed.

Print Assumptions right_scan_spec.
Print Assumptions left_scan_spec.
Print Assumptions turn_spec.
Print Assumptions halts_iff_turns.
Print Assumptions blank_halts_iff_turns.
Print Assumptions no_isolated_one_is_insufficient.
End FractalSweep.
