From BusyCoq Require Import Individual62 Line448Engine.
From Coq Require Import List NArith ExtrOcamlZBigInt.
Import ListNotations.
Import Line448Engine.H155900.
Open Scope sym_scope.

Definition blank_start448 (q : Q) : FastState :=
  MkFastState [] (MkRTape [] [] [] []) (RAW q R).

Definition next448 := stepFast.
Definition reading_F1 (s : FastState) : bool :=
  match fs_mode s with
  | RAW F L => sym_eqb (fst (runs_pop (fs_L s))) 1
  | RAW F R => sym_eqb (fst (popBitRTape (fs_R s))) 1
  | _ => false
  end.

(* Accelerate the independent executable replay with arbitrary-precision
   integers. The halting theorem uses Gallina's own binary arithmetic. *)
Extract Constant PrimInt63.int => "Uint63.t".
Extract Constant N.eqb => "Z.equal".
Extract Constant N.leb => "Z.leq".
Extract Constant N.ltb => "Z.lt".
Extract Constant N.div2 => "(fun x -> Z.shift_right x 1)".
Extraction Language OCaml.
Extraction "engine448.ml" blank_start448 next448 reading_F1.
