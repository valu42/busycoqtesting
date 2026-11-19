(* Executable single-bit DFA for the complete leftward phase. *)
From BusyCoq Require Import Individual62 Line429Engine.
From BusyCoq Require Import Line429LeftLanguage.
From Coq Require Import List Arith Lia.
Import ListNotations Bell429 LeftLanguage429.
Open Scope list_scope.
Open Scope sym_scope.

Module LeftDFA429.
Inductive node := l | j | l0 | l1 | d | e | b | z | done (o : outcome).
Definition initial m := match m with ML => l | MJ => j end.
Definition hop (a : node) (x : Sym) : node :=
  match a,x with
  | l,S0 => l0 | l,S1 => l1 | j,S0 => d | j,S1 => l
  | l0,S0 => d | l0,S1 => l | l1,S0 => j | l1,S1 => done Turn
  | d,S0 => z | d,S1 => e | z,S0 => done Turn | z,S1 => done Stop
  | e,S0 => b | e,S1 => e | b,S0 => j | b,S1 => done Turn
  | done o,_ => done o
  end.
Fixpoint feed (q : node) (w : list Sym) : node :=
  match w with [] => q | x::xs => feed (hop q x) xs end.
Fixpoint peek (n:nat) (q:node) (s:side) : node :=
  match n with O => q | S k => peek k (hop q (Streams.hd s)) (Streams.tl s) end.
Lemma peek_prefix w n q s : peek (length w+n) q (w *> s) = peek n (feed q w) s.
Proof. revert q. induction w; cbn; auto. Qed.
Lemma peek_ones n : forall k s, peek (n+k) e (copies S1 n s) = peek k e s.
Proof. induction n; cbn; auto. Qed.
Definition recognized q s o := exists n, peek n q s = done o.
Lemma pref w q s o : recognized (feed q w) s o -> recognized q (w *> s) o.
Proof. intros [k P]. exists (length w+k)%nat. now rewrite peek_prefix. Qed.
Lemma e_prefix n s o : recognized e s o -> recognized e (copies S1 n s) o.
Proof. intros [k P]. exists (n+k)%nat. now rewrite peek_ones. Qed.

Theorem sound m s o : accepts m s o -> recognized (initial m) s o.
Proof.
  induction 1; cbn [initial] in *.
  - exact (pref [0;1] l _ _ IHaccepts).
  - exact (pref [1;0] l _ _ IHaccepts).
  - apply (pref [0;0;1] l). apply e_prefix. exact (pref [0;0] e _ _ IHaccepts).
  - exact (pref [1] j _ _ IHaccepts).
  - apply (pref [0;1] j). apply e_prefix. exact (pref [0;0] e _ _ IHaccepts).
  - exists 4%nat; reflexivity.
  - exists 3%nat; reflexivity.
  - exists 2%nat; reflexivity.
  - exists 4%nat; reflexivity.
  - apply (pref [0;0;1] l), e_prefix. exists 2%nat; reflexivity.
  - exists 3%nat; reflexivity.
  - apply (pref [0;1] j), e_prefix. exists 2%nat; reflexivity.
Qed.

Lemma peek_done k o s : peek k (done o) s = done o.
Proof. revert s. induction k; cbn; auto. Qed.
Lemma extend k : forall q s o, peek k q s = done o ->
  forall n, peek (k+n) q s = done o.
Proof.
  induction k; intros q s o H n; [cbn in H; subst; apply peek_done |].
  cbn in H |- *. eauto.
Qed.
Lemma unique q s a c : recognized q s a -> recognized q s c -> a = c.
Proof.
  intros [i I] [k K]. pose proof (extend i _ _ _ I k) as H.
  rewrite Nat.add_comm, (extend k _ _ _ K i) in H. now inversion H.
Qed.

(* On implicit blanks every nonterminal reaches Turn in at most five symbols. *)
Definition decide (m : mode) (w : list Sym) :=
  match feed (initial m) w with done Stop => Stop | _ => Turn end.
Lemma finite_recognized m w : recognized (initial m) (w *> 0inf) (decide m w).
Proof.
  apply pref. exists 5%nat. unfold decide. destruct (feed (initial m) w) . all: try reflexivity. destruct o; reflexivity.
Qed.
Theorem decide_exact m w o : decide m w = o <-> accepts m (w *> 0inf) o.
Proof.
  split.
  - intros E. destruct (accepts_total w m) as [u A]. pose proof (sound _ _ _ A) as G.
    pose proof (unique _ _ _ _ (finite_recognized m w) G) as F. rewrite <-E,F. exact A.
  - intros A. eapply unique; [apply finite_recognized|apply sound,A].
Qed.
Corollary decides_first m w r o : decide m w = o <-> first o (at_left m (w *> 0inf) r).
Proof. rewrite decide_exact. apply accepts_exact. Qed.
End LeftDFA429.
Print Assumptions LeftDFA429.decides_first.
