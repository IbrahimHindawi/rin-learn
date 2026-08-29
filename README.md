# rin-learn

Small, runnable lessons for the rin programming language.

This repository is deliberately separate from the compiler repo. It should feel
like a user project: it uses the packaged compiler from `rin-windows-x64` or from
`RIN_HOME` / `PATH`, and it imports `std` from beside that compiler.

## Quick Check

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check_all.ps1
```

The script compiles every file in `src/lessons` and writes lowered output under
`build/gen`. It does not require the compiler source tree.

## Reading Order

Read `book/00-how-to-read.md` first, then the chapters in order. The order is
the argument: each lesson needs the one before it.

This is a course in **low-level programming** that happens to use rin. The
subject is the machine -- how much space a value takes, where it lives, how long
it lasts -- because everything else in a systems language follows from that.

The order follows the one K&R uses, for the reason that ordering exists: write a
whole program, then types and sizes, then control flow, then procs, and only
then pointers. You cannot see why an address is worth passing until you have
watched a copy fail to come back.

- `01-getting-started.md` -- what a program is, arithmetic with visible
  conversions, and what a value costs in bytes. Lessons 00 through 02.
- `02-control-and-procedures.md` -- branching, looping, a `switch` that does not
  fall through, and giving a piece of work a name. Lessons 03 through 04.
- `03-pointers-and-arrays.md` -- a variable is a place, an array is a run of
  bytes. Lessons 05 through 06.
- `04-structs-and-layout.md` -- structs as named offsets, where padding comes
  from, and a struct that holds something callable. Lessons 07 through 09.
- `05-storage-and-memory.md` -- static, automatic and manual storage, and the
  arena. Lessons 10 through 11.
- `06-generics-and-printing.md` -- generics as stamped-out copies, printing as
  ordinary code, and letting the compiler size a table. Lessons 12 through 14.
- `07-the-c-boundary.md` -- calling something this compiler did not compile.
  Lesson 15.
- `08-reflection.md` -- the compiler's own knowledge about your types, readable
  at runtime. Lessons 16 through 19.

There is also a single-page version with every lesson's source inline:
`docs/lessons.html`, and the same as a PDF. It opens with what the language is
and how to install it.

The three lessons carrying the most weight are 02 (sizes), 05 (addresses) and
08 (layout and padding). If you read three, read those.

The point is not to cover the whole language. The point is to build a working
mental model one small program at a time.
