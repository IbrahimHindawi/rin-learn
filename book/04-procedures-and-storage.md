# 04 - Procedures And Storage

Lessons 08 and 09.

You now know what a value costs and where it sits. These two lessons are about
what happens when a value crosses into a procedure, and how long it survives
afterwards.

## Lesson 08 - Calls, copies, and code with addresses

`src/lessons/08_procs_and_callbacks.rin`

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

## Lesson 09 - Where memory comes from, and when it stops

`src/lessons/09_storage_and_lifetime.rin`

Three kinds of storage, and you choose every time you declare something.

**Static.** One copy, created before `main` runs, alive until the process exits.
Declared at file scope, or with `static` inside a procedure. In the lesson,
`g_counter` counts up across calls because it was never destroyed.

**Automatic.** Created when a procedure is entered, gone when it returns. In the
lesson, `local` prints `1` every time -- a fresh one per call. This is "the
stack", and it is fast precisely because ending a call is just moving a pointer
back.

**Manual.** Memory you ask for and are responsible for. That is lesson 10.

The addresses show the split. The static lives in the executable's own data and
barely moves between runs. The stack is somewhere else entirely, and the
operating system relocates it each time.

Then the part the lesson exists for:

```i
leak_a_local: proc() -> *i32 = {
    doomed: i32 = 42;
    return doomed.&;
}
```

`doomed` stops existing when the procedure returns. The address remains a
perfectly ordinary number that points at a stack slot the next call will reuse.
Reading through it is undefined behaviour.

Build it and clang does say something:

```
warning: address of stack memory associated with local variable 'doomed' returned
```

Understand why you got that warning, because it is narrow. The return statement
is right there, so the analysis is easy. Store the same address in a struct
field, hand the struct to another procedure, and return *that* -- nothing warns.
The lesson to take is not "the compiler will tell me".

The exercise is worth doing and worth being unsettled by: call it, print through
the pointer, and you will probably get 42. That is the worst outcome, because it
teaches you the code works. Call another procedure first and print again.

## The through-line

Automatic storage dies too soon for most data. Static storage has to be sized
before the program runs. Real programs need something in between, and that is
what the next chapter is about.
