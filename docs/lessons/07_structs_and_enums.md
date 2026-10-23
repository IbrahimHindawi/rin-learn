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
- `printfmt` printing an enum by its member name, `Player`, rather than `0`
- a status enum marked `enum[must_use]`, and `_ = f();` to ignore one on purpose

## Why this is here

Enum members are always written with their type in front. That is why two
different enums can never be compared by accident, and why `Stat<>.count` in
lesson 12 knows which enum you mean.

That is also why an enum works as an error code. A proc returns `LoadStatus`,
and the caller compares it against `LoadStatus.Ok`. `must_use` closes the gap C
leaves open: there, calling `load_level(2);` and ignoring the result compiles
silently. Here it is an error. When ignoring it really is what you want,
`_ = load_level(2);` says so in the code. Printing the status gives its name
(`FileMissing`), so the message stays right when you add a member.

## Before you move on

You can nest a struct in a struct and reach a leaf field. Uncomment
`load_level(2);` and read the error.

---

*Source: [`src/lessons/07_structs_and_enums.rin`](https://github.com/IbrahimHindawi/rin-learn/blob/main/src/lessons/07_structs_and_enums.rin). The file itself
carries "What to notice" and "Try this" sections — read the code first, then come
back here.*
