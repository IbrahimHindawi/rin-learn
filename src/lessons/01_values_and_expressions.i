cinclude "stdio.h"

main: proc()->i32 = {
    count: i32 = 6;
    scale: f32 = 2.5f;
    total: i32 = count * 3 + 1;
    ratio: f32 = cast(total, f32) / scale;

    printf("count=%d total=%d ratio=%f\n", count, total, cast(ratio, f64));
    return 0;
}

