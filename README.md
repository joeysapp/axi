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
- [ ] Repeat sketch
- [ ] Cancel sketch
- [ ] Save Sketches on exit
- [ ] Load Sketches on load
- [ ] Save entire state of Scheduler (or convert it to a Sketch itself?)

# Shapes
All shapes are an ordered list of lines. Shapes can receive `Params` objects on creation to define unique properties of the shape. Shapes can also be used as building blocks for new, more complex shapes.
- [ ] shape.bounds _(which is a Shape itself)_
- [ ] shape.centroid
- [ ] shape.contains_vector(_vector) 
- [ ] shape.area
- [ ] shape.pen_travel_distance
- [ ] shape.params.is_drawn
- [ ] shape.estimated_draw_time

## ShapeTypes
- [x] Line
- [ ] Point
- [ ] Rect
- [ ] Polygon
- [ ] AsymetricPolygon
- [ ] Text (`fonttools` and Glyph Tables, oh my)
- [ ] SVG, SVG.load_file
- [ ] CSV, CSV.parse_file

## Shape Methods
Turn complex sketches into parameterized shapes for future/easier usage.
- [ ] readable-timestamp
- [ ] page-number-for-notebook
- [ ] git-commit-and-hash( ... )
- [ ] my-3d-cube( rotate, xsize, ysize, zsize )

## Shape creation with existing Shapes
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





# Feature Roadmap and Documentation
Axi is a personal hobby project attempting to address several issues I've had with my Axidraw and generative work in the past. WYSIWYG and I make no claims for this being a worthwhile tool to use - I just like having fun with it.

What follows are explanations of the internal logic of Axi and possible future features I'd like to implement.

# Architecture 
* `Shapes` are created by the user and are simply a list of coordinates `[[0, 0], [10, 10], ...`
* `Sketches` are an ordered list of `Shapes`.
* The `Generator` stores and translates `Sketches` into linked lists of `Nodes` for the `Scheduler`.
- This translation of `Sketch` to `Node` handles pen position and location.
* The `Scheduler` has a main linked list that it traverses, sending serial communication when needed.





# Troubleshooting
Loss of serial connection from the Axi has resulted in some problems in the past. Worst case scenario you may have to flash on a new EBB firmware (which - I have not been able to compile the `mphidflash` tool on my M1 mac.
* https://wiki.evilmadscientist.com/Updating_EBB_firmware
* https://github.com/evil-mad/EggBot/tree/master/EBB_firmware/Releases/combined





## Notes
* AxiDraw Software 3.5.0
- added `progress bar`, `draw_path()` [https://github.com/evil-mad/axidraw/releases/tag/v3.5.0](https://github.com/evil-mad/axidraw/releases/tag/v3.5.0)
