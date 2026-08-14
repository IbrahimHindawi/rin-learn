cinclude "stdio.h"

Op: alias = *proc(a: i32, b: i32)->i32;

Adder: struct = {
    call: Op;
}

add: proc(a: i32, b: i32)->i32 = {
    return a + b;
}

mul: proc(a: i32, b: i32)->i32 = {
    return a * b;
}

main: proc()->i32 = {
    table: [2]Op = {};
    table[0] = add;
    table[1] = mul;

    adder: Adder = {};
    adder.call = add;

    printf("%d %d %d\n", table[0](2, 3), table[1](2, 3), adder.call(10, 5));
    return 0;
}

