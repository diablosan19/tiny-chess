# Engine notes — tiny-chess-01 (v4)

`main.py`: 3,598 bytes (cap 4,096): packed with `makefun compress` from
`v4h_src.py` (the readable source, kept beside the repo for the bundle) —
an lzma payload plus a one-line unpacker, which the rules expressly allow
(the house baseline ships the same way).
Stdlib only; fixed node budget, no clocks, no unseeded randomness: a trial
replays byte for byte (verified).

Design (v4, from v3):
- 0x88 board; precomputed knight/king targets and slider rays.
- Zobrist keys (fixed-seed PRNG), updated incrementally in make/unmake;
  transposition table (exact/lower/upper, mate-distance adjusted), kept
  across moves.
- Incremental evaluation: material + six piece-square tables (rows
  symmetric, stored half-width), maintained move by move; the king blends
  middlegame and endgame tables by game phase. Queen PST fixed for symmetry.
- PVS alpha-beta with check extensions; quiescence over captures and
  promotions, plus all evasions when in check; delta pruning in quiescence.
  Ordering: TT move, killer moves, then MVV-LVA. A repetition inside the
  search, or of an earlier game position, scores 0. Legality is lazy:
  pseudo-legal moves are made and tested one at a time.
- Budget: 120,000 nodes a move (worst middlegame move ~2 s on one CPU
  against the 10 s limit); a lone legal move is played without searching.

Perft (exact): startpos d4 197,281; Kiwipete d3 97,862; ep/pin d4 43,238;
promotion d3 9,467; CPW5 d3 62,379.

Local practice (kit env + scorer, 6 games each): trial-0 Elo 1,364,
trial-1 Elo 1,451. v3 scored 1,191 on trial-0 and 1,279 on trial-1.
