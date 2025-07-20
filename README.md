# RP6502 VSCode Scaffolding for CC65

This provides scaffolding for a new Picocomputer 6502 software project. Both
C and assembly examples of "Hello, world!" are included. Make sure
`CMakeLists.txt` points to your choice of `main.c` or `main.s`, then delete
the one you aren't using.

### Linux Tools Install:
 * [VSCode](https://code.visualstudio.com/) - This has its own installer.
 * A source build of [CC65](https://cc65.github.io/getting-started.html).
 * The following tools installed from your package managers:
    * `sudo apt-get install cmake python3 pip git build-essential`
    * `pip install pyserial`

### Windows Tools Install:
 * `winget install -e --id Microsoft.VisualStudioCode`
 * `winget install -e --id Git.Git`
 * `winget install -e --id Kitware.CMake`
 * `winget install -e --id GnuWin32.Make`
    Add `C:\Program Files (x86)\GnuWin32\bin` to your PATH.
 * A source build of [CC65](https://cc65.github.io/getting-started.html) -
   Do not skip the step about adding the `bin` directory to your PATH.
 * Install Python by typing `python3` in a command prompt, which will launch
   the Microsoft Store where you can start the installation. If Python runs,
   this has already been done — exit Python with Ctrl-Z plus Enter.
 * `pip install pyserial`

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

Install the recommended extensions when VSCode prompts you, choosing the
default or obvious choice for any other prompts. The tools we use in VSCode
are constantly improving and changing making it too difficult to maintain
documentation.

"Start Debugging" (F5) will build your project and upload it to the
Picocomputer over a USB cable plugged into the Pico VGA. There is no debugger
for the 6502; this process will exit immediately after the upload. If the
default communication device doesn't work, edit `.rp6502` in the project root
folder. This file will be created the first time you run "Start Debugging"
and will be ignored by git.

Edit `CMakeLists.txt` to add new source and asset files. From here on, it's
standard C/assembly development for the 6502 platform.
