# Axi
Generatively create and draw composable shapes with your [Axidraw](https://axidraw.com). Currently a wrapper around [pyaxidraw](https://github.com/evil-mad/axidraw/tree/master/cli/pyaxidraw). 

# Features
Axi allows you to create sketches of complex shapes, which themselves are eventually translated into a series of ordered, safe serial commands for the Axidraw to execute.
* Composable, procedural sketch and shape creation
* Base is a stateful directed graph of serial instructions
* Pausing, resuming, canceling, and looping of sketches
* Handles all possible exits and disconnects from serial

# Usage
Currently usable as a `python` module:
```console
$ git clone https://github.com/joeysapp/axi.git
$ cd axi
$ python3.8 -m axi
```

## To-do
- [x] Handle exit signals for serial safely
- [ ] Pause to reposition medium or change pen
- [ ] Pause / resume sketch 
- [ ] Cancel / repeat sketch
- [ ] Save sketches on exit, load sketches on start
- [ ] Save entire state of scheduler (or flatten it to a sketch itself)

# Goals and Documentation
Axi is a personal hobby project attempting to address several issues I've had with my Axidraw and generative work in the past. WYSIWYG, I'm just having fun making it.

What follows are explanations of the internal logic of Axi and possible future features I'd like to implement.

# Architecture and Event Loop
* `Shapes` are defined by the user and are simply a generated list of coords `[[0, 0], [10, 10], ...]`
* `Sketches` are an ordered list of `Shapes`
* The `Generator` stores and translates sketches into linked lists of `Nodes` for the `Scheduler`.
* The `Scheduler` has a main linked list that it traverses, sending serial to Axidraw when needed.

# Fundamental Types
## Shapes
All shapes are an ordered list of lines. Shapes can receive `Params` objects on creation to define unique properties of the shape. Shapes can also be used as building blocks for new, more complex shapes.
- [ ] shape.bounding_box _(which is a Bounds object, which extends Shape)_
- [ ] shape.centroid
- [ ] shape.contains(vector) 
- [ ] shape.area
- [ ] shape.pen_travel_distance
- [ ] shape.estimated_draw_time

- [ ] shape.params.is_drawn
- [ ] shape.params.transform
- [ ] shape.params.translate
- [ ] shape.params.skew
- [ ] shape.params.warp


## ShapeTypes
- [x] Line
- [ ] Point
- [ ] Rect
- [ ] Polygon
- [ ] AsymetricPolygon
- [ ] Text (`fonttools` and Glyph Tables, heavy sigh)
- [ ] SVG, SVG.load_file
- [ ] CSV, CSV.parse_file

## Shape Methods
Turn complex sketches into parameterized shapes for easier use.
- [ ] readable-timestamp(now)
- [ ] page-number-for-notebook(42)
- [ ] git-commit-and-hash( ... )
- [ ] my-3d-cube(rotate, xsize, ysize, zsize)

## Shape Creation with other Shapes
Possibly not within a Shape itself, but an external `Modifier` or `Selector`
- [ ] repeat_shapes( shapes, x_amount, y_amount ) - create a simple grid
- [ ] repeat_shapes( shapes, offset_vector, times ) - draw shapes, adding offset_vector every loop
- [ ] Masking a Shape within another Shape ("hatch fill")

# Other Types
## id
- [ ] Simplify `id` setting, make `Generator`'s linked list creation simpler

## Bounds
- [ ] Convert to extending Shape itself, allowing for a Bound to be any ShapeType
- [ ] bounds.contains(vector)

## Vectors
- [ ] Fully-implemented vector math
- [ ] vector.is_within(bounds)

## Nodes
- [ ] Neighbors with weighted distances

## Params
- [ ] Class design allowing for intuitive/arbitrary params
- [ ] Handle undefined values

## Longterm Goals
- [ ] macOS and iOS interface
- [ ] Quaternion -> (3D, STL) ShapeType, 3D to 2D projection (again)
- [ ] Web interface
- [ ] Bare C

# Troubleshooting
Loss of serial connection from the Axi has resulted in some problems in the past. Worst case scenario you may have to flash on a new EBB firmware (which - I have not been able to compile the `mphidflash` tool on my M1 mac.
* https://wiki.evilmadscientist.com/Updating_EBB_firmware
* https://github.com/evil-mad/EggBot/tree/master/EBB_firmware/Releases/combined





## Notes
* AxiDraw Software 3.5.0
- added `progress bar`, `draw_path()` [https://github.com/evil-mad/axidraw/releases/tag/v3.5.0](https://github.com/evil-mad/axidraw/releases/tag/v3.5.0)
