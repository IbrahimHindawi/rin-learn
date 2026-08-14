# 01 - The Shape Of I

Before looking outward, learn the grammar I wants you to see everywhere:

```i
name: Type = value;
name: proc(arg: Type)->Return = { ... }
Name: struct = { field: Type; }
```

The name comes first. The type comes after `:`. The value or body comes after
`=`. That same shape is used for local variables, procedures, aliases, structs,
and generic definitions.

## Lesson 00 - Hello World

`src/lessons/00_hello_world.i` shows the whole outer shape:

```i
main: proc()->i32 = {
    printf("hello from I\n");
    return 0;
}
```

Read it as a declaration named `main`. Its type is a procedure taking no
arguments and returning `i32`. Its value is the block after `=`.

Notice the habit this creates. You do not need a separate mental rule for global
functions. A function is a value with a procedure type.

Try this:

- change the printed text
- change the return value to `1`
- remove the `return` and see what the compiler says

## Lesson 01 - Values And Expressions

`src/lessons/01_values_and_expressions.i` adds local variables and casts:

```i
count: i32 = 6;
scale: f32 = 2.5f;
total: i32 = count * 3 + 1;
ratio: f32 = cast(total, f32) / scale;
```

The lesson is small, but it teaches three important habits:

- choose a concrete type for storage
- let expressions combine values of known type
- make conversions visible with `cast`

The `2.5f` suffix is also doing work. It keeps the literal in the `f32` world
before the later print call widens the value for output.

Try this:

- change `count` and predict `total`
- remove the `cast` in `ratio`
- introduce a second `f32` and combine it with `scale`

## Lesson 02 - Control Flow

`src/lessons/02_control_flow.i` gives you a compact tour of decisions:

```i
for (i: i32 = 0; i < 5; i += 1) { ... }

if (i == 3) {
    continue;
}
```

Loops keep their counter declaration in the loop header. `if` blocks are ordinary
blocks. `continue` moves to the next loop iteration.

The same lesson also shows a scoped `switch`:

```i
switch (mode) {
    case Mode.Idle: { ... }
    case Mode.Walk: { ... }
    default: { ... }
}
```

Each case owns a block. That makes the local scope obvious and keeps each arm
from accidentally becoming part of the next arm.

Try this:

- add a `Mode.Jump` value
- add a matching case
- remove the `continue` and predict the new sum

The first three lessons are enough to read a lot of I source: declarations,
blocks, expressions, branches, loops, and enum-qualified names.
