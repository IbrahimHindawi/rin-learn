# 03 — Values and expressions

> Arithmetic, and the fact that conversions are never silent.

## The idea

Expressions look like C. What differs is that rin will not quietly convert
between types for you: mixing an `i32` and an `f32` needs a `cast`, written
out, at the point it happens.

That is more typing and it is the point. A silent conversion is a decision the
compiler made on your behalf, in a place you were not looking.

## What the lesson shows

- integer and float arithmetic side by side
- `cast(total, f32)` written explicitly before dividing by a float
- the `f` suffix on `2.5f` marks a 32-bit float literal

## Why this is here

Every later lesson that computes an offset, a size or a ratio does this. The
habit of writing the conversion where it happens is worth forming on a
four-line program rather than in a renderer.

## Before you move on

You know why `cast` is required here and what it would mean to leave it out.

---

*Source: [`src/lessons/03_values_and_expressions.rin`](../../src/lessons/03_values_and_expressions.rin). The file itself
carries "What to notice" and "Try this" sections — read the code first, then come
back here.*
