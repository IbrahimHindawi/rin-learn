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
it lasts -- because everything else in a systems language follows from that. So
memory comes first rather than last.

- `01-values-memory-and-shape.md` -- what a program is, what a value costs in
  bytes, and why a variable is a place with an address. Lessons 00-02.
- `02-expressions-and-control.md` -- arithmetic, visible conversions, loops, and
  a `switch` that does not fall through. Lessons 03-04.
- `03-arrays-structs-and-layout.md` -- arrays as runs of bytes, structs as named
  offsets, and where padding comes from. Lessons 05-07.
- `04-procedures-and-storage.md` -- parameters are copies, code has addresses,
  and the difference between static, automatic and manual storage. Lessons
  08-09.
- `05-managing-memory.md` -- arenas, generics as stamped-out copies, and letting
  the compiler size a table. Lessons 10-12.
- `06-the-c-boundary.md` -- how printing works, and what it means to call
  something this compiler did not compile. Lessons 13-14.
- `07-reflection.md` -- the compiler's own knowledge about your types, available
  at runtime. Lessons 15-18.

The three lessons carrying the most weight are 01 (sizes), 02 (addresses) and
07 (layout and padding). If you read three, read those.

The point is not to cover the whole language. The point is to build a working
mental model one small program at a time.
