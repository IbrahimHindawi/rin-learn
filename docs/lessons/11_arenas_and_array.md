# 11 — Arenas and containers

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

std's containers are all built on it, and all take the arena as their first
argument:

| container | what it is |
|---|---|
| `array<T>` | a fixed length, set when it is reserved |
| `vec<T>` | grows on append, doubling its storage |
| `map<T>` | string keys to values |
| `list<T>`, `stack<T>`, `queue<T>` | linked nodes, pushed from the arena |

## What the lesson shows

- one arena feeding an `array`, a `vec` and a `map`
- `squares.data[0..squares.length]`: a container's storage as a checked slice
- `vec<f32>get` returning an `option` instead of reading past the end
- `memops_arena_clear` freeing every container at once

## Why this is here

Every container in std takes an arena. Once you see why, the signature stops
looking like boilerplate and starts looking like the allocation decision being
made where it belongs: at the call site, by you.

## Before you move on

You can say what happens to an `array`, a `vec` and a `map` when their arena is
cleared, and why none of them has a destructor.

---

*Source: [`src/lessons/11_arenas_and_array.rin`](https://github.com/IbrahimHindawi/rin-learn/blob/main/src/lessons/11_arenas_and_array.rin). The file itself
carries "What to notice" and "Try this" sections — read the code first, then come
back here.*
