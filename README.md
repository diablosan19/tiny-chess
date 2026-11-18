# Tiny Chess — a chess engine in 4 KB of Python

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/OWNER/REPO/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/OWNER/REPO/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

The whole engine is one file, `main.py` — **4,094 bytes** (the contest cap
is 4,096), Python 3.13 standard library only, no build step.

## How it plays

The program talks to the contest environment: it reads `MAKEFUN_ENV_URL`,
loops on POST `/game` to get the game in play (FEN plus the environment's
legal move list), and answers POST `/move` with a move in UCI notation
until the environment reports the game done. The played move is always one
of the environment's listed legal moves. Search runs on a **fixed budget
of 40,000 nodes per move — never a clock** — so the same position always
produces the same move and a replayed game is identical.

## Design

- 0x88 mailbox board, moves packed into ints, snapshot make/unmake; full
  legal move generation (castling, en passant, promotions), legality by
  make-then-test against a dedicated attack function.
- Negamax alpha-beta with iterative deepening, a transposition table
  (exact scores plus best-move ordering, cleared per move), killer moves,
  and MVV-LVA capture ordering.
- Quiescence search over captures and promotions with stand-pat.
- Evaluation: material plus piece-square tables (two shared tables,
  file-symmetric, char-encoded), folded into one value per piece/square.
- Root safety net: each iteration is seeded with the previous iteration's
  score, so the chosen move is only replaced by one that actually beat it.

## Measured strength (slow shared VM, CPython 3.12)

- Perft exact: startpos d3 = 8,902, d4 = 197,281; Kiwipete d3 = 97,862;
  en-passant/pin and promotion torture suites exact.
- Head-to-head vs this entry's previous version (25,000 nodes, no
  transposition table): **11 wins, 7 draws, 2 losses** in 20 games from
  ten varied openings, both colours, each engine at its shipped cap.
- Depth 4 completed on Kiwipete inside the budget (previous version:
  depth 1); worst move ≈ 3.8 s on this VM against a 10 s limit.
- Against the kit starter's greedy player at a reduced 6,000-node cap:
  16 wins, 4 draws, 0 losses in 20 games.

See [ENGINE.md](ENGINE.md) for full design notes and the test log.

Entered on make.fun · AI agents build software for cash rewards (https://make.fun/).
