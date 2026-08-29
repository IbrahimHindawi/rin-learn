# 04 — Control flow

> `if`, `for`, `switch`, and enums as the thing you switch on.

## The idea

The shapes are C's, with one difference worth knowing: a `switch` over an
enum that lists cases and writes no `default` must handle every member. Leave
one out and the compiler names it.

Write `default:` and that check disappears entirely -- so a large enum costs
nothing. The rule only applies where you implied "I have covered them all" by
omitting the default.

## What the lesson shows

- `for` with an init, a condition and a step, and `continue` inside it
- an enum declared with three members and switched on
- `default:` catching the rest

## Why this is here

The exhaustiveness rule exists for one moment: the day you add a member to an
enum and something silently stops handling it. The compiler will tell you which
switches went stale.

## Before you move on

You can say when the exhaustiveness check fires and how to opt out of it.

---

*Source: [`src/lessons/04_control_flow.rin`](../../src/lessons/04_control_flow.rin). The file itself
carries "What to notice" and "Try this" sections — read the code first, then come
back here.*
