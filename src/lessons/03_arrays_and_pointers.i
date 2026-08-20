import "std/Print.i"

increment: proc(value: *i32)->void = {
    value[0] += 1;
}

main: proc()->i32 = {
    values: [4]i32 = {};
    for (i: i32 = 0; i < 4; i += 1) {
        values[i] = i * 10;
    }

    first: *i32 = values[0].&;
    increment(first);

    printfmt("{} {} {} {}\n", values[0], values[1], values[2], values[3]);
    return 0;
}

