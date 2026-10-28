# 06 — Arrays, slices and pointers

> An array is a run of bytes, not a collection. A slice is that run plus its length.

## The idea

There is no header, no length field, no bookkeeping. `[4]i32` is sixteen bytes
with four values laid end to end, and its size is the element size times the
count. That one fact explains why indexing is fast and why the compiler can
compute an offset at compile time.

Rin gives that memory four shapes, all read with `x[i]` and addressed with
`x[i]&`:

| type | what it is | indexing |
|---|---|---|
| `[N]T` | N elements, stored inline | checked against N |
| `[]T` | a pointer and a length | checked against the length |
| `*T` | the address of exactly one `T` | `p*` reads it; `[0]` also works |
| `^T` | a raw address, C's pointer | unchecked |

The slice is the useful one. `sum(xs: []const i32)` takes a whole array, part
of one, or memory from anywhere else, and never needs a second "how many"
argument. An array converts to a slice with the length taken from its type,
and `values[1..3]` is a sub-slice: the same memory with a new start and
length, no copy.

## What the lesson shows

- `sizeof(values)` is `sizeof(i32) * 4`, with nothing added
- each element starts exactly one element-size after the last
- `values[0]&` is a `*i32`, and writing through it changes the array
- an array passes to a `[]const i32` parameter as is
- `values[1..3]` has two elements, and writing to it writes the array
- a raw `^i32` becomes a checked slice once you name its length: `raw[0..4]`

## Why this is here

Every "pointer plus count" API in C is a slice waiting to happen, and every
buffer overrun is that count going wrong. A constant index out of range does
not compile. A variable index into an array or a slice is checked in debug
builds, and the check compiles away in release. Only `^T` is unchecked,
because only there is the length unknown.

## Before you move on

You can compute the byte offset of `values[3]` without running anything, and
say which of the four types a C function's `int *` should become.

---

*Source: [`src/lessons/06_arrays_and_pointers.rin`](https://github.com/IbrahimHindawi/rin-learn/blob/main/src/lessons/06_arrays_and_pointers.rin). The file itself
carries "What to notice" and "Try this" sections — read the code first, then come
back here.*
