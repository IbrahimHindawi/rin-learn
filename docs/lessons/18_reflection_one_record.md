# 18 — One record, three kinds

> Structs, unions and enums are all described by the same shape.

## The idea

There is one record type. `.kind` says which sort of type it describes, and
`.variant` is a union whose live arm follows from that: `fields` for a struct or
union, `values` for an enum.

Reading the wrong arm is the mistake this design invites, so the compiler helps:
completion only offers the arm that is live for the kind you have.

## What the lesson shows

- a struct, a union and an enum described side by side
- `.kind` switched on to pick the right arm
- `variant.values` for the enum, with each member's name and number
- a union whose fields all sit at offset 0

## Why this is here

The union at offset 0 is a nice check on lesson 07: reflection tells you the
same thing the layout rules would, and now you can read it at runtime instead of
working it out.

## Before you move on

You can write one proc that prints any type's members, whatever its kind.

---

*Source: [`src/lessons/18_reflection_one_record.rin`](https://github.com/IbrahimHindawi/rin-learn/blob/main/src/lessons/18_reflection_one_record.rin). The file itself
carries "What to notice" and "Try this" sections — read the code first, then come
back here.*
