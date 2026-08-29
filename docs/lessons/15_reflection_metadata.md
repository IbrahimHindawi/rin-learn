# 15 — Reflection: the record

> `T<>` is a record the compiler emits describing the type.

## The idea

For any type, `T<>` gives a value with its name, size, alignment, kind and
member count. It is not a runtime lookup and not a hashtable -- it is a `const`
struct the compiler wrote into the output, and reading it is reading a global.

If nothing in your program mentions `T<>`, nothing is emitted. Reflection costs
what you use.

## What the lesson shows

- `.name`, `.size`, `.align`, `.count` on a struct
- the same four on an enum
- `.kind` telling the two apart
- the record being ordinary data you can pass around

## Why this is here

Everything in the next three lessons is built from this record. It is worth
seeing the plain fields before the ones that lead to arrays of other records.

## Before you move on

You can print the size of a type two ways and get the same number.

---

*Source: [`src/lessons/15_reflection_metadata.rin`](../../src/lessons/15_reflection_metadata.rin). The file itself
carries "What to notice" and "Try this" sections — read the code first, then come
back here.*
