import "std/Print.i"

// A complete ilang program looks like a small C program, but declarations use
// `name: Type = value` order.
main: proc() -> i32 = {
    printfmt("hello from ilang\n");
    return 0;
}

