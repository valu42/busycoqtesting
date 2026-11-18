(** Overflow at a full counter on line 133, ID 35069. The shared single-level
    sweeps are from M172044 (BusyCoq PR 76). Past the last full level the
    suffix determines where the outward sweep first turns or reaches F0. *)
From Coq Require Import Lists.List PArith.
From BusyCoq Require Import Individual62 M_1RB1RD_1RC1RB_1LD0RA_1RA0LE_1LF0LC_HHH1LE.
Require Import Line133Odometer.
Import ListNotations.

(** All streams below are nearest cell first. Each list entry m denotes a
    counter with S m copies of W = 110. The first barrier bit is already
    accounted for by the leading 1 in carry_input. *)
Fixpoint full_levels (levels : list nat) (tail : side) : side :=
  match levels with
  | [] => tail
  | m :: rest => 0 >> Odo.W ^^ S m *> 1 >> full_levels rest tail
  end.

Fixpoint cleared_levels (levels : list nat) (tail : side) : side :=
  match levels with
  | [] => tail
  | m :: rest => 1 >> 1 >> Odo.W ^^ S m *> cleared_levels rest tail
  end.

Definition carry_input front levels tail :=
  0inf <{{C}} (0 >> Odo.W ^^ front *> 1 >> full_levels levels tail).
Definition carry_output front levels tail :=
  0inf <{{C}} (0 >> Odo.W ^^ S front *> cleared_levels levels tail).

(** As the outward sweep consumes levels it leaves a return path on the other
    side of the head. The innermost level is crossed last on the way back. *)
Fixpoint return_path (levels : list nat) (r : side) : side :=
  match levels with
  | [] => r
  | m :: rest => return_path rest (Odo.X ^^ m *> 1 >> 0 >> 1 >> 1 >> 0 >> r)
  end.

Definition front_path front := Odo.X ^^ front *> 1 >> 0 >> 0 >> 1 >> 0inf.

Lemma carry_outward levels tail r :
  (full_levels levels tail) {{D}}> (1 >> r) -[Odo.tm]->*
  tail {{D}}> (1 >> return_path levels r).
Proof.
  revert r. induction levels as [|m rest IH]; intro r.
  - apply evstep_refl.
  - cbn [full_levels return_path].
    eapply evstep_trans; [apply Odo.macL_tape | apply IH].
Qed.

Lemma carry_inward levels tail r :
  tail {{C}}> (return_path levels r) -[Odo.tm]->*
  (cleared_levels levels tail) {{C}}> r.
Proof.
  revert r. induction levels as [|m rest IH]; intro r.
  - apply evstep_refl.
  - cbn [cleared_levels return_path].
    eapply evstep_trans; [apply IH | apply Odo.macR_tape].
Qed.

Lemma enter_carry front levels tail :
  (0 >> Odo.W ^^ front *> 1 >> full_levels levels tail) {{A}}> 0inf -[Odo.tm]->*
  tail {{D}}> (1 >> return_path levels (front_path front)).
Proof.
  rewrite Odo.rot.
  eapply evstep_trans; [apply Odo.p_start |].
  eapply evstep_trans; [apply Odo.p_left |].
  apply carry_outward.
Qed.

Lemma finish_carry front levels tail :
  tail {{C}}> (return_path levels (front_path front)) -[Odo.tm]->*
  (0 >> Odo.W ^^ S front *> cleared_levels levels tail) {{A}}> 0inf.
Proof.
  eapply evstep_trans; [apply carry_inward |]. unfold front_path.
  eapply evstep_trans; [apply Odo.shiftC |].
  cbn [lpow]. rewrite Str_app_assoc. apply Odo.p_end.
Qed.

(** From E, exactly two words return to E while still moving outwards:
    01 through F, and 101 through C and D in the reflected table.
    The only exits are a halt on 00 and a turn on 11 or 100. *)
Inductive outward_cycle := Pair01 | Triple101.
Inductive outward_exit := Stop00 | Turn11 | Turn100.

Fixpoint cycle_word (cycles : list outward_cycle) (tail : side) : side :=
  match cycles with
  | [] => tail
  | Pair01 :: rest => 0 >> 1 >> cycle_word rest tail
  | Triple101 :: rest => 1 >> 0 >> 1 >> cycle_word rest tail
  end.

Fixpoint cycle_writes (cycles : list outward_cycle) (behind : side) : side :=
  match cycles with
  | [] => behind
  | Pair01 :: rest => cycle_writes rest (1 >> 1 >> behind)
  | Triple101 :: rest => cycle_writes rest (0 >> 1 >> 0 >> behind)
  end.

