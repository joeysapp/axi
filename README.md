# axi
This is a library and tool used to interface with an [Axidraw](https://axidraw.com/).
It can be used as a python module, and will eventually be released as a python package.

## Usage
Usage as a `python3.8` module:
```bash
$ python3.8 -m axi
```

Install and use as `python3.8` package:
```bash
$ pwd
../axi/
$ python3.8 setup.py develop
$ chmod +x /bin/axi
$ axi
...
$ axi-repl
> (goto 20 20)
> (square 10 10)
```

## Features
* Safe serial connections and resets
  - Allows for arbitrary disconnects/errors, the plotter will always return home.
* Bounds checking
  - Axidraw will never attempt to go out of physical bounds. This depends on your model.

## Roadmap
- [x] Handle serial interrupts and resets
- [ ] Network connectivity/control
- [ ] Easy interrupt / resuming
- [ ] [REPL](#repl) interface
- [ ] USB interface (e.g. controllers, webcam, Wacom tablet)
- [ ] Replacing `pyaxidraw` itself

## REPL
Using `axi-repl` will open a serial connection to your Axidraw and allows you to create, store and edit objects on the fly. The intent of this is to make the Axidraw a more interactive experience, hopefully inspiring some creativity.
