cinclude "stdio.h"

Box: struct<T> = {
    value: T;
}

Box<T>make: proc<T>(value: T)->Box<T> = {
    box: Box<T> = {};
    box.value = value;
    return box;
}

Box<T>unwrap: proc<T>(box: Box<T>)->T = {
    return box.value;
}

main: proc()->i32 = {
    a: Box<i32> = Box<i32>make(12);
    b: Box<f32> = Box<f32>make(3.5f);

    printf("%d %f\n", Box<i32>unwrap(a), cast(Box<f32>unwrap(b), f64));
    return 0;
}

