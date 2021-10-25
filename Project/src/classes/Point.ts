class Point {
	private x: number;
	private y: number;
	private pointType: EventType;
	private lineSegment: LineSegment | undefined;
	//
	// defines the point class
	// stores the point x and y coordinates and the line segment it belongs to
	//

	// __slots__ = "x", "y", "line_segment", "point_type"

	constructor(x: number, y: number, point_type: EventType) {
		this.x = x;
		this.y = y;
		this.pointType = point_type;
		this.lineSegment = undefined;
	}

	get X(): number {
		return this.x;
	}

	get Y(): number {
		return this.y;
	}

	get LineSegment(): LineSegment {
		return this.lineSegment;
	}

	set_segment(line: LineSegment) {
		this.lineSegment = line;
	}

	toString() {
		return "{" + this.x + ", " + this.y + "}";
	}
}
