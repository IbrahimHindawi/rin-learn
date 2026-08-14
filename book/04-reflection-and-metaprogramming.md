# 04 - Reflection And Metaprogramming

I's metaprogramming starts with concrete declarations, not runtime magic. The
compiler already knows the names, fields, sizes, enum values, and generic
instantiations in your program. Reflection makes a useful slice of that knowledge
available as ordinary data.

## Lesson 11 - Reflection Metadata

`src/lessons/11_reflection_metadata.i` asks what information the compiler can
produce about a type you already wrote.

The data shape is ordinary:

```i
Payload: struct = {
    id: i32;
    weight: f32;
    label: *const char;
}
```

Then the lesson asks for metadata with the short reflection form:

```i
Payload<>.name
Payload<>.field_count
Payload<>.size
Payload<>.fields[0].name
Payload<>.fields[0].type
Payload<>.fields[2].pointer_depth
```

Read `Payload<>` as "the reflected description of `Payload`." The result is not
a special incantation. It is generated data with fields your editor and tools can
reason about.

After it runs, the struct has described itself. You can see the type name, how
many fields it has, how large it is, and details for individual fields. That is
the first reflection habit: ask the declaration for facts instead of copying
those facts into a second table.

Try this:

- add a `flags: u32` field to `Payload`
- print `Payload<>.field_count` again
- inspect the new field's reflected name and type

## Lesson 12 - Reflection Fields

`src/lessons/12_reflection_fields.i` asks how reflection becomes useful when you
walk across fields instead of inspecting one fixed field.

The struct includes an attribute on one field:

```i
Thing: struct = {
    id: i32 @ "save,editor";
    name: *const char;
    scores: [3]i32;
}
```

The loop is the heart of the lesson:

```i
for (i: u64 = 0; i < Thing<>.field_count; i += 1) {
    printf("%s : %s\n", Thing<>.fields[i].name, Thing<>.fields[i].type);
}
```

Before the loop, the field list belongs to the type. During the loop, each index
selects one reflected field record. From that record, the lesson reads the field
name, type, size, and attribute string.

After it runs, the output looks like the beginning of a serializer, editor panel,
debug inspector, or save-file mapper. The type was written once, and the loop can
respond to its current fields.

Try this:

- add an attribute to `name`
- add another array field
- print `size` for each field and compare the results

## Lesson 13 - Metaprogramming Shape

`src/lessons/13_metaprogramming_shape.i` asks what happens when generics and
reflection meet.

The generic type is a tiny optional-slot shape:

```i
Slot: struct<T> = {
    value: T;
    occupied: bool;
}
```

The helper procedures construct either a filled slot or an empty one:

```i
Slot<T>some: proc<T>(value: T)->Slot<T> = { ... }
Slot<T>none: proc<T>()->Slot<T> = { ... }
```

Using `Slot<i32>` and `Slot<f32>` creates concrete instantiations. The lesson then
prints their reflected concrete names and field counts:

```i
Slot_i32_reflect.name
Slot_i32_reflect.field_count
Slot_f32_reflect.name
Slot_f32_reflect.field_count
```

After it runs, you should see the practical metaprogramming shape: one generic
source definition produced multiple concrete shapes, and those concrete shapes
have metadata of their own.

Try this:

- create a `Slot<bool>`
- print its reflected name
- add another field to `Slot<T>` and confirm every reflected field count changes

## The Habit

Reflection should remove duplicated bookkeeping. If you find yourself writing a
manual table that repeats a struct's field names, stop and ask whether the type's
metadata already knows the answer.

That is the I style this book is aiming for: direct data, explicit storage,
generic reuse, and reflection where repetition would otherwise creep in.
