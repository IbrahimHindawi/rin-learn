# 00 - How To Read This

This is a course in low-level programming. rin is the language it uses, but
the subject is the machine: how much space a value takes, where it lives, how
long it lasts, and what the computer actually does with it.

That is a deliberate choice. Most introductions teach a language's syntax and
mention memory later, as an advanced topic. Here it is the first topic, because
everything else in a systems language is downstream of it. You cannot reason
about a struct's cost without knowing what padding is, and you cannot reason
about a pointer without knowing that a variable is a place.

## The order is the argument

Read the lessons in numeric order. They are not a reference organised by
feature; they are a sequence where each one needs the one before it.

| | |
|---|---|
| 00-02 | what a program is, what a value costs, where it lives |
| 03-04 | expressions and control flow, now that values have a size |
| 05-07 | arrays, structs, and what layout actually means |
| 08-09 | procedures, copies, and storage lifetime |
| 10-12 | memory you manage yourself, generics, tables |
| 13-14 | printing, and the boundary with C |
| 15-18 | reflection: the compiler's own knowledge, at runtime |

The three lessons doing the heaviest lifting are 01, 02 and 07. If you only read
three, read those.

## Every lesson runs

Each file in `src/lessons` is a complete program. Open it, read the comments,
build it, then change one line and build again. The loop should be short enough
that the compiler answers your question faster than reasoning about it would.

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check_all.ps1
```

That compiles every lesson, builds the generated C, and runs it. All 19 should
build and exit 0.

## The thing this language lets you see

rin compiles to C that a person can read. That is unusual, and it is the best
teaching tool here: after any lesson, open the matching file under `build/gen`
and look at what your code became.

    src/lessons/07_layout_and_padding.rin   ->   build/gen/07_layout_and_padding.c

You will see your struct as a C struct, your generic as a stamped-out copy with
a mangled name, and your reflection data as a plain table of bytes. Nothing is
hidden behind a runtime you cannot inspect. When a lesson says "this is what the
machine does", you can go and check.

## What the lessons will not do

They will not protect you. This language keeps C's bargain: no bounds checking,
no overflow trapping, no lifetime enforcement. Lesson 01 puts 200 into an 8-bit
integer and reads back -56, and nothing complains. Lesson 09 shows a procedure
returning the address of a dead local.

Those are in the course on purpose. The protection in a language like this comes
from understanding the machine, not from the machine understanding you.

## Where the numbers come from

Some outputs differ on your machine -- addresses especially, since the operating
system decides them fresh each run. The lessons say so where it matters. Sizes
and offsets will match, because those are fixed by the target, and that is the
point of writing `i32` rather than `int`.
