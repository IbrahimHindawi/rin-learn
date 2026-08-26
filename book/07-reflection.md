# 07 - Reflection And Metaprogramming

ilang's metaprogramming starts with concrete declarations, not runtime magic. The
compiler already knows the names, fields, sizes, enum values, and generic
instantiations in your program. Reflection makes a useful slice of that knowledge
available as ordinary data.

## Lesson 15 - Reflection Metadata

`src/lessons/15_reflection_metadata.i` asks what information the compiler can
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
Payload<>.kind
Payload<>.count
Payload<>.size
Payload<>.variant.fields[0].name
Payload<>.variant.fields[0].type
Payload<>.variant.fields[2].pointer_depth
```

Read `Payload<>` as "the reflected description of `Payload`." The result is not
a special incantation. It is generated data with fields your editor and tools can
reason about.

One record describes every reflected type, whether it is a struct, a union or an
enum. `kind` says which one you have. `count` means fields for a struct and
members for an enum. The part that only one kind has -- a struct's fields, an
enum's values -- lives behind `variant`, so the record stays one shape while the
payload varies.

Asking for the wrong arm is a compile error wherever the compiler can see the
kind, which is every `Type<>`. Writing `Payload<>.variant.values` gets you a
diagnostic, not a wrong answer.

After it runs, the struct has described itself. You can see the type name, how
many fields it has, how large it is, and details for individual fields. That is
the first reflection habit: ask the declaration for facts instead of copying
those facts into a second table.

Try this:

- add a `flags: u32` field to `Payload`
- print `Payload<>.count` again
- inspect the new field's reflected name and type
- try `Payload<>.variant.values[0]` and read the error you get

## Lesson 16 - Reflection Fields

`src/lessons/16_reflection_fields.i` asks how reflection becomes useful when you
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
for (i: u64 = 0; i < Thing<>.count; i += 1) {
    field: *const reflect_field = Thing<>.variant.fields[i].&;
    printfmt("{} : {}\n", field[0].name, field[0].type);
}
```

Before the loop, the field list belongs to the type. During the loop, each index
selects one reflected field record. From that record, the lesson reads the field
name, type, size, and attribute string.

The second loop is the one that matters most. A field's `type` is only a name --
the string `"Inner"` will not get you to `Inner`. `info` is the link: it points
at the record for the field's own type, so a walk can descend instead of stopping
at a string. It is null for anything with no record of its own, like a builtin.

```i
if (field[0].info != null) {
    printfmt("{} -> {} ({} fields)\n",
        field[0].name, field[0].info[0].name, field[0].info[0].count);
}
```

That link is what turns a one-level field listing into a real serialiser or tree
inspector.

After it runs, the output looks like the beginning of a serializer, editor panel,
debug inspector, or save-file mapper. The type was written once, and the loop can
respond to its current fields.

Try this:

- add an attribute to `name`
- add another array field
- print `size` for each field and compare the results
- nest another struct inside `Inner` and follow `info` two levels down

## Lesson 18 - Metaprogramming Shape

`src/lessons/18_metaprogramming_shape.i` asks what happens when generics and
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
Slot_i32_reflect.count
Slot_f32_reflect.name
Slot_f32_reflect.count
```

`Type<>` and the generated `Type_reflect` global are the same thing spelled two
ways, and both are checked the same way: a field name the record does not have is
an error either way.

After it runs, you should see the practical metaprogramming shape: one generic
source definition produced multiple concrete shapes, and those concrete shapes
have metadata of their own.

Try this:

- create a `Slot<bool>`
- print its reflected name
- add another field to `Slot<T>` and confirm every reflected field count changes

## Lesson 17 - One Record For Every Kind

`src/lessons/17_reflection_one_record.i` asks what you can write once that works
for a struct, a union and an enum alike.

The answer is a single procedure that takes the record and never asks what it was
given:

```i
describe: proc(meta: *const reflect)->void = {
    fields: *const reflect_field = reflect_fields(meta);
    values: *const reflect_value = reflect_values(meta);
    ...
}
```

`reflect_fields` and `reflect_values` are the checked way into the variant. They
hand back the arm only when `kind` matches and null otherwise, so a struct passed
to code expecting an enum gets null rather than a pointer reinterpreted as the
wrong type. Inside `describe` the kind is not known until run time -- that is
exactly the case these exist for.

They are also worth reading. Open `std/reflect.i` beside the compiler: every one
of these helpers is written in ilang, in a few lines each, over the same records the
lesson has been printing. Nothing about reflection is hidden in the runtime.

Watch the union in the output. Both of its members report offset zero, because
they share storage. That is why a union reflects as its own kind rather than as a
struct with a flag set: a walker that only understood structs would place those
members one after another and produce output that is quietly wrong rather than
obviously broken.

Watch the enum too. `Empty = -1` round-trips as `-1`, because reflected enum
values are signed.

Try this:

- add a third member to `Word` and confirm it also sits at offset zero
- pass `Slot<>.&` to something expecting fields and see what `reflect_fields`
  returns
- uncomment the wrong-arm line at the bottom and read the compile error

## The Habit

Reflection should remove duplicated bookkeeping. If you find yourself writing a
manual table that repeats a struct's field names, stop and ask whether the type's
metadata already knows the answer.

That is the ilang style this book is aiming for: direct data, explicit storage,
generic reuse, and reflection where repetition would otherwise creep in.
