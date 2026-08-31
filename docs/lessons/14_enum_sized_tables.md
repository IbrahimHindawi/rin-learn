# 14 — Enum-sized tables

> An array whose length is an enum's member count, checked by the compiler.

## The idea

`Stat<>` is the enum's reflection record and `.count` is how many members it
declares. The compiler knows that number as soon as the enum is parsed, so it can
size an array with it: `[Stat<>.count]i32`.

The alternative is a hand-written `STAT_COUNT` constant sitting next to the enum,
which is correct exactly until someone adds a member and forgets. Here there is
nothing to forget, because there is nothing to keep in step.

## What the lesson shows

- `Stat<>.count` used as an array length
- indexing that array by casting the enum member
- adding a member grows the table automatically

## Why this is here

This is the first place reflection earns its keep, and it does so at compile
time with no runtime cost at all. The array is exactly as fast as one with a
literal length, because after compilation it *is* one.

## Before you move on

You can add a fourth `Stat` member and predict what changes.

---

*Source: [`src/lessons/14_enum_sized_tables.rin`](https://github.com/IbrahimHindawi/rin-learn/blob/main/src/lessons/14_enum_sized_tables.rin). The file itself
carries "What to notice" and "Try this" sections — read the code first, then come
back here.*
