# RP6502 Project Template

Scaffolding for a new Picocomputer 6502 software project. It builds with
either 6502 compiler, cc65 or llvm-mos, and switching between them is one
setting. Three "Hello, world!" examples are included to start from:

 * `src/main.c` — C, and builds with either compiler.
 * `src/main-cc65.s` — assembly for cc65, which uses the ca65 syntax.
 * `src/main-llvm-mos.s` — the same program in llvm-mos assembly.

Make sure `CMakeLists.txt` points to the one you want, then delete the others.
The two assembly files pick up where the C runtime leaves off, so they read
alike; only the assembler directives differ.

### Requirements:
 * CMake 3.21 or newer
 * Python 3
 * git
 * A build tool CMake can drive — GNU Make or Ninja
 * At least one 6502 compiler:
   [CC65](https://cc65.github.io/getting-started.html) and/or
   [LLVM-MOS](https://llvm-mos.org/wiki/Welcome). Install both if you want to
   try both; nothing here makes you choose once.

VS Code is strongly recommended and this project is set up for it, but it is
not required. Everything works from a command line and any editor, which the
sections below cover.

Linux:
```bash
$ sudo apt install cmake python3 git build-essential
```
CC65 needs a source build. LLVM-MOS has its own installer.

Windows:
 * `winget install -e --id Git.Git`
 * `winget install -e --id Kitware.CMake`
 * `winget install -e --id GnuWin32.Make`
   Add `C:\Program Files (x86)\GnuWin32\bin` to your PATH.
 * The current snapshot of [CC65](https://cc65.github.io/getting-started.html) -
   Do not skip the step about adding the `bin` directory to your PATH.
   And/or an install of [LLVM-MOS](https://llvm-mos.org/wiki/Welcome).
 * Install Python by typing `python3` in a command prompt, which will launch
   the Microsoft Store where you can start the installation. If Python runs,
   this has already been done - exit Python with Ctrl-Z plus Enter.
 * For VS Code: `winget install -e --id Microsoft.VisualStudioCode`

### Getting Started:
Go to the [GitHub template](https://github.com/picocomputer/vscode-cc65) and
select "Use this template" then "Create a new repository". GitHub will create
a clean project for you to start with. Then you can clone the repository.

```bash
$ git clone [path_to_github]
$ cd [to_where_it_cloned]
```

### Choosing a compiler and building:
The choice is a CMake preset. There is a Debug and a Release of each compiler,
building into its own directory under `build/`, so you can switch back and
forth without a rebuild from scratch. Debugging needs a Debug build, because
that is the one carrying the information a debugger uses to stop on a line of
your source.

```bash
$ cmake --list-presets
$ cmake --preset cc65/Debug
$ cmake --build --preset cc65/Debug
```

That leaves a ROM at `build/cc65/debug/hello.rp6502`.

In VS Code, open the folder and install the recommended extensions when
prompted. From the CMake side panel, select Configure:cc65/Debug and press
Build instead of typing the commands.

The first configure fails until a compiler is chosen. If your editor does not
drive presets, name one on the command line instead:

```bash
$ cmake -B build -DCC65_TARGET_SYSTEM=rp6502 -DCMAKE_BUILD_TYPE=Debug
$ cmake --build build
```

`LLVM_MOS_PLATFORM=rp6502` selects the other compiler the same way.

### Running it:
`tools/rp6502.py` sends a ROM to a Picocomputer and gives you its console. It
needs nothing but Python.

```bash
$ python3 tools/rp6502.py run build/cc65/debug/hello.rp6502
```

That uploads the ROM, starts it, and attaches a terminal. Ctrl-A then X exits,
Ctrl-A then B sends a break. Other commands:

```bash
$ python3 tools/rp6502.py term                 # console terminal, nothing else
$ python3 tools/rp6502.py upload file...       # copy files to USB storage
$ python3 tools/rp6502.py basic prog.bas       # run a BASIC program
$ python3 tools/rp6502.py --help
```

The device defaults to the USB serial port where the Picocomputer usually
mounts: `/dev/ttyACM0` on Linux, `/dev/cu.usbmodem*` on macOS, `COM1` on
Windows. Override it with `-d`, and connect over telnet by giving a hostname
plus the passkey:

```bash
$ python3 tools/rp6502.py -d /dev/ttyUSB0 run build/cc65/debug/hello.rp6502
$ python3 tools/rp6502.py -d picocomputer.local -k mykey term
```

To run without hardware, pass the ROM to the emulator:

```bash
$ rp6502-emu build/cc65/debug/hello.rp6502
```

The emulator is a separate download; see the Picocomputer documentation.

### Debugging:
The emulator is a DAP debug adapter, so any editor that speaks the Debug
Adapter Protocol can do source-level debugging of 6502 code. It finds the
debug information beside the ROM, so `program` is the only thing your launch
configuration has to name.

```bash
$ rp6502-emu --dap
```

In VS Code this is already wired up. "Start Debugging" (F5) offers two
configurations:

 * **RP6502 (Emulator)** is the default. It builds your project and runs it with
   source-level debugging in the rp6502 emulator.
 * **RP6502 (Hardware)** builds your project and runs it on a Picocomputer 6502.
   Connect with telnet or a USB cable plugged into the RP6502-VGA USB port.

Both read `.rp6502` in the project root, which is created the first time you
"Start Debugging" and is ignored by git. It holds the same settings the
command line takes as flags:

```ini
[RP6502][Launch]
emulator = rp6502-emu
device = /dev/ttyACM0
key =
workdir =
args =
term = True
```

For the emulator, `emulator` must point to the `rp6502-emu` executable; a bare
name is searched on your PATH. For hardware, set `device` to the serial port.
If you get a Python error about the communications device not being found,
that is the setting to edit. You may also connect over telnet by giving a
hostname for the device and setting the key.

Once the program is running, a debug console becomes available on the terminal
tab. It will say "Python Debug Console" because the rp6502.py tool is Python.

Edit `CMakeLists.txt` to add new source and asset files. From here on, it's
standard C/C++/assembly development for the 6502 platform.

### The tools directory:
`tools/` holds the ROM packager, the CMake commands your project calls, and
the cc65 toolchain file. A new project starts with only a small script that
goes and gets them from
[picocomputer/rp6502](https://github.com/picocomputer/rp6502) on the first
configure. They are ordinary files in your repository after that, so commit
them along with everything else.

To pull down the current versions:

```bash
$ cmake -P tools/CMakeLists.txt
```

VS Code has this as the "RP6502: update tools" task. Either way the result is
a diff you can read before you commit it. Nothing is fetched behind your back:
configuring a project that already has its tools never goes to the network,
and a tool you delete stays deleted.

### Updating an older project:
Projects made before this template merged cc65 and llvm-mos have their compiler
wired into the top of `CMakeLists.txt`, and a `tools/` that predates any of
this. Start by copying this template's `tools/CMakeLists.txt` over yours — it
is the small script that fetches the rest, and it replaces itself on the next
configure. Then replace everything above `project()` with:

```cmake
cmake_minimum_required(VERSION 3.21)

include(${CMAKE_CURRENT_LIST_DIR}/tools/CMakeLists.txt)
```

Delete the `add_subdirectory(tools)` line, which the `include()` replaces, and
`tools/rp6502.cmake`, which is now `tools/cc65.cmake`. Copy
`CMakePresets.json` from this template as well — that is where the compiler is
chosen now. Old projects called `rp6502_executable()` with the address their
compiler happened to use; `DATA default RESET default` works under both.

### Documentation:
 * [Picocomputer](https://picocomputer.github.io)
 * [CC65](https://cc65.github.io/)
 * [LLVM-MOS](https://llvm-mos.org/)
