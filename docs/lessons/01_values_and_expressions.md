# 01 — Values and expressions

> Arithmetic, and which conversions the compiler will do for you.

## The idea

Expressions look like C. Conversions do not. Rin converts on its own only
when nothing can go wrong: an integer to a wider one, and an integer to a
float. Anything that can lose bits, drop a fraction or change sign needs a
`cast`, written at the point it happens.

Literals have no suffixes. `2.5` becomes whatever the context wants -- an
`f32` when assigned to one, a `u8` when compared with one -- and it must fit.
Only where nothing says what a literal is does it default, to `i32` or `f64`,
and there a tick names the type: `5000000000'i64`, `0.1'f32`.

## What the lesson shows

- `u8` to `u32` to `i64` with no casts, because each step only widens
- `total / scale` dividing an `i32` by an `f32`, the int becoming a float
- `cast(wider, u8)` and `cast(ratio, i32)`: the two places a value can change
- typed literals where a call gives no context

## Why this is here

Every later lesson that computes an offset, a size or a ratio meets these
rules. The ones that remain are the conversions that are actually bugs:
wrapping, truncating, flipping sign. They are worth meeting on a short program
rather than in a renderer.

## Before you move on

You can say which of `u8 -> u16`, `i32 -> u32`, `i32 -> f32` and `f32 -> i32`
compile without a `cast`, and why.

---

*Source: [`src/lessons/01_values_and_expressions.rin`](https://github.com/IbrahimHindawi/rin-learn/blob/main/src/lessons/01_values_and_expressions.rin). The file itself
carries "What to notice" and "Try this" sections — read the code first, then come
back here.*
