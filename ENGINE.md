# Engine notes — tiny-chess-01 (v4h)

## Design deep dive (v4h)

### Board and move generation
The board is a 128-cell 0x88 array, so a square is off the board exactly
when its index has bit 0x88 set; that one test replaces all edge checks.
Knight and king targets plus the bishop/rook/queen rays for every square
are precomputed once at load, so move generation is table lookups and a
ray walk that stops at the first occupied square. Moves are packed into

### Search
The search is principal-variation search over alpha-beta: the first move
is searched with a full window and the rest with a null window, with a
re-search whenever a null-window search comes back inside the window.
Depth is extended by one ply when the side to move is in check, so
tactical lines are not cut off by the horizon. A transposition table
keyed by the incremental Zobrist key stores exact, lower-bound and
upper-bound entries with mate-distance adjustment, and it survives

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


## Trial results (v4h)
- v4h trial-0 (run v4h-t0c, 24 Nov 2026, ~28 min wall): Elo 1,451
  (4W/0D/2L; 5 checkmates, 1 adjudicated), working 1, spare plies 133.
  Target was ≥ 1,271 and accept ≥ 1,200 — both cleared with margin.
  Per-move think time rose to ~4 s (from ~2 s on v4) because the static
  evaluation now scans for passed pawns every node; still comfortably
  inside the 10 s limit. No second trial was run: the first finished
  after 22:55 WIB, so per the task rules the result stands as measured.
