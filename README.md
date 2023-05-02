# RP6502 VSCode Scaffolding

This is scaffolding for your new Picocomputer project.

You'll need [VSCode](https://code.visualstudio.com/) and the following suite of tools.
```
$ sudo apt-get install cc65 cmake python3 pip git build-essential
$ pip install pyserial
```

Download and unpack the latest [zip from GitHub](https://github.com/picocomputer/rp6502-vscode/archive/refs/heads/main.zip
). Retrieve the latest RP6502 SDK using git.
```
$ cd to_unzipped_folder
$ git init
$ git submodule update --init
```

Now launch VSCode and "Open Folder..." your new project.

Install the extensions VSCode will recommend.

When asked for a CMake "kit" choose "RP6502".

When asked to configure IntelliSense, choose "Don't Allow". When asked again, choose "No". This has already been configured with hacks since CC65 isn't supported by IntelliSense.

You can build with F7. Uploading and running a program is done with "Run Build Task..." CTRL-SHIFT-B.

You're all set to create the next big thing. Edit CMakeLists.txt to add new C and ASM source files.
