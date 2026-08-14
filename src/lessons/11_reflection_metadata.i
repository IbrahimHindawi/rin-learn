cinclude "stdio.h"

Payload: struct = {
    id: i32;
    weight: f32;
    label: *const char;
}

main: proc()->i32 = {
    printf("type=%s fields=%llu size=%llu\n", Payload<>.name, Payload<>.field_count, Payload<>.size);
    printf("field0=%s:%s\n", Payload<>.fields[0].name, Payload<>.fields[0].type);
    printf("field2=%s ptr_depth=%llu\n", Payload<>.fields[2].name, Payload<>.fields[2].pointer_depth);
    return 0;
}

