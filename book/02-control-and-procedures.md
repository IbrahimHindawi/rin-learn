# 02 - Control And Procedures

Lessons 03 through 04.

Branching, looping, and giving a piece of work a name. Everything here works on values you already have; nothing yet reaches for an address.

## Lesson 03 - Loops, branches, and a switch that does not fall through


`src/lessons/03_control_flow.rin`

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

## Lesson 04 - A piece of work with a name

`src/lessons/04_procs.rin`

```
double_it: proc(n: i32) -> i32 = {
    return n * 2;
}
```

Everything so far has lived inside `main`. A proc is how you give a piece of
work its own name, its own parameters, and its own place to put things.

The declaration is the shape you already know, with a parameter list in the
middle: `double_it` is a proc, it takes an `i32` called `n`, it hands back an
`i32`. Read left to right, same as a variable, same as a struct.

**A parameter is a copy.** This is the sentence the next chapter is built on.
When you call `spend(budget)`, the proc gets its own `budget`, initialised from
yours. It can assign to it all it likes; yours does not move. Watch it fail:

```
budget: i32 = 100;
spend(budget);          // sets its own copy to 0
// budget is still 100
```

There is no way to fix that from inside the proc, because the proc was never
given anything but a number. To change a caller's variable you have to hand over
*where it lives*, and that is an address -- which is exactly why K&R spends a
chapter on functions before it says the word pointer, and why this book does
too.

**Order does not matter.** A proc may be called by something declared above it.
The compiler resolves names across the whole file, so there are no prototypes
and no header discipline. C requires a forward declaration here and rin does
not.

**A proc may call itself.** `factorial(5)` calls `factorial(4)` before it can
finish, and so on down. Five sets of `n` exist at once, each in its own frame,
and they unwind as the calls return. That storage is handed back automatically,
which is a preview of the stack that chapter 05 names properly.
