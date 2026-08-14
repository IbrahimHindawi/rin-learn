# 02 - I In Small Steps

I declarations use one shape:

```i
name: Type = value;
name: proc(arg: Type)->Return = { ... }
Name: struct = { field: Type; }
```

Variables must say what storage state they want:

```i
zeroed: Payload = {};
uninitialized: [256]u8 = ?;
```

Bodies are blocks. Switch cases are blocks too, so each case has its own scope
and does not accidentally fall through.

Imports are source-level dependencies. `import "std/Print.i"` finds the `std`
folder beside the installed `I.exe`. That is what lets a normal project use the
packaged compiler without reaching back into the compiler source tree.

