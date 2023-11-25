# RP6502 VSCode Scaffolding

This is scaffolding for your new Picocomputer software project. These
instructions are for Linux distributions that use apt. A Windows install is
demonstrated in a [video by Lee Smith](https://www.youtube.com/watch?v=zJpz16XDL9c&t=1535s).
MacOS requires translating the apt-get below to a package manager like brew or port.


You must have on your development system:
 * [VSCode](https://code.visualstudio.com/). This has its own installer.
 * A source install of [this CC65](https://github.com/picocomputer/cc65).
 * The following suite of tools for your specific OS.
```
$ sudo apt-get install cmake python3 pip git build-essential
$ pip install pyserial
```

Go to the [GitHub template](https://github.com/picocomputer/rp6502-vscode) and
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

You can build with F7. Running a program is done with "Run Build Task..."
CTRL-SHIFT-B. If the default communications device doesn't work, edit ".rp6502"
in the project root folder. This file will be created the first time you
"Run Build Task..." and will be ignored by git.

Edit CMakeLists.txt to add new source and asset files. It's
pretty normal C/ASM development from here on.
