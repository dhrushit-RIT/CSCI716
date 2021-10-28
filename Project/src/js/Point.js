class Point {
	x;
	y;
	pointType;
	lineSegment;
	//
	// defines the point class
	// stores the point x and y coordinates and the line segment it belongs to
	//

	// __slots__ = "x", "y", "line_segment", "point_type"

	constructor(x, y, point_type) {
		this.x = x;
		this.y = y;
		this.pointType = point_type;
		this.lineSegment = undefined;
	}

	get X() {
		return this.x;
	}

	get Y() {
		return this.y;
	}

	get LineSegment() {
		return this.lineSegment;
	}

	set Segment(line) {
		this.lineSegment = line;
	}

	toString() {
		return "{" + this.x + ", " + this.y + "}";
	}
}
