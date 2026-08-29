# 17 — Reflection: fields

> Walking a struct's members, and the attributes you can attach to them.

## The idea

`T<>.variant.fields` is an array of one record per field: name, type name,
offset, size, and the attribute string you wrote after `@`.

That last part is the interesting one. `id: i32 @ "save,editor"` attaches text to
a field that the compiler carries into the reflection table, where your own code
can read it. Serialisation, editor UI and diffing are all "walk the fields, look
at the tags, do something" -- and none of it needs the compiler to know what
"save" means.

## What the lesson shows

- iterating `fields[i]` up to `.count`
- `.offset` matching what lesson 07 taught you to predict
- attributes read back as a string you can search
- a nested struct field, and reaching its own record through `.info`

## Why this is here

This is the mechanism njinn uses for its editor and its save format. It is also
the strongest argument for reflection existing at all: the alternative is a
hand-maintained table that drifts.

## Before you move on

You can find a field by name and print its offset.

---

*Source: [`src/lessons/17_reflection_fields.rin`](../../src/lessons/17_reflection_fields.rin). The file itself
carries "What to notice" and "Try this" sections — read the code first, then come
back here.*
