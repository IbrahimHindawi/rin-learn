# 19 — Where this leads

> Generics and reflection together: code shaped by types.

## The idea

The last lesson puts the two halves next to each other. A generic type gives you
one definition instantiated per type; reflection gives you a description of each
instantiation. Together they are enough to write code that adapts to a type it
was not written for -- a serialiser, a comparison, an editor field -- with the
adaptation resolved while compiling.

That is the whole of rin's metaprogramming. There is no macro system, no
compile-time execution, and no `comptime` block. Generics plus reflection plus
the preprocessor is the budget, deliberately.

## What the lesson shows

- a generic type with an occupancy flag, instantiated twice
- reflection over the instantiated type
- the generated C, with one concrete struct per instantiation

## Why this is here

You now have every tool the language offers. What remains is not more features
-- it is judgement about which of these to reach for, which the book chapters and
your own programs will teach better than a lesson can.

## Before you move on

You can describe what you would build with these two together.

---

*Source: [`src/lessons/19_metaprogramming_shape.rin`](../../src/lessons/19_metaprogramming_shape.rin). The file itself
carries "What to notice" and "Try this" sections — read the code first, then come
back here.*
