# 03 - Imports, Storage, And Generic Data

Once declarations, blocks, and plain data are comfortable, the lessons move into
library-shaped code. The important shift is that I can keep storage explicit
while still giving you reusable definitions.

## Lesson 07 - Standard Print

`src/lessons/07_std_print.i` asks how a normal project uses library source that
ships beside the packaged compiler.

The file begins with an import:

```i
import "std/Print.i"
```

Read this as a source dependency. The lesson is not reaching into the compiler
repository. It is asking the installed compiler environment for the standard file
named by the import path.

The calls are generic:

```i
print<*const char>("std print says ");
print<i32>(42);
print<*const char>("\n");
```

The type argument inside `<...>` chooses the concrete print shape for that call.
This is deliberately explicit here so the generic relationship stays visible.

Then the lesson shows the short form:

```i
printfmt("{} says {} and {}\n", name, count, ratio);
```

Each `{}` takes the next argument and prints it using the `print<T>` for that
argument's type. There is no format letter to choose and none to get wrong, and
no cast: a C `printf` needs `cast(ratio, f64)` for an `f32` because varargs hide
the type, while `printfmt` already knows it.

That extends to your own types. The lesson defines `print<Color>` and then writes
`printfmt("color is {}\n", Color.Green)` without printfmt knowing anything about
`Color`.

The part worth understanding is that **none of this exists at run time.** The
compiler splits the format string, works out each argument's type, and emits the
calls itself. Where every argument has a matching C conversion it emits a single
`printf`; where one does not {D} your `Color`, or a `b32`, which prints as
`true`/`false` rather than a number {D} it falls back to a call per piece for
that line. Open `build/gen/07_std_print.c` and you can see both outcomes side by
side.

So the convenient spelling is also the fast one. That is the intended shape for I
library code: the compiler knows the types, so it should be the thing doing the
formatting work, not a runtime parser reading `%d` out of a string.

Try this:

- print another integer
- print two strings with a number between them
- add a `print<T>` for a struct of your own and use it from `printfmt`
- compare the generated C for a line of numbers against a line containing your
  struct

## Lesson 08 - Arenas And Array

`src/lessons/08_arenas_and_array.i` asks how reusable containers can still keep
allocation explicit.

The imports bring in an array type and arena helpers:

```i
import "std/Array.i"
import "std/memops.i"
```

The arena is ordinary storage initialized by a helper procedure:

```i
arena: memops_arena = {};
memops_arena_initialize(arena.&);
```

The array reserves backing storage from that arena:

```i
values: Array<i32> = Array<i32>reserve(arena.&, 5);
```

Read `Array<i32>` as the concrete array shape for `i32` elements. The resulting
value carries metadata like `length` and a pointer-like `data` field for the
backing storage.

The fill loop uses both pieces:

```i
for (i: u64 = 0; i < values.length; i += 1) {
    values.data[i] = cast(i * i, i32);
}
```

After it runs, the printed values come from reserved storage owned by the arena.
That pair, `length` and `data`, is the basic shape to notice: the array value is
small metadata, and the arena owns the allocation.

Try this:

- reserve 8 values
- store `i + 100` instead of `i * i`
- print the last element by using `values.length - 1`

## Lesson 09 - Generic Box

`src/lessons/09_generics_box.i` asks how one definition can describe many
concrete data shapes.

The generic type is intentionally tiny:

```i
Box: struct<T> = {
    value: T;
}
```

`T` is a placeholder in the definition. It becomes a real type when the program
uses `Box<i32>`, `Box<f32>`, or another concrete type.

The procedures are owner-qualified:

```i
Box<T>make: proc<T>(value: T)->Box<T> = { ... }
Box<T>unwrap: proc<T>(box: Box<T>)->T = { ... }
```

The owner prefix says these operations belong with `Box<T>`. The generic
procedure parameter says the operation can be instantiated for the same concrete
`T` as the box.

After it runs, the lesson has created two boxes from one source definition. One
holds an `i32`, one holds an `f32`, and neither needed a duplicate handwritten
struct.

Try this:

- make a `Box<bool>`
- rename `value` to `item` and update the procedures
- add `Box<T>replace` that returns a new box with a new value

## Lesson 10 - Enum-Sized Tables

`src/lessons/10_enum_sized_tables.i` asks how declarations can remove a little
manual counting.

The enum gives the table's indexes names:

```i
Stat: enum = {
    Health,
    Stamina,
    Focus,
}
```

The array size comes from the enum metadata:

```i
values: [Stat<>.count]i32 = {};
values[Stat.Health] = 100;
values[Stat.Stamina] = 50;
values[Stat.Focus] = 25;
```

Read `Stat<>.count` as "the number of members declared by `Stat`." The table
size follows the enum, and the assignments use enum names instead of raw indexes.

After it runs, the output proves the table and enum stayed aligned. If you add a
new stat, the count changes at the declaration site instead of hiding in a
separate magic number.

Try this:

- add `Mana` to `Stat`
- assign a value for `Stat.Mana`
- print all four values with a loop

By the end of this chapter, the pieces should feel connected: imports bring in
library code, arenas make allocation explicit, generics remove repetition, and
metadata lets declarations describe useful table sizes.