Definition exit_word e tail :=
  match e with
  | Stop00 => 0 >> 0 >> tail
  | Turn11 => 1 >> 1 >> tail
  | Turn100 => 1 >> 0 >> 0 >> tail
  end.

Definition exit_config e tail behind :=
  match e with
  | Stop00 => (0 >> tail) <{{F}} (1 >> behind)
  | Turn11 => (0 >> tail) {{A}}> (0 >> behind)
  | Turn100 => (1 >> tail) {{A}}> (1 >> 0 >> behind)
  end.

Lemma scan_cycles cycles tail behind :
  (cycle_word cycles tail) <{{E}} behind -[Odo.tm]->*
  tail <{{E}} (cycle_writes cycles behind).
Proof.
  revert behind. induction cycles as [|[] rest IH]; intro behind; cbn [cycle_word cycle_writes].
  - apply evstep_refl.
  - do 2 step. apply IH.
  - do 3 step. apply IH.
Qed.

Lemma take_exit e tail behind :
  (exit_word e tail) <{{E}} behind -[Odo.tm]->* exit_config e tail behind.
Proof. destruct e; cbn [exit_word exit_config]; es. Qed.

Lemma enter_suffix (tail behind : side) :
  tail {{D}}> (1 >> behind) -[Odo.tm]->* tail <{{E}} (0 >> behind).
Proof. step. apply evstep_refl. Qed.

(** Coming back from Turn11, B crosses the saved pairs and triples in
    reverse order. Each input 01 becomes 11 and each input 101 is restored. *)
Fixpoint restored_cycles (cycles : list outward_cycle) (tail : side) : side :=
  match cycles with
  | [] => tail
  | Pair01 :: rest => 1 >> 1 >> restored_cycles rest tail
  | Triple101 :: rest => 1 >> 0 >> 1 >> restored_cycles rest tail
  end.

Lemma rewind_cycles cycles l r :
  l {{B}}> (cycle_writes cycles r) -[Odo.tm]->*
  (restored_cycles cycles l) {{B}}> r.
Proof.
  revert l r. induction cycles as [|[] rest IH]; intros l r; cbn [cycle_writes restored_cycles].
  - apply evstep_refl.
  - eapply evstep_trans; [apply IH |]. do 2 step. apply evstep_refl.
  - eapply evstep_trans; [apply IH |]. do 3 step. apply evstep_refl.
Qed.

Lemma terminal_return cycles tail r :
  (cycle_word cycles (exit_word Turn11 tail)) {{D}}> (1 >> r) -[Odo.tm]->*
  (1 >> restored_cycles cycles (1 >> 0 >> tail)) {{C}}> r.
Proof.
  eapply evstep_trans; [apply enter_suffix |].
  eapply evstep_trans; [apply scan_cycles |].
  eapply evstep_trans; [apply take_exit |]. cbn [exit_config].
  step. eapply evstep_trans; [apply rewind_cycles |]. step. apply evstep_refl.
Qed.

Theorem line133_carry_return front levels cycles tail :
  carry_input front levels (cycle_word cycles (exit_word Turn11 tail)) -[line133]->*
  carry_output front levels (1 >> restored_cycles cycles (1 >> 0 >> tail)).
Proof.
  pose proof (evstep_trans _ _ _ _ (enter_carry front levels _)
    (evstep_trans _ _ _ _ (terminal_return cycles tail _) (finish_carry front levels _))) as path.
  destruct (with_counter path) as [n Hn].
  exact (without_counter _ _ _ _ (transfer_steps _ _ _ Hn)).
Qed.

(** Every finite word followed by blanks has an exit. The last zero or two
    may be the first blank cells beyond the written tape. *)
Lemma finite_suffix_exit : forall w : list Sym, exists cycles e tail,
  w *> 0inf = cycle_word cycles (exit_word e tail).
Proof.
  fix IH 1. intros [|[] w].
  - exists (@nil outward_cycle), Stop00, 0inf. cbn [Str_app cycle_word exit_word]. now rewrite <- !const_unfold.
  - destruct w as [|[] w].
    + exists (@nil outward_cycle), Stop00, 0inf. cbn [Str_app cycle_word exit_word]. now rewrite <- !const_unfold.
    + exists (@nil outward_cycle), Stop00, (w *> 0inf). reflexivity.
    + destruct (IH w) as [cs [e [tail H]]].
      exists (Pair01 :: cs), e, tail. cbn [Str_app cycle_word]. now rewrite H.
  - destruct w as [|[] w].
    + exists (@nil outward_cycle), Turn100, 0inf. cbn [Str_app cycle_word exit_word]. now rewrite <- !const_unfold.
    + destruct w as [|[] w].
      * exists (@nil outward_cycle), Turn100, 0inf. cbn [Str_app cycle_word exit_word]. now rewrite <- !const_unfold.
      * exists (@nil outward_cycle), Turn100, (w *> 0inf). reflexivity.
      * destruct (IH w) as [cs [e [tail H]]].
        exists (Triple101 :: cs), e, tail. cbn [Str_app cycle_word]. now rewrite H.
    + exists (@nil outward_cycle), Turn11, (w *> 0inf). reflexivity.
