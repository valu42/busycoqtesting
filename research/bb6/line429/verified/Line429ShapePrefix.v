(* Finite audit of every normalized A with nearest-left 0 and scanned 1,
   including intermediate A visits inside a rightward phase. *)
From BusyCoq Require Import Individual62 Line429Engine.
From BusyCoq Require Import Line429RightSweep Line429LeftLanguage Line429LeftDFA.
From Coq Require Import List Arith Lia.
Import Bell429 LeftLanguage429 ListNotations.
Open Scope sym_scope.

Module ShapePrefix429.
Record snapshot := mk { st : Q; west : list Sym; under : Sym; east : list Sym }.
Definition decode s := (st s ;; (west s *> 0inf) {{under s}} (east s *> 0inf)).
Definition here (w:list Sym) := match w with [] => S0 | h::_ => h end.
Definition rest (w:list Sym) := match w with [] => [] | _::t => t end.
Lemma unroll w : w *> 0inf = here w >> (rest w *> 0inf).
Proof. destruct w; [apply const_unfold|reflexivity]. Qed.

Definition advance s := match src_tm (st s, under s) with
  | Some (v,L,p) => Some (mk p (rest (west s)) (here (west s)) (v::east s))
  | Some (v,R,p) => Some (mk p (v::west s) (here (east s)) (rest (east s)))
  | None => None end.
Lemma literal s t : advance s = Some t -> decode s -[src_tm]-> decode t.
Proof.
  destruct s as [p u x v]. unfold advance; cbn [st under east west].
  destruct (src_tm (p,x)) as [[[a dir] q]|] eqn:T; [|discriminate].
  destruct dir; intros E; inversion E; subst; unfold decode; cbn [st under east west].
  - rewrite (unroll u) at 1. exact (@step_left src_tm p q x a (here u >> rest u *> 0inf) (v *> 0inf) T).
  - rewrite (unroll v) at 1. exact (@step_right src_tm p q x a (u *> 0inf) (here v >> rest v *> 0inf) T).
Qed.

(* The DFA can stop as soon as either absorbing state is known. *)
Fixpoint evaluate (w:list Sym) (q:LeftDFA429.node) : outcome :=
  match q with
  | LeftDFA429.done o => o
  | _ => match w with [] => Turn | x::xs => evaluate xs (LeftDFA429.hop q x) end
  end.
Definition ending q := match q with LeftDFA429.done Stop => Stop | _ => Turn end.
Lemma evaluate_spec w q : evaluate w q = ending (LeftDFA429.feed q w).
Proof.
  revert q. induction w as [|x w IH]; intro q.
  - destruct q; try reflexivity. destruct o; reflexivity.
  - destruct q; cbn [evaluate LeftDFA429.feed]; try apply IH.
    unfold LeftDFA429.hop. rewrite <-IH. destruct w; destruct o; reflexivity.
Qed.
Definition safe s :=
  match st s,under s,here (west s) with
  | A,S1,S0 => match evaluate (rest (west s)) LeftDFA429.j with Turn=>true|Stop=>false end
  | _,_,_=>true end.
Definition property c := forall y v, c = AR (0 >> y) (1 >> v) -> accepts MJ y Turn.
Lemma safe_spec s : safe s=true -> property (decode s).
Proof.
  destruct s as [p u x v]; cbn [safe st under west decode east].
  unfold property, decode, AR; cbn [st under west east].
  intros G y z E. change ((p,(u *> 0inf,x,v *> 0inf))=(A,(0 >> y,S1,z))) in E.
  injection E as Q L M R. subst p x.
  assert (D: here u >> (rest u *> 0inf) = 0 >> y).
  { transitivity (u *> 0inf); [symmetry; apply unroll | exact L]. }
  injection D as Z V. subst y.
  unfold safe in G; cbn [st under west] in G. rewrite Z in G.
  apply (proj1 (LeftDFA429.decide_exact _ _ _)).
  change (ending (LeftDFA429.feed LeftDFA429.j (rest u))=Turn).
  rewrite <-evaluate_spec. destruct (evaluate (rest u) LeftDFA429.j); [discriminate|reflexivity].
Qed.

Fixpoint audit (depth:nat) s :=
 match depth with
 | O => if safe s then advance s else None
 | S k => match audit k s with Some t => audit k t | None => None end
 end.

Lemma suffix c d k : c -[src_tm]->> k / d ->
  forall n h, c -[src_tm]->> (k+n) / h -> d -[src_tm]->> n / h.
Proof.
  induction 1 as [c|k c e d F _ IH]; intros n h M; [exact M|].
  inversion M; subst. match goal with K:c -[src_tm]-> ?x |- _ =>
    assert (e=x) by (eapply step_deterministic; eauto); subst x end.
  eapply IH; eauto.
Qed.
Lemma audit_sound k s t : audit k s = Some t ->
  (decode s -[src_tm]->> 2^k / decode t) /\
  forall i c, (i<2^k)%nat -> decode s -[src_tm]->> i / c -> property c.
Proof.
  revert s t. induction k as [|k IH]; intros s t E.
  - cbn [audit] in E. destruct (safe s) eqn:G; [|discriminate].
    split; [apply literal in E; eapply multistep_S; [exact E|constructor]|].
    intros i c N P. replace i with O in P by (cbn in N; lia).
    inversion P; subst. apply safe_spec,G.
  - cbn [audit] in E. destruct (audit k s) as [v|] eqn:F; [|discriminate].
    destruct (IH _ _ F) as [a A]. destruct (IH _ _ E) as [b B].
    replace (2^S k)%nat with (2^k + 2^k)%nat by (rewrite Nat.pow_succ_r'; lia).
    split; [eapply multistep_trans; eassumption|]. intros i c N P.
    destruct (Nat.lt_ge_cases i (2^k)) as [L|L]; [exact (A _ _ L P)|].
    apply (B (i-2^k)%nat c); [lia|]. apply (suffix _ _ _ a).
    replace (2^k+(i-2^k))%nat with i by lia. exact P.
Qed.
Definition blank := mk B [] S0 [].
Definition success depth := match audit depth blank with Some _=>true|None=>false end.

Lemma safe_if depth : success depth=true -> forall i y v, (i<2^depth)%nat ->
   (B;;tape0) -[src_tm]->> i / AR (0 >> y) (1 >> v) -> accepts MJ y Turn.
Proof.
  unfold success. destruct (audit depth blank) as [t|] eqn:E; [|discriminate].
  intros _ i y v N H. destruct (audit_sound _ _ _ E) as [_ P].
  exact (P _ _ N H y v eq_refl).
Qed.
Lemma verified : success 20=true.
Proof. vm_check_eq. Qed.
Theorem no_masked_stop_prefix i y v : (i<2^20)%nat ->
   (B;;tape0) -[src_tm]->> i / AR (0 >> y) (1 >> v) -> accepts MJ y Turn.
Proof. exact (safe_if 20 verified i y v). Qed.
End ShapePrefix429.
Print Assumptions ShapePrefix429.no_masked_stop_prefix.
