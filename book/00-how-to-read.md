# 00 - How To Read This

I is a systems language in the C tradition. It keeps C's direct model of memory,
data layout, pointers, procedures, and object-file-oriented compilation, but it
uses a smaller and more regular source syntax.

Each lesson in `src/lessons` is a complete program. Read the comments, compile
the file, then inspect the generated C if something feels mysterious.

Useful commands:

```powershell
C:\devel\i-windows-x64\I.exe compile src\lessons\00_hello_world.i -o build\gen\00_hello_world.c
powershell -ExecutionPolicy Bypass -File scripts\check_all.ps1
```

The generated C is not an implementation detail to be feared. It is part of the
learning loop. I should make source nicer without hiding what kind of program is
being built.

