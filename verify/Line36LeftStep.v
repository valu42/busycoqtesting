(** Concrete word evaluation for a finite-debt left-front transition.
    Digits are true for opening 1. For piece alternatives false selects the
    first displayed option; for halo mask bits, a set bit means closing 2. *)
From Coq Require Import List Bool Arith ZArith Lia.
From BusyCoq Require Import Line36Left Line36Matching Line36Tiles.
Import ListNotations L36Left L36Tiles.
Local Open Scope nat_scope.

Module L36LeftStep.
Definition table := Eval vm_compute in
  (map (fun t => map (fun k => (phase_pieces t k false, phase_pieces t k true))
                     (seq 0 6)) (seq 0 6)).
Definition piece (t k : nat) (v : bool) : list bool :=
  let '(a,b) := nth k (nth t table []) ([],[]) in if v then b else a.
Definition prefixes := Eval vm_compute in (map phase_prefix (seq 0 6)).
Definition pre (t : nat) : list bool := nth t prefixes [].
Definition halo_word (n : nat) : list bool :=
  [negb (Nat.testbit n 0); negb (Nat.testbit n 1); negb (Nat.testbit n 2)].
Definition encode_halo (w : list bool) : nat :=
  match w with
  | a :: b :: c :: _ =>
    (if a then 0 else 1) + (if b then 0 else 2) + (if c then 0 else 4)
  | _ => 8
  end.

Definition piece_count (k : nat) := 11 + ((k+55) mod 6).
Definition representative (s : state) (history : nat) : list bool :=
  let cnt := piece_count (kind s) in
  let variant := fun j => if Nat.eqb (S j) cnt then last_choice s
                          else if j <? cnt-5 then false
                          else Nat.testbit history (j-(cnt-5)) in
  pre (phase s) ++ flat_map (fun j => piece (phase s) (j mod 6) (variant j)) (seq 0 cnt)
      ++ firstn (partial_len s) (piece (phase s) (kind s) (partial_choice s)).

Definition physical_header (guard : nat) : list bool :=
  match guard with
  | 0 | 1 => [false]
  | 2 => [true]
  | 3 => [false;false;true;true;false;true]
  | 4 => [false;false;true;true;false;false]
  | _ => [false;false;true;true;true;true]
  end.
Fixpoint derivative (previous : bool) (bits : list bool) : list bool :=
  match bits with
  | [] => []
  | b :: r => Bool.eqb previous b :: derivative b r
  end.

(** [scan w p a] follows the physical checkerboard parity starting at [p]
    and the most recent closing's colour [a]. *)
Fixpoint scan (w : list bool) (p a : bool) (cost : nat) : bool * nat :=
  match w with
  | [] => (a,cost)
  | true :: r => scan r (negb p) a cost
  | false :: r => scan r (negb p) p (if Bool.eqb p a then cost else S cost)
  end.

(** Match as many digits as possible, returning the unmatched suffix of
    the input exactly when the entire candidate piece fit. *)
Fixpoint read_piece (p w : list bool) : nat * option (list bool) :=
  match p,w with
  | [],_ => (0,Some w)
  | _::_,[] => (0,None)
  | a::q,b::r => if Bool.eqb a b
                 then let '(n,rest) := read_piece q r in (S n, rest)
                 else (0,None)
  end.

Record parsed := Parsed {
  complete : nat; next_kind : nat; prev_bit : bool;
  next_bit : bool; partial : nat; cut : nat
}.
Fixpoint reparse (gas ph k n : nat) (last : bool) (pos : nat) (w : list bool)
  : option parsed :=
  match gas with
  | 0 => None
  | S gas' =>
    let '(l0,r0) := read_piece (piece ph k false) w in
    match r0 with
    | Some r => reparse gas' ph ((S k) mod 6) (S n) false (pos+l0) r
    | None =>
      let '(l1,r1) := read_piece (piece ph k true) w in
      match r1 with
      | Some r => reparse gas' ph ((S k) mod 6) (S n) true (pos+l1) r
      | None => let choice := l0 <? l1 in
                let len := if choice then l1 else l0 in
                Some (Parsed n k last choice len (pos+len))
      end
    end
  end.
Record context := Ctx {
  x : nat; full : list bool; old_color : bool; old_switches : nat
}.
Definition prepare s history : context :=
  let p := representative s history in
  let h := halo_word (halo s) in
  let x := length p in
  let color := fst (scan p false false 0) in
  let '(last,cost) := scan h (Nat.odd x) color 0 in
  Ctx x (p++h) last cost.
Definition change (p q : bool) : Z := if Bool.eqb p q then 0%Z else 1%Z.

Definition bridge_cost (old last beta bridge : bool) (d : nat) (survives : bool) : Z :=
  let alignment := negb (Bool.eqb old bridge) in
  let low := d - (if alignment then 1 else 0) in
  let consumed := if Bool.eqb (Nat.odd low) (xorb old beta) then low else S low in
  let boundary := if survives then (change last bridge + change bridge beta)%Z
                             else change last beta in
  let nonempty := (boundary - Z.of_nat consumed)%Z in
  if Nat.eqb d 0
  then Z.max nonempty (if survives then change last old
                      else (change last bridge + change bridge old)%Z)
  else nonempty.

Definition evaluate (s : state) (c : context) (d : nat) : option edge :=
  let t := phase s in
  let next := (S t) mod 6 in
  let '(guard,bits) := mark36 (full c) d in
  if negb (guard =? phase_guard t) then None else
  let head := physical_header guard in
  let h := length head in
  let out := head ++ derivative (guard =? 1) bits in
  let '(prefix_size,remain) := read_piece (pre next) (firstn (x c + h) out) in
  match remain with None => None | Some r =>
  match reparse 24 next 0 0 false prefix_size r with None => None | Some parsed =>
  if complete parsed <? piece_count (kind s)-4 then None else
  let pos := cut parsed in
  let tail := skipn pos out in
  let nh := encode_halo tail in
  if nh =? 8 then None else
  let dst := State next (next_kind parsed) (prev_bit parsed)
                   (next_bit parsed) (partial parsed) nh in
  (* In the new row use colour (j-h+1) mod 2 for the cell at j. *)
  let flip := Nat.even h in
  let new_anchor := fst (scan (firstn pos out) flip false 0) in
  let '(color,switches) := scan tail (xorb (Nat.odd pos) flip) new_anchor 0 in
  let y := x c + 3 in
  let survives := andb (Nat.eqb d 0) (last (full c) false) in
  let boundary := bridge_cost (old_color c) color (Nat.odd (y+d+1))
                                  (Nat.odd (y+1)) d survives in
  Some (Edge dst (Z.of_nat pos - Z.of_nat (x c))%Z
             (Z.of_nat switches + boundary - Z.of_nat (old_switches c))%Z)
  end end.
Definition step s history d := evaluate s (prepare s history) d.
End L36LeftStep.