Qed.

Theorem line133_carry_exit front levels cycles e tail :
  carry_input front levels (cycle_word cycles (exit_word e tail)) -[line133]->*
  reflect_config (exit_config e tail
    (cycle_writes cycles (0 >> return_path levels (front_path front)))).
Proof.
  pose proof (evstep_trans _ _ _ _ (enter_carry front levels (cycle_word cycles (exit_word e tail)))
    (enter_suffix _ _)) as H.
  pose proof (evstep_trans _ _ _ _ H
    (evstep_trans _ _ _ _ (scan_cycles cycles (exit_word e tail) _) (take_exit e tail _))) as path.
  destruct (with_counter path) as [n Hn].
  exact (without_counter _ _ _ _ (transfer_steps _ _ _ Hn)).
Qed.

Corollary line133_carry_f0 front levels cycles tail :
  halts_at_trans line133 (carry_input front levels (cycle_word cycles (exit_word Stop00 tail))) (F, S0).
Proof.
  destruct (with_counter (line133_carry_exit front levels cycles Stop00 tail)) as [n Hn].
  exists n. econstructor; [exact Hn | reflexivity].
Qed.

(** The eight full separators observed just after atVisit in round 4,195,128.
    Each integer is the corresponding positive counter minus one, nearest
    first. Compare compressed integers before interpreting them as tape runs. *)
Definition marker_counts : list positive :=
  [310982904488982636595955722720554739536;
   404277775835677427574742439536721155018;
   57013532489646816709258549165435034787;
   35112623795979516469774062193602028894;
   28773967746289180904466715862585560840;
   15934098844137445157042091681768710142;
   17456079841327191459068676380209926856;
   20825734162953554078445218618036489086]%positive.

(** A later marker meets both kinds of outward cycle. *)
Definition mixed_counts : list positive :=
  [1990290588729488874214116625411550306630;
   663430196243162958071372208470516768872;
   165857549060790739517843052117629192217]%positive.

Fixpoint marker_code (counts : list positive) : list Odo.item :=
  match counts with
  | [] => []
  | p :: rest => Odo.Bit S0 :: Odo.Run Odo.W (Pos.succ p) :: Odo.Bit S1 :: marker_code rest
  end.

Definition marker_prefix front counts :=
  Odo.Bit S0 :: Odo.Run Odo.W front :: Odo.Bit S1 :: marker_code counts.

Lemma marker_code_tape counts tail : Odo.den (marker_code counts) tail =
  full_levels (List.map Pos.to_nat counts) tail.
Proof.
  induction counts as [|p rest IH]; [reflexivity |].
  cbn [marker_code List.map Odo.den full_levels]. now rewrite Pos2Nat.inj_succ, IH.
Qed.

Fixpoint return_bits cycles : list Sym :=
  match cycles with
  | [] => [1;1]
  | Pair01 :: rest => 0 :: 1 :: return_bits rest
  | Triple101 :: rest => 1 :: 0 :: 1 :: return_bits rest
  end.

Lemma return_bits_tape cycles tail : return_bits cycles *> tail = cycle_word cycles (exit_word Turn11 tail).
Proof. induction cycles as [|[] rest IH]; cbn [return_bits cycle_word Str_app]; now rewrite ?IH. Qed.

(** A terminal bit may be the first cell of a compressed run. Expose at
    most one copy at a time while checking only the finite marker word. *)
Definition read_cell xs :=
  match xs with
  | Odo.Run w n :: rest => Odo.popc (Odo.unpack w n rest)
  | _ => Odo.popc xs
  end.

Lemma read_cell_tape xs b rest : read_cell xs = Some (b, rest) ->
  Odo.den xs 0inf = b >> Odo.den rest 0inf.
Proof.
  destruct xs as [|[s|w n] xs]; cbn [read_cell]; intro H.
  - exact (Odo.popc_den _ _ _ H).
  - exact (Odo.popc_den _ _ _ H).
  - rewrite <- (Odo.den_unpack w n xs 0inf). exact (Odo.popc_den _ _ _ H).
Qed.

