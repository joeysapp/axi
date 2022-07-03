# axi
This is a tool to interface with an [Axidraw](https://axidraw.com/). 

## use
You can either use `axi` as a cli tool or as a Python package. Example usage:
```python3 -m axi -h```

## features
* plotter state management
* safe connect/disconnects
* safe head limits
* simple resetting

## roadmap
* network connectivity (outside world -> axi -> axidraw)
* easy interrupt / resuming
  - save pos -> return home -> pen up/down -> go back to pos
* live interface to axidraw / REPL
* usb interfaces: controllers / wacom / other

