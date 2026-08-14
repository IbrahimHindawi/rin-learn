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

`src/lessons/00_hello_world.i` asks the smallest possible question: what does a
complete I program look like?

Before you read the file, ignore the output call and look for the declaration
shape. The program is one top-level name with one procedure type:

```i
main: proc()->i32 = {
    printf("hello from I\n");
    return 0;
}
```

Read it as a declaration named `main`. Its type is a procedure taking no
arguments and returning `i32`. Its value is the block after `=`. The block is not
separate syntax for a special global function; it is the value assigned to the
name.

After it runs, the important result is not the greeting. The important result is
that you have seen the outer frame used by every later lesson: name, type, value,
body, return.

Try this:

- change the printed text
- change the return value to `1`
- remove the `return` and see what the compiler says

## Lesson 01 - Values And Expressions

`src/lessons/01_values_and_expressions.i` asks how typed storage and expressions
fit together inside a procedure body.

Start by reading the local declarations as little facts about storage:

```i
count: i32 = 6;
scale: f32 = 2.5f;
total: i32 = count * 3 + 1;
ratio: f32 = cast(total, f32) / scale;
```

`count` is integer storage. `scale` is floating-point storage. `total` is another
integer computed from `count`. `ratio` crosses from integer arithmetic into
floating-point arithmetic, so the conversion is visible with `cast`.

After it runs, you should be able to predict the printed values before looking at
them: `count` stays `6`, `total` becomes `19`, and `ratio` is computed from `19 /
2.5`. The lesson is training you to read types and expressions together, instead
of treating the type annotation as decoration.

Try this:

- change `count` and predict `total`
- remove the `cast` in `ratio`
- introduce a second `f32` and combine it with `scale`

## Lesson 02 - Control Flow

`src/lessons/02_control_flow.i` asks how a program changes direction while still
keeping scope clear.

The loop gives its counter a type right where the counter is introduced:

```i
for (i: i32 = 0; i < 5; i += 1) {
    if (i == 3) {
        continue;
    }
    sum += i;
}
```

The `if` block makes the exceptional case visible. The `continue` says the loop
should skip the rest of this iteration and move to the next value of `i`.

The same file then switches over a named mode:

```i
switch (mode) {
    case Mode.Idle: { sum += 10; }
    case Mode.Walk: { sum += 20; }
    default: { sum += 30; }
}
```

Each case owns a block. That matters because local names introduced in one case
belong to that case, and the shape of each arm stays explicit.

After it runs, the sum is the story of the branches taken. The loop adds `0`,
`1`, `2`, and `4`; the selected mode then chooses the default arm and adds more.
That makes the output a compact check that the loop, branch, and switch all did
what you expected.

Try this:

- add a `Mode.Jump` value
- add a matching case
- remove the `continue` and predict the new sum

The first three lessons are enough to read a lot of I source: declarations,
blocks, expressions, branches, loops, and enum-qualified names.
