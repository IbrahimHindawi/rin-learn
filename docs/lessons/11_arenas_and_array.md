# 11 — Arenas and Array

> Ask once for a lot of memory, hand out pieces, throw the lot away.

## The idea

An arena holds a block of memory and a cursor. Allocating moves the cursor
forward and hands back what it passed. There is no free list, no per-allocation
header, and no way to release one piece on its own -- you release everything at
once by moving the cursor back.

That sounds like a limitation and is mostly a relief. Most memory in a real
program has the same lifetime as some phase: a frame, a level load, a parse.
When the phase ends the whole arena resets, and nothing can be leaked or freed
twice because nothing was individually owned.

`Array<T>` is the first container built on it: a pointer and a length, with its
storage pushed from an arena you hand it.

## What the lesson shows

- creating an arena and initialising it
- `Array<i32>reserve` taking the arena as its first argument
- `.data` and `.length` -- the array carries its count, unlike `[4]i32`
- nothing is freed, because the arena will be reset

## Why this is here

Every container in std takes an arena. Once you see why, the signature stops
looking like boilerplate and starts looking like the allocation decision being
made where it belongs: at the call site, by you.

## Before you move on

You can say what happens to an `Array` when its arena resets.

---

*Source: [`src/lessons/11_arenas_and_array.rin`](../../src/lessons/11_arenas_and_array.rin). The file itself
carries "What to notice" and "Try this" sections — read the code first, then come
back here.*
