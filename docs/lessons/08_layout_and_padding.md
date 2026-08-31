# 08 — Layout and padding

> Two structs with the same three fields, different sizes.

## The idea

A struct is a block of bytes with your fields at fixed offsets inside it. The
compiler places them under rules you can predict: each field starts at an offset
divisible by its own alignment, and the struct is padded at the end so an array
of it stays aligned.

Reorder the declarations and the size changes. That is not a quirk -- it follows
from the placement rule, and once you know the rule you can do it deliberately.

## What the lesson shows

- `Loose` and `Tight` hold the same values and are different sizes
- `offsetof` printed for each field, showing the gaps
- the padding at the end, and why an array of the struct needs it

## Why this is here

This is where the series stops being about syntax. Everything from here --
arenas, reflection, the C boundary -- assumes you can look at a struct and see
bytes rather than a bag of names.

## Before you move on

You can reorder a struct to shrink it, and say by how much before compiling.

---

*Source: [`src/lessons/08_layout_and_padding.rin`](https://github.com/IbrahimHindawi/rin-learn/blob/main/src/lessons/08_layout_and_padding.rin). The file itself
carries "What to notice" and "Try this" sections — read the code first, then come
back here.*