Fixpoint strip_bits bits xs : option (list Odo.item) :=
  match bits with
  | [] => Some xs
  | b :: bs => match read_cell xs with
               | Some (s, rest) => if Odo.sym_eqb b s then strip_bits bs rest else None
               | None => None
               end
  end.

Lemma strip_bits_tape bits xs rest : strip_bits bits xs = Some rest ->
  Odo.den xs 0inf = bits *> Odo.den rest 0inf.
Proof.
  revert xs. induction bits as [|b bs IH]; intros xs H; cbn [strip_bits] in H.
  - now inversion H.
  - destruct (read_cell xs) as [[s rest']|] eqn:E; [|discriminate].
    destruct (Odo.sym_eqb b s) eqn:Eb; [|discriminate]. apply Odo.sym_eqb_eq in Eb. subst s.
    rewrite (read_cell_tape _ _ _ E), (IH _ H). reflexivity.
Qed.

Definition marker_seen front counts cycles c :=
  match c with
  | Odo.MC true [] back A =>
      let data := Odo.canonL back in
      let prefix := marker_prefix front counts in
      if Odo.items_eqb (firstn (length prefix) data) prefix
      then strip_bits (return_bits cycles) (skipn (length prefix) data) else None
  | _ => None
  end.

Definition marker_input front counts cycles tail :=
  carry_input (Pos.to_nat front) (List.map Pos.to_nat counts) (cycle_word cycles (exit_word Turn11 tail)).
Definition marker_output front counts cycles tail :=
  carry_output (Pos.to_nat front) (List.map Pos.to_nat counts) (1 >> restored_cycles cycles (1 >> 0 >> tail)).

Lemma marker_seen_spec front counts cycles c rest : marker_seen front counts cycles c = Some rest ->
  reflect_config (Odo.semc c) = marker_input front counts cycles (Odo.den rest 0inf).
Proof.
  destruct c as [[] [|x f] back []]; cbn [marker_seen]; intro H; try discriminate.
  set (prefix := marker_prefix front counts) in *.
  destruct (Odo.items_eqb _ prefix) eqn:E; [|discriminate]. apply Odo.items_eqb_eq in E.
  pose proof (firstn_skipn (length prefix) (Odo.canonL back)) as Es. rewrite E in Es.
  set (remaining := skipn (length prefix) (Odo.canonL back)) in *.
  change (0inf <{{C}} (Odo.den back 0inf) = marker_input front counts cycles (Odo.den rest 0inf)).
  rewrite <- (Odo.den_canonL back 0inf), <- Es, Odo.den_app.
  unfold prefix, marker_prefix. cbn [Odo.den].
  rewrite marker_code_tape, (strip_bits_tape _ _ _ H), return_bits_tape. reflexivity.
Qed.

Definition next_marker front counts cycles r :=
  match r with
  | Odo.RNext c => match marker_seen front counts cycles (Odo.atVisit c) with
                   | Some _ => true | None => false end
  | Odo.RHalt => false
  end.

Definition reachable_return front counts cycles := exists tail,
  c0 -[line133]->* marker_input front counts cycles tail /\
  marker_input front counts cycles tail -[line133]->* marker_output front counts cycles tail.

Lemma blank_return_from_observation rounds front counts cycles :
  next_marker front counts cycles (Odo.run rounds seed) = true -> reachable_return front counts cycles.
Proof.
  intro Hseen. pose proof (Odo.run_sound rounds seed) as Hrun.
  destruct (Odo.run rounds seed) as [|c]; [discriminate |]. cbn [next_marker] in Hseen.
  destruct (marker_seen front counts cycles (Odo.atVisit c)) as [rest|] eqn:E; [|discriminate].
  exists (Odo.den rest 0inf). split.
  - rewrite <- (marker_seen_spec _ _ _ _ _ E).
    destruct (with_counter (evstep_trans _ _ _ _ Hrun (Odo.atVisit_sound c))) as [n Hn].
    exact (without_counter _ _ _ _ (transfer_steps _ _ _ Hn)).
  - apply line133_carry_return.
Qed.

Theorem line133_blank_marker_return : reachable_return 28 marker_counts [Pair01].
Proof. apply (blank_return_from_observation 4195128%positive). vm_cast_no_check (eq_refl true). Qed.

Theorem line133_blank_mixed_return : reachable_return 412 mixed_counts [Pair01; Triple101; Triple101].
Proof. apply (blank_return_from_observation 4311329%positive). vm_cast_no_check (eq_refl true). Qed.

Print Assumptions line133_carry_return.
Print Assumptions finite_suffix_exit.
Print Assumptions line133_carry_exit.
Print Assumptions line133_carry_f0.
Print Assumptions line133_blank_marker_return.
Print Assumptions line133_blank_mixed_return.
