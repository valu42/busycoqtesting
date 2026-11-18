From Coq Require Import List Bool.
From BusyCoq Require Import Line36Matching.
Import ListNotations.

Fixpoint cap_after_anchor (w : list bool) : list bool :=
  match w with
  | [] => []
  | false :: rest => rest
  | true :: rest => cap_after_anchor rest
  end.

Fixpoint cap_deriv (previous : bool) (bits : list bool) : list bool :=
  match bits with
  | [] => []
  | s :: rest => Bool.eqb previous s :: cap_deriv s rest
  end.

Definition cap_next (w : list bool) (previous : bool) : list bool :=
  let '(debt,bits) := mark36 w 0 in
  let out := cap_deriv (andb previous (Nat.eqb debt 0)) bits in
  if last w false then tl out ++ [false] else out.
