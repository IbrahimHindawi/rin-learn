import "std/Array.i"
import "std/memops.i"
cinclude "stdio.h"

main: proc()->i32 = {
    arena: memops_arena = {};
    memops_arena_initialize(arena.&);

    values: Array<i32> = Array<i32>reserve(arena.&, 5);
    for (i: u64 = 0; i < values.length; i += 1) {
        values.data[i] = cast(i * i, i32);
    }

    printf("%d %d %d\n", values.data[0], values.data[2], values.data[4]);
    return 0;
}

