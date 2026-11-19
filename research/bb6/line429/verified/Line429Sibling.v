(** Two exact stopping tests on one total five-state machine. *)
From BusyCoq Require Import Individual62.
From Coq Require Import String.
Open Scope sym_scope.

Module Sibling429.
Definition machine429 : TM := Eval compute in (TM_from_str "1RB0LC_1RC1RA_1RD0RF_0LE---_1LA1LE_0RA0RF").
Definition machine279 : TM := Eval compute in (TM_from_str "1RB0LC_1RC1RA_1LD0RE_1LA1LD_0RA1RF_0LC---").
Inductive core_state := ca | cb | cc | go_left | go_right.
Definition configuration := (core_state*tape)%type.
Definition start : configuration := (ca,tape0).
Definition state429 q := match q with ca=>A | cb=>B | cc=>C | go_left=>E | go_right=>F end.
Definition state279 q := match q with ca=>A | cb=>B | cc=>C | go_left=>D | go_right=>E end.
Definition embed (f:core_state->Q) (x:configuration) := (f (fst x), snd x).
Definition instruction (q:core_state) (b:Sym) : Sym*dir*core_state :=
  match q,b with
  | ca,0 => (1,R,cb) | ca,1 => (0,L,cc)
  | cb,0 => (1,R,cc) | cb,1 => (1,R,ca)
  | cc,0 => (1,L,go_left) | cc,1 => (0,R,go_right)
  | go_left,0 => (1,L,ca) | go_left,1 => (1,L,go_left)
  | go_right,0 => (0,R,ca) | go_right,1 => (0,R,go_right)
  end.
Definition next (x:configuration) : configuration :=
  let '(q,(l,b,r)) := x in let '(w,d,q') := instruction q b in
  (q', match d with L => move_left (l,w,r) | R => move_right (l,w,r) end).
Definition guard429 (x:configuration) := match x with
  | (cc,(_,S0,r)) => match Streams.hd r with S1=>true | S0=>false end | _=>false end.
Definition guard279 (x:configuration) := match x with
  | (go_right,(_,S1,r)) => match Streams.hd r with S1=>true | S0=>false end | _=>false end.
Definition watched (g:configuration->bool) x := if g x then None else Some (next x).
Fixpoint orbit (n:nat) (x:configuration) := match n with O=>x | S k=>orbit k (next x) end.
Definition reaches g x := exists n, g (orbit n x) = true.

Lemma watched_iff g x : iter_halts (watched g) x <-> reaches g x.
Proof.
  split.
  - induction 1 as [x H|x y H _ [n Hn]]; unfold watched in H; destruct (g x) eqn:G; try discriminate.
    + exists O; exact G.
    + inversion H; subst. exists (S n); exact Hn.
  - intros [n H]. revert x H. induction n as [|n IH]; intros x H.
    + constructor. unfold watched. cbn [orbit] in H. now rewrite H.
    + destruct (g x) eqn:G.
      * constructor. unfold watched. now rewrite G.
      * eapply iter_halts_S; [unfold watched; now rewrite G|]. apply IH; exact H.
Qed.

Ltac literal_move := first [eapply step_left; reflexivity | eapply step_right; reflexivity].
Ltac verify_case := first [solve [eapply progress_intro; [literal_move|apply evstep_refl]] |
  solve [eapply progress_step; [literal_move|]; eapply progress_intro; [literal_move|]; eapply evstep_step; [literal_move|apply evstep_refl]] |
  solve [eapply halts_step; [|literal_move]; apply halted_halts; reflexivity]].
Lemma sim429 x : match watched guard429 x with
  | Some y => embed state429 x -[machine429]->+ embed state429 y
  | None => halts machine429 (embed state429 x) end.
Proof. destruct x as [q [[l b] [v r]]]. destruct q,b,v; cbn; verify_case. Qed.
Lemma sim279 x : match watched guard279 x with
  | Some y => embed state279 x -[machine279]->+ embed state279 y
  | None => halts machine279 (embed state279 x) end.
Proof. destruct x as [q [[l b] [v r]]]. destruct q,b,v; cbn; verify_case. Qed.

Lemma guard_decision tm f g (H:forall x, match watched g x with
  | Some y => embed f x -[tm]->+ embed f y | None => halts tm (embed f x) end) x :
  halts tm (embed f x) <-> reaches g x.
Proof.
  rewrite <- watched_iff. eapply (halts_iff tm configuration x (watched g) (embed f) (fun _ => True)).
  - intros y _. specialize (H y). destruct (watched g y); auto.
  - exact I.
Qed.
Theorem blank429 : halts machine429 c0 <-> reaches guard429 start.
Proof. apply (guard_decision machine429 state429 guard429 sim429 start). Qed.
Theorem blank279 : halts machine279 c0 <-> reaches guard279 start.
Proof. apply (guard_decision machine279 state279 guard279 sim279 start). Qed.

(** A finite prefix of the total orbit can be followed in 429 unless it has already halted. *)
Lemma follow_or_halt n x : halts machine429 (embed state429 x) \/
  embed state429 x -[machine429]->* embed state429 (orbit n x).
Proof.
  revert x. induction n as [|n IH]; intros x; [right; constructor|].
  pose proof (sim429 x) as H. unfold watched in H; destruct (guard429 x); [now left|].
  destruct (IH (next x)) as [stop|follow].
  - left. eapply halts_evstep; [exact stop|]. now apply progress_evstep.
  - right. eapply evstep_trans; [now apply (progress_evstep _ _ _ H)|exact follow].
Qed.
Theorem sibling_milestone : halts machine279 c0 ->
  halts machine429 c0 \/ exists x, guard279 x = true /\ c0 -[machine429]->* embed state429 x.
Proof.
  intro H; apply blank279 in H; destruct H as [n H]. destruct (follow_or_halt n start) as [stop|follow].
  - now left.
  - right; exists (orbit n start); split; assumption.
Qed.
End Sibling429.
Print Assumptions Sibling429.sibling_milestone.
