# 01 — Sizes

> Every value occupies a fixed number of bytes, and you choose how many.

## The idea

In a language with one `int`, the size is chosen for you and you stop thinking
about it. Here the size is written into the name. `i32` is a 32-bit signed
integer: 4 bytes, on every machine, for ever. `u8` is one unsigned byte. There
is nothing to look up and nothing that changes when you move platform -- which
C's `int` does not promise.

This is the first low-level decision there is, and rin makes you make it every
time you declare something.

## What the lesson shows

- `sizeof` on every scalar type, printed so you can read the numbers
- all pointers are the same size, because they all hold the same kind of thing
- `usize` is big enough to count any object, and matches the pointer size
- 200 stored in an `i8` reads back as -56, with no warning from anyone

## Why this is here

That last point is the language's bargain stated early: the machine does
exactly what you asked. The protection is not a check at runtime, it is that
you wrote `i8` deliberately. Everything later in this series assumes you accept
that trade.

## Before you move on

You can predict `sizeof` for any scalar without running the program.

---

*Source: [`src/lessons/01_sizes.rin`](../../src/lessons/01_sizes.rin). The file itself
carries "What to notice" and "Try this" sections — read the code first, then come
back here.*
