import "std/Print.i"

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

    // Each instantiation gets its own record under its monomorphised name, so
    // Slot<i32> and Slot<f32> reflect separately rather than sharing one entry
    // for the template. `Type<>` and the generated `Type_reflect` global are
    // the same thing; both are checked the same way.
    printfmt("{} {} {} {}\n",
        Slot_i32_reflect.name,
        Slot_i32_reflect.count,
        Slot_f32_reflect.name,
        Slot_f32_reflect.count);

    if (health.occupied and !empty.occupied) {
        return health.value;
    }
    return 0;
}

