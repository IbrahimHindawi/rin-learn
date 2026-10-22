# 03 - Pointers And Arrays

Lessons 05 through 06.

A variable is a place, and a place has a number. This is the chapter K&R puts fifth, for the reason its ordering exists: passing a copy has to fail before passing an address means anything.

## Lesson 05 - A variable is a place


`src/lessons/05_addresses.rin`

Two operators do all of it:

    value&      the address of `value`
    place[0]     the value at `place`

They are exact inverses. `x&[0]` is `x`.

The lesson prints where `a` and `b` live, then passes `a`'s address to a
procedure that never sees `a`:

```i
set_to_seven: proc(place: *i32) -> void = {
    place[0] = 7;
}
```

After the call, `a` is 7. That is the entire idea of a pointer: the procedure
received a number, went to that place, and wrote there. Nothing was returned and
nothing was copied back.

Three things to notice in the output.

**The addresses are huge and look arbitrary.** They are. The operating system
decides where your stack goes, and it moves between runs -- partly as a security
measure. Run the lesson twice and the numbers change. The *distance* between the
two variables will not.

**The order is not yours to choose.** The lesson prints which of `a` and `b`
sits lower, because the compiler decides, and it is free to decide differently.
Declaring `a` first does not put it first.

**A pointer is an ordinary value.** It has a size, you can copy it, you can
store it in a struct, and it has an address of its own. `p = b&` moved no
integers -- it changed 8 bytes of pointer.

The exercise at the bottom of that lesson is worth doing. Subtract the two
addresses in the wrong order and you get 18446744073709551612 rather than -4,
because `uintptr` is unsigned and subtracting past zero wraps around to the top
of its range. Same bargain as the `i8`, in a different costume.

## Where this leaves you

After three lessons you know that a program has one entry and one exit code,
that every value has a size you chose, and that every variable is a place with a
number. Everything from here is built on those.

## Lesson 06 - An array is a run of bytes


`src/lessons/06_arrays_and_pointers.rin`

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
