cinclude "stdio.h"

Point: struct = {
    x: f32;
    y: f32;
}

SpriteKind: enum = {
    Player,
    Pickup,
    Door,
}

Sprite: struct = {
    kind: SpriteKind;
    pos: Point;
}

main: proc()->i32 = {
    s: Sprite = {};
    s.kind = SpriteKind.Player;
    s.pos.x = 3.0f;
    s.pos.y = 4.0f;

    printf("sprite kind=%d pos=(%f,%f)\n", cast(s.kind, i32), cast(s.pos.x, f64), cast(s.pos.y, f64));
    return 0;
}

