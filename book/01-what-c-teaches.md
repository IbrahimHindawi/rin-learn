# 01 - What C Teaches

C's durable ideas are simple:

- memory is bytes
- values live somewhere
- addresses can be passed around
- arrays are contiguous
- structs are layout
- enums give names to integers
- functions are symbols with calling conventions
- source files compile into pieces that link

Those ideas matter more than C's exact declaration syntax.

I keeps the same physical model. A pointer in I is still a pointer. A struct is
still data layout. An imported C header still matters. The difference is that I
tries to make common declarations, generics, diagnostics, and reflection explicit
enough for tools to understand.

When a lesson says "this is a C idea", it means the idea is about the machine or
the C ABI, not about copying every quirk of C's syntax.

