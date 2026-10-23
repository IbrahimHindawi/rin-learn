# 05 - Storage And Memory

Lessons 10 through 11.

Where a value lives decides how long it lasts, and an arena is the answer this language gives to the third kind.

## Lesson 10 - Where memory comes from, and when it stops


`src/lessons/10_storage_and_lifetime.rin`

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
    return doomed&;
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

## Lesson 11 - Memory you are responsible for


`src/lessons/11_arenas_and_array.rin`

```i
arena: memops_arena = {};
memops_arena_initialize(arena&);

values: array<i32> = array<i32>reserve(arena&, 5);
```

An arena is a large block of memory obtained once, handed out in pieces, and
released all at once. Asking for a piece is a pointer bump: return the current
position, then move it forward. That is the whole allocator.

It is worth understanding why this shape is common in systems code rather than
the `malloc`/`free` pair you may expect.

**Allocation is nearly free.** A bump is an addition. `malloc` has to search a
structure of free blocks, and may take a lock.

**There is no individual free.** You do not release one `array`; you release the
arena and everything in it goes at once. That sounds like a limitation and is
usually the point -- most programs have natural moments where a whole batch of
work is finished. A frame ends. A request completes. A file finishes parsing.

**It removes a class of bug by removing the decision.** You cannot free
something twice, or free it and keep using it, if there is no per-object free.
What you can still do is keep a pointer past the arena's own lifetime, which is
lesson 09's mistake wearing different clothes.

**Everything in it is contiguous**, so it inherits lesson 05's cache behaviour.

`array<i32>` here is a pointer plus a length, pointing into the arena. It does
not own the memory and does not free anything.
