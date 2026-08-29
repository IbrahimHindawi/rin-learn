# 02 — Addresses

> A variable is a name for a place; a pointer holds that place's number.

## The idea

Two operators do all the work, and they are exact opposites:

    value.&     the address of value
    place[0]    the value at place

So `x.&[0]` is `x` again. A pointer is an ordinary value -- it has a size, it
can be copied, it can be stored in a struct. It just happens to mean "the thing
over there".

The lesson passes an address to a proc that then writes through it. The proc
never sees the caller's variable; it sees a number, goes to that place, and
writes. That is the entire mechanism, and every data structure later is built
from it.

## What the lesson shows

- two variables print two different addresses, close together but never equal
- nothing promises declaration order matches address order
- a proc changes its caller's variable by writing through an address
- repointing a pointer moves 8 bytes and no `i32` at all

## Why this is here

Arrays, structs, arenas and every container in std are addresses plus
arithmetic. If this lesson is fuzzy, the rest will feel like magic instead of
like counting.

## Before you move on

You can explain why `a.&[0] = 5` and `a = 5` do the same thing.

---

*Source: [`src/lessons/02_addresses.rin`](../../src/lessons/02_addresses.rin). The file itself
carries "What to notice" and "Try this" sections — read the code first, then come
back here.*
