# RP6502 VS Code Scaffolding

This provides scaffolding for a new Picocomputer 6502 software project. It
builds with either 6502 compiler, cc65 or llvm-mos, and switching between them
is a menu pick. Both C and assembly examples of "Hello, world!" are included.
Make sure `CMakeLists.txt` points to your choice of `main.c` or `main.s`, then
delete the one you aren't using. The assembly example is ca65 syntax, so it is
for cc65 only.

### Tools Install:

You need VS Code, CMake, Python, git, and at least one 6502 compiler. Install
both compilers if you want to try both; nothing here makes you choose once.

Linux:
 * [VS Code](https://code.visualstudio.com/) - This has its own installer.
 * `sudo apt install cmake python3 git build-essential`
 * A source build of [CC65](https://cc65.github.io/getting-started.html),
   and/or an install of [LLVM-MOS](https://llvm-mos.org/wiki/Welcome).

Windows:
 * `winget install -e --id Microsoft.VisualStudioCode`
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

LLVM-MOS must be in your PATH. However, this may conflict with other LLVM
installations, like the one that comes with your operating system. In that
case, you can adjust the path for only CMake with a VS Code setting. Add a
`cmake.environment` setting to `.vscode/settings.json`, adjusting the path
for where you installed LLVM-MOS.
```json
    "cmake.environment": {
        "PATH": "~/llvm-mos/bin:${env:PATH}"
    },
```

### Getting Started:
Go to the [GitHub template](https://github.com/picocomputer/vscode-cc65) and
select "Use this template" then "Create a new repository". GitHub will create
a clean project for you to start with. Then you can clone the repository and
open the files.

```bash
$ git clone [path_to_github]
$ cd [to_where_it_cloned]
$ code .
```

Install the recommended extensions when VS Code prompts you, choosing the
default or obvious choice for any other prompts. The tools we use in VS Code
are constantly improving and have their own documentation. The full
documentation for the CMake plugin is here:
https://github.com/microsoft/vscode-cmake-tools/blob/main/docs/README.md

### Choosing a compiler:
Pick `cc65/Debug` or `llvm-mos/Debug` from the CMake status bar, at the bottom
of the VS Code window. Each builds into its own directory under `build/`, so
you can switch back and forth without a rebuild from scratch. There is a
Release of each for the ROM you hand to someone else; debugging needs a Debug
build, because that is the one carrying the information F5 uses to stop on a
line of your source. From a command line:

```bash
$ cmake --list-presets
$ cmake --preset cc65/Debug
$ cmake --build --preset cc65/Debug
```

The first configure fails until a compiler is chosen. If you would rather fix
the choice in the project than pick it every time, uncomment one line near the
top of `CMakeLists.txt`:

```cmake
#set(CC65_TARGET_SYSTEM rp6502)
#set(LLVM_MOS_PLATFORM rp6502)
```

### Running and debugging:
"Start Debugging" (F5) offers two launch configurations:

 * **RP6502 (Emulator)** is the default. It builds your project and runs it with
   source-level debugging in the rp6502 emulator.
 * **RP6502 (Hardware)** builds your project and runs it on a Picocomputer 6502.
   Connect with telnet or a USB cable plugged into the RP6502-VGA USB port.

Both read `.rp6502` in the project root. This file is created the first time you
"Start Debugging" and is ignored by git.

For the emulator, the `emulator` setting must point to the `rp6502-emu`
executable (a bare name is searched on your PATH).

For hardware, set `device` to the serial port. If you get a Python error about
the communications device not being found, edit `device` in `.rp6502`. You may
also connect over telnet by instead providing a hostname for the device and
setting the key.

Once the program is running, a debug console becomes available on the terminal
tab. It will say "Python Debug Console" because the rp6502.py tool is Python.
Ctrl-A then X will exit. Ctrl-A then B will send a break.

Edit `CMakeLists.txt` to add new source and asset files. From here on, it's
standard C/C++/assembly development for the 6502 platform.

### The tools directory:
`tools/` holds the ROM packager, the CMake commands your project calls, and
the cc65 toolchain file. A new project starts with only a small script that
goes and gets them from
[picocomputer/rp6502](https://github.com/picocomputer/rp6502) on the first
configure. They are ordinary files in your repository after that, so commit
them along with everything else.

To pull down the current versions, run the "RP6502: update tools" task, or
from a command line:

```bash
$ cmake -P tools/CMakeLists.txt
```

Either way the result is a diff you can read before you commit it.

### Updating an older project:
Projects made before this template merged cc65 and llvm-mos have their compiler
wired into the top of `CMakeLists.txt`. Replace everything above `project()`
with:

```cmake
cmake_minimum_required(VERSION 3.21)

include(${CMAKE_CURRENT_LIST_DIR}/tools/CMakeLists.txt)

#set(CC65_TARGET_SYSTEM rp6502)
#set(LLVM_MOS_PLATFORM rp6502)

if(DEFINED CC65_TARGET_SYSTEM)
    find_package(cc65 REQUIRED)
elseif(DEFINED LLVM_MOS_PLATFORM)
    find_package(llvm-mos-sdk REQUIRED)
else()
    rp6502_require_toolchain()
endif()
```

Delete the `add_subdirectory(tools)` line, which the `include()` replaces, and
copy `CMakePresets.json` from this template if you want the compiler picker.
Old projects called `rp6502_executable()` with the address their compiler
happened to use; `DATA default RESET default` works under both.

### Documentation:
 * [Picocomputer](https://picocomputer.github.io)
 * [CC65](https://cc65.github.io/)
 * [LLVM-MOS](https://llvm-mos.org/)
