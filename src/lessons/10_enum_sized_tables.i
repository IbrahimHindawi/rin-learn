cinclude "stdio.h"

Stat: enum = {
    Health,
    Stamina,
    Focus,
}

main: proc()->i32 = {
    values: [Stat<>.value_count]i32 = {};
    values[Stat.Health] = 100;
    values[Stat.Stamina] = 50;
    values[Stat.Focus] = 25;

    printf("stats=%d count=%llu\n", values[Stat.Health] + values[Stat.Focus], Stat<>.value_count);
    return 0;
}

