(** Binary checkpoint map for the physical machine on line 36. *)
From Coq Require Import List Bool Arith.
From BusyCoq Require Export Line36Matching.
Import ListNotations.

Fixpoint deriv36 (previous : bool) (bits : list bool) : list bool :=
  match bits with
  | [] => []
  | current :: rest => Bool.eqb previous current :: deriv36 current rest
  end.

Definition carry36 (previous : bool) (bits : list bool) : list bool :=
  if last bits previous then [false] else [].

Definition guard36 (d : nat) : list bool :=
  match d with
  | 0 | 1 => [false]
  | 2 => [true]
  | 3 => [false;false;true;true;false;true]
  | 4 => [false;false;true;true;false;false]
  | _ => [false;false;true;true;true;true]
  end.

Definition output36 d bits :=
  guard36 d ++ deriv36 (Nat.eqb d 1) bits ++ carry36 (Nat.eqb d 1) bits.

Definition step36 w : option (list bool) :=
  let '(d,bits) := mark36 w 0 in
  if d <? 6 then Some (output36 d bits) else None.

Lemma last36_cons (a p : bool) w : last (a::w) p = last w a.
Proof.
  revert a p. induction w as [|b w IH]; intros a p; [reflexivity|].
  change (last (b::w) p = last (b::w) a).
  now rewrite (IH b p), (IH b a).
Qed.

Lemma last36_app (a : bool) l r :
  last (l ++ r) a = last r (last l a).
Proof.
  revert a. induction l as [|b l IH]; intros a; [reflexivity|].
  cbn [app]. repeat rewrite last36_cons. apply IH.
Qed.

Lemma deriv36_app a l r :
  deriv36 a (l++r) = deriv36 a l ++ deriv36 (last l a) r.
Proof.
  revert a. induction l as [|b l IH]; intros a; [reflexivity|].
  cbn [app deriv36]. rewrite last36_cons, IH. reflexivity.
Qed.
