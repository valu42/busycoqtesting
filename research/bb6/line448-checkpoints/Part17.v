From BusyCoq Require Import Individual62 Line448Engine.
From Coq Require Import List NArith ZArith PrimInt63.
From Coq Require Uint63.
Require Import ChunkTools.
Import ListNotations Line448Engine.H155900.
Require S423936.

Definition last_calls : list nat := [0%nat; 1%nat; 2%nat; 3%nat; 5%nat; 10%nat; 11%nat].

Definition stopped_on_F1 (s : FastState) : bool :=
  match fs_mode s with
  | RAW F L => sym_eqb (fst (runs_pop (fs_L s))) 1
  | RAW F R => sym_eqb (fst (popBitRTape (fs_R s))) 1
  | _ => false
  end && match stepFast s with None => true | Some _ => false end.

Definition checked_end (s : option FastState) : bool :=
  match s with Some t => stopped_on_F1 t | None => false end.

Lemma checked : checked_end (pieces last_calls S423936.checkpoint) = true.
Proof. vm_check_eq. Qed.

Lemma segment : True -> halts src_tm (fs_denote S423936.checkpoint).
Proof.
  intros _. apply (backwards last_calls S423936.checkpoint).
  pose proof checked as h.
  destruct (pieces last_calls S423936.checkpoint) as [s|]; [|discriminate].
  cbn [checked_end] in h. unfold stopped_on_F1 in h.
  apply Bool.andb_true_iff in h. destruct h as [_ stop].
  pose proof (stepFast_spec s) as h.
  destruct (stepFast s); [discriminate | exact h].
Qed.
Print Assumptions segment.
