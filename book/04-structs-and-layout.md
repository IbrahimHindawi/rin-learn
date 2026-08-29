# 04 - Structs And Layout

Lessons 07 through 09.

Grouping values, where the compiler actually puts them, and what happens when a struct holds something callable.

## Lesson 07 - A struct names offsets


`src/lessons/07_structs_and_enums.rin`

A struct groups values that belong together and gives each one a name. At the
machine level, the names are the interesting part: `s.pos.x` is not a lookup,
it is a fixed offset from `s`, decided at compile time.

An enum is an integer with named values. `SpriteKind.Player` is `0`. That is
worth knowing rather than guessing, because it decides what an enum costs and
how it can be stored -- and lesson 12 turns exactly that fact into a
compile-time-sized table.

## Lesson 08 - Layout is not free


`src/lessons/08_layout_and_padding.rin`

This is the one to slow down on. Two structs, identical fields, different
declaration order:

```
Loose  is 12 bytes, aligned to 4
Tight  is 8 bytes, aligned to 4
Packed is 6 bytes, aligned to 1
the three fields themselves are 6 bytes
```

Six bytes of data. Twelve bytes of struct. Where did the other six go?

**Alignment.** Look at where `value` sits in `Loose`: offset 4, not offset 1. An
`i32` wants to begin at an address divisible by 4, because that is what the
processor is built to load in one go. `flag` took byte 0, so the compiler left
bytes 1, 2 and 3 empty to bring `value` to a multiple of 4. Those three bytes
are padding. You allocated them, you cannot use them, and you did not ask for
them.

**Order changes the answer.** `Tight` puts the 4-byte field first, so the two
1-byte fields land afterwards where they already fit. No hole in the middle. It
still pads at the end -- a struct's size must be a multiple of its own alignment
so that an *array* of them keeps every element aligned. Padding at the end is
paying for lesson 05's contiguity.

**`packed` removes it, and charges you.** `Packed` is 6 bytes with alignment 1,
which means `value` may now start at an odd address. On x86 that costs extra
work; on some architectures it is a fault. Reach for `packed` when a layout is
dictated from outside your program -- a file format, a network packet, a
hardware register -- not to save memory.

The practical rule that falls out: **declare fields largest first**. It is not
always optimal, but it is right far more often than declaration-by-topic, and it
costs nothing to do.

Then multiply. `sizeof(Loose) * 1000` against `sizeof(Tight) * 1000` is four
kilobytes of nothing, from field order alone, in an array you might really
allocate.

## What to take from these three

A compound value is a block of bytes with your names attached to offsets. The
offsets are decided at compile time, by rules about alignment you can predict.
Once you can see that, questions like "why is my struct bigger than its fields"
and "why is iterating this array so much faster than that one" stop being
mysteries and become arithmetic.

## Lesson 09 - Calls, copies, and code with addresses


`src/lessons/09_procs_and_callbacks.rin`

**A parameter is a copy.** Passing an `i32` copies four bytes onto the call. The
procedure gets its own, and writing to it changes nothing the caller can see.
That is why lesson 02 had to pass an *address* to change `a` -- copying the
address is still a copy, but both copies name the same place.

This matters more as values get bigger. Passing a 64-byte struct by value copies
64 bytes on every call. Passing `*Struct` copies 8. The language will not choose
for you.

**Code has an address too.** This lesson's real subject:

```i
Op: alias = *proc(a: i32, b: i32) -> i32;

table: [2]Op = {};
table[0] = add;
table[1] = mul;
```

`add` is a procedure, and `*proc(a: i32, b: i32) -> i32` is a pointer to one.
Your compiled procedures live in memory like everything else, at addresses, and
you can store those addresses in a variable, an array, or a struct field.

Note the `*`. There is no such thing as a variable holding a procedure *by
value* -- you cannot copy code into a local the way you copy an `i32`. You hold
its address. C has the same rule, for the same reason.

That array of two `Op`s is a dispatch table: `table[i](2, 3)` picks a procedure
by index and calls it. Every virtual method system, every plugin interface and
every callback in any language is this, with more syntax on top.

`Adder` shows the other half -- a struct with a procedure pointer field. A
struct holding data and the code that works on it is the whole of what an object
is, assembled by hand so you can see the parts.
