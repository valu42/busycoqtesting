; Nonhalting certificate, BBi(9) six states and three symbols, line 80.
; Run: z3 line80.smt2
; An array indexed by mathematical integers represents the entire two-way tape.
; An undefined table entry is precisely a halt. All directions move one cell.
(set-logic ALL)
(declare-datatypes () ((Sym Zero One Two) (State A B C D E F) (Dir L R)))
(declare-datatypes () ((Instruction H (Go (write Sym) (direction Dir) (target State)))))
(define-sort Tape () (Array Int Sym))

; Machine 1RB---2LF_2LC------_---2LD---_0LE---0LD_2RE---2RA_------0RE
(define-fun action ((q State) (s Sym)) Instruction
  (match q
    ((A (match s ((Zero (Go One R B)) (One H) (Two (Go Two L F)))))
     (B (match s ((Zero (Go Two L C)) (One H) (Two H))))
     (C (match s ((Zero H) (One (Go Two L D)) (Two H))))
     (D (match s ((Zero (Go Zero L E)) (One H) (Two (Go Zero L D)))))
     (E (match s ((Zero (Go Two R E)) (One H) (Two (Go Two R A)))))
     (F (match s ((Zero H) (One H) (Two (Go Zero R E))))))))

(define-fun even ((x Int)) Bool (= (mod x 2) 0))
(define-fun digit ((s Sym)) Int (match s ((Zero 0) (One 1) (Two 2))))
(define-fun pair ((t Tape) (i Int)) Int
  (+ (* 10 (digit (select t i))) (digit (select t (+ i 1)))))

; Decimal codes have fixed width: two digits for pairs, five for windows.
; Leading zeroes are implicit. Parity refers to the leftmost cell of a pair.
(define-fun leftOK ((p Bool) (v Int)) Bool
  (ite p (or (= v 0) (= v 2) (= v 22))
         (or (= v 0) (= v 1) (= v 2) (= v 20) (= v 21) (= v 22))))
(define-fun rightOK ((p Bool) (v Int)) Bool
  (ite p (or (= v 0) (= v 22))
         (or (= v 0) (= v 2) (= v 20) (= v 22))))

; A pair wholly to one side of the head uses the pair list for that side.
(define-fun pairOK ((t Tape) (x Int) (i Int)) Bool
  (and (=> (< (+ i 1) x) (leftOK (even i) (pair t i)))
       (=> (> i x) (rightOK (even i) (pair t i)))))

; The 73 allowed combinations of state, head parity, and five-cell window.
(define-fun windowOK ((t Tape) (x Int) (q State)) Bool
  (let ((v (+ (* 10000 (digit (select t (- x 2))))
              (* 1000 (digit (select t (- x 1))))
              (* 100 (digit (select t x)))
              (* 10 (digit (select t (+ x 1))))
              (digit (select t (+ x 2))))))
    (ite (even x)
      (match q
        ((A (or (= v 0) (= v 2000) (= v 2002) (= v 2220) (= v 2222) (= v 22000) (= v 22002)))
         (B false)
         (C (or (= v 120) (= v 2120) (= v 2122) (= v 22120) (= v 22122)))
         (D (or (= v 0) (= v 2) (= v 200) (= v 202) (= v 2000) (= v 2002) (= v 2200) (= v 2202) (= v 22000) (= v 22002) (= v 22200) (= v 22202)))
         (E (or (= v 0) (= v 2) (= v 220) (= v 222) (= v 2000) (= v 2002) (= v 22000) (= v 22002) (= v 22220) (= v 22222)))
         (F (or (= v 220) (= v 222) (= v 2220) (= v 2222) (= v 22220) (= v 22222)))))
      (match q
        ((A (or (= v 2200) (= v 2222) (= v 22200) (= v 22222)))
         (B (or (= v 1000) (= v 21000) (= v 21022)))
         (C false)
         (D (or (= v 0) (= v 22) (= v 200) (= v 222) (= v 2200) (= v 2222) (= v 20000) (= v 20022) (= v 20200) (= v 20222) (= v 22200) (= v 22222)))
         (E (or (= v 0) (= v 200) (= v 222) (= v 2000) (= v 2022) (= v 2200) (= v 20000) (= v 20200) (= v 20222) (= v 22000) (= v 22022) (= v 22200)))
         (F (or (= v 222) (= v 20222))))))))

; An invariant tape satisfies windowOK and pairOK at EVERY integer i.
; Each test asks for a counterexample. Free constants are arbitrary.
(declare-const t Tape)
(declare-const x Int)
(declare-const i Int)
(declare-const q State)
(define-fun blank () Tape ((as const Tape) Zero))
(define-fun step () Instruction (action q (select t x)))
(define-fun tape1 () Tape (store t x (write step)))
(define-fun head1 () Int (ite (= (direction step) R) (+ x 1) (- x 1)))

; Base: A at position 0 on the two-way blank tape meets the whole invariant.
(push 1)
(assert (not (and (windowOK blank 0 A) (pairOK blank 0 i))))
(check-sat)
(pop 1)

; Every admitted head has a defined elementary instruction.
(assert (windowOK t x q))
(push 1)
(assert (= step H))
(check-sat)
(pop 1)

; On a right move the new window takes its new cell from the pair at x+2.
; On a left move the corresponding old pair starts at x-3.
(assert (not (= step H)))
(push 1)
(assert (= (direction step) R))
(assert (pairOK t x (+ x 2)))
(assert (not (windowOK tape1 head1 (target step))))
(check-sat)
(pop 1)
(push 1)
(assert (= (direction step) L))
(assert (pairOK t x (- x 3)))
(assert (not (windowOK tape1 head1 (target step))))
(check-sat)
(pop 1)

; For each fixed integer i, the full concrete step preserves its pair condition.
; The old pair premise holds at i because the invariant covers every integer.
(push 1)
(assert (pairOK t x i))
(assert (not (pairOK tape1 head1 i)))
(check-sat)
(pop 1)
(exit)
