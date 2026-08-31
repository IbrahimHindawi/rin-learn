# 09 — Procs and callbacks

> A proc has an address too, so it can be stored and passed.

## The idea

`Op: alias = *proc(a: i32, b: i32) -> i32` names a type: pointer to a proc
taking two `i32`s and returning one. A struct can hold one. A variable can hold
one. Calling through it looks like calling anything else.

This is how you get behaviour that varies at runtime without any of the
machinery a language with methods would need. rin has no methods and never
will; a proc pointer in a struct is the whole answer.

## What the lesson shows

- an alias naming a proc-pointer type
- a struct with a callable field
- swapping which proc a struct calls, at runtime

## Why this is here

Every callback, every dispatch table, every "do this later" in a real rin
program is this. It is also why `alias` exists -- writing the pointer type out
at each use would be unreadable.

## Before you move on

You can add a third operation and swap it in without touching the struct.

---

*Source: [`src/lessons/09_procs_and_callbacks.rin`](https://github.com/IbrahimHindawi/rin-learn/blob/main/src/lessons/09_procs_and_callbacks.rin). The file itself
carries "What to notice" and "Try this" sections — read the code first, then come
back here.*
