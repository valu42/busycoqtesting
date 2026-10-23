(* Halting of original BB6_holdouts_663.txt entry 274:
   1RB0LB_0RC0LD_1LD1RE_0LA0RB_0RD0RF_1RA---.

   Longitudinal packets describe a C/[0] call and its A/[0] return.
   Seven local packet laws yield binary-arithmetic batches. The evaluator
   preserves the semantics of returned calls and early halts; exhaustion
   returns Unknown and cannot establish a decision. A checked finite orbit
   then reaches a halting packet from the exact blank initial configuration.
   This proves the outcome only, not the total running time or sigma score. *)
From BusyCoq Require Import Individual62 Longitudinal LongitudinalHalt.
From Coq Require Import String List Lia NArith Bool.
Import ListNotations.
Open Scope list.
Set Warnings "-abstract-large-number".

Module TM1.
Definition tm := Eval compute in
  TM_from_str "1RB0LB_0RC0LD_1LD1RE_0LA0RB_0RD0RF_1RA---".
Definition hR : DH0 := (C,[0]).
Definition hL : DH0 := (A,[0]).
Definition h := [(hR,hL)].

(* Finite packets hold for arbitrary surrounding tape. *)
Lemma packet0 : segRLs tm h [] [0] [1].
Proof. unfold h,hR,hL. solve_segRLs. Qed.
Lemma packet100 : segRLs tm h h [1;0;0] [0;0;0].
Proof. unfold h,hR,hL. solve_segRLs. Qed.
Lemma packet1010 : segRLs tm h (h++h) [1;0;1;0] [1;0;1;0].
Proof. unfold h,hR,hL. solve_segRLs. Qed.
Lemma packet1011 : segRLs tm h [] [1;0;1;1] [0;0;0;1].
Proof. unfold h,hR,hL. solve_segRLs. Qed.
Lemma packet1101 : segRLs tm h [] [1;1;0;1] [1;0;0;0].
Proof. unfold h,hR,hL. solve_segRLs. Qed.
Lemma packet11000 : segRLs tm h h [1;1;0;0;0] [1;0;0;0;0].
Proof. unfold h,hR,hL. solve_segRLs. Qed.
Lemma packet11001 : segRLs tm h (h++h) [1;1;0;0;1] [1;0;0;0;0].
Proof. unfold h,hR,hL. solve_segRLs. Qed.

(* Batch adjacent calls using binary arithmetic. *)
Lemma batch1010 n : segRLs tm (h^^n) (h^^(n*2)) [1;0;1;0] [1;0;1;0].
Proof. applys_eq (Longitudinal.segRLs_addmul_v2 1 2 n 0 0 tm h [1;0;1;0] [1;0;1;0]); try (f_equal; lia); unfold h,hR,hL; solve_segRLs. Qed.
Lemma batch000_even n : segRLs tm (h^^(n*2)) (h^^n) [0;0;0] [0;0;0].
Proof. applys_eq (Longitudinal.segRLs_addmul_v2 2 1 n 0 0 tm h [0;0;0] [0;0;0]); try (f_equal; lia); unfold h,hR,hL; solve_segRLs. Qed.
Lemma batch100_even n : segRLs tm (h^^(n*2)) (h^^n) [1;0;0] [1;0;0].
Proof. applys_eq (Longitudinal.segRLs_addmul_v2 2 1 n 0 0 tm h [1;0;0] [1;0;0]); try (f_equal; lia); unfold h,hR,hL; solve_segRLs. Qed.
Lemma batch000_odd n : segRLs tm (h^^(n*2+1)) (h^^n) [0;0;0] [1;0;0].
Proof. applys_eq (Longitudinal.segRLs_addmul_v2 2 1 n 1 0 tm h [0;0;0] [1;0;0]); try (f_equal; lia); unfold h,hR,hL; solve_segRLs. Qed.
Lemma batch100_odd n : segRLs tm (h^^(n*2+1)) (h^^(n+1)) [1;0;0] [0;0;0].
Proof. applys_eq (Longitudinal.segRLs_addmul_v2 2 1 n 1 1 tm h [1;0;0] [0;0;0]); try (f_equal; lia); unfold h,hR,hL; solve_segRLs. Qed.
Lemma batch0010 n : segRLs tm (h^^(S n)) (h^^(n*2)) [0;0;1;0] [1;0;1;0].
Proof. replace (S n) with (n+1) by lia. applys_eq (Longitudinal.segRLs_addmul_v2 1 2 n 1 0 tm h [0;0;1;0] [1;0;1;0]); try (f_equal; lia); unfold h,hR,hL; solve_segRLs. Qed.
Lemma terminal111 l r : halts tm (l {{{(hR,R)}}} [1;1;1] *> r).
Proof. unfold hR. solve_halt. Qed.

