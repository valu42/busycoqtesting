(* Run from verify/ with the same -Q . BusyCoq mapping as the normal build.
   Generates ignored algebraic_far.ml/.mli in the current directory. *)
From BusyCoq Require Import Individual62 ResearchAlgebraicFAR.
From Coq Require Import Extraction ExtrOCamlInt63 ExtrOCamlPArray
  ExtrOcamlNativeString ExtrOcamlNatInt.
Extract Constant PArray.array "'a" => "'a Parray.t".
Extraction NoInline PArray.array.
Extraction "algebraic_far.ml" AlgebraicFAR.decide TM_from_str flip.
