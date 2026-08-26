# 05 - Managing Memory, And Code The Compiler Writes

Lessons 10 through 12.

## Lesson 10 - Memory you are responsible for

`src/lessons/10_arenas_and_array.i`

```i
arena: memops_arena = {};
memops_arena_initialize(arena.&);

values: Array<i32> = Array<i32>reserve(arena.&, 5);
```

An arena is a large block of memory obtained once, handed out in pieces, and
released all at once. Asking for a piece is a pointer bump: return the current
position, then move it forward. That is the whole allocator.

It is worth understanding why this shape is common in systems code rather than
the `malloc`/`free` pair you may expect.

**Allocation is nearly free.** A bump is an addition. `malloc` has to search a
structure of free blocks, and may take a lock.

**There is no individual free.** You do not release one `Array`; you release the
arena and everything in it goes at once. That sounds like a limitation and is
usually the point -- most programs have natural moments where a whole batch of
work is finished. A frame ends. A request completes. A file finishes parsing.

**It removes a class of bug by removing the decision.** You cannot free
something twice, or free it and keep using it, if there is no per-object free.
What you can still do is keep a pointer past the arena's own lifetime, which is
lesson 09's mistake wearing different clothes.

**Everything in it is contiguous**, so it inherits lesson 05's cache behaviour.

`Array<i32>` here is a pointer plus a length, pointing into the arena. It does
not own the memory and does not free anything.

## Lesson 11 - A generic is a stamp

`src/lessons/11_generics_box.i`

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

## Lesson 12 - Letting the compiler size a table

`src/lessons/12_enum_sized_tables.i`

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
