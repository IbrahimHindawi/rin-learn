# 04 - Generics And Reflection

I's metaprogramming starts with concrete code generation, not runtime magic.

A generic type:

```i
Box: struct<T> = { value: T; }
```

becomes concrete when used:

```i
box: Box<i32> = {};
```

Reflection is generated metadata about concrete structs and enums. For a type
named `Payload`, the compiler emits `Payload_reflect`, and I source can use the
short form:

```i
Payload<>.name
Payload<>.field_count
Payload<>.fields[0].name
```

That metadata is ordinary data. The point is not to make the language mystical;
the point is to remove handwritten tables that drift away from the structs they
describe.

