# Assignment 2 Plane Sweep Algorithm for Line Segment Intersection 

## Usage:
`python3 plane_sweep_line_segment_intersection.py datapoints.txt`

`python3 plane_sweep_line_segment_intersection.py input_file`

## Note
This algorithm assumes that 
- no line is vertical
- not more than two lines intersect at the same point
- this implementation needs an external library called pytreemap
  - this provides the red black tree implementation
  - to install this library run : `pip install pytreemap`
  - the implementation uses treeset that internally uses red black tree

Also, to see the plot, set the SAVE_TO_FILE to False in the first few lines of code

`SAVE_TO_FILE = False`


If the value is true, it will save the output in a `output.png` file 

