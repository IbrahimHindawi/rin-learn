# 00 - How To Read This

I is a small systems language with a deliberately regular source shape. The
lessons in this repository are not a reference manual. They are a path of tiny,
runnable programs that build one habit at a time.

Each file in `src/lessons` is complete. Open the lesson, read the comments,
compile it, then change one line and compile again. The best way to learn I is to
keep the loop short enough that the compiler can answer your question.

Useful command:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check_all.ps1
```

Read the book in order, but treat the lesson files as the real source of truth.
If a chapter describes a pattern, find that pattern in the matching `.i` file and
try a small variation.

The one intentional wrinkle is lesson 06. It teaches the outside-language
boundary, so the book explains it in the final chapter after the I-first ideas
are already in place.
