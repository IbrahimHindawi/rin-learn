# 05 — Arrays and pointers

> An array is a run of bytes, not a collection.

## The idea

There is no header, no length field, no bookkeeping. `[4]i32` is sixteen bytes
with four values laid end to end, and its size is the element size times the
count. That single fact explains why indexing is fast, why the compiler can
compute an offset at compile time, and why running off the end is dangerous
rather than impossible.

The lesson prints where each element actually sits, as a distance from the
first. The numbers come out as exact multiples of `sizeof(i32)`, because that
is all indexing is.

## What the lesson shows

- `sizeof(values)` is `sizeof(i32) * 4`, with nothing added
- each element starts exactly one element-size after the last
- an array passed as a pointer loses its length -- nothing carries it
- writing through `*i32` changes the array

## Why this is here

"The length is not part of the pointer" is the reason `slice<T>` and
`string8slice` exist in std: they are a pointer *and* a length, travelling
together. You have to feel the absence before the fix means anything.

## Before you move on

You can compute the byte offset of `values[3]` without running anything.

---

*Source: [`src/lessons/05_arrays_and_pointers.rin`](../../src/lessons/05_arrays_and_pointers.rin). The file itself
carries "What to notice" and "Try this" sections — read the code first, then come
back here.*
