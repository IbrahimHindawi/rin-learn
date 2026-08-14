# 04 - Reflection And Metaprogramming

I's metaprogramming starts with concrete declarations, not runtime magic. The
compiler already knows the names, fields, sizes, enum values, and generic
instantiations in your program. Reflection makes a useful slice of that knowledge
available as ordinary data.

## Lesson 11 - Reflection Metadata

`src/lessons/11_reflection_metadata.i` defines a plain struct:

```i
Payload: struct = {
    id: i32;
    weight: f32;
    label: *const char;
}
```

Then it asks for metadata with the short reflection form:

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

Try this:

- add a `flags: u32` field to `Payload`
- print `Payload<>.field_count` again
- inspect the new field's reflected name and type

## Lesson 12 - Reflection Fields

`src/lessons/12_reflection_fields.i` turns metadata into a loop:

```i
for (i: u64 = 0; i < Thing<>.field_count; i += 1) {
    printf("%s : %s\n", Thing<>.fields[i].name, Thing<>.fields[i].type);
}
```

The struct also has an attribute string:

```i
id: i32 @ "save,editor";
```

That small annotation is enough to show the pattern. You can attach policy to a
field once, then let reflection-powered code read it later. Serialization, editor
panels, debug dumps, and validation tables all want this kind of shape.

Try this:

- add an attribute to `name`
- add another array field
- print `size` for each field and compare the results

## Lesson 13 - Metaprogramming Shape

`src/lessons/13_metaprogramming_shape.i` combines generics and reflection:

```i
Slot: struct<T> = {
    value: T;
    occupied: bool;
}
```

Using `Slot<i32>` and `Slot<f32>` creates concrete instantiations. The lesson then
prints their reflected concrete names and field counts:

```i
Slot_i32_reflect.name
Slot_i32_reflect.field_count
Slot_f32_reflect.name
Slot_f32_reflect.field_count
```

This is the practical metaprogramming lesson: one generic source definition can
produce multiple concrete shapes, and those concrete shapes can have metadata of
their own.

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
