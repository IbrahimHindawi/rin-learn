# 00 — Hello, world

> The smallest complete program, and the declaration order everything else follows.

## The idea

Every rin declaration reads the same way: a name, a colon, what it is, then
`=` and its value. `main: proc() -> i32 = { ... }` is a name called `main`,
which is a proc taking nothing and returning an `i32`, whose value is a block.

That order never changes. A variable is `count: i32 = 6`. A struct is
`Point: struct = { ... }`. A proc is the same shape with a body. C puts the type
first and wraps the name in declarator syntax that nobody reads left to right;
rin puts the name first, always, and the rest follows.

## What the lesson shows

- `main` returns `i32`, exactly like C -- 0 means success
- `printfmt` comes from `std/Print.rin`, which has to be imported
- `import` is not `#include`: it brings rin declarations in, not text

## Why this is here

You will read this shape several thousand times. Getting used to it now costs
one lesson; getting used to it later costs every lesson.

## Before you move on

You can say what each part of `main: proc() -> i32 = {}` means, out loud.

---

*Source: [`src/lessons/00_hello_world.rin`](../../src/lessons/00_hello_world.rin). The file itself
carries "What to notice" and "Try this" sections — read the code first, then come
back here.*