Definition Calls (n:N) := h^^N.to_nat n.
Lemma doubleN n : segRLs tm (Calls n) (Calls (N.double n)) [1;0;1;0] [1;0;1;0].
Proof. unfold Calls. rewrite N2Nat.inj_double. replace (2*N.to_nat n) with (N.to_nat n*2) by lia. apply batch1010. Qed.
Lemma half0N n : segRLs tm (Calls n) (Calls (N.div2 n)) [0;0;0] [(if N.odd n then 1 else 0);0;0].
Proof.
 unfold Calls. pose proof (f_equal N.to_nat (N.div2_odd n)) as E.
 rewrite N2Nat.inj_add,N2Nat.inj_mul in E.
 destruct (N.odd n); cbn[N.b2n N.to_nat] in E |- *.
 - change (N.to_nat n = 2*N.to_nat (N.div2 n)+1) in E.
   applys_eq (batch000_odd (N.to_nat (N.div2 n))); f_equal; lia.
 - change (N.to_nat n = 2*N.to_nat (N.div2 n)+0) in E.
   applys_eq (batch000_even (N.to_nat (N.div2 n))); f_equal; lia.
Qed.
Lemma half1N n : segRLs tm (Calls n) (Calls (N.div2 (N.succ n))) [1;0;0] [(if negb (N.odd n) then 1 else 0);0;0].
Proof.
 unfold Calls. pose proof (f_equal N.to_nat (N.div2_odd n)) as E.
 pose proof (f_equal N.to_nat (N.div2_odd (N.succ n))) as F.
 rewrite N2Nat.inj_add,N2Nat.inj_mul in E.
 rewrite N2Nat.inj_add,N2Nat.inj_mul,N2Nat.inj_succ in F.
 rewrite N.odd_succ, <-N.negb_odd in F.
 destruct (N.odd n); cbn[N.b2n N.to_nat negb] in E,F |- *.
 - change (N.to_nat n = 2*N.to_nat (N.div2 n)+1) in E.
   change (S(N.to_nat n) = 2*N.to_nat (N.div2 (N.succ n))+0) in F.
   applys_eq (batch100_odd (N.to_nat (N.div2 n))); f_equal; lia.
 - change (N.to_nat n = 2*N.to_nat (N.div2 n)+0) in E.
   change (S(N.to_nat n) = 2*N.to_nat (N.div2 (N.succ n))+1) in F.
   applys_eq (batch100_even (N.to_nat (N.div2 n))); f_equal; lia.
Qed.
Lemma q0010N n : (0<n)%N -> segRLs tm (Calls n) (Calls (N.double (N.pred n))) [0;0;1;0] [1;0;1;0].
Proof. intros Hn. unfold Calls. rewrite N2Nat.inj_double,N2Nat.inj_pred. replace (N.to_nat n) with (S (Nat.pred (N.to_nat n))) at 1 by lia. replace (2*Nat.pred (N.to_nat n)) with (Nat.pred (N.to_nat n)*2) by lia. apply batch0010. Qed.

(* Total prefix decoding, padded by the known blank right tail. *)
Inductive Action :=
| Double | Half0 | Half1 | Q0010 | Flip0
| Reset1011 | Reset1101 | Child1 | Child2 | Terminal.
Definition prefix (a:Action) : list Sym :=
 match a with
 | Double => [1;0;1;0] | Half0 => [0;0;0] | Half1 => [1;0;0]
 | Q0010 => [0;0;1;0] | Flip0 => [0]
 | Reset1011 => [1;0;1;1] | Reset1101 => [1;1;0;1]
 | Child1 => [1;1;0;0;0] | Child2 => [1;1;0;0;1]
 | Terminal => [1;1;1] end.
