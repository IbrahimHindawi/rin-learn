# 01 - Values, Memory, And Shape

Lessons 00 through 02.

Three questions come before everything else in a low-level language. What is a
program? How much space does a value take? Where does it live?

## Lesson 00 - What a program is

`src/lessons/00_hello_world.rin`

```i
main: proc() -> i32 = {
    printfmt("hello from rin\n");
    return 0;
}
```

Two things are worth more than the greeting.

**There is an entry point.** The operating system loads your executable, finds
`main`, and calls it. Before that call, nothing of yours has run. After it
returns, the process ends.

**The return value is an exit code**, not a result. `0` means the program
succeeded; anything else means it did not, and a shell or a build script will
act on that. It is not where you put your answer. Lesson 18 originally returned
its computed value here, which looked reasonable and was wrong.

The declaration shape is worth naming once, because every later lesson uses it:

    name : type = value

`main` is the name. `proc() -> i32` is the type: a procedure taking nothing and
returning an `i32`. The block after `=` is the value. A procedure body is not
special syntax; it is the value bound to that name, the same way `1` is the
value bound to `n` in `n: i32 = 1;`.

Now open `build/gen/00_hello_world.c` and find your `main`. It is there, in C,
recognisable. That relationship holds for the whole course.

## Lesson 01 - A value costs bytes

`src/lessons/01_sizes.rin`

Run it first. The output is the lesson.

```
i8   1 byte    u8   1 byte
i32  4 bytes   u32  4 bytes
i64  8 bytes   u64  8 bytes
*i32 8 bytes   *f64 8 bytes
usize 8 bytes
200 stored in an i8 reads back as -56
```

**The size is in the name.** `i32` is a 32-bit signed integer: 4 bytes, always,
on every target this compiler supports. C's `int` is not like this -- its size
is up to the implementation, which is why portable C code is full of `int32_t`.
rin starts where careful C ends up.

**Every pointer is the same size**, whatever it points at, because a pointer
holds an address and an address is a fixed-width number on a given machine. 8
bytes here, because this is a 64-bit target. What lives at that address is a
question of type, not of storage.

**`usize` is the size of a size.** It is big enough to count any object in
memory, which is why it is the type of a length or a byte count, and why it
matches the pointer width. There is deliberately no `isize`: a length is never
negative.

**And then the last line.** 200 does not fit in a signed 8-bit integer, whose
range stops at 127. The bits that did not fit were discarded and you got -56.
No error, no warning, no exception.

That is the bargain this language makes, and it is C's bargain. The compiler
will not stop you; it assumes you meant it. Your protection is that you wrote
`i8` yourself, knowing what it holds. This is the first place the course is
asking you to be careful rather than promising to be careful for you.

## Lesson 02 - A variable is a place

`src/lessons/02_addresses.rin`

Two operators do all of it:

    value.&      the address of `value`
    place[0]     the value at `place`

They are exact inverses. `x.&[0]` is `x`.

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
store it in a struct, and it has an address of its own. `p = b.&` moved no
integers -- it changed 8 bytes of pointer.

The exercise at the bottom of that lesson is worth doing. Subtract the two
addresses in the wrong order and you get 18446744073709551612 rather than -4,
because `uintptr` is unsigned and subtracting past zero wraps around to the top
of its range. Same bargain as the `i8`, in a different costume.

## Where this leaves you

After three lessons you know that a program has one entry and one exit code,
that every value has a size you chose, and that every variable is a place with a
number. Everything from here is built on those.
