class MyEvent {
	// """
	// defines the events class
	// point : the point associated with this event
	// event_type : the type of event (EventType)
	// lines : set if the point is an intersection point
	// """
	point;
	event_type;
	lines;

	constructor(point, event_type) {
		this.point = point;
		this.event_type = event_type;
		this.lines = undefined;
	}

	set_event_lines(lines) {
		// """
		// sets the list "lines" when the event is intersection
		// :param lines:
		// :return:
		// """
		if (this.event_type == EventType.INTERSECTION) {
			if (!this.lines) {
				this.lines = lines;
			} else {
				this.lines.push(...lines);
			}
			this.lines.sort((a, b) => (a.CurrY > b.CurrY ? 1 : -1));
		}
	}

	get Point() {
		return this.point;
	}

	get Event_Type() {
		return this.event_type;
	}

	get Lines() {
		return this.lines;
	}

	toString() {
		let s = "";
		if (this.event_type == EventType.START_POINT) {
			s += "S " + this.point.LineSegment;
		} else if (this.event_type == EventType.END_POINT) {
			s += "E " + this.point.LineSegment;
		} else {
			s += "I " + this.lines[0] + "-" + this.lines[1];
		}

		return s;
	}
}
