# 04 — Procs

> A piece of work with a name. You have been calling one since lesson 00.

## The idea

The declaration is the same shape as everything else in the language:

    name : proc (parameters) -> ReturnType = { body }

Read left to right: `double_it` is a proc, it takes an `i32` called `n`, it gives
back an `i32`, and here is how. Nothing about that order changes for a struct, a
variable or a type — which is the whole argument for it.

Two things matter more than the syntax.

**Parameters are copies.** A proc receives its own variable, initialised from
whatever the caller passed. Writing to it changes nothing outside. That is the
single fact the next lesson is built on: to change a caller's variable you have
to pass its *address*, because passing its value cannot possibly work.

**Order does not matter.** A proc may be called by something declared above it.
rin resolves names across the whole file, so there are no prototypes and no
header discipline — C makes you write a forward declaration for this, and rin
does not.

## What the lesson shows

- one parameter, several parameters, and a `void` return
- a parameter written to inside the proc, with the caller's variable unchanged
- `factorial` calling itself, five frames alive at once before any returns
- a proc used before it is declared, with nothing to declare in advance
- a call used as an expression, nested inside another call

## Why this is here

K&R spends a chapter on functions before it says a word about pointers, and that
order is deliberate: you cannot understand why an address is worth passing until
you have watched a copy fail to come back. Every lesson from 00 to 03 quietly
used procs; this is where they stop being scenery.

Recursion earns its place for the same reason. Watching five `n`s exist at once
is the first concrete picture of the stack, which lesson 10 will name.

## Before you move on

You can say why `spend(budget)` left `budget` at 100, and what you would have to
pass instead to change it.

---

*Source: [`src/lessons/04_procs.rin`](../../src/lessons/04_procs.rin). The file itself
carries "What to notice" and "Try this" sections — read the code first, then come
back here.*
