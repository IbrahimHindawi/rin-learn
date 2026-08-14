cinclude "stdio.h"
#define I_LEARN_BONUS 7

// `external` means C already owns the declaration. The I compiler can type-check
// calls without emitting another definition for it.
puts: proc(text: *const char)->i32 = { external; }

main: proc()->i32 = {
    puts("this call is checked by I and provided by C");
    printf("bonus=%d\n", I_LEARN_BONUS);
    return 0;
}

