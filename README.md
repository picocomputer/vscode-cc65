# RP6502 VSCode Scaffolding

You'll need [VSCode](https://code.visualstudio.com/) and the following suite of tools.
```
$ sudo apt-get install cc65 cmake python3 pip build-essential
$ pip install pyserial
```

Download and unpack the zip from GitHub. Retrieve the latest SDK using git.
```
$ cd to_where_you_unzipped
$ git init
$ git submodule update --init
```

Now launch VSCode and "Open Folder..." your new project. Install the extensions it will recommend. You can build with F7.

Uploading and running a program is done with "Run Build Task..." CTRL-SHIFT-B by default.
