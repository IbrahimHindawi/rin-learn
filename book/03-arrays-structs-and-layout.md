# 03 - Arrays, Structs, And Layout

Lessons 05 through 07.

Lesson 02 established that a variable is a place. These three lessons are about
what happens when you put more than one thing in a place.

## Lesson 05 - An array is a run of bytes

`src/lessons/05_arrays_and_pointers.i`

The output that matters:

```
the array is 16 bytes, an element is 4
  values[0] at +0
  values[1] at +4
  values[2] at +8
  values[3] at +12
```

Nothing sits between the elements. No length field, no header, no bookkeeping.
`[4]i32` is sixteen bytes and that is all it is.

Which turns indexing into arithmetic:

    address of element i  =  base + i * sizeof(element)

The compiler can do the multiplication only because the element size is in the
type. That is the same fact from lesson 01 doing real work: `i32` is 4 bytes, so
element 3 is at +12, and the compiler knows it without asking anything at
runtime.

Two consequences follow, and they are the same consequence.

**Walking an array is the fastest thing a processor does.** The next element is
adjacent, so it is already in cache by the time you ask for it. This is why
array-of-struct versus struct-of-array is a real performance question and not a
style preference.

**`values[7]` is not an error.** It computes `base + 28` and reads whatever is
there. Often it appears to work, which is precisely what makes it dangerous --
you get a plausible number and no indication that it came from somewhere else.
The count is in the type, so the compiler *could* reject a constant index out of
range. It does not. `sizeof(values)` being 16 rather than 8 is worth pausing on
too: the array is the bytes, not a pointer to them.

## Lesson 06 - A struct names offsets

`src/lessons/06_structs_and_enums.i`

A struct groups values that belong together and gives each one a name. At the
machine level, the names are the interesting part: `s.pos.x` is not a lookup,
it is a fixed offset from `s`, decided at compile time.

An enum is an integer with named values. `SpriteKind.Player` is `0`. That is
worth knowing rather than guessing, because it decides what an enum costs and
how it can be stored -- and lesson 12 turns exactly that fact into a
compile-time-sized table.

## Lesson 07 - Layout is not free

`src/lessons/07_layout_and_padding.i`

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
