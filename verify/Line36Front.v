(** One concrete cut on an actual tape. A cutoff at the end of a piece
    uses an empty initial part of the next piece. *)
From Coq Require Import List Bool Arith ZArith Lia.
From BusyCoq Require Import Line36Tiles Line36Left Line36LeftStep.
Import ListNotations.
Local Open Scope list_scope.
Local Open Scope nat_scope.

Record front36 := Front36 {
  fphase : nat; fchoices : list bool; foption : bool; flen : nat; ftail : list bool
}.
Definition fkind f := length (fchoices f) mod 6.
Definition fpart f := firstn (flen f) (L36Tiles.phase_pieces (fphase f) (fkind f) (foption f)).
Definition fdata f := L36Tiles.segments (fphase f) 0 (fchoices f) ++ fpart f.
Definition fprefix f := L36Tiles.phase_prefix (fphase f) ++ fdata f.
Definition fword f := fprefix f ++ ftail f.
Definition fstate f := L36Left.State (fphase f) (fkind f) (last (fchoices f) false)
                        (foption f) (flen f) (L36LeftStep.encode_halo (ftail f)).
Definition fvalid f :=
  fphase f < 6 /\ flen f < length (L36Tiles.phase_pieces (fphase f) (fkind f) (foption f))
  /\ 53 <= length (ftail f).
