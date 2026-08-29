# 15 — The C boundary

> `cinclude` sends a header to C; `external` declares a name to rin.

## The idea

These are two separate things and confusing them is the most common early
mistake.

`cinclude "stdio.h"` arranges for that header to reach the C compiler. It brings
**no name into rin**. That is why `printf` still has to be declared with
`proc[external]` even though `<stdio.h>` is right there.

`external` means "C already owns this definition". rin type-checks your calls
against the declaration you wrote and emits nothing for it -- no prototype, no
body. If your declaration disagrees with the real header, that is your bug to
find, and the C compiler will usually find it.

## What the lesson shows

- `cinclude` and `proc[external]` used together, and why both are needed
- `#define` passing straight through to the C preprocessor
- a varargs C function declared with `...`
- `*const char` as the C string type

## Why this is here

Every real rin program has a boundary like this -- njinn calls D3D11, cgltf and
miniaudio through exactly these declarations. The discipline of writing them out
is what lets the compiler check the calls at all.

## Before you move on

You can declare and call a C function that is not in this lesson.

---

*Source: [`src/lessons/15_c_surface.rin`](../../src/lessons/15_c_surface.rin). The file itself
carries "What to notice" and "Try this" sections — read the code first, then come
back here.*
