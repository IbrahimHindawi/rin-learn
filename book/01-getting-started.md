# 01 - Getting Started

Lessons 00 through 02.

What a program is, what a value costs, and how much space you chose.

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

## Lesson 01 - Conversions are visible


`src/lessons/01_values_and_expressions.rin`

```i
count: i32 = 6;
scale: f32 = 2.5f;
total: i32 = count * 3 + 1;
ratio: f32 = cast(total, f32) / scale;
```

The arithmetic holds no surprises. The `cast` is the lesson.

Dividing an `i32` by an `f32` requires one of them to change representation --
an integer and a float are different bit patterns, not different amounts of the
same thing. Turning `19` into `19.0f` is real work, and it can lose information
going the other way.

So it is written down. `cast(total, f32)` is visible at the point it happens,
and a reader can see where a conversion occurred without knowing the promotion
rules by heart.

Be aware of what `cast` does *not* do: it will not stop you losing data. Casting
an `i64` to an `i8` discards the top bits exactly as lesson 01 did, silently.
The value of writing it down is that it is written down.

The `f` in `2.5f` marks a 32-bit float literal. Without it you have an `f64`,
and assigning that to an `f32` is another narrowing.

## Lesson 02 - A value costs bytes


`src/lessons/02_sizes.rin`

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
