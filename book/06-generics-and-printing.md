# 06 - Generics And Printing

Lessons 12 through 14.

One definition instantiated per type, and the first place the compiler knowing about your types pays for itself.

## Lesson 12 - A generic is a stamp


`src/lessons/12_generics_box.rin`

```i
Box: struct<T> = {
    value: T;
}
```

`Box<i32>` and `Box<f32>` are two different types. Not one type that adapts --
two, generated separately, with different sizes.

This is the lesson where you should open the generated C. In
`build/gen/11_generics_box.c` you will find something like:

```c
typedef struct Box_i32 { i32 value; } Box_i32;
typedef struct Box_f32 { f32 value; } Box_f32;
```

Two structs. Two copies of every procedure, one per type, with the type name
mangled into the symbol. The compiler wrote out what you would have written by
hand, which is exactly what "monomorphisation" means -- one shape per concrete
type.

The consequences are all visible from that:

**No runtime cost.** `Box<i32>` is as fast as a hand-written struct holding an
`i32`, because that is what it compiled to. Nothing is boxed, nothing is looked
up, nothing is checked at runtime.

**Code size grows with instantiations.** Ten types means ten copies. This is the
trade the technique makes, and it is why generic-heavy C++ builds are slow.

**Errors appear inside the copy.** Write `a + b` in a generic body and use it
with a type that has no `+`, and the error is reported in the generated
instantiation, not at the call that asked for it. There are no constraints in
this language to catch it earlier -- a deliberate choice, since adding them is
the fastest route to C++-shaped complexity.

## Lesson 13 - Printing is ordinary code


`src/lessons/13_std_print.rin`

`printfmt` is not built into the language. It is a procedure in `std/print.rin`,
and the `{}` placeholders are resolved at compile time by matching each argument
against a `print<T>` overload.

Which means you can add your own:

```i
print: proc<Color>(c: Color) -> void = {
    if (c == Color.Red) {
        print_cstr("red");
    } else {
        print_cstr("green");
    }
}
```

Now `printfmt("{}", some_color)` finds it, the same way it finds the one for
`i32`. Nothing registered it and nothing looked it up at runtime -- the compiler
picked the overload by type when it compiled the call.

For an enum, the overload is optional. Without one, `{}` prints the member's
name (`Red`), so you only write `print<Color>` to spell it differently.

That is worth contrasting with C's `printf`, where `%d` is a promise you make in
a string and nothing checks. Pass an `i32` to a `%s` and you get whatever
happens. Here the argument's type selects the code, so there is no format string
to get wrong.

## What C is doing in this story

Now that the rin lessons have their own shape, it is useful to say what C is
doing here.

C is C because it keeps a small, sharp contract with the machine and the linker:

- memory is bytes, and values live in storage
- addresses can be passed around explicitly
- arrays are contiguous storage, not growable objects
- structs describe layout by fields and order
- enums give names to integer states
- functions are symbols with calling conventions
- headers, declarations, and object files form a build boundary
- the language keeps very little runtime between you and the program

That list matters more than C's punctuation. The durable lesson is not where the
asterisk goes. The durable lesson is that a program has physical shape.

rin keeps that shape visible, but asks the source to be more regular. Declarations
use `name: Type = value`. Procedures, structs, aliases, generic types, and local
variables all follow the same left-to-right rhythm. Reflection metadata is also
generated from the declarations you already wrote, instead of being maintained in
a separate table by hand.

## Lesson 14 - Letting the compiler size a table


`src/lessons/14_enum_sized_tables.rin`

```i
values: [Stat<>.count]i32 = {};
```

`Stat<>` is the enum's reflection record, and `.count` is how many members it
declares. The compiler knows that number as soon as the enum is parsed, so it
can be an array length.

The bug this removes is small and extremely common. Every C codebase has this:

```c
typedef enum { Health, Stamina, Focus, STAT_COUNT } Stat;
int values[STAT_COUNT];
```

A sentinel member that exists only to be counted, and that shows up in every
`switch`, every iteration, and every reflection over the enum. Add a real member
in the wrong place and the count silently stops matching.

Here the count is derived rather than declared. Add a member to `Stat` and the
array grows. There is nothing to keep in step because there is only one source
of truth.

That is the first appearance of a bigger idea: the compiler already knows things
about your types, and it can hand them back. The next chapter is about how much
it knows.
