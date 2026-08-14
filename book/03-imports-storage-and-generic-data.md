# 03 - Imports, Storage, And Generic Data

Once declarations, blocks, and plain data are comfortable, the lessons move into
library-shaped code. The important shift is that I can keep storage explicit
while still giving you reusable definitions.

## Lesson 07 - Standard Print

`src/lessons/07_std_print.i` imports from the installed standard library:

```i
import "std/Print.i"
```

The import is resolved relative to the packaged compiler's `std` folder. That is
why this repository can behave like a user project instead of reaching into the
compiler source tree.

The calls are generic:

```i
print<*const char>("std print says ");
print<i32>(42);
```

Read `print<i32>` as "use the `i32` version of `print` here." The type argument
is explicit, so the lesson is easy to follow even before inference exists.

Try this:

- print another integer
- print two strings with a number between them
- change the import path and confirm the compiler reports it

## Lesson 08 - Arenas And Array

`src/lessons/08_arenas_and_array.i` combines two standard-library pieces:

```i
import "std/Array.i"
import "std/memops.i"
```

The arena owns allocation. `Array<i32>` is a generic container whose concrete
element type is `i32`:

```i
arena: memops_arena = {};
memops_arena_initialize(arena.&);

values: Array<i32> = Array<i32>reserve(arena.&, 5);
```

The loop writes through `values.data` and uses `values.length` as the count:

```i
for (i: u64 = 0; i < values.length; i += 1) {
    values.data[i] = cast(i * i, i32);
}
```

That pair, `length` and `data`, is the basic shape to notice. The array object is
small metadata; the arena owns the backing storage.

Try this:

- reserve 8 values
- store `i + 100` instead of `i * i`
- print the last element by using `values.length - 1`

## Lesson 09 - Generic Box

`src/lessons/09_generics_box.i` shows a generic type you can hold in your head:

```i
Box: struct<T> = {
    value: T;
}
```

The type parameter `T` is a placeholder in the definition. It becomes concrete
when used as `Box<i32>` or `Box<f32>`.

The procedures are owner-qualified:

```i
Box<T>make: proc<T>(value: T)->Box<T> = { ... }
Box<T>unwrap: proc<T>(box: Box<T>)->T = { ... }
```

That naming style keeps related operations near the type they operate on. A call
like `Box<i32>unwrap(a)` tells you both the owner shape and the concrete type.

Try this:

- make a `Box<bool>`
- rename `value` to `item` and update the procedures
- add `Box<T>replace` that returns a new box with a new value

## Lesson 10 - Enum-Sized Tables

`src/lessons/10_enum_sized_tables.i` uses reflection-flavored metadata without a
full reflection loop:

```i
values: [Stat<>.value_count]i32 = {};
values[Stat.Health] = 100;
```

The enum gives names to indexes. `Stat<>.value_count` gives the array its size.
That means adding a new enum value updates the intended table size in one place.

Try this:

- add `Mana` to `Stat`
- assign a value for `Stat.Mana`
- print all four values with a loop

By the end of this chapter, the pieces should feel connected: imports bring in
library code, arenas make allocation explicit, generics remove repetition, and
metadata lets declarations describe useful table sizes.
