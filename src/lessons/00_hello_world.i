import "std/Print.i"

// A complete I program looks like a small C program, but declarations use
// `name: Type = value` order.
main: proc()->i32 = {
    printfmt("hello from I\n");
    return 0;
}

