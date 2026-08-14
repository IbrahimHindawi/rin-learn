# 02 - Data, Pointers, And Shape

After the first control-flow lessons, the next step is to understand how I names
data shape. The lesson files keep the shapes tiny so you can see every piece.

## Lesson 03 - Arrays And Pointers

`src/lessons/03_arrays_and_pointers.i` asks what it means for a value to live in
storage that another procedure can touch.

Begin with the array declaration:

```i
values: [4]i32 = {};
```

The count is part of the type. This is not a promise that the array might grow;
it is four `i32` slots. The initializer `{}` asks for zeroed storage, so the file
starts from a known state.

The helper procedure accepts a pointer:

```i
increment: proc(value: *i32)->void = {
    value[0] += 1;
}
```

The caller creates that pointer from an existing array element:

```i
first: *i32 = values[0].&;
increment(first);
```

Read `values[0].&` as "the address of the first slot." Inside `increment`,
`value[0]` means "the storage this pointer points at." The procedure does not
receive a copy of the integer; it receives access to the caller's slot.

After it runs, the first element has changed and the others keep the values from
the loop. That is the point of the lesson: if a procedure should mutate something
the caller already owns, pass a pointer to that storage.

Try this:

- pass `values[2].&` instead of `values[0].&`
- change the array count to 5 and update the loop
- make `increment` add 10 instead of 1

## Lesson 04 - Structs And Enums

`src/lessons/04_structs_and_enums.i` asks how to give names to related fields and
states.

The file starts with two small shapes:

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

`Point` groups two coordinates. `SpriteKind` gives names to the states a sprite
can be in. Neither shape does anything by itself; they are vocabulary for the
next declaration.

`Sprite` nests both ideas:

```i
Sprite: struct = {
    kind: SpriteKind;
    pos: Point;
}
```

Then `main` initializes one sprite by assigning through field paths such as
`s.kind`, `s.pos.x`, and `s.pos.y`. Those paths are intentionally boring. The way
you write into a nested value is the same way you later read from it.

After it runs, you have seen the basic data-modeling move in I: name a few small
shapes, compose them into a bigger shape, then use field paths to work with the
result.

Try this:

- add `Enemy` to `SpriteKind`
- add a `health: i32` field to `Sprite`
- initialize two sprites with different positions

## Lesson 05 - Procedures And Callbacks

`src/lessons/05_procs_and_callbacks.i` asks how behavior can be stored in data.

The file first gives a procedure pointer type a short name:

```i
Op: alias = *proc(a: i32, b: i32)->i32;
```

`Op` is a pointer to a procedure that takes two `i32` values and returns an
`i32`. Once that shape has a name, the rest of the file can use it like any other
type.

The lesson stores operations in an array:

```i
table: [2]Op = {};
table[0] = add;
table[1] = mul;
```

It also stores one operation in a struct:

```i
Adder: struct = {
    call: Op;
}
```

After it runs, the three calls demonstrate the same idea from different angles:
one operation is called through the first table slot, one through the second table
slot, and one through a field on a struct value. The data chooses the behavior.

Try this:

- add a `sub` procedure
- make the table hold three operations
- add a second field to `Adder` for another callback

These lessons are where I starts feeling like a practical systems language:
storage is explicit, names describe shape, and procedures can travel through
data just like other values.