Definition pop (w:list Sym) : Sym * list Sym :=
 match w with [] => (0,[]) | b::t => (b,t) end.
Definition decode (w:list Sym) : Action * list Sym :=
 let '(b0,t0) := pop w in
 match b0 with
 | S0 => let '(b1,t1) := pop t0 in
     match b1 with
     | S1 => (Flip0,t0)
     | S0 => let '(b2,t2) := pop t1 in
         match b2 with
         | S0 => (Half0,t2)
         | S1 => let '(b3,t3) := pop t2 in
             match b3 with S0 => (Q0010,t3) | S1 => (Flip0,t0) end
         end
     end
 | S1 => let '(b1,t1) := pop t0 in
     match b1 with
     | S0 => let '(b2,t2) := pop t1 in
         match b2 with
         | S0 => (Half1,t2)
         | S1 => let '(b3,t3) := pop t2 in
             match b3 with S0 => (Double,t3) | S1 => (Reset1011,t3) end
         end
     | S1 => let '(b2,t2) := pop t1 in
         match b2 with
         | S1 => (Terminal,t2)
         | S0 => let '(b3,t3) := pop t2 in
             match b3 with
             | S1 => (Reset1101,t3)
             | S0 => let '(b4,t4) := pop t3 in
                 match b4 with S0 => (Child1,t4) | S1 => (Child2,t4) end
             end
         end
     end
 end.
Lemma pop_sound w :
 w *> 0inf = [fst (pop w)] *> (snd (pop w) *> 0inf).
Proof.
 destruct w as [|b t]; cbn[pop fst snd Str_app].
 - apply const_unfold.
 - reflexivity.
Qed.
Lemma decode_sound w :
 let '(a,t) := decode w in w *> 0inf = prefix a *> (t *> 0inf).
Proof.
 unfold decode.
 repeat match goal with
 | |- context [pop ?t] =>
   let H := fresh "Hpop" in let b := fresh "b" in let u := fresh "tail" in
   pose proof (pop_sound t) as H;
   destruct (pop t) as [b u]; cbn[fst snd] in H; destruct b
 end.
 all: cbn[prefix].
 all: unfold Sym in *.
 all: rewrite Hpop.
 all: repeat match goal with H : _ = _ |- _ => progress rewrite H end.
 all: reflexivity.
Qed.

Inductive Outcome := Unknown | Done (w:list Sym) | Halt.
Definition prepend (w:list Sym) (x:Outcome) :=
 match x with Done t => Done (w++t) | _ => x end.
Definition digit (b:bool) : Sym := if b then 1 else 0.
Fixpoint eval (fuel:nat) (n:N) (w:list Sym) : Outcome :=
 match n with
 | N0 => Done w
 | Npos _ => match fuel with
   | O => Unknown
   | S fuel => let '(a,t):=decode w in
     match a with
     | Double => prepend [1;0;1;0] (eval fuel (N.double n) t)
     | Half0 => prepend [digit (N.odd n);0;0] (eval fuel (N.div2 n) t)
     | Half1 => prepend [digit (negb (N.odd n));0;0] (eval fuel (N.div2 (N.succ n)) t)
     | Q0010 => prepend [1;0;1;0] (eval fuel (N.double (N.pred n)) t)
     | Flip0 => eval fuel (N.pred n) (1::t)
     | Reset1011 => eval fuel (N.pred n) ([0;0;0;1]++t)
     | Reset1101 => eval fuel (N.pred n) ([1;0;0;0]++t)
     | Child1 => match eval fuel 1 t with
         | Done u => eval fuel (N.pred n) ([1;0;0;0;0]++u) | x => x end
     | Child2 => match eval fuel 2 t with
         | Done u => eval fuel (N.pred n) ([1;0;0;0;0]++u) | x => x end
     | Terminal => Halt
     end
   end
 end.
