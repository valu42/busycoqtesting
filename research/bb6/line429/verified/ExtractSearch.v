From BusyCoq Require Import Line429Engine Line429Score.
From Coq Require Import Extraction ExtrOcamlZBigInt.
Extraction Language OCaml.
Extraction "bell429z.ml" Bell429.stepFast Bell429.initFastB Bell429.fs_mode Bell429.fs_L Bell429.fs_R
  Bell429.runs_pop Bell429.popBitRTape Score429.config_count.
