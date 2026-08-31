# 13 — Printing, and extending it

> `printfmt` finds a `print` overload per type, including yours.

## The idea

`print<T>` is one overload per type. std provides them for the scalars and its
own containers; you add one for your type by declaring `print: proc<YourType>`
and `printfmt` finds it exactly the way it finds the built-in ones.

No registration, no interface to implement, no runtime lookup. The overload is
selected while compiling, from the type of the argument.

## What the lesson shows

- `printfmt` with `{}` holes rather than `%d`/`%s` codes
- a user-written `print` overload for an enum
- the overload being picked automatically at the call site

## Why this is here

This is the pattern for "the language knows how to handle my type" in a
language with no methods and no interfaces. It generalises: overload per type,
resolved at compile time, extended by declaring one more.

## Before you move on

You can add a `print` overload for a struct of your own.

---

*Source: [`src/lessons/13_std_print.rin`](https://github.com/IbrahimHindawi/rin-learn/blob/main/src/lessons/13_std_print.rin). The file itself
carries "What to notice" and "Try this" sections — read the code first, then come
back here.*
