import "std/Print.i"

main: proc() -> i32 = {
    count: i32 = 6;
    scale: f32 = 2.5f;
    total: i32 = count * 3 + 1;
    ratio: f32 = cast(total, f32) / scale;

    printfmt("count={} total={} ratio={}\n", count, total, ratio);
    return 0;
}

