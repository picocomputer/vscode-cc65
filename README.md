# Archived - DO NOT USE

Use the [SDK](https://github.com/picocomputer/rp6502-sdk) instead.

## RP6502 VS Code Scaffolding for CC65

This provides scaffolding for a new Picocomputer 6502 software project. Both
C and assembly examples of "Hello, world!" are included. Make sure
`CMakeLists.txt` points to your choice of `main.c` or `main.s`, then delete
the one you aren't using.

### Linux Tools Install:
 * [VS Code](https://code.visualstudio.com/) - This has its own installer.
 * A source build of [CC65](https://cc65.github.io/getting-started.html).
 * The following tools installed from your package manager:
    * `sudo apt install cmake python3 git build-essential`

### Windows Tools Install:
 * `winget install -e --id Microsoft.VisualStudioCode`
 * `winget install -e --id Git.Git`
 * `winget install -e --id Kitware.CMake`
 * `winget install -e --id GnuWin32.Make`
   Add `C:\Program Files (x86)\GnuWin32\bin` to your PATH.
 * The current snapshot of [CC65](https://cc65.github.io/getting-started.html) -
   Do not skip the step about adding the `bin` directory to your PATH.
 * Install Python by typing `python3` in a command prompt, which will launch
   the Microsoft Store where you can start the installation. If Python runs,
   this has already been done - exit Python with Ctrl-Z plus Enter.

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
are constantly improving and have their own documentation. The first problem
you might encounter is that no kit is configured, so begin by reading this
and choosing the `[Unspecified]` kit:
https://code.visualstudio.com/docs/cpp/cmake-linux
The full documentation for the CMake plugin is here:
https://github.com/microsoft/vscode-cmake-tools/blob/main/docs/README.md

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
standard C/assembly development for the 6502 platform.

### Documentation:
 * [Picocomputer](https://picocomputer.github.io)
 * [CC65](https://cc65.github.io/)
