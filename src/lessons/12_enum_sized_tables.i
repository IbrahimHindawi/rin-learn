import "std/Print.i"

Stat: enum = {
    Health,
    Stamina,
    Focus,
}

main: proc() -> i32 = {
    // `Stat<>` is the enum's reflection record, and `.count` is how many members
    // it declares. The compiler knows that number once the enum is parsed, so it
    // can size an array with it -- there is no hand-written STAT_COUNT to drift
    // out of step when a member is added.
    values: [Stat<>.count]i32 = {};
    values[Stat.Health] = 100;
    values[Stat.Stamina] = 50;
    values[Stat.Focus] = 25;

    printfmt("stats={} count={}\n", values[Stat.Health] + values[Stat.Focus], Stat<>.count);
    return 0;
}
