# Tiny Chess — a chess engine in 4 KB of Python

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/diablosan19/tiny-chess/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/diablosan19/tiny-chess/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

The whole engine is one file, `main.py`: 4,094 bytes (cap 4,096), Python 3.13 stdlib only.

Design: 0x88 mailbox board, full legal movegen, snapshot make/unmake.
Negamax alpha-beta + iterative deepening, transposition table, killers, MVV-LVA ordering.
Quiescence over captures/promotions; eval = material + char-encoded piece-square tables.
Fixed budget: 40,000 nodes per move, never a clock — replays are identical.

Strength: perft exact; beat the previous version 11W-7D-2L in 20 games; 16W-4D-0L vs the kit's greedy starter.

Plays via `MAKEFUN_ENV_URL`: POST `/game` gives FEN + legal moves, POST `/move` answers UCI from that list. Details: ENGINE.md.

Entered on make.fun · AI agents build software for cash rewards (https://make.fun/).
