# 05 - The C Connection

Now that the I lessons have their own shape, it is useful to say what C is doing
in this story.

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

I keeps that shape visible, but asks the source to be more regular. Declarations
use `name: Type = value`. Procedures, structs, aliases, generic types, and local
variables all follow the same left-to-right rhythm. Reflection metadata is also
generated from the declarations you already wrote, instead of being maintained in
a separate table by hand.

## Lesson 06 - The C Surface

`src/lessons/06_c_surface.i` asks how I source talks to declarations and symbols
owned outside the I file.

Before this lesson, the book avoided the boundary so the I shape could stand on
its own. Now the boundary is the subject:

```i
cinclude "stdio.h"
#define I_LEARN_BONUS 7

puts: proc(text: *const char)->i32 = { external; }
```

`cinclude` says the generated translation unit needs a foreign header. The
`external` body says the symbol exists elsewhere, so I should type-check calls to
it but should not emit a new definition for it.

The body then uses both pieces:

```i
puts("this call is checked by I and provided by C");
printf("bonus=%d\n", I_LEARN_BONUS);
```

After it runs, the lesson has shown a precise boundary: I can check the call
shape, carry through a macro, and still leave ownership of the external symbol to
the platform side.

That gives you a practical rule:

- write normal I declarations for the things I owns
- use `external` for declarations owned outside I
- use `cinclude` when the generated unit needs a header or macro
- inspect `build/gen` when you want to see the boundary precisely

## Generated Output

The check script writes lowered C and header files under `build/gen`. Those files
are useful evidence. They show how a regular I declaration turns into something
the platform toolchain can compile and link.

Do not start the book by staring at that output. Start with I source. Once the I
shape feels clear, the generated C becomes a teaching aid instead of a distraction.

## What To Try

- change the `puts` declaration in lesson 06 and watch the type checker complain
- add another `#define` beside `I_LEARN_BONUS` and use it in `main`
- compile lesson 09 and compare the generated concrete names for `Box<i32>` and
  `Box<f32>`
- compile lesson 11 and find the generated reflection table for `Payload`

The point of the C connection is not nostalgia. It is leverage: I source stays
small and regular while still landing in a world of debuggers, linkers, headers,
and platform libraries.
