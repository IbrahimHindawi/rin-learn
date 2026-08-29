# 12 — Generics

> One definition, many types, resolved at compile time.

## The idea

`Box: struct<T>` is a template with a hole in it. `Box<i32>` fills the hole and
the compiler emits a real struct holding an `i32`. `Box<f32>` emits a different
one. Neither costs anything at runtime -- there is no boxing, no vtable and no
type tag, because the decision was made while compiling.

The naming is worth noting: a proc belonging to a generic type is written
`Box<T>make`, with the type parameter attached to the type, not the proc. That
is why it reads as "Box's make" rather than a free function that happens to
mention Box.

## What the lesson shows

- a generic struct with one type parameter
- `Box<T>make` and `Box<T>unwrap`, both generic procs
- instantiating at two different types in the same program
- the generated C has one concrete struct per instantiation

## Why this is here

`Array<T>`, `Vec<T>`, `Option<T>`, `Map<K,V>` and `slice<T>` are all this. So is
every container you will write. And because rin has no methods, generics plus
proc pointers are the whole of its abstraction budget.

## Before you move on

You can write a generic type with two parameters and instantiate it.

---

*Source: [`src/lessons/12_generics_box.rin`](../../src/lessons/12_generics_box.rin). The file itself
carries "What to notice" and "Try this" sections — read the code first, then come
back here.*
