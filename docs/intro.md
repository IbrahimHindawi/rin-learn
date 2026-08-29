# What rin is

> A small systems language that compiles to C, for people who want to know what
> the machine is doing.

## The shape of it

rin is a language in the C family with the parts of C that hurt taken out and
almost nothing added. It compiles to readable C, which your existing C compiler
then turns into a binary — so it runs everywhere C runs, links against any C
library, and needs no runtime of its own.

Everything is declared the same way, name first:

    count:  i32   = 6;
    Point:  struct = { x: f32; y: f32; }
    main:   proc() -> i32 = { return 0; }

That order never changes. C puts the type first and wraps the name in declarator
syntax nobody reads left to right; rin does not.

## What it does differently

**Sizes are in the names.** `i32` is a signed 32-bit integer, on every machine,
for ever. There is no `int` whose width depends on where you compiled it, and
nothing to look up.

**Conversions are written down.** Mixing an integer and a float needs a `cast`,
at the place it happens. A silent conversion is a decision the compiler made
while you were not looking.

**Order does not matter.** A type or proc may be used before it is declared. No
forward declarations, no header discipline, no include order to get right.

**Memory is arenas.** You ask once for a block, hand out pieces, and release the
whole thing at once. Most memory in a real program shares a lifetime with some
phase — a frame, a level load, a parse — and an arena says so out loud.

**Generics and reflection, no macros.** One definition instantiated per type,
resolved while compiling, and a record describing every type that anything asks
about. There is no macro system and no compile-time execution; that is the whole
metaprogramming budget, deliberately.

**No methods.** Not now and not later. Data is data, procs are procs, and a proc
pointer in a struct is the whole of what dispatch needs.

## What it does not do

It does not manage memory for you, check your indices, or stop you storing 200
in an `i8`. It keeps C's bargain: the machine does exactly what you asked. The
protection is that you wrote the type deliberately, and that the compiler
refuses the mistakes it genuinely can catch — mismatched arities, silent
conversions, two enums compared to each other, a `switch` that stopped covering
its enum.

## Is it real

The compiler is about 17,000 lines of C with a suite of several hundred
discriminating checks. The largest program written in rin is a 3D engine of
roughly 25,000 lines with a D3D11 renderer, which builds with zero warnings and
uses no C string functions at all.

Debug information points at your `.rin` files, not the generated C — you step
through rin in a debugger, and the machine-code line tables name your source.

## How to read these lessons

Twenty short programs, in order. Each one compiles, runs, and teaches one thing.
Read the source first — the files carry their own commentary, including a "What
to notice" and a "Try this" at the bottom — then read the page here for the
framing.

The order matters. It follows the arc K&R uses: write a whole program, then
types and sizes, then control flow, then procs, and only then pointers. You
cannot see why an address is worth passing until you have watched a copy fail to
come back.
