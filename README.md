# i-learn

Small, runnable lessons for the I programming language.

This repository is deliberately separate from the compiler repo. It should feel
like a user project: it uses the packaged compiler from `C:\devel\i-windows-x64`
or from `I_HOME` / `PATH`, and it imports `std` from beside that compiler.

## Quick Check

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check_all.ps1
```

The script compiles every file in `src/lessons` to generated C under `build/gen`.
It does not require the compiler source tree.

## Reading Order

Read `book/00-how-to-read.md` first, then walk through the lesson files in
numeric order.

The early lessons explain C's core ideas through I:

- values, expressions, and simple output
- control flow
- arrays and pointers
- structs and enums
- procedures and callback-shaped data

The later lessons move into I-specific pieces:

- uniform declarations
- standard-library imports from the installed compiler
- generic structs and procs
- enum-sized tables
- reflection metadata
- simple metaprogramming habits

The point is not to cover the whole language. The point is to build a working
mental model one small program at a time.

