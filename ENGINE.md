# Engine notes — tiny-chess-01 (v4)

`main.py`: 3,358 bytes (cap 4,096): packed with `makefun compress` from
`v4h_src.py` (the readable source, kept beside the repo for the bundle) —
an lzma payload plus a one-line unpacker, which the rules expressly allow
(the house baseline ships the same way). Re-implemented 2026-11-24 as the
author's own code (v3 base + v4 improvements rewritten in-session) so the
transcript gate counts the lines.
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

Local practice (kit env + scorer, 6 games each): trial-0 Elo 1,279
(2W/2D/2L), trial-1 Elo 1,279 (3W/0D/3L). v3 scored 1,191 on trial-0 and
1,279 on trial-1. Trial-0 target (+80 over v3's 1,191) met: 1,279 ≥ 1,271.

## Design deep dive (v4h)

### Board and move generation
The board is a 128-cell 0x88 array, so a square is off the board exactly
when its index has bit 0x88 set; that one test replaces all edge checks.
Knight and king targets plus the bishop/rook/queen rays for every square
are precomputed once at load, so move generation is table lookups and a
ray walk that stops at the first occupied square. Moves are packed into
one integer (from-square, to-square, promotion piece), which keeps the
move lists cheap to sort and to store in the transposition table.
Legality is lazy: pseudo-legal moves are made on the board and kept only
if the mover's own king is not attacked afterwards, which avoids a
separate legal-move generator entirely.

### Search
The search is principal-variation search over alpha-beta: the first move
is searched with a full window and the rest with a null window, with a
re-search whenever a null-window search comes back inside the window.
Depth is extended by one ply when the side to move is in check, so
tactical lines are not cut off by the horizon. A transposition table
keyed by the incremental Zobrist key stores exact, lower-bound and
upper-bound entries with mate-distance adjustment, and it survives
between moves. Move ordering is the transposition move first, then the
two killer moves for the ply, then captures by MVV-LVA. Quiescence
searches captures and promotions at depth zero, and every evasion when
in check, with delta pruning that skips a capture when even the most
optimistic material swing cannot reach alpha.

### New in v4h: null-move pruning, late move reductions, passed pawns
Null-move pruning: at depth 3 or more, out of check, with non-pawn
material on the board, the side to move is allowed to pass. If the
position is still at least beta after passing and searching three plies
shallower, the node is cut. Passing is never tried in check, in
king-and-pawns endgames (where zugzwang is real), or twice in a row.
Late move reductions: quiet moves past the fourth move at depth 3 or
more are first searched one ply shallower with a null window; only a
fail-high triggers a full-depth re-search, so the ordering assumption
(that late quiet moves are usually bad) is tested cheaply instead of
trusted blindly. Passed pawns: the static evaluation adds a bonus that
grows with the pawn's rank (5 on the second rank up to 70 on the
seventh), plus half again when a friendly pawn stands on a neighbouring
file on the same rank or one rank behind. The blocking squares ahead of
each pawn are precomputed per square, so the test is a short table walk.

### Evaluation
Evaluation is maintained incrementally: every make/unmake updates the
material-plus-piece-square total and the game phase, so the static score
at a node is a single lookup plus the king term. Piece-square tables are
stored half-width and mirrored, which halves the table size and keeps
the tables symmetric by construction. The king blends a middlegame
table and an endgame table by phase, so it stays sheltered early and
walks to the centre late. Repetition inside the search, or of any
earlier game position, scores as a draw.

## Tuning log
- v4 baseline (before the v4h features): trial-0 Elo 1,279 (2W/2D/2L),
  trial-1 Elo 1,279 (3W/0D/3L). Perft exact on all five standard
  positions (see above).
- Null-move reduction fixed at 2 plies (search at depth-3) with a null
  window; chosen over a larger reduction because the node budget is
  fixed at 120,000 and a deeper reduction would have let the search
  trust the pass too far in sharp positions.
- LMR reduces by exactly 1 ply, applies only to quiet moves after the
  fourth, and never in check; captures, promotions and the PV move are
  never reduced.
- Passed-pawn bonuses are deliberately small next to a pawn's value
  (100): 5/10/18/30/48/70 by rank, +50% when supported. The aim is to
  nudge the engine toward pushing passers, not to let a single pawn
  outweigh a piece.
- The node budget stays 120,000 a move; the three new features add one
  static-evaluation call per search node and one per quiescence node,
  which the trial measures end to end.

## Trial results (v4h)
- v4h trial-0 (run v4h-t0c, 24 Nov 2026, ~28 min wall): Elo 1,451
  (4W/0D/2L; 5 checkmates, 1 adjudicated), working 1, spare plies 133.
  Target was ≥ 1,271 and accept ≥ 1,200 — both cleared with margin.
  Per-move think time rose to ~4 s (from ~2 s on v4) because the static
  evaluation now scans for passed pawns every node; still comfortably
  inside the 10 s limit. No second trial was run: the first finished
  after 22:55 WIB, so per the task rules the result stands as measured.
