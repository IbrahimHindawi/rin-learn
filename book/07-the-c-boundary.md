# 07 - The C Boundary

Lessons 15.

Calling C, and being called by it.

## Lesson 15 - The C Surface


`src/lessons/15_c_surface.rin` asks how rin source talks to declarations and symbols
owned outside the rin file.

Before this lesson, the book avoided the boundary so the rin shape could stand on
its own. Now the boundary is the subject:

```i
cinclude "stdio.h"
#define I_LEARN_BONUS 7

puts: proc(text: *const char)->i32 = { external; }
```

`cinclude` says the generated translation unit needs a foreign header. The
`external` body says the symbol exists elsewhere, so rin should type-check calls to
it but should not emit a new definition for it.

The body then uses both pieces:

```i
puts("this call is checked by rin and provided by C");
printf("bonus=%d\n", I_LEARN_BONUS);
```

After it runs, the lesson has shown a precise boundary: rin can check the call
shape, carry through a macro, and still leave ownership of the external symbol to
the platform side.

That gives you a practical rule:

- write normal rin declarations for the things rin owns
- use `external` for declarations owned outside rin
- use `cinclude` when the generated unit needs a header or macro
- inspect `build/gen` when you want to see the boundary precisely

## Generated Output

The check script writes lowered C and header files under `build/gen`. Those files
are useful evidence. They show how a regular rin declaration turns into something
the platform toolchain can compile and link.

Do not start the book by staring at that output. Start with rin source. Once the rin
shape feels clear, the generated C becomes a teaching aid instead of a distraction.

## What To Try

- change the `puts` declaration in lesson 14 and watch the type checker complain
- add another `#define` beside `I_LEARN_BONUS` and use it in `main`
- compile lesson 11 and compare the generated concrete names for `Box<i32>` and
  `Box<f32>`
- compile lesson 15 and find the generated reflection table for `Payload`
- add a `print<T>` overload for one of your own structs and use it in a
  `printfmt`

The point of the C connection is not nostalgia. It is leverage: rin source stays
small and regular while still landing in a world of debuggers, linkers, headers,
and platform libraries.
