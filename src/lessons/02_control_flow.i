cinclude "stdio.h"

Mode: enum = {
    Idle,
    Walk,
    Run,
}

main: proc()->i32 = {
    sum: i32 = 0;

    for (i: i32 = 0; i < 5; i += 1) {
        if (i == 3) {
            continue;
        }
        sum += i;
    }

    mode: Mode = Mode.Run;
    switch (mode) {
        case Mode.Idle: {
            sum += 10;
        }
        case Mode.Walk: {
            sum += 20;
        }
        default: {
            sum += 30;
        }
    }

    printf("sum=%d\n", sum);
    return 0;
}

