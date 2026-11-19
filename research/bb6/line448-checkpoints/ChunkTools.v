From BusyCoq Require Import Individual62 Line448Engine.
From Coq Require Import List NArith ZArith PrimInt63.
From Coq Require Uint63.
Import ListNotations.
Module E := Line448Engine.H155900.

Definition from_limbs (xs : list int) : N :=
  fold_left (fun a limb => (N.shiftl a 60 + Z.to_N (Uint63.to_Z limb))%N) xs 0%N.

Fixpoint pieces (ks : list nat) (s : E.FastState) : option E.FastState :=
  match ks with
  | [] => Some s
  | k :: more => match E.run_pow k s with
                  | None => None
                  | Some t => pieces more t
                  end
  end.

Definition pending (x : option E.FastState) : Prop :=
  match x with None => True | Some s => halts E.src_tm (E.fs_denote s) end.

Lemma backwards ks s : pending (pieces ks s) -> halts E.src_tm (E.fs_denote s).
Proof.
  revert s. induction ks as [|k ks IH]; intro s; [exact (fun h => h)|].
  simpl pieces. pose proof (E.run_pow_spec k s) as H.
  destruct (E.run_pow k s) as [t|].
  - intro Ht. eapply E.evstep_halts; [exact H | apply IH, Ht].
  - exact (fun _ => H).
Qed.
