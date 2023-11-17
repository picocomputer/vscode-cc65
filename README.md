# RP6502 VSCode Scaffolding

This is scaffolding for your new Picocomputer software project. These
instructions are for Linux distributions that use apt. A Windows install is
demonstrated in a [video by Lee Smith](https://www.youtube.com/watch?v=zJpz16XDL9c&t=1535s).
MacOS requires translating the apt-get below to a package manager like brew or port.


You must have on your development system:
 * [VSCode](https://code.visualstudio.com/). This has its own installer.
 * A source install of [CC65](https://github.com/picocomputer/cc65).
 * The following suite of tools for your specific OS.
```
$ sudo apt-get install cmake python3 pip git build-essential
$ pip install pyserial
```

Go to the [GitHub template](https://github.com/picocomputer/rp6502-vscode) and
select "Use this template" then "Create a new repository". GitHub will make a
clean project for you to start with. After you clone your new project, don't
forget to grab the SDK as a submodule.

```
$ git clone [path_to_github]
$ cd [to_where_it_cloned]
$ git submodule update --init
```

Now launch VSCode and "Open Folder..." your new project. If you've worked with
C/C++ in VSCode before then you know what to expect next. The only exception
is IntelliSense. When asked to configure IntelliSense, which may happen
several times, choose "Don't allow", "No", "Don't ask again" or whatever
answer isn't going to change the hacks in settings.json that make CC65 work.

You can build with F7. Running a program is done with "Run Build Task..."
CTRL-SHIFT-B. If the default communications device doesn't work, edit ".rp6502"
in the project root folder. This file will be created the first time you
"Run Build Task..." and will be ignored by git.

Edit CMakeLists.txt to add new source and asset files. It's
pretty normal C/ASM development from here on.

If you're new to VSCode or C development, here's some of the things VSCode
will ask. In general, clicking through the default or obvious choice is what
you want (except for IntelliSense). You may not be asked everything. It
depends on how VSCode has been used in the past, if this is the first time
opening the project, and other moving targets.

 * You must trust the folder if asked.
 * Install the extensions VSCode will recommend.
 * When asked to configure your project, choose "Yes".
 * When asked for a CMake kit, choose "RP6502".
