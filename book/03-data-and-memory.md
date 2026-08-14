# 03 - Data And Memory

The early lessons are about data shape.

Use fixed arrays when the count is part of the type:

```i
samples: [4]i32 = {};
```

Use pointers when a procedure should operate on existing storage:

```i
value: i32 = 3;
ptr: *i32 = value.&;
ptr[0] += 1;
```

Use structs when fields belong together:

```i
Point: struct = { x: f32; y: f32; }
```

Use enums when a value should be one of a named set:

```i
Mode: enum = { Idle, Run, Sleep }
```

These are C ideas with I syntax. The lesson programs keep them small on purpose.

