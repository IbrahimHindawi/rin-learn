import "std/Print.i"

main: proc()->i32 = {
    print<*const char>("std print says ");
    print<i32>(42);
    print<*const char>("\n");
    return 0;
}

