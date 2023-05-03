# RP6502 VSCode Scaffolding

This is scaffolding for your new Picocomputer project.

You'll need [VSCode](https://code.visualstudio.com/) and the following suite of tools.
```
$ sudo apt-get install cc65 cmake python3 pip git build-essential
$ pip install pyserial
```

Download and unpack the latest [zip from GitHub](https://github.com/picocomputer/rp6502-vscode/archive/refs/heads/main.zip
). Then retrieve the latest RP6502 SDK as a submodule using git.
```
$ cd to_your_new_project
$ git init
$ rmdir rp6502-sdk
$ git submodule add https://github.com/picocomputer/rp6502-sdk.git
```

Now launch VSCode and "Open Folder..." your new project.

Install the extensions VSCode will recommend.

When asked to configure project "your_new_project", choose "Yes".

When asked for a CMake kit, choose "RP6502".

When asked to configure IntelliSense, choose "Don't Allow". If asked again, choose "No". This has already been configured with hacks since CC65 isn't fully supported by CMake or IntelliSense.

You can build with F7. Running a program is done with "Run Build Task..." CTRL-SHIFT-B.

You're all set to create the next big thing. Edit CMakeLists.txt to add new C and ASM source files.