Definition denotes (w:list Sym) := w *> 0inf.
Definition Sem (n:N) (w:list Sym) (x:Outcome) : Prop :=
 match x with
 | Unknown => True
 | Done y => sideRLs tm (Calls n) (denotes w) (denotes y)
 | Halt => sideRLs_halt tm (Calls n) (denotes w)
 end.

(* Soundness covers both ordinary returns and early halts in nested calls. *)
Lemma sem_input_eq n w w' x : denotes w = denotes w' -> Sem n w' x -> Sem n w x.
Proof. destruct x; cbn[Sem]; intros E H; [exact I|rewrite E|rewrite E]; assumption. Qed.
Lemma sem_segment n m u v t x :
 segRLs tm (Calls n) (Calls m) u v ->
 Sem m t x -> Sem n (u++t) (prepend v x).
Proof.
 destruct x; cbn[Sem prepend]; intros HS HX; [exact I| |]; unfold denotes in *;
 repeat rewrite Str_app_assoc;
 [eapply segRLs_sideRLs_concat | eapply segRLs_sideRLs_halt_concat]; eassumption.
Qed.
Lemma calls_addN n m : Calls (n+m)%N = Calls n ++ Calls m.
Proof. unfold Calls. rewrite N2Nat.inj_add,lpow_add. reflexivity. Qed.
Lemma sem_after n w u x :
 (0<n)%N -> sideRLs tm (Calls 1) (denotes w) (denotes u) ->
 Sem (N.pred n) u x -> Sem n w x.
Proof.
 intros Hn HS HX. replace n with (1+N.pred n)%N by lia.
 destruct x; cbn[Sem] in *; [exact I| |]; rewrite calls_addN;
 [eapply sideRLs_trans | eapply sideRLs_halt_app_right]; eassumption.
Qed.
Lemma sem_early n w : (0<n)%N -> Sem 1 w Halt -> Sem n w Halt.
Proof.
 intros Hn H. cbn[Sem] in *.
 replace n with (1+N.pred n)%N by lia.
 rewrite calls_addN. apply sideRLs_halt_app_left. exact H.
Qed.
Lemma packet_return u v t : segRLs tm (Calls 1) [] u v ->
 sideRLs tm (Calls 1) (denotes (u++t)) (denotes (v++t)).
Proof. intros H. unfold denotes. repeat rewrite Str_app_assoc.
 eapply segRLs_sideRLs_concat; [exact H|constructor]. Qed.
Lemma sem_single n u v t x : (0<n)%N -> segRLs tm (Calls 1) [] u v ->
 Sem (N.pred n) (v++t) x -> Sem n (u++t) x.
Proof. intros Hn H Hx. eapply sem_after; [exact Hn|eapply packet_return; exact H|exact Hx]. Qed.
Lemma sem_child n m u v t x f : (0<n)%N ->
 segRLs tm (Calls 1) (Calls m) u v ->
 Sem m t x ->
 (forall y, x=Done y -> Sem (N.pred n) (v++y) (f y)) ->
 Sem n (u++t) (match x with Unknown => Unknown | Done y => f y | Halt => Halt end).
Proof.
 intros Hn HS HX HF. destruct x; cbn[Sem] in *.
 - exact I.
 - apply (sem_after n (u++t) (v++w)); [exact Hn| |exact (HF w eq_refl)].
   unfold denotes. repeat rewrite Str_app_assoc. eapply segRLs_sideRLs_concat; eassumption.
 - apply sem_early; [exact Hn|]. cbn[Sem]. unfold denotes.
   rewrite Str_app_assoc. eapply segRLs_sideRLs_halt_concat; eassumption.
