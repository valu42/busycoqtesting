(** Explicit integer witness. The step checker recomputes every transition. *)
From Coq Require Import ZArith List.
From BusyCoq Require Import Line36Left.
Import ListNotations L36Left.
Module L36LeftPotential.
Local Open Scope nat_scope.
Definition r0 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-32)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-4)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r1 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-26)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-8)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r2 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r3 (h : nat) : Z := match h with
| 0 => (-20)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-4)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r4 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-56)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-4)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r5 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-50)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-50)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r6 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-50)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-4)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r7 (h : nat) : Z := match h with
| 0 => (-14)%Z | 1 => (-14)%Z | 2 => (-14)%Z | 3 => (0)%Z | 4 => (-14)%Z | 5 => (-14)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r8 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-8)%Z | 2 => (0)%Z | 3 => (-8)%Z | 4 => (0)%Z | 5 => (-8)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r9 (h : nat) : Z := match h with
| 0 => (-8)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-8)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r10 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-38)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-4)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r11 (h : nat) : Z := match h with
| 0 => (-8)%Z | 1 => (0)%Z | 2 => (-8)%Z | 3 => (0)%Z | 4 => (-8)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r12 (h : nat) : Z := match h with
| 0 => (-20)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-20)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r13 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-14)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-14)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r14 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-8)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-8)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r15 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-44)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-14)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r16 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-38)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-8)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r17 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-80)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-32)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r18 (h : nat) : Z := match h with
| 0 => (-32)%Z | 1 => (0)%Z | 2 => (-8)%Z | 3 => (0)%Z | 4 => (-8)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r19 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-44)%Z | 2 => (0)%Z | 3 => (-20)%Z | 4 => (0)%Z | 5 => (-20)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r20 (h : nat) : Z := match h with
| 0 => (-38)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-8)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r21 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-80)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-4)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r22 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-74)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-26)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r23 (h : nat) : Z := match h with
| 0 => (-14)%Z | 1 => (0)%Z | 2 => (-14)%Z | 3 => (0)%Z | 4 => (-14)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r24 (h : nat) : Z := match h with
| 0 => (-8)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-38)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r25 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-8)%Z | 2 => (0)%Z | 3 => (-14)%Z | 4 => (0)%Z | 5 => (-14)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r26 (h : nat) : Z := match h with
| 0 => (-8)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-26)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r27 (h : nat) : Z := match h with
| 0 => (-8)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-4)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r28 (h : nat) : Z := match h with
| 0 => (-20)%Z | 1 => (0)%Z | 2 => (-8)%Z | 3 => (0)%Z | 4 => (-8)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r29 (h : nat) : Z := match h with
| 0 => (-32)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-32)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r30 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-26)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-38)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r31 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-20)%Z | 2 => (0)%Z | 3 => (-20)%Z | 4 => (0)%Z | 5 => (-20)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r32 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-32)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-14)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r33 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-68)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-44)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r34 (h : nat) : Z := match h with
| 0 => (-14)%Z | 1 => (0)%Z | 2 => (-8)%Z | 3 => (0)%Z | 4 => (-8)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r35 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-92)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-4)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r36 (h : nat) : Z := match h with
| 0 => (-38)%Z | 1 => (0)%Z | 2 => (-8)%Z | 3 => (0)%Z | 4 => (-8)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r37 (h : nat) : Z := match h with
| 0 => (-26)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-74)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r38 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-26)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-44)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r39 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-68)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-4)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r40 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-8)%Z | 2 => (0)%Z | 3 => (-38)%Z | 4 => (0)%Z | 5 => (-38)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r41 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-62)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-38)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r42 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-104)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-80)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r43 (h : nat) : Z := match h with
| 0 => (-110)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-8)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r44 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-20)%Z | 2 => (0)%Z | 3 => (-8)%Z | 4 => (0)%Z | 5 => (-8)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r45 (h : nat) : Z := match h with
| 0 => (-14)%Z | 1 => (0)%Z | 2 => (-62)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (-62)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r46 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-32)%Z | 2 => (0)%Z | 3 => (-32)%Z | 4 => (0)%Z | 5 => (-32)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r47 (h : nat) : Z := match h with
| 0 => (-14)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r48 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (0)%Z | 2 => (-38)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (-38)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r49 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-26)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-4)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r50 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-20)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-20)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r51 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-44)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-4)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r52 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-44)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-68)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r53 (h : nat) : Z := match h with
| 0 => (-8)%Z | 1 => (0)%Z | 2 => (-26)%Z | 3 => (0)%Z | 4 => (-26)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r54 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-14)%Z | 2 => (0)%Z | 3 => (-8)%Z | 4 => (0)%Z | 5 => (-8)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r55 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-8)%Z | 2 => (0)%Z | 3 => (-26)%Z | 4 => (0)%Z | 5 => (-26)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r56 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-38)%Z | 2 => (0)%Z | 3 => (-8)%Z | 4 => (0)%Z | 5 => (-8)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r57 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-26)%Z | 2 => (0)%Z | 3 => (-74)%Z | 4 => (0)%Z | 5 => (-74)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r58 (h : nat) : Z := match h with
| 0 => (-20)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r59 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-14)%Z | 2 => (0)%Z | 3 => (-14)%Z | 4 => (0)%Z | 5 => (-14)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r60 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-38)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-62)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r61 (h : nat) : Z := match h with
| 0 => (-50)%Z | 1 => (0)%Z | 2 => (-74)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (-74)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r62 (h : nat) : Z := match h with
| 0 => (-4)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-4)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r63 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-14)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-4)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r64 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-38)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-38)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r65 (h : nat) : Z := match h with
| 0 => (-8)%Z | 1 => (-14)%Z | 2 => (-8)%Z | 3 => (0)%Z | 4 => (-8)%Z | 5 => (-14)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r66 (h : nat) : Z := match h with
| 0 => (-32)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-8)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r67 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-92)%Z | 2 => (0)%Z | 3 => (-44)%Z | 4 => (0)%Z | 5 => (-44)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r68 (h : nat) : Z := match h with
| 0 => (-8)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-14)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r69 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-62)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-4)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r70 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-56)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-8)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r71 (h : nat) : Z := match h with
| 0 => (-32)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-20)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r72 (h : nat) : Z := match h with
| 0 => (-44)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-26)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r73 (h : nat) : Z := match h with
| 0 => (-50)%Z | 1 => (-26)%Z | 2 => (0)%Z | 3 => (-26)%Z | 4 => (-50)%Z | 5 => (-26)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r74 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-10)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-4)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r75 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-4)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-4)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r76 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-44)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-44)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r77 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-38)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-14)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r78 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-32)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-8)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r79 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-98)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-50)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r80 (h : nat) : Z := match h with
| 0 => (-8)%Z | 1 => (0)%Z | 2 => (-8)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (-8)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r81 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-32)%Z | 2 => (0)%Z | 3 => (-8)%Z | 4 => (0)%Z | 5 => (-8)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r82 (h : nat) : Z := match h with
| 0 => (-44)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-92)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r83 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-26)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-26)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r84 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-14)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-62)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r85 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-8)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-56)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r86 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-32)%Z | 2 => (0)%Z | 3 => (-20)%Z | 4 => (0)%Z | 5 => (-20)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r87 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-50)%Z | 2 => (0)%Z | 3 => (-50)%Z | 4 => (0)%Z | 5 => (-50)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r88 (h : nat) : Z := match h with
| 0 => (-20)%Z | 1 => (0)%Z | 2 => (-20)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (-20)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r89 (h : nat) : Z := match h with
| 0 => (-14)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-8)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r90 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-38)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-26)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r91 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-14)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-38)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r92 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-8)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-32)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r93 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-50)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-98)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r94 (h : nat) : Z := match h with
| 0 => (-8)%Z | 1 => (-2)%Z | 2 => (0)%Z | 3 => (-2)%Z | 4 => (-32)%Z | 5 => (-2)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r95 (h : nat) : Z := match h with
| 0 => (-44)%Z | 1 => (0)%Z | 2 => (-20)%Z | 3 => (0)%Z | 4 => (-20)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r96 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-44)%Z | 2 => (0)%Z | 3 => (-92)%Z | 4 => (0)%Z | 5 => (-92)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r97 (h : nat) : Z := match h with
| 0 => (-38)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r98 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-50)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-26)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r99 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-62)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-14)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r100 (h : nat) : Z := match h with
| 0 => (-20)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-32)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r101 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-30)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r102 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-72)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-24)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r103 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (-6)%Z | 4 => (0)%Z | 5 => (-6)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r104 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-42)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r105 (h : nat) : Z := match h with
| 0 => (-24)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-24)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r106 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-24)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r107 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-24)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r108 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-6)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r109 (h : nat) : Z := match h with
| 0 => (-6)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r110 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-18)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r111 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-66)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r112 (h : nat) : Z := match h with
| 0 => (-12)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r113 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-48)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r114 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (-12)%Z | 4 => (0)%Z | 5 => (-12)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r115 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-42)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-18)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r116 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-36)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-12)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r117 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-78)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-54)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r118 (h : nat) : Z := match h with
| 0 => (-84)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r119 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (0)%Z | 2 => (-36)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (-36)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r120 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-6)%Z | 2 => (0)%Z | 3 => (-6)%Z | 4 => (0)%Z | 5 => (-6)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r121 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (0)%Z | 2 => (-12)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (-12)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r122 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-12)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r123 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (-48)%Z | 4 => (0)%Z | 5 => (-48)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r124 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-18)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r125 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-18)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-42)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r126 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-12)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-36)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r127 (h : nat) : Z := match h with
| 0 => (-24)%Z | 1 => (0)%Z | 2 => (-48)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (-48)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r128 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-36)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r129 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-30)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-30)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r130 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-6)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-6)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r131 (h : nat) : Z := match h with
| 0 => (-24)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r132 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-84)%Z | 2 => (0)%Z | 3 => (-36)%Z | 4 => (0)%Z | 5 => (-36)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r133 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-12)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-12)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r134 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-54)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r135 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-48)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r136 (h : nat) : Z := match h with
| 0 => (-24)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-12)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r137 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-66)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-18)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r138 (h : nat) : Z := match h with
| 0 => (-36)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-12)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r139 (h : nat) : Z := match h with
| 0 => (-42)%Z | 1 => (-18)%Z | 2 => (0)%Z | 3 => (-18)%Z | 4 => (-42)%Z | 5 => (-18)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r140 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-18)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-18)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r141 (h : nat) : Z := match h with
| 0 => (-18)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-66)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r142 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-36)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r143 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-30)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r144 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-24)%Z | 2 => (0)%Z | 3 => (-24)%Z | 4 => (0)%Z | 5 => (-24)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r145 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-12)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r146 (h : nat) : Z := match h with
| 0 => (-18)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r147 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-18)%Z | 2 => (0)%Z | 3 => (-66)%Z | 4 => (0)%Z | 5 => (-66)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r148 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-6)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r149 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-24)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-72)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r150 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-6)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r151 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-24)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-24)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r152 (h : nat) : Z := match h with
| 0 => (-12)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-12)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r153 (h : nat) : Z := match h with
| 0 => (-30)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r154 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-72)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r155 (h : nat) : Z := match h with
| 0 => (-6)%Z | 1 => (0)%Z | 2 => (-6)%Z | 3 => (0)%Z | 4 => (-6)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r156 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-30)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r157 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-58)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-34)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r158 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-100)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-76)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r159 (h : nat) : Z := match h with
| 0 => (-4)%Z | 1 => (0)%Z | 2 => (-4)%Z | 3 => (0)%Z | 4 => (-4)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r160 (h : nat) : Z := match h with
| 0 => (-88)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-4)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r161 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-4)%Z | 2 => (0)%Z | 3 => (-4)%Z | 4 => (0)%Z | 5 => (-4)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r162 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (0)%Z | 2 => (-40)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (-40)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r163 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-28)%Z | 2 => (0)%Z | 3 => (-28)%Z | 4 => (0)%Z | 5 => (-28)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r164 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (0)%Z | 2 => (-16)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (-16)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r165 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-22)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-4)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r166 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-10)%Z | 2 => (0)%Z | 3 => (-4)%Z | 4 => (0)%Z | 5 => (-4)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r167 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-4)%Z | 2 => (0)%Z | 3 => (-22)%Z | 4 => (0)%Z | 5 => (-22)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r168 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-16)%Z | 2 => (0)%Z | 3 => (-4)%Z | 4 => (0)%Z | 5 => (-4)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r169 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-4)%Z | 2 => (0)%Z | 3 => (-52)%Z | 4 => (0)%Z | 5 => (-52)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r170 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-16)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-4)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r171 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-28)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-46)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r172 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-22)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-40)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r173 (h : nat) : Z := match h with
| 0 => (-28)%Z | 1 => (0)%Z | 2 => (-52)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (-52)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r174 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-40)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-4)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r175 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-34)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-34)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r176 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-46)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-4)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r177 (h : nat) : Z := match h with
| 0 => (-4)%Z | 1 => (-10)%Z | 2 => (-4)%Z | 3 => (0)%Z | 4 => (-4)%Z | 5 => (-10)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r178 (h : nat) : Z := match h with
| 0 => (-28)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-4)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r179 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-88)%Z | 2 => (0)%Z | 3 => (-40)%Z | 4 => (0)%Z | 5 => (-40)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r180 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-16)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-16)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r181 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-58)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-4)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r182 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-52)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-4)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r183 (h : nat) : Z := match h with
| 0 => (-28)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-16)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r184 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-70)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-22)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r185 (h : nat) : Z := match h with
| 0 => (-40)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-16)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r186 (h : nat) : Z := match h with
| 0 => (-46)%Z | 1 => (-22)%Z | 2 => (0)%Z | 3 => (-22)%Z | 4 => (-46)%Z | 5 => (-22)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r187 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-40)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-40)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r188 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-34)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-10)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r189 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-28)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-4)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r190 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-94)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-46)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r191 (h : nat) : Z := match h with
| 0 => (-4)%Z | 1 => (0)%Z | 2 => (-4)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (-4)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r192 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-28)%Z | 2 => (0)%Z | 3 => (-4)%Z | 4 => (0)%Z | 5 => (-4)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r193 (h : nat) : Z := match h with
| 0 => (-40)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-88)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r194 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-22)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-22)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r195 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-10)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-58)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r196 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-4)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-52)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r197 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-28)%Z | 2 => (0)%Z | 3 => (-16)%Z | 4 => (0)%Z | 5 => (-16)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r198 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-46)%Z | 2 => (0)%Z | 3 => (-46)%Z | 4 => (0)%Z | 5 => (-46)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r199 (h : nat) : Z := match h with
| 0 => (-16)%Z | 1 => (0)%Z | 2 => (-16)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (-16)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r200 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-34)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-4)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r201 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-10)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-16)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r202 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-4)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-10)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r203 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-28)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-76)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r204 (h : nat) : Z := match h with
| 0 => (-40)%Z | 1 => (0)%Z | 2 => (-16)%Z | 3 => (0)%Z | 4 => (-16)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r205 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-22)%Z | 2 => (0)%Z | 3 => (-70)%Z | 4 => (0)%Z | 5 => (-70)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r206 (h : nat) : Z := match h with
| 0 => (-16)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r207 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-34)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-22)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r208 (h : nat) : Z := match h with
| 0 => (-4)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-10)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r209 (h : nat) : Z := match h with
| 0 => (-16)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-4)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r210 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-28)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-28)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r211 (h : nat) : Z := match h with
| 0 => (-16)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-16)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r212 (h : nat) : Z := match h with
| 0 => (-10)%Z | 1 => (0)%Z | 2 => (-4)%Z | 3 => (0)%Z | 4 => (-4)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r213 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-22)%Z | 2 => (0)%Z | 3 => (-4)%Z | 4 => (0)%Z | 5 => (-4)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r214 (h : nat) : Z := match h with
| 0 => (-34)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-4)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r215 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-76)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-4)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r216 (h : nat) : Z := match h with
| 0 => (-10)%Z | 1 => (0)%Z | 2 => (-10)%Z | 3 => (0)%Z | 4 => (-10)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r217 (h : nat) : Z := match h with
| 0 => (-4)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-34)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r218 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-76)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-28)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r219 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-4)%Z | 2 => (0)%Z | 3 => (-10)%Z | 4 => (0)%Z | 5 => (-10)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r220 (h : nat) : Z := match h with
| 0 => (-4)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-22)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r221 (h : nat) : Z := match h with
| 0 => (-16)%Z | 1 => (0)%Z | 2 => (-4)%Z | 3 => (0)%Z | 4 => (-4)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r222 (h : nat) : Z := match h with
| 0 => (-28)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-28)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r223 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-22)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-28)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r224 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-16)%Z | 2 => (0)%Z | 3 => (-16)%Z | 4 => (0)%Z | 5 => (-16)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r225 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-64)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-40)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r226 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-88)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-4)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r227 (h : nat) : Z := match h with
| 0 => (-34)%Z | 1 => (0)%Z | 2 => (-4)%Z | 3 => (0)%Z | 4 => (-4)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r228 (h : nat) : Z := match h with
| 0 => (-22)%Z | 1 => (0)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (-70)%Z | 5 => (0)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r229 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-64)%Z | 2 => (0)%Z | 3 => (0)%Z | 4 => (0)%Z | 5 => (-4)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition r230 (h : nat) : Z := match h with
| 0 => (0)%Z | 1 => (-4)%Z | 2 => (0)%Z | 3 => (-34)%Z | 4 => (0)%Z | 5 => (-34)%Z | 6 => (0)%Z | 7 => (0)%Z | _ => 0%Z end.
Definition g0 (n : nat) : nat -> Z := match n with
| 0 => r0 | 1 => r1 | 2 => r2 | 3 => r2 | 4 => r2 | 5 => r2 | 6 => r3 | 7 => r4 | 8 => r5 | 9 => r6 | 10 => r7 | 11 => r2 | 12 => r8 | 13 => r2 | 14 => r9 | 15 => r10 | 16 => r11 | 17 => r2 | 18 => r12 | 19 => r13 | 20 => r14 | 21 => r13 | 22 => r14 | 23 => r15 | 24 => r16 | 25 => r17 | 26 => r11 | _ => fun _ => 0%Z end.
Definition g1 (n : nat) : nat -> Z := match n with
| 0 => r0 | 1 => r1 | 2 => r2 | 3 => r18 | 4 => r2 | 5 => r19 | 6 => r2 | 7 => r20 | 8 => r21 | 9 => r22 | 10 => r6 | 11 => r23 | 12 => r2 | 13 => r8 | 14 => r2 | 15 => r9 | 16 => r4 | 17 => r11 | 18 => r2 | 19 => r24 | 20 => r13 | 21 => r14 | 22 => r13 | 23 => r14 | 24 => r15 | 25 => r16 | 26 => r17 | 27 => r11 | _ => fun _ => 0%Z end.
Definition g2 (n : nat) : nat -> Z := match n with
| 0 => r2 | 1 => r25 | 2 => r2 | 3 => r26 | 4 => r2 | 5 => r2 | 6 => r27 | 7 => r6 | 8 => r28 | 9 => r2 | 10 => r29 | 11 => r30 | 12 => r11 | 13 => r2 | 14 => r9 | 15 => r6 | 16 => r11 | 17 => r2 | 18 => r8 | 19 => r2 | 20 => r31 | 21 => r2 | 22 => r9 | 23 => r32 | 24 => r1 | 25 => r33 | _ => fun _ => 0%Z end.
Definition g3 (n : nat) : nat -> Z := match n with
| 0 => r2 | 1 => r25 | 2 => r2 | 3 => r26 | 4 => r2 | 5 => r34 | 6 => r2 | 7 => r26 | 8 => r35 | 9 => r36 | 10 => r2 | 11 => r37 | 12 => r38 | 13 => r23 | 14 => r2 | 15 => r9 | 16 => r39 | 17 => r11 | 18 => r2 | 19 => r8 | 20 => r2 | 21 => r40 | 22 => r2 | 23 => r9 | 24 => r32 | 25 => r1 | 26 => r33 | _ => fun _ => 0%Z end.
Definition g4 (n : nat) : nat -> Z := match n with
| 0 => r41 | 1 => r42 | 2 => r11 | 3 => r2 | 4 => r43 | 5 => r2 | 6 => r2 | 7 => r2 | 8 => r2 | 9 => r8 | 10 => r2 | 11 => r44 | 12 => r45 | 13 => r46 | 14 => r2 | 15 => r8 | 16 => r47 | 17 => r8 | 18 => r2 | 19 => r8 | 20 => r48 | 21 => r9 | 22 => r49 | 23 => r50 | 24 => r51 | 25 => r11 | 26 => r2 | 27 => r26 | 28 => r52 | _ => fun _ => 0%Z end.
Definition g5 (n : nat) : nat -> Z := match n with
| 0 => r41 | 1 => r42 | 2 => r11 | 3 => r2 | 4 => r43 | 5 => r2 | 6 => r53 | 7 => r2 | 8 => r54 | 9 => r2 | 10 => r55 | 11 => r2 | 12 => r56 | 13 => r2 | 14 => r57 | 15 => r58 | 16 => r59 | 17 => r2 | 18 => r8 | 19 => r2 | 20 => r8 | 21 => r2 | 22 => r9 | 23 => r51 | 24 => r16 | 25 => r51 | 26 => r11 | 27 => r2 | 28 => r26 | 29 => r52 | _ => fun _ => 0%Z end.
Definition g6 (n : nat) : nat -> Z := match n with
| 0 => r60 | 1 => r2 | 2 => r61 | 3 => r2 | 4 => r2 | 5 => r2 | 6 => r2 | 7 => r62 | 8 => r63 | 9 => r14 | 10 => r63 | 11 => r14 | 12 => r51 | 13 => r64 | 14 => r63 | 15 => r14 | 16 => r63 | 17 => r14 | 18 => r63 | 19 => r14 | 20 => r6 | 21 => r65 | 22 => r2 | 23 => r66 | 24 => r22 | 25 => r11 | 26 => r2 | _ => fun _ => 0%Z end.
Definition g7 (n : nat) : nat -> Z := match n with
| 0 => r60 | 1 => r2 | 2 => r11 | 3 => r2 | 4 => r67 | 5 => r2 | 6 => r8 | 7 => r2 | 8 => r68 | 9 => r0 | 10 => r1 | 11 => r49 | 12 => r50 | 13 => r69 | 14 => r70 | 15 => r63 | 16 => r14 | 17 => r63 | 18 => r14 | 19 => r63 | 20 => r14 | 21 => r6 | 22 => r11 | 23 => r2 | 24 => r71 | 25 => r22 | 26 => r11 | 27 => r2 | _ => fun _ => 0%Z end.
Definition g8 (n : nat) : nat -> Z := match n with
| 0 => r8 | 1 => r2 | 2 => r72 | 3 => r2 | 4 => r2 | 5 => r73 | 6 => r74 | 7 => r75 | 8 => r49 | 9 => r11 | 10 => r2 | 11 => r9 | 12 => r13 | 13 => r14 | 14 => r76 | 15 => r64 | 16 => r13 | 17 => r14 | 18 => r13 | 19 => r14 | 20 => r77 | 21 => r78 | 22 => r79 | 23 => r11 | 24 => r80 | 25 => r81 | _ => fun _ => 0%Z end.
Definition g9 (n : nat) : nat -> Z := match n with
| 0 => r8 | 1 => r2 | 2 => r72 | 3 => r2 | 4 => r11 | 5 => r2 | 6 => r82 | 7 => r63 | 8 => r14 | 9 => r49 | 10 => r11 | 11 => r2 | 12 => r9 | 13 => r83 | 14 => r50 | 15 => r84 | 16 => r85 | 17 => r13 | 18 => r14 | 19 => r13 | 20 => r14 | 21 => r77 | 22 => r78 | 23 => r79 | 24 => r11 | 25 => r2 | 26 => r86 | _ => fun _ => 0%Z end.
Definition g10 (n : nat) : nat -> Z := match n with
| 0 => r2 | 1 => r8 | 2 => r2 | 3 => r66 | 4 => r2 | 5 => r2 | 6 => r2 | 7 => r2 | 8 => r87 | 9 => r88 | 10 => r89 | 11 => r90 | 12 => r11 | 13 => r2 | 14 => r8 | 15 => r2 | 16 => r9 | 17 => r76 | 18 => r64 | 19 => r13 | 20 => r14 | 21 => r13 | 22 => r14 | 23 => r91 | 24 => r92 | 25 => r93 | 26 => r11 | 27 => r2 | 28 => r94 | _ => fun _ => 0%Z end.
Definition g11 (n : nat) : nat -> Z := match n with
| 0 => r2 | 1 => r8 | 2 => r2 | 3 => r66 | 4 => r2 | 5 => r95 | 6 => r2 | 7 => r8 | 8 => r2 | 9 => r96 | 10 => r97 | 11 => r9 | 12 => r98 | 13 => r11 | 14 => r2 | 15 => r8 | 16 => r2 | 17 => r12 | 18 => r99 | 19 => r70 | 20 => r13 | 21 => r14 | 22 => r13 | 23 => r14 | 24 => r91 | 25 => r92 | 26 => r93 | 27 => r11 | 28 => r2 | 29 => r100 | _ => fun _ => 0%Z end.
Definition g12 (n : nat) : nat -> Z := match n with
| 0 => r101 | 1 => r102 | 2 => r2 | 3 => r2 | 4 => r103 | 5 => r2 | 6 => r2 | 7 => r2 | 8 => r2 | 9 => r2 | 10 => r104 | 11 => r2 | 12 => r2 | 13 => r105 | 14 => r106 | 15 => r2 | 16 => r2 | 17 => r2 | 18 => r107 | 19 => r2 | 20 => r2 | 21 => r2 | 22 => r2 | 23 => r2 | 24 => r2 | 25 => r2 | 26 => r108 | _ => fun _ => 0%Z end.
Definition g13 (n : nat) : nat -> Z := match n with
| 0 => r101 | 1 => r102 | 2 => r2 | 3 => r2 | 4 => r103 | 5 => r2 | 6 => r2 | 7 => r2 | 8 => r109 | 9 => r2 | 10 => r110 | 11 => r111 | 12 => r112 | 13 => r2 | 14 => r113 | 15 => r106 | 16 => r2 | 17 => r2 | 18 => r2 | 19 => r104 | 20 => r2 | 21 => r2 | 22 => r2 | 23 => r2 | 24 => r114 | 25 => r2 | 26 => r2 | 27 => r108 | _ => fun _ => 0%Z end.
Definition g14 (n : nat) : nat -> Z := match n with
| 0 => r2 | 1 => r115 | 2 => r116 | 3 => r117 | 4 => r2 | 5 => r2 | 6 => r118 | 7 => r2 | 8 => r2 | 9 => r2 | 10 => r2 | 11 => r2 | 12 => r2 | 13 => r2 | 14 => r119 | 15 => r120 | 16 => r2 | 17 => r2 | 18 => r2 | 19 => r2 | 20 => r2 | 21 => r2 | 22 => r121 | 23 => r2 | 24 => r2 | 25 => r2 | _ => fun _ => 0%Z end.
Definition g15 (n : nat) : nat -> Z := match n with
| 0 => r2 | 1 => r115 | 2 => r116 | 3 => r117 | 4 => r2 | 5 => r2 | 6 => r118 | 7 => r2 | 8 => r2 | 9 => r2 | 10 => r2 | 11 => r2 | 12 => r2 | 13 => r2 | 14 => r122 | 15 => r2 | 16 => r123 | 17 => r2 | 18 => r2 | 19 => r2 | 20 => r2 | 21 => r2 | 22 => r2 | 23 => r2 | 24 => r2 | 25 => r124 | 26 => r122 | _ => fun _ => 0%Z end.
Definition g16 (n : nat) : nat -> Z := match n with
| 0 => r124 | 1 => r2 | 2 => r2 | 3 => r2 | 4 => r125 | 5 => r126 | 6 => r2 | 7 => r127 | 8 => r2 | 9 => r2 | 10 => r2 | 11 => r2 | 12 => r2 | 13 => r2 | 14 => r2 | 15 => r2 | 16 => r2 | 17 => r128 | 18 => r129 | 19 => r2 | 20 => r2 | 21 => r2 | 22 => r2 | 23 => r108 | 24 => r2 | 25 => r104 | 26 => r130 | 27 => r2 | 28 => r131 | _ => fun _ => 0%Z end.
Definition g17 (n : nat) : nat -> Z := match n with
| 0 => r124 | 1 => r2 | 2 => r2 | 3 => r2 | 4 => r125 | 5 => r126 | 6 => r2 | 7 => r2 | 8 => r2 | 9 => r132 | 10 => r2 | 11 => r2 | 12 => r2 | 13 => r2 | 14 => r108 | 15 => r2 | 16 => r124 | 17 => r133 | 18 => r134 | 19 => r135 | 20 => r2 | 21 => r2 | 22 => r2 | 23 => r2 | 24 => r108 | 25 => r2 | 26 => r104 | 27 => r2 | 28 => r2 | 29 => r136 | _ => fun _ => 0%Z end.
Definition g18 (n : nat) : nat -> Z := match n with
| 0 => r137 | 1 => r2 | 2 => r2 | 3 => r2 | 4 => r2 | 5 => r138 | 6 => r2 | 7 => r2 | 8 => r139 | 9 => r2 | 10 => r2 | 11 => r2 | 12 => r2 | 13 => r2 | 14 => r2 | 15 => r2 | 16 => r2 | 17 => r140 | 18 => r133 | 19 => r2 | 20 => r2 | 21 => r2 | 22 => r2 | 23 => r122 | 24 => r108 | 25 => r102 | 26 => r2 | _ => fun _ => 0%Z end.
Definition g19 (n : nat) : nat -> Z := match n with
| 0 => r137 | 1 => r2 | 2 => r2 | 3 => r2 | 4 => r2 | 5 => r138 | 6 => r2 | 7 => r2 | 8 => r2 | 9 => r141 | 10 => r2 | 11 => r2 | 12 => r124 | 13 => r2 | 14 => r2 | 15 => r2 | 16 => r2 | 17 => r2 | 18 => r142 | 19 => r143 | 20 => r2 | 21 => r2 | 22 => r2 | 23 => r2 | 24 => r122 | 25 => r108 | 26 => r102 | 27 => r2 | _ => fun _ => 0%Z end.
Definition g20 (n : nat) : nat -> Z := match n with
| 0 => r2 | 1 => r108 | 2 => r2 | 3 => r2 | 4 => r2 | 5 => r109 | 6 => r2 | 7 => r2 | 8 => r2 | 9 => r2 | 10 => r144 | 11 => r2 | 12 => r2 | 13 => r122 | 14 => r2 | 15 => r2 | 16 => r2 | 17 => r2 | 18 => r2 | 19 => r140 | 20 => r133 | 21 => r2 | 22 => r2 | 23 => r2 | 24 => r2 | 25 => r145 | _ => fun _ => 0%Z end.
Definition g21 (n : nat) : nat -> Z := match n with
| 0 => r2 | 1 => r108 | 2 => r2 | 3 => r2 | 4 => r2 | 5 => r109 | 6 => r2 | 7 => r146 | 8 => r2 | 9 => r2 | 10 => r2 | 11 => r147 | 12 => r112 | 13 => r2 | 14 => r107 | 15 => r2 | 16 => r2 | 17 => r2 | 18 => r2 | 19 => r2 | 20 => r128 | 21 => r101 | 22 => r2 | 23 => r2 | 24 => r2 | 25 => r2 | 26 => r145 | _ => fun _ => 0%Z end.
Definition g22 (n : nat) : nat -> Z := match n with
| 0 => r148 | 1 => r149 | 2 => r2 | 3 => r2 | 4 => r150 | 5 => r107 | 6 => r124 | 7 => r2 | 8 => r2 | 9 => r2 | 10 => r2 | 11 => r112 | 12 => r101 | 13 => r151 | 14 => r107 | 15 => r2 | 16 => r2 | 17 => r2 | 18 => r2 | 19 => r2 | 20 => r101 | 21 => r2 | 22 => r2 | 23 => r152 | 24 => r2 | 25 => r2 | 26 => r2 | 27 => r2 | 28 => r128 | _ => fun _ => 0%Z end.
Definition g23 (n : nat) : nat -> Z := match n with
| 0 => r148 | 1 => r149 | 2 => r2 | 3 => r2 | 4 => r150 | 5 => r107 | 6 => r124 | 7 => r2 | 8 => r109 | 9 => r2 | 10 => r124 | 11 => r2 | 12 => r153 | 13 => r154 | 14 => r137 | 15 => r128 | 16 => r155 | 17 => r2 | 18 => r2 | 19 => r2 | 20 => r2 | 21 => r135 | 22 => r2 | 23 => r2 | 24 => r156 | 25 => r2 | 26 => r2 | 27 => r2 | 28 => r2 | 29 => r128 | _ => fun _ => 0%Z end.
Definition g24 (n : nat) : nat -> Z := match n with
| 0 => r157 | 1 => r158 | 2 => r159 | 3 => r2 | 4 => r160 | 5 => r2 | 6 => r2 | 7 => r2 | 8 => r2 | 9 => r161 | 10 => r2 | 11 => r161 | 12 => r162 | 13 => r163 | 14 => r2 | 15 => r161 | 16 => r2 | 17 => r161 | 18 => r2 | 19 => r161 | 20 => r164 | 21 => r62 | 22 => r74 | 23 => r75 | 24 => r165 | 25 => r159 | 26 => r2 | _ => fun _ => 0%Z end.
Definition g25 (n : nat) : nat -> Z := match n with
| 0 => r157 | 1 => r158 | 2 => r159 | 3 => r2 | 4 => r160 | 5 => r2 | 6 => r159 | 7 => r2 | 8 => r166 | 9 => r2 | 10 => r167 | 11 => r2 | 12 => r168 | 13 => r2 | 14 => r169 | 15 => r2 | 16 => r161 | 17 => r2 | 18 => r161 | 19 => r2 | 20 => r161 | 21 => r2 | 22 => r62 | 23 => r165 | 24 => r170 | 25 => r165 | 26 => r159 | 27 => r2 | _ => fun _ => 0%Z end.
Definition g26 (n : nat) : nat -> Z := match n with
| 0 => r62 | 1 => r171 | 2 => r172 | 3 => r2 | 4 => r173 | 5 => r2 | 6 => r2 | 7 => r2 | 8 => r2 | 9 => r62 | 10 => r74 | 11 => r75 | 12 => r74 | 13 => r75 | 14 => r174 | 15 => r175 | 16 => r74 | 17 => r75 | 18 => r74 | 19 => r75 | 20 => r74 | 21 => r75 | 22 => r176 | 23 => r177 | 24 => r2 | 25 => r178 | _ => fun _ => 0%Z end.
Definition g27 (n : nat) : nat -> Z := match n with
| 0 => r62 | 1 => r171 | 2 => r172 | 3 => r2 | 4 => r159 | 5 => r2 | 6 => r179 | 7 => r2 | 8 => r161 | 9 => r2 | 10 => r62 | 11 => r74 | 12 => r75 | 13 => r165 | 14 => r180 | 15 => r181 | 16 => r182 | 17 => r74 | 18 => r75 | 19 => r74 | 20 => r75 | 21 => r74 | 22 => r75 | 23 => r176 | 24 => r159 | 25 => r2 | 26 => r183 | _ => fun _ => 0%Z end.
Definition g28 (n : nat) : nat -> Z := match n with
| 0 => r184 | 1 => r159 | 2 => r2 | 3 => r161 | 4 => r2 | 5 => r185 | 6 => r2 | 7 => r2 | 8 => r186 | 9 => r74 | 10 => r75 | 11 => r165 | 12 => r159 | 13 => r2 | 14 => r62 | 15 => r74 | 16 => r75 | 17 => r187 | 18 => r175 | 19 => r74 | 20 => r75 | 21 => r74 | 22 => r75 | 23 => r188 | 24 => r189 | 25 => r190 | 26 => r159 | 27 => r191 | 28 => r192 | _ => fun _ => 0%Z end.
Definition g29 (n : nat) : nat -> Z := match n with
| 0 => r184 | 1 => r159 | 2 => r2 | 3 => r161 | 4 => r2 | 5 => r185 | 6 => r2 | 7 => r159 | 8 => r2 | 9 => r193 | 10 => r74 | 11 => r75 | 12 => r165 | 13 => r159 | 14 => r2 | 15 => r62 | 16 => r194 | 17 => r180 | 18 => r195 | 19 => r196 | 20 => r74 | 21 => r75 | 22 => r74 | 23 => r75 | 24 => r188 | 25 => r189 | 26 => r190 | 27 => r159 | 28 => r2 | 29 => r197 | _ => fun _ => 0%Z end.
Definition g30 (n : nat) : nat -> Z := match n with
| 0 => r2 | 1 => r161 | 2 => r2 | 3 => r178 | 4 => r2 | 5 => r2 | 6 => r2 | 7 => r2 | 8 => r198 | 9 => r199 | 10 => r62 | 11 => r200 | 12 => r159 | 13 => r2 | 14 => r161 | 15 => r2 | 16 => r62 | 17 => r194 | 18 => r180 | 19 => r74 | 20 => r75 | 21 => r74 | 22 => r75 | 23 => r201 | 24 => r202 | 25 => r203 | 26 => r159 | _ => fun _ => 0%Z end.
Definition g31 (n : nat) : nat -> Z := match n with
| 0 => r2 | 1 => r161 | 2 => r2 | 3 => r178 | 4 => r2 | 5 => r204 | 6 => r2 | 7 => r161 | 8 => r2 | 9 => r205 | 10 => r206 | 11 => r62 | 12 => r207 | 13 => r159 | 14 => r2 | 15 => r161 | 16 => r2 | 17 => r62 | 18 => r174 | 19 => r200 | 20 => r74 | 21 => r75 | 22 => r74 | 23 => r75 | 24 => r201 | 25 => r202 | 26 => r203 | 27 => r159 | _ => fun _ => 0%Z end.
Definition g32 (n : nat) : nat -> Z := match n with
| 0 => r2 | 1 => r208 | 2 => r189 | 3 => r165 | 4 => r2 | 5 => r2 | 6 => r2 | 7 => r2 | 8 => r209 | 9 => r200 | 10 => r210 | 11 => r200 | 12 => r159 | 13 => r2 | 14 => r161 | 15 => r2 | 16 => r62 | 17 => r200 | 18 => r159 | 19 => r2 | 20 => r211 | 21 => r74 | 22 => r75 | 23 => r74 | 24 => r75 | 25 => r174 | _ => fun _ => 0%Z end.
Definition g33 (n : nat) : nat -> Z := match n with
| 0 => r2 | 1 => r208 | 2 => r189 | 3 => r165 | 4 => r2 | 5 => r212 | 6 => r2 | 7 => r213 | 8 => r2 | 9 => r214 | 10 => r215 | 11 => r184 | 12 => r174 | 13 => r216 | 14 => r2 | 15 => r161 | 16 => r2 | 17 => r62 | 18 => r182 | 19 => r159 | 20 => r2 | 21 => r217 | 22 => r74 | 23 => r75 | 24 => r74 | 25 => r75 | 26 => r174 | _ => fun _ => 0%Z end.
Definition g34 (n : nat) : nat -> Z := match n with
| 0 => r200 | 1 => r218 | 2 => r159 | 3 => r2 | 4 => r219 | 5 => r2 | 6 => r220 | 7 => r2 | 8 => r2 | 9 => r62 | 10 => r176 | 11 => r221 | 12 => r2 | 13 => r222 | 14 => r223 | 15 => r159 | 16 => r2 | 17 => r62 | 18 => r176 | 19 => r159 | 20 => r2 | 21 => r161 | 22 => r2 | 23 => r224 | 24 => r2 | 25 => r62 | 26 => r189 | 27 => r165 | 28 => r225 | _ => fun _ => 0%Z end.
Definition g35 (n : nat) : nat -> Z := match n with
| 0 => r200 | 1 => r218 | 2 => r159 | 3 => r2 | 4 => r219 | 5 => r2 | 6 => r220 | 7 => r2 | 8 => r212 | 9 => r2 | 10 => r220 | 11 => r226 | 12 => r227 | 13 => r2 | 14 => r228 | 15 => r172 | 16 => r216 | 17 => r2 | 18 => r62 | 19 => r229 | 20 => r159 | 21 => r2 | 22 => r161 | 23 => r2 | 24 => r230 | 25 => r2 | 26 => r62 | 27 => r189 | 28 => r165 | 29 => r225 | _ => fun _ => 0%Z end.
Definition raw (s : state) : Z := let index :=
  (((phase s*6 + kind s)*2 + (if last_choice s then 1 else 0))*2
    + (if partial_choice s then 1 else 0))%nat in
 (match index with
 | 0 => g0
 | 1 => g1
 | 2 => g0
 | 3 => g1
 | 4 => g2
 | 5 => g3
 | 6 => g2
 | 7 => g3
 | 8 => g4
 | 9 => g5
 | 10 => g4
 | 11 => g5
 | 12 => g6
 | 13 => g7
 | 14 => g6
 | 15 => g7
 | 16 => g8
 | 17 => g9
 | 18 => g8
 | 19 => g9
 | 20 => g10
 | 21 => g11
 | 22 => g10
 | 23 => g11
 | 24 => g12
 | 25 => g13
 | 26 => g12
 | 27 => g13
 | 28 => g14
 | 29 => g15
 | 30 => g14
 | 31 => g15
 | 32 => g16
 | 33 => g17
 | 34 => g16
 | 35 => g17
 | 36 => g18
 | 37 => g19
 | 38 => g18
 | 39 => g19
 | 40 => g20
 | 41 => g21
 | 42 => g20
 | 43 => g21
 | 44 => g22
 | 45 => g23
 | 46 => g22
 | 47 => g23
 | 48 => g24
 | 49 => g25
 | 50 => g24
 | 51 => g25
 | 52 => g26
 | 53 => g27
 | 54 => g26
 | 55 => g27
 | 56 => g28
 | 57 => g29
 | 58 => g28
 | 59 => g29
 | 60 => g30
 | 61 => g31
 | 62 => g30
 | 63 => g31
 | 64 => g32
 | 65 => g33
 | 66 => g32
 | 67 => g33
 | 68 => g34
 | 69 => g35
 | 70 => g34
 | 71 => g35
 | 72 => g6
 | 73 => g7
 | 74 => g6
 | 75 => g7
 | 76 => g8
 | 77 => g9
 | 78 => g8
 | 79 => g9
 | 80 => g10
 | 81 => g11
 | 82 => g10
 | 83 => g11
 | 84 => g0
 | 85 => g1
 | 86 => g0
 | 87 => g1
 | 88 => g2
 | 89 => g3
 | 90 => g2
 | 91 => g3
 | 92 => g4
 | 93 => g5
 | 94 => g4
 | 95 => g5
 | 96 => g18
 | 97 => g19
 | 98 => g18
 | 99 => g19
 | 100 => g20
 | 101 => g21
 | 102 => g20
 | 103 => g21
 | 104 => g22
 | 105 => g23
 | 106 => g22
 | 107 => g23
 | 108 => g12
 | 109 => g13
 | 110 => g12
 | 111 => g13
 | 112 => g14
 | 113 => g15
 | 114 => g14
 | 115 => g15
 | 116 => g16
 | 117 => g17
 | 118 => g16
 | 119 => g17
 | 120 => g30
 | 121 => g31
 | 122 => g30
 | 123 => g31
 | 124 => g32
 | 125 => g33
 | 126 => g32
 | 127 => g33
 | 128 => g34
 | 129 => g35
 | 130 => g34
 | 131 => g35
 | 132 => g24
 | 133 => g25
 | 134 => g24
 | 135 => g25
 | 136 => g26
 | 137 => g27
 | 138 => g26
 | 139 => g27
 | 140 => g28
 | 141 => g29
 | 142 => g28
 | 143 => g29
 | _ => fun _ _ => 0%Z end) (partial_len s) (halo s).
Definition value := clipped raw.
End L36LeftPotential.
