# Installing

> You need two things: the rin compiler, and a C compiler for it to hand its
> output to.

## 1. Get the compiler

The packaged toolchain is a directory containing four things:

    rin-windows-x64/
        rin.exe          the compiler
        rinbind.exe      generates rin declarations from a C header
        libclang.dll     used by rinbind
        std/             the standard library, as rin source

**`std` must sit beside `rin.exe`.** The compiler resolves `import "std/..."`
relative to its own location, and refuses to start if it cannot find it — a
missing `std` is a broken install, and saying so once is better than one
confusing error per import.

Put the directory wherever you like, then either add it to `PATH` or point
`RIN_HOME` at it:

    setx RIN_HOME C:\devel\rin-windows-x64

Check it:

    rin --version

If that prints a version, the compiler is installed.

## 2. Get a C compiler

rin emits C, so something has to compile it. Any of these works:

- **clang-cl** — the default, and what the lessons are tested against
- **clang**
- **Microsoft C compiler `cl.exe`** — the whole lesson suite is tested against this too

If you have Visual Studio Build Tools or the Clang toolchain installed, you already have one.

## 3. Run a lesson

Two steps, because there are two compilers:

    rin compile src/lessons/00_hello_world.rin -o build/hello.c --header build/hello.h
    clang build/hello.c -I %RIN_HOME% -I %RIN_HOME%\std -o build/hello.exe
    build\hello.exe

The two `-I` flags are how the C compiler finds `core.h` and `reflect.h`, which
live beside the compiler along with `std`.

## 4. Or let the script do it

To build and run all twenty lessons at once:

    powershell -ExecutionPolicy Bypass -File scripts/check_all.ps1

It finds the compiler through `RIN_HOME`, then `PATH`, then the default
location, compiles every lesson, links it, runs it, and reports.

## 5. Or use `rin build`

For a project of your own, describe the build once in a `build.rin` and let the
compiler drive cmake:

    build_name:  ^const char = "hello";
    build_entry: ^const char = "src/main.rin";

Then:

    rin build

which transpiles, generates a `CMakeLists.txt` and runs cmake and ninja. This
repository has one that builds all twenty lessons as separate programs.

## Building the compiler from source

Only needed if you are working on rin itself. It wants cmake, ninja and
clang-cl, then:

    python bunyan.py build

which builds the compiler, copies `std` next to it, and packages the result.

## If something goes wrong

**`no input files`** — `rin` with nothing to do says this, like any compiler.
Give it a file.

**`the compiler cannot find its own std`** — `std/` is not beside `rin.exe`.
Re-copy it, or pass `--no-std` if you genuinely mean to compile without it.

**`a std directory next to the source shadows the compiler's own`** — you have a
folder called `std` next to the file you are compiling, and its contents differ
from the shipped one. Rename it.

**Missing `core.h`** from the C compiler — the `-I` flags are wrong. They must
point at the directory holding `rin.exe`, and at its `std` subdirectory.
