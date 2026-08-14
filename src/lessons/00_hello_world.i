cinclude "stdio.h"

// A complete I program looks like a small C program, but declarations use
// `name: Type = value` order.
main: proc()->i32 = {
    printf("hello from I\n");
    return 0;
}

