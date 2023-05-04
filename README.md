# RP6502 VSCode Scaffolding

This is scaffolding for your new Picocomputer software project. These instructions are for Linux. Windows and MacOS instructions will be available when someone contributes them.

You'll need [VSCode](https://code.visualstudio.com/) and the following suite of tools.
```
$ sudo apt-get install cc65 cmake python3 pip git build-essential
$ pip install pyserial
```

Go to the [GitHub template](https://github.com/picocomputer/rp6502-vscode) and select "Use this template" then "Create a new repositoy". GitHub will make a clean project for you to start with. After you clone your new project, don't forget to grab the SDK as a submodule.

```
$ git clone [path_to_github]
$ cd [to_where_it_cloned]
$ git submodule update --init
```

Now launch VSCode and "Open Folder..." your new project. If you've worked with C/C++ in VSCode before then you know what to expect next. The only exception is IntelliSense. When asked to configure IntelliSense, which may happen several times, choose "Don't allow", "No", "Don't ask again" or whatever answer isn't going to change the hacks to make CC65 work.

You can build with F7. Running a program is done with "Run Build Task..." CTRL-SHIFT-B. Edit CMakeLists.txt to add new C and ASM source files. It's pretty normal C/ASM develpment from here on.

If you're new to VSCode or C development, here's some of the things VSCode will ask. In general, clicking through the default or obvious choice is what you want (except for IntelliSense). You may not be asked everything. It depends on how VSCode has been used in the past, if this is the first time opening the project, and other moving targets.

 * You must trust the folder if asked.
 * Install the extensions VSCode will recommend.
 * When asked to configure your project, choose "Yes".
 * When asked for a CMake kit, choose "RP6502".
