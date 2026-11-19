# Engine notes — tiny-chess-01 (v3)

`main.py`: 4,070 bytes (cap 4,096): an lzma payload plus a two-line unpacker,
which the rules expressly allow (the house baseline ships the same way).
Stdlib only; fixed node budget, no clocks, no unseeded randomness: a trial
replays byte for byte (verified).

Design (v3, rewritten from v2):
- 0x88 board of small ints; precomputed knight/king target lists and slider
  rays for attack tests and move generation.
- Zobrist keys from a fixed-seed xorshift, updated incrementally in
  make/unmake; transposition table with exact/lower/upper flags and
  mate-distance adjustment, kept across moves.
- Incremental evaluation: material + six piece-square tables, maintained move
  by move (no leaf rescan); the king blends middlegame and endgame tables by
  game phase.
- PVS alpha-beta with check extensions; quiescence over captures and
  promotions, and over every evasion when in check. Ordering: TT move, then
  MVV-LVA. A repetition inside the search, or of a position from earlier in
  the game, scores 0. Legality is lazy: pseudo-legal moves are made and
  tested one at a time, so cut nodes skip most make/unmake work.
- Budget: 120,000 nodes a move (worst middlegame move ~2 s on one CPU
  against the 10 s limit); a lone legal move is played without searching.

Perft (exact): startpos d4 197,281; Kiwipete d3 97,862; ep/pin d4 43,238;
promotion d3 9,467; CPW5 d3 62,379.

Local practice (kit env + scorer, 6 games each): trial-0 Elo 1,191,
trial-1 Elo 1,279. v2 scored 876 on trial-0; head to head v3 beat v2
11.0–1.0 in 12 games.
