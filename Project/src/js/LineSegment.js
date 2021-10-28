class LineSegment {
	name;
	point1;
	point2;
	slope;
	y_intercept;
	curr_y;
	prev_y;
	// """
	// class to represent a line segment
	// name: name of the line
	// point1 : the starting point of the line. will be sorted so that it is always the first point from y-axis
	// point2 : the end point of the line. it is the further point from the y-axis
	// slope : slope of the line
	// y_intercept : y_intercept of the line
	// curr_y : value of the y coordinate for the current value of x in the sweep line status
	// """

	constructor(point1, point2, name = "") {
		this.point1 = point1;
		this.point2 = point2;

		if (this.point1.X > this.point2.X) {
			this.point1 = point2;
			this.point2 = point1;
		}

		if (this.point1.X - this.point2.X != 0) {
			this.slope =
				(this.point2.Y - this.point1.Y) / (this.point2.X - this.point1.X);
		} else {
			this.slope = undefined;
		}

		this.curr_y = undefined;
		this.prev_y = undefined;

		this.name = name;

		// # y = mx + b
		// # point1.y = m * point1.x + b
		// # point2.y = m * point2.x + b
		// # m = (point2.y - point1.y) / (point2.x - point1.x)
		// # b = point1.y - {(point2.y - point1.y)/(point2.x - point1.x)} * point1.x
		this.y_intercept =
			point1.Y - ((point2.Y - point1.Y) / (point2.X - point1.X)) * point1.X;
	}

	get_points() {
		//  """
		//  gives the value of points making up the line segment
		//  :return: list of points
		//  """
		return [this.point1, this.point2];
	}

	set_curr_y(x) {
		//  """
		//  sets the value of current y in the line segment
		//  :param x:
		//  :return: None
		//  """
		this.prev_y = this.curr_y;
		this.curr_y = this.slope * x + this.y_intercept;
	}

	get_curr_y() {
		//  """
		//  gives the value of current y stored in the self
		//  :param x:
		//  :return: self.curr_y
		//  """
		return this.curr_y;
	}

	get_other_point(point) {
		//  """
		//  gets the other point that make up the line segment
		//  :param point:
		//  :return: other point
		//  """
		if (point == this.point1) {
			return this.point2;
		} else {
			return this.point1;
		}
	}

	get CurrY() {
		return this.curr_y;
	}

	set CurrY(x) {
		this.prev_y = this.curr_y;
		this.curr_y = this.slope * x + this.y_intercept;
	}

	get PrevY() {
		return this.prev_y;
	}

	get Point1() {
		return this.point1;
	}

	get Point2() {
		return this.point2;
	}

	get Name() {
		return this.name;
	}

	toString() {
		return this.name;
	}
}
