# 02 - Expressions And Control Flow

Lessons 03 and 04.

A short chapter. These are the parts most familiar from other languages, and the
reason they come after sizes and addresses rather than before is that two of the
rules here only make sense once you know a value has a width.

## Lesson 03 - Conversions are visible

`src/lessons/03_values_and_expressions.rin`

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

## Lesson 04 - Loops, branches, and a switch that does not fall through

`src/lessons/04_control_flow.rin`

`for`, `if`, `continue` and `break` behave as you expect. Two things do not.

**A `switch` case does not fall through.** Each case takes a block and is
self-contained; there is no `break` to forget:

```i
switch (mode) {
    case Mode.Idle: {
        sum += 10;
    }
    case Mode.Walk: {
        sum += 20;
    }
}
```

C's fall-through is famously a source of bugs, and the cases where you actually
want it are rare enough to be worth writing out. Go, Rust and Zig all made the
same decision.

**A branch requires braces.** `if (x) return;` is not accepted. That makes the
dangling-else ambiguity impossible to write, and it means adding a second
statement to a branch cannot silently leave it outside the branch.

Worth knowing while you are here: a condition is C's condition. `if (n)` on an
integer means `n != 0`, and `and`/`or` accept any integer rather than requiring
a boolean. That is deliberate, and it is the same bargain as lesson 01 -- the
convention is to write `x != 0 and y != 0` and say what you mean.

## Where this fits

Nothing here is exotic, which is the point. The unusual parts of this language
are the parts about memory, and those are the surrounding chapters. Control flow
is the ordinary machinery in between.
