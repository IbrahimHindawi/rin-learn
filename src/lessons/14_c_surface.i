cinclude "stdio.h"
#define I_LEARN_BONUS 7

// `external` means C already owns the declaration. The ilang compiler can type-check
// calls without emitting another definition for it.
//
// Every C function needs one of these before you can call it. `cinclude` sends
// the header to the C compiler; it does not bring any name into ilang. That is why
// `printf` is declared here too, even though <stdio.h> is included above.
puts: proc[external](text: *const char) -> i32 = {}
printf: proc[external](fmt: *const char, ...) -> i32 = {}

main: proc() -> i32 = {
    puts("this call is checked by ilang and provided by C");
    printf("bonus=%d\n", I_LEARN_BONUS);
    return 0;
}

