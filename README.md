# RP6502 VSCode Scaffolding for CC65

This is scaffolding for a new Picocomputer 6502 software project.

### Linux Tools Install:
 * [VSCode](https://code.visualstudio.com/). This has its own installer.
 * A source install of [CC65](https://cc65.github.io/getting-started.html).
 * The following tools installed from your package managers:
    * `sudo apt-get install cmake python3 pip git build-essential`
    * `pip install pyserial`

### Windows Tools Install:
 * [VSCode](https://code.visualstudio.com/). This has its own installer.
 * A source install of [CC65](https://cc65.github.io/getting-started.html).
   Do not skip the step about adding bin to your path.
 * Install python by typing `python3` which will launch the Microsoft Store
   where you start the install. If python runs, this has already been done,
   exit python with Ctrl-Z plus Return.
 * Install the python serial library with `pip install pyserial`.
 * `winget install -e --id Kitware.CMake`.
 * `winget install -e --id GnuWin32.Make`.
    Add "C:\Program Files (x86)\GnuWin32\bin" to your path.
 * `winget install -e --id Git.Git`.

### Getting Started:
Go to the [GitHub template](https://github.com/picocomputer/vscode-cc65) and
select "Use this template" then "Create a new repository". GitHub will make a
clean project for you to start with. Then you can download the repository
and open the files.

```
$ git clone [path_to_github]
$ cd [to_where_it_cloned]
$ code .
```

Install the extensions and choose the default or obvious choice if VSCode
prompts you.

"Start Debugging" (F5) will build your project and upload it to the
Picocomputer over a USB cable plugged into the Pico VGA. There is no debugger
for the 6502; this process will exit immediately after the upload.
If the default communications device doesn't work, edit ".rp6502" in the
project root folder. This file will be created the first time you
"Start Debugging" and will be ignored by git.

Edit CMakeLists.txt to add new source and asset files. It's
pretty normal C/ASM development from here on.
