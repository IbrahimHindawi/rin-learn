# i-learn

Small, runnable lessons for the I programming language.

This repository is deliberately separate from the compiler repo. It should feel
like a user project: it uses the packaged compiler from `i-windows-x64` or from
`I_HOME` / `PATH`, and it imports `std` from beside that compiler.

## Quick Check

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check_all.ps1
```

The script compiles every file in `src/lessons` and writes lowered output under
`build/gen`. It does not require the compiler source tree.

## Reading Order

Read `book/00-how-to-read.md` first, then walk through the chapters in numeric
order.

The book is intentionally I-first. Each lesson section is wrapped in prose before
and after the code idea: what the lesson is asking, what to notice in the source,
what should feel different after it runs, and one or two small experiments to try
next.

- `01-the-shape-of-i.md` covers tiny programs, declarations, expressions, and
  control flow.
- `02-data-pointers-and-shape.md` covers arrays, pointers, structs, enums, and
  callback-shaped data.
- `03-imports-storage-and-generic-data.md` covers imports, standard-library
  storage, generic containers, and enum-sized tables.
- `04-reflection-and-metaprogramming.md` covers generated metadata, reflected
  fields, attributes, and generic instantiation shape.
- `05-the-c-connection.md` saves the outside-language comparison for the end,
  including lesson 06 and the generated output under `build/gen`.

The point is not to cover the whole language. The point is to build a working
mental model one small program at a time.
