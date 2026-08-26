# 06 - Printing, And The C Boundary

Lessons 13 and 14.

Everything so far stayed inside ilang. These two lessons are about the edge: how
output actually happens, and what it means to call something this compiler did
not compile.

## Lesson 13 - Printing is ordinary code

`src/lessons/13_std_print.i`

`printfmt` is not built into the language. It is a procedure in `std/Print.i`,
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

That is worth contrasting with C's `printf`, where `%d` is a promise you make in
a string and nothing checks. Pass an `i32` to a `%s` and you get whatever
happens. Here the argument's type selects the code, so there is no format string
to get wrong.

## What C is doing in this story

Now that the ilang lessons have their own shape, it is useful to say what C is
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

ilang keeps that shape visible, but asks the source to be more regular. Declarations
use `name: Type = value`. Procedures, structs, aliases, generic types, and local
variables all follow the same left-to-right rhythm. Reflection metadata is also
generated from the declarations you already wrote, instead of being maintained in
a separate table by hand.

## Lesson 14 - The C Surface

`src/lessons/14_c_surface.i` asks how ilang source talks to declarations and symbols
owned outside the ilang file.

Before this lesson, the book avoided the boundary so the ilang shape could stand on
its own. Now the boundary is the subject:

```i
cinclude "stdio.h"
#define I_LEARN_BONUS 7

puts: proc(text: *const char)->i32 = { external; }
```

`cinclude` says the generated translation unit needs a foreign header. The
`external` body says the symbol exists elsewhere, so ilang should type-check calls to
it but should not emit a new definition for it.

The body then uses both pieces:

```i
puts("this call is checked by ilang and provided by C");
printf("bonus=%d\n", I_LEARN_BONUS);
```

After it runs, the lesson has shown a precise boundary: ilang can check the call
shape, carry through a macro, and still leave ownership of the external symbol to
the platform side.

That gives you a practical rule:

- write normal ilang declarations for the things ilang owns
- use `external` for declarations owned outside ilang
- use `cinclude` when the generated unit needs a header or macro
- inspect `build/gen` when you want to see the boundary precisely

## Generated Output

The check script writes lowered C and header files under `build/gen`. Those files
are useful evidence. They show how a regular ilang declaration turns into something
the platform toolchain can compile and link.

Do not start the book by staring at that output. Start with ilang source. Once the ilang
shape feels clear, the generated C becomes a teaching aid instead of a distraction.

## What To Try

- change the `puts` declaration in lesson 14 and watch the type checker complain
- add another `#define` beside `I_LEARN_BONUS` and use it in `main`
- compile lesson 11 and compare the generated concrete names for `Box<i32>` and
  `Box<f32>`
- compile lesson 15 and find the generated reflection table for `Payload`
- add a `print<T>` overload for one of your own structs and use it in a
  `printfmt`

The point of the C connection is not nostalgia. It is leverage: ilang source stays
small and regular while still landing in a world of debuggers, linkers, headers,
and platform libraries.
