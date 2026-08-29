# 10 — Storage and lifetime

> Where a value lives decides how long it lasts. There are three answers.

## The idea

**Static**: one copy, created before `main` runs, alive until the program exits.
`static` on it means "not visible outside this file", exactly as in C.

**Local**: created when the block is entered, gone when it exits. Fast, and the
default for a reason.

**Dynamic**: memory you asked for explicitly, alive until you say otherwise.

You choose one every time you declare something, usually without noticing. This
lesson is about telling them apart by looking at the declaration.

## What the lesson shows

- a static counter that survives across calls
- a local that does not, and is fresh each time
- the file-scope/global distinction that `static` controls
- returning the address of a local, and why that is the classic mistake

## Why this is here

The next lesson replaces "dynamic" with an arena, which is rin's actual answer.
You need the three-way distinction first, because an arena is a way of managing
the third one, not a fourth thing.

## Before you move on

For any declaration you can say which of the three it is and why.

---

*Source: [`src/lessons/10_storage_and_lifetime.rin`](../../src/lessons/10_storage_and_lifetime.rin). The file itself
carries "What to notice" and "Try this" sections — read the code first, then come
back here.*
