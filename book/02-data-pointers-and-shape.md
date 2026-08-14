# 02 - Data, Pointers, And Shape

After the first control-flow lessons, the next step is to understand how I names
data shape. The lesson files keep the shapes tiny so you can see every piece.

## Lesson 03 - Arrays And Pointers

`src/lessons/03_arrays_and_pointers.i` starts with fixed storage:

```i
values: [4]i32 = {};
```

The count is part of the type. This is not a promise that the array might grow;
it is four `i32` slots. The initializer `{}` asks for zeroed storage.

The procedure in the same file accepts a pointer:

```i
increment: proc(value: *i32)->void = {
    value[0] += 1;
}
```

The caller passes the address of existing storage:

```i
first: *i32 = values[0].&;
increment(first);
```

That is the core pointer idea in I: if a procedure should mutate something the
caller already owns, pass a pointer to that storage.

Try this:

- pass `values[2].&` instead of `values[0].&`
- change the array count to 5 and update the loop
- make `increment` add 10 instead of 1

## Lesson 04 - Structs And Enums

`src/lessons/04_structs_and_enums.i` combines named fields and named states:

```i
Point: struct = {
    x: f32;
    y: f32;
}

SpriteKind: enum = {
    Player,
    Pickup,
    Door,
}
```

`Sprite` then nests those ideas:

```i
Sprite: struct = {
    kind: SpriteKind;
    pos: Point;
}
```

The lesson is worth reading slowly because it shows how I keeps composition
plain. A sprite has a kind and a position. A position has two fields. Assignment
uses the same path you would use to read the value: `s.pos.x`.

Try this:

- add `Enemy` to `SpriteKind`
- add a `health: i32` field to `Sprite`
- initialize two sprites with different positions

## Lesson 05 - Procedures And Callbacks

`src/lessons/05_procs_and_callbacks.i` shows that procedure types can be named:

```i
Op: alias = *proc(a: i32, b: i32)->i32;
```

`Op` is a pointer to a procedure that takes two `i32` values and returns an
`i32`. The lesson stores those procedure pointers in an array and inside a
struct:

```i
table: [2]Op = {};
table[0] = add;
table[1] = mul;
```

This is the callback pattern in its smallest useful form. The data structure does
not need to know which operation it will call until you put a procedure into it.

Try this:

- add a `sub` procedure
- make the table hold three operations
- add a second field to `Adder` for another callback

These lessons are where I starts feeling like a practical systems language:
storage is explicit, names describe shape, and procedures can travel through
data just like other values.
