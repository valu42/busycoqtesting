(* Stable BB(6) line 110, ID 28035. Uses Individual62 from BusyCoq's BB6 branch. *)
From BusyCoq Require Import Individual62.
From Coq Require Import String.

Module Line110.
Definition tm := Eval compute in
  (TM_from_str "1RB0LB_0RC0LD_1LD1RE_0LA0RF_1RB0RD_0RB---"%string).

(* Enter starts at C with a zero immediately to the left. A completed visit
   returns in A two cells left of that entry. A frame says what to do next. *)
Inductive frame :=
  | Root
  | Pass (parent : frame)
  | DoubleFirst (parent : frame) | DoubleSecond (parent : frame)
  | NestedFirst (parent : frame) | NestedSecond (parent : frame).

Inductive phase := Enter (k : frame) (word : side) | Return (k : frame) (word : side).

Definition advance (p : phase) : nat * option phase :=
  match p with
  | Enter k (Cons S0 u) => (2%nat, Some (Return k (S1 >> u)))
  | Enter k (Cons S1 (Cons S0 (Cons S0 u))) => (3%nat, Some (Enter (Pass k) u))
  | Enter k (Cons S1 (Cons S1 (Cons S0 u))) => (5%nat, Some (Enter (Pass k) u))
  | Enter k (Cons S1 (Cons S0 (Cons S1 (Cons S0 u)))) => (6%nat, Some (Enter (DoubleFirst k) u))
  | Enter k (Cons S1 (Cons S0 (Cons S1 (Cons S1 u)))) => (14%nat, Some (Return k (S0 >> S0 >> S0 >> S1 >> u)))
  | Enter k (Cons S1 (Cons S1 (Cons S1 (Cons S0 (Cons S0 u))))) => (5%nat, Some (Enter (NestedFirst k) u))
  | Enter k (Cons S1 (Cons S1 (Cons S1 (Cons S0 (Cons S1 u))))) => (18%nat, Some (Return k (S1 >> S0 >> S1 >> S0 >> S1 >> u)))
  | Enter _ (Cons S1 (Cons S1 (Cons S1 (Cons S1 _)))) => (3%nat, None)
  | Return Root u => (6%nat, Some (Enter Root (S1 >> S0 >> u)))
  | Return (Pass k) u => (3%nat, Some (Return k (S0 >> S0 >> S0 >> u)))
  | Return (DoubleFirst k) u => (2%nat, Some (Enter (DoubleSecond k) u))
  | Return (DoubleSecond k) u => (8%nat, Some (Return k (S1 >> S0 >> S1 >> S0 >> u)))
  | Return (NestedFirst k) u => (2%nat, Some (Enter (NestedSecond k) u))
  | Return (NestedSecond k) u => (6%nat, Some (Enter (Pass k) (S1 >> S0 >> u)))
  end.

Definition next (p : phase) := snd (advance p).

(* Nearest first, the cells left of a visit are 0, marker k, then exterior k. *)
Definition marker k : Sym :=
  match k with DoubleFirst _ | NestedFirst _ => S0 | _ => S1 end.

Fixpoint exterior k : side :=
  match k with
  | Root => const S0
  | Pass p => S1 >> S0 >> marker p >> exterior p
  | DoubleFirst p | DoubleSecond p => S0 >> S1 >> S0 >> marker p >> exterior p
  | NestedFirst p | NestedSecond p => S0 >> S0 >> S1 >> S0 >> marker p >> exterior p
  end.

Definition decode (p : phase) : Q * tape :=
  match p with
  | Enter k u => S0 >> marker k >> exterior k {{C}}> u
  | Return k u => exterior k {{A}}> marker k >> S0 >> u
  end.

Definition start := Enter Root (const S0).

Lemma blank_entry : c0 -[tm]->+ decode start.
Proof. unfold start, decode, c0, tape0; cbn; execute. Qed.

(* Each clock counts defined instructions. On 1111 the last configuration
   scans the undefined F1 instruction; entering it costs three steps. *)
Ltac count_steps :=
  repeat first [apply multistep_0 | eapply multistep_S; [prove_step | simpl_tape]].

Lemma advance_spec p :
  let '(n, result) := advance p in
  match result with
  | Some p' => 0 < n /\ decode p -[tm]->> n / decode p'
  | None => halts_in tm (decode p) n
  end.
Proof.
  destruct p as [k u | k u].
  - do 5 (destruct u as [[|] u]); cbn [advance decode marker exterior];
      first [solve [split; [auto with arith | count_steps]]
            | solve [eexists; split; [count_steps | reflexivity]]].
  - destruct k; cbn [advance decode marker exterior];
      (split; [auto with arith | count_steps]).
Qed.

Lemma next_spec p :
  match next p with
  | Some p' => decode p -[tm]->+ decode p'
  | None => halts tm (decode p)
  end.
Proof.
  pose proof (advance_spec p) as H. unfold next.
  destruct (advance p) as [n [p'|]]; cbn in *.
  - destruct H as [Hn Hsteps]. destruct n; [inversion Hn |].
    exact (multistep_progress _ _ _ _ Hsteps).
  - exists n. exact H.
Qed.

Theorem blank_iff : halts tm c0 <-> iter_halts next start.
Proof.
  rewrite (halts_evstep_iff _ _ _ (progress_evstep _ _ _ blank_entry)).
  apply (halts_iff tm phase start next decode (fun _ => True)).
  - intros p _. pose proof (next_spec p) as H. destruct (next p); tauto.
  - exact I.
Qed.
End Line110.
