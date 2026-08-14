cinclude "stdio.h"

Slot: struct<T> = {
    value: T;
    occupied: bool;
}

Slot<T>some: proc<T>(value: T)->Slot<T> = {
    slot: Slot<T> = {};
    slot.value = value;
    slot.occupied = 1;
    return slot;
}

Slot<T>none: proc<T>()->Slot<T> = {
    return {};
}

main: proc()->i32 = {
    health: Slot<i32> = Slot<i32>some(10);
    empty: Slot<f32> = Slot<f32>none();

    printf("%s %llu %s %llu\n",
        Slot_i32_reflect.name,
        Slot_i32_reflect.field_count,
        Slot_f32_reflect.name,
        Slot_f32_reflect.field_count);

    if (health.occupied and !empty.occupied) {
        return health.value;
    }
    return 0;
}

