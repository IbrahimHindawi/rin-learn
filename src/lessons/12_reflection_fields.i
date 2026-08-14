cinclude "stdio.h"

Thing: struct = {
    id: i32 @ "save,editor";
    name: *const char;
    scores: [3]i32;
}

main: proc()->i32 = {
    printf("%s has %llu reflected fields\n", Thing<>.name, Thing<>.field_count);
    for (i: u64 = 0; i < Thing<>.field_count; i += 1) {
        printf("  %s : %s size=%llu attrs=%s\n",
            Thing<>.fields[i].name,
            Thing<>.fields[i].type,
            Thing<>.fields[i].size,
            Thing<>.fields[i].attrs);
    }
    return 0;
}

