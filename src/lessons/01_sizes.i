import "std/Print.i"

// Every value your program holds occupies a fixed number of bytes, and you
// choose how many. That choice is the first low-level decision there is.
//
// In a language with one `int`, the size is picked for you and you stop
// thinking about it. Here the size is written into the name: i32 is a 32-bit
// signed integer, which is 4 bytes. Nothing is hidden.
//
// Run this and read the numbers before reading the explanation below it.

main: proc() -> i32 = {
    printfmt("i8   {} byte    u8   {} byte\n", sizeof(i8), sizeof(u8));
    printfmt("i16  {} bytes   u16  {} bytes\n", sizeof(i16), sizeof(u16));
    printfmt("i32  {} bytes   u32  {} bytes\n", sizeof(i32), sizeof(u32));
    printfmt("i64  {} bytes   u64  {} bytes\n", sizeof(i64), sizeof(u64));
    printfmt("f32  {} bytes   f64  {} bytes\n", sizeof(f32), sizeof(f64));
    printfmt("b32  {} bytes   c8   {} byte\n", sizeof(b32), sizeof(c8));

    // A pointer holds an address, and an address is the same size whatever it
    // points at. On this machine that is 8 bytes, because it is 64-bit.
    printfmt("*i32 {} bytes   *f64 {} bytes\n", sizeof(*i32), sizeof(*f64));

    // usize is "big enough to count any object in memory", which is why it is
    // the type of a size or a length. Notice it matches the pointer size.
    printfmt("usize {} bytes\n", sizeof(usize));

    // Size is not decoration. It decides the range of values that fit.
    // An i8 holds -128 to 127. Put 200 in one and the top bits are gone.
    small: i8 = cast(200, i8);
    printfmt("200 stored in an i8 reads back as {}\n", cast(small, i32));

    return 0;
}

// What to notice
//
// 1. The name tells you the size. You never have to look it up, and it does
//    not change when you move to another machine. `int` in C does.
//
// 2. Pointers are all one size, because they all hold the same thing: a
//    number that identifies a location. What lives there is a matter of type,
//    not of storage.
//
// 3. The i8 line is not a trick question. 200 does not fit in 8 signed bits,
//    so the bits that did not fit were discarded. The machine did not warn
//    you and neither did the compiler -- this language keeps C's bargain. The
//    protection is that you chose `i8` deliberately.
//
// Try this
//
// - change `small` to i16 and run again; the value survives, because 200 fits
// - print `sizeof(i32) * 8` to see the bit count you already knew
// - add `sizeof(*const c8)` and confirm const changes nothing about storage
