# 07 — Structs and enums

> Grouping values, and naming a small set of states.

## The idea

A struct is several values with one name. An enum is a name for each of a small
number of states, stored as an integer.

Both are what you would expect from C. The lesson is short on purpose -- the
interesting part is not the syntax, it is what the bytes look like, and that is
the next lesson.

## What the lesson shows

- a struct containing another struct, reached with `.`
- an enum member written `SpriteKind.Player`, always qualified
- zero-initialisation with `= {}`

## Why this is here

Enum members are always written with their type in front. That is why two
different enums can never be compared by accident, and why `Stat<>.count` in
lesson 12 knows which enum you mean.

## Before you move on

You can nest a struct in a struct and reach a leaf field.

---

*Source: [`src/lessons/07_structs_and_enums.rin`](../../src/lessons/07_structs_and_enums.rin). The file itself
carries "What to notice" and "Try this" sections — read the code first, then come
back here.*
