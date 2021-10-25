function cmp_event(e1: MyEvent, e2: MyEvent) {
	// """
	// comparison function to compare two events

	// :param e1: first event
	// :param e2: second evednt
	// :return: integer 1 if e1 happens after e2, -1 if e1 happens before e2 && 0 if both event are equally likely to occur now
	// """
	if (e1.Point.X < e2.Point.X) {
		return -1;
	} else if (e1.Point.X > e2.Point.X) {
		return 1;
	} else {
		if (
			e1.Event_Type == EventType.INTERSECTION &&
			e2.Event_Type != EventType.INTERSECTION
		) {
			return -1;
		} else if (
			e2.Event_Type == EventType.INTERSECTION &&
			e1.Event_Type != EventType.INTERSECTION
		) {
			return 1;
		} else {
			if (
				e1.Event_Type == EventType.START_POINT &&
				e2.Event_Type == EventType.END_POINT
			) {
				return -1;
			} else if (
				e1.Event_Type == EventType.END_POINT &&
				e2.Event_Type == EventType.START_POINT
			) {
				return 1;
			} else {
				// # issue here
				// # TODO fix this
				if (e1.Point.LineSegment != e2.Point.LineSegment) {
					if (
						e1.Point.LineSegment.get_other_point(e1.Point).X <
						e2.Point.LineSegment.get_other_point(e2.Point).X
					) {
						return -1;
					} else {
						return 1;
					}
				} else {
					return 0;
				}
			}
		}
	}
}

function cmp_line(l1: LineSegment, l2: LineSegment) {
	// """
	// function to compare two line segments
	// :param l1: first line segment
	// :param l2: second line segment
	// :return: 1 if l1's current y coordinate value > l2's. -1 other wise and 0 if both y values are same
	// """
	let y_1 = l1.CurrY.toFixed(5);
	let y_2 = l2.CurrY.toFixed(5);
	if (y_1 < y_2) return -1;
	else if (y_1 > y_2) return 1;
	// # if currently its intersecting then the two have same y value
	else if (l1 == l2) return 0;
	else {
		let y_1_prev = l1.PrevY.toFixed(5);
		let y_2_prev = l2.PrevY.toFixed(5);

		if (y_1_prev != null && y_2_prev != null)
			if (y_1_prev > y_2_prev) return -1;
			else if (y_1_prev < y_2_prev) return 1;
			else return 0;
		else return 1;
	}
}
