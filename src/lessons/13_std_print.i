import "std/Print.i"

Color: enum = {
    Red,
    Green,
}

// `print<T>` is one overload per type, and you can add your own. printfmt finds
// this the same way it finds the built-in ones.
print: proc<Color>(c: Color) -> void = {
    if (c == Color.Red) {
        print_cstr("red");
    } else {
        print_cstr("green");
    }
}

main: proc() -> i32 = {
    count: i32 = 42;
    ratio: f32 = 0.5f;
    name: *const char = "std print";

    // The long way: one call per piece, picking the overload by hand.
    print<*const char>("std print says ");
    print<i32>(count);
    print<*const char>("\n");

    // The short way. Each `{}` takes the next argument and prints it with the
    // `print<T>` for that argument's type -- so there is no format letter to get
    // wrong, and no cast to f64 the way a C printf would need for a f32.
    printfmt("{} says {} and {}\n", name, count, ratio);

    // Including your own types, without printfmt knowing anything about them.
    printfmt("color is {}\n", Color.Green);

    // Both of these are resolved while compiling. `{}` never exists at run time:
    // the compiler splits the string, works out each argument's type, and emits
    // a single printf where it can. Look in build/gen to see what came out.
    printfmt("{} + {} = {}\n", count, count, count + count);
    return 0;
}
