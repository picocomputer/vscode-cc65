Documentation:

- [Picocomputer](https://picocomputer.github.io)
- [Examples](https://github.com/picocomputer/examples)
- [cc65](https://cc65.github.io/)

Rules:

- CMake is the build system.
- cc65 is the compiler.
- cc65 int is 16 bits.
- cc65 does not support float, double, or 64-bit int.
- Target platform for cc65 is RP6502.
- Variable declarations must be c89 style.
- Local stack limit is 256 bytes.
- xreg() setting must be done in a single call.
