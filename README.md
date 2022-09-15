# Axi
Axi is a personal hobby project attempting to address several issues I've had with my Axidraw and generative work in the past. What follows are explanations of the internal logic of Axi and possible future features I'd like to implement.

Currently using [pyaxidraw](https://github.com/evil-mad/axidraw/tree/master/cli/pyaxidraw)'s basic `.connect()`, need to use python's serial lib above 3.8 (... or below 3)

# Features
This tool gives you an interface to interactively create series of shapes that get translated into stateful serial instructions.
* Defining something to be drawn is procedural
  - You create compositions of fundamental shapes, the base shape being a line
* Serial control structure is a linked list the plotter traverses 
  - Never lose control of the Axidraw
  - Non-blocking event loop
  - Safe serial disconnects, always
* Working on: pausing, resuming, canceling, and looping of sketches


# Usage
Currently usable as a python3.8 module
```console
$ git clone https://github.com/joeysapp/axi.git
$ cd axi
$ python3.8 -m axi
```

## To-do
Current main goal is "make it easier to use" however that can be done. I would like to sit down, plot out my idea quickly and save it for later.
- [ ] Pause / resume / cancel / repeat sketch
- [ ] Save sketches - and/or state of scheduler, flattened
- [ ] Require less typing - "inferrable" structure to things

- [ ] Easy Vector usage - is it possible to override/extend python lists?
  - [ ] Re-code quaternions and `3D-to-2D` projection ...
- [ ] Custom hash table/container for Nodes
  - may make finding shapes easier e.g. b-trees or simple buckets for now
  - faster collision/intersection calculations
  - "insert a circle every 25mm along the current Node container, doing `xyz` rel to surrounding 3 Nodes"


# Axi's general structure
* Shapes are created by the user and are just ordered lists of coordinates
* Shapes are added to sketches which are an ordered list of shapes
* Sketches are translated into linked lists of stateful serial instructions (the main feature I wanted)
  - Never lose track of the plotter's position or pen state

## Caveats
* All units are millimeters unless specified
  - The Axi has a microstep resolution of **(TBD)** so a point(**TBD**) will really depend on your pen and medium
* All shapes are a series of lines
* Shapes are created with unit vector lines `(0,0 to 1,1)` unless specified.
* Shapes are created relative to `[0, 0]` unless specified
  - Handy usage: plot shapes, move the plotter `[dx, dy]` and plot them again
* Check what `XY` is for you and your plotter
* Most things in Axi are designed to be easy to use, meaning there are a lot of optional arguments and params. As a result, most things are passed around as kwargs. (is this good or bad practice, I don't know)

# Types
## Shapes
All shapes are an ordered list of lines. Shapes _always_ receive a single argument, a `Params` object which is simply a helper class around a dictionary. This informs the shape properties about itself.

All Shapes have the following props:
- [ ] shape.bounding_rect
- [ ] shape.centroid
- [ ] shape.area
- [ ] shape.pen_travel_distance
- [ ] shape.estimated_plot_time

All shapes have the following helper functions:
- [ ] shape.contains(`vector`)
- [ ] shape.copy()

## Shape Creation
All shapes can be created in multiple ways. I wanted to do this to offload a lot of reptitive math from myself. You should be able to get this information from a given shape via the `help(thing)` method. Essentially it's just overloading. I may decide eventually something more pythonic would be better, but this is what I ended up with after a week or two of building this. Here are a few examples:
```
    # line of 10mm placed at 0,0
    line({ length: 10, degree: 60 })
    
    # "center" for a line means its midpoint
    line({ pos: [10,10], length: 10, center: true })
    
    # line creation with 2 positions
    line({ pos1: [10,10], pos2: [20,20] })
    
    # some shapes have helper creator params which are noted in .info(), such as:
    [ ... lines ...] = line({ pos1: [10,10], pos2: [20,20], pos3: [30,30], ... })
    
    # a triangle with radius of 1mm
    polygon({ sides: 3 })
    
    # a circle
    polygon({ sides: 360 })
    polygon({ radians: math.pi/720 })

    # rect whose corner is at 0,0, goes to edge
    rect({ center: true, pos: [5, 5], width: 10, height: 10 })
```

## Shape Params for Creation
There are some base props and methods of `Params` objects, such as:
- [ ] translate
  - Translate by xyz versus translation matrix
  - [ ] transform 
  - [ ] skew
  - [ ] warp
- [ ] subdivide

## Shape Params for the Plotter
- [ ] is_drawn

## Shape Helper methods for Composition or Generation
Turn complex sketches into parameterized shapes for easier use
- [ ] grid({ width, height, rows, columns })
- [ ] repeat({ shapes, translation_matrix, times )
  - draw shapes n times, translating reference matrix every loop
  
- [ ] Masking a Shape within another Shape ("hatch fill")

- [ ] timestamp({ time, font, size })
- [ ] git-commit-and-hash( ... )
- [ ] my-cool-frame( ... )




# More Types
## Vectors
- [ ] Implemented most-used vector math and utility

## Nodes
- [ ] Implement `neighbors` weighted distances
  - If there's a ShapeType.Graph (e.g. draw a MST), we might want nodes outside of the scheduler.

## Longterm Goals
- [ ] macOS and iOS interface
- [ ] Quaternion -> (3D, STL) ShapeType, 3D to 2D projection (again)
- [ ] Web/remote interface - e.g. rpi hooked up to Axidraw, send it commands
- [ ] Bare C implementation
- [ ] Serial implementation

# Troubleshooting
Loss of serial connection from the Axi has resulted in some problems in the past. Worst case scenario you may have to flash on a new EBB firmware (which - I have not been able to compile the `mphidflash` tool on my M1 mac.
* https://wiki.evilmadscientist.com/Updating_EBB_firmware
* https://github.com/evil-mad/EggBot/tree/master/EBB_firmware/Releases/combined




## Notes
* pyaxidraw - [https://github.com/evil-mad/axidraw/tree/master/cli/pyaxidraw](https://github.com/evil-mad/axidraw/tree/master/cli/pyaxidraw)

* AxiDraw Software 3.5.0 - [https://github.com/evil-mad/axidraw/releases/tag/v3.5.0](https://github.com/evil-mad/axidraw/releases/tag/v3.5.0)
  - `progress bar`, https://axidraw.com/doc/cli_api/#progress
  - `draw_path(vertices)` - the irony is not lost on me