Qed.
Theorem eval_sound fuel n w : Sem n w (eval fuel n w).
Proof.
 revert n w. induction fuel as [|fuel IH]; intros n w.
 - destruct n; cbn[eval Sem Calls]; [constructor|exact I].
 - destruct n as [|p]; [cbn[eval Sem Calls]; constructor|].
   cbn[eval]. pose proof (decode_sound w) as HD.
   destruct (decode w) as [a t] eqn:ED. cbn in HD.
   eapply sem_input_eq.
   { unfold denotes. rewrite Str_app_assoc. exact HD. }
   destruct a; cbn[prefix].
   + eapply sem_segment; [apply doubleN|apply IH].
   + eapply sem_segment; [apply half0N|apply IH].
   + eapply sem_segment; [apply half1N|apply IH].
   + eapply sem_segment; [apply q0010N; lia|apply IH].
   + eapply sem_single; [lia|exact packet0|apply IH].
   + eapply sem_single; [lia|exact packet1011|apply IH].
   + eapply sem_single; [lia|exact packet1101|apply IH].
   + eapply (sem_child (Npos p) 1 [1;1;0;0;0] [1;0;0;0;0] t (eval fuel 1 t) (fun y => eval fuel (N.pred (Npos p)) ([1;0;0;0;0]++y))); [lia|exact packet11000|apply IH|]. intros y E. apply IH.
   + eapply (sem_child (Npos p) 2 [1;1;0;0;1] [1;0;0;0;0] t (eval fuel 2 t) (fun y => eval fuel (N.pred (Npos p)) ([1;0;0;0;0]++y))); [lia|exact packet11001|apply IH|]. intros y E. apply IH.
   + apply sem_early; [lia|]. cbn[Sem Calls N.to_nat]. constructor. intro l.
     unfold denotes. rewrite Str_app_assoc. apply terminal111.
Qed.

(* The blank tape reaches this boundary in four ordinary steps. *)
Definition boundary r := (A,(0inf,1,0>>r)).
Lemma boundary_entry r : boundary r -[tm]->* (0inf <*< [1]) {{{(hR,R)}}} [1;0] *> r.
Proof. unfold boundary,hR. esx. Qed.
Lemma boundary_return r : (0inf <*< [1]) {{{(hL,L)}}} r = boundary r.
Proof. reflexivity. Qed.
Lemma blank_seed : c0 -[tm]->* boundary ([1] *> 0inf).
Proof. unfold boundary. esx. Qed.
Fixpoint orbit (rounds fuel:nat) (w:list Sym) : bool :=
 match rounds with
 | O => false
 | S rounds' => match eval fuel 1%N ([1;0]++w) with
   | Unknown => false | Done u => orbit rounds' fuel u | Halt => true end
 end.
Lemma denotes_app u v : denotes (u++v) = u *> denotes v.
Proof. unfold denotes. apply Str_app_assoc. Qed.
Lemma boundary_done fuel w u : eval fuel 1%N ([1;0]++w) = Done u ->
 boundary (denotes w) -[tm]->* boundary (denotes u).
Proof.
 intro E. pose proof (eval_sound fuel 1%N ([1;0]++w)) as H.
 rewrite E in H. cbn[Sem Calls N.to_nat] in H. rewrite denotes_app in H.
 eapply evstep_trans; [apply boundary_entry|]. rewrite <- boundary_return.
 apply progress_evstep. apply sideRLs_1. exact H.
Qed.
Lemma boundary_halt fuel w : eval fuel 1%N ([1;0]++w) = Halt ->
 halts tm (boundary (denotes w)).
Proof.
 intro E. pose proof (eval_sound fuel 1%N ([1;0]++w)) as H.
 rewrite E in H. cbn[Sem Calls N.to_nat] in H. rewrite denotes_app in H.
 eapply halts_evstep; [|apply boundary_entry].
 eapply sideRLs_halt_single. exact H.
Qed.
Lemma orbit_halts rounds fuel w : orbit rounds fuel w = true ->
 halts tm (boundary (denotes w)).
Proof.
 revert w. induction rounds as [|rounds IH]; intros w H.
 - discriminate.
 - cbn[orbit] in H.
   destruct (eval fuel 1%N ([1;0]++w)) as [|u|] eqn:E.
   + discriminate.
   + eapply halts_evstep; [apply IH,H|]. eapply boundary_done; exact E.
   + apply boundary_halt with (fuel:=fuel). exact E.
Qed.
Lemma checked_orbit : orbit 3116 60000 [1] = true.
Proof. vm_compute. reflexivity. Qed.
Theorem halt : halts tm c0.
Proof.
 eapply halts_evstep; [|apply blank_seed].
 exact (orbit_halts 3116 60000 [1] checked_orbit).
Qed.
End TM1.
Print Assumptions TM1.halt.
