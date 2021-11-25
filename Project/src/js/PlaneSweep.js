var DEBUG_MODE = true;

function cmp_event(e1, e2) {
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

function cmp_line(l1, l2) {
	// """
	// function to compare two line segments
	// :param l1: first line segment
	// :param l2: second line segment
	// :return: 1 if l1's current y coordinate value > l2's. -1 other wise and 0 if both y values are same
	// """
	let y_1 = parseFloat(l1.CurrY.toFixed(5));
	let y_2 = parseFloat(l2.CurrY.toFixed(5));
	if (y_1 < y_2) return -1;
	else if (y_1 > y_2) return 1;
	// # if currently its intersecting then the two have same y value
	else if (l1 == l2) return 0;
	else {
		let y_1_prev = parseFloat(l1.PrevY.toFixed(5));
		let y_2_prev = parseFloat(l2.PrevY.toFixed(5));

		if (y_1_prev != null && y_2_prev != null)
			if (y_1_prev > y_2_prev) return -1;
			else if (y_1_prev < y_2_prev) return 1;
			else return 0;
		else return 1;
	}
}

function check_if_intersecting_in_range(l1, l2) {
	// """
	// checks if the line segments intersect within a given set of conditions

	// :param l1: line 1 line segment
	// :param l2: line 2 line segment
	// :return: tuple of whether there was an intersection and if so, what point
	// """
	let x1 = l1.Point1.X;
	let y1 = l1.Point1.Y;
	let x2 = l1.Point2.X;
	let y2 = l1.Point2.Y;

	let x3 = l2.Point1.X;
	let y3 = l2.Point1.Y;
	let x4 = l2.Point2.X;
	let y4 = l2.Point2.Y;

	let t1_numerator = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4);
	let t1_denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4);

	let t2_numerator = (x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2);
	let t2_denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4);

	let t1, t2;

	// # does not handle the vertical lines
	// # assuming no lines are vertical or horizontal
	let t1_in_range =
		t1_denominator != 0 &&
		0 <= t1_numerator / t1_denominator &&
		t1_numerator / t1_denominator <= 1;
	let t2_in_range =
		t2_denominator != 0 &&
		0 <= t2_numerator / t2_denominator &&
		t2_numerator / t2_denominator <= 1;

	let intersection_point = null;
	if (t1_in_range && t2_in_range) {
		t1 = t1_numerator / t1_denominator;
		t2 = t2_numerator / t2_denominator;

		intersection_point = new Point(
			x1 + t1 * (x2 - x1),
			y1 + t1 * (y2 - y1),
			EventType.INTERSECTION
		);
	}

	return [t1_in_range && t2_in_range, intersection_point];
}

function check_for_intersection(event_queue, l1, l2, sweep_line_status) {
	// """
	// checks for the intersection of the line segments and adds to the event queue

	// :param event_queue: the queue of events to add a new event to
	// :param l1: first of the two intersecting lines
	// :param l2: second of the two intersecting lines
	// :param sweep_line_status: data structure for maintaining the line segments in sorted order of y at a given x
	// :return: None
	// """
	let [intersecting_in_range, intersection_point] =
		check_if_intersecting_in_range(l1, l2);

	if (intersecting_in_range) {
		if (intersection_point.X > sweep_line_status.X) {
			let intersection_event = new MyEvent(
				intersection_point,
				EventType.INTERSECTION
			);

			// # check for the sequence of lines and then add
			let lines_sorted_by_y = [l1, l2].sort((a, b) => b.CurrY - a.CurrY);
			intersection_event.set_event_lines(lines_sorted_by_y);
			if (!event_queue.has(intersection_event)) {
				if (DEBUG_MODE)
					console.log(
						"intersection event added to queue for",
						lines_sorted_by_y[0].name,
						"and",
						lines_sorted_by_y[1].name
					);
				event_queue.add(intersection_event);
			}
		}
	}
}

function handle_start(event, sweep_line_status, event_queue) {
	// """
	// handles the processing of event if the event is start point of the line segment
	// :param event: the current event object
	// :param sweep_line_status: sweep line status object
	// :param event_queue: event queue object
	// :return: None
	// """
	// # add to sweep line status
	if (DEBUG_MODE) {
		console.log("START POINT for line", event.point.LineSegment.name);
		console.log(
			"adding " + event.point.LineSegment.name + " to the sweep status"
		);
	}
	sweep_line_status.OrderedBST.add(event.Point.LineSegment);
	if (DEBUG_MODE) console.log(sweep_line_status.toString());
	// # check if it intersects with successor
	const next_itr = sweep_line_status.OrderedBST.find(event.Point.LineSegment);
	next_itr.next();
	let successor_line = next_itr.key;
	if (successor_line)
		check_for_intersection(
			event_queue,
			event.Point.LineSegment,
			successor_line,
			sweep_line_status
		);
	// # check if it intersects with predecessor
	const prev_itr = sweep_line_status.OrderedBST.find(event.Point.LineSegment);
	prev_itr.prev();
	let predecessor_line = prev_itr.key;
	if (predecessor_line)
		check_for_intersection(
			event_queue,
			event.Point.LineSegment,
			predecessor_line,
			sweep_line_status
		);
}

function handle_end(event, sweep_line_status, event_queue) {
	// """
	// handles the processing of event if the event is end point of the line segment
	// :param event: the current event object
	// :param sweep_line_status: sweep line status object
	// :param event_queue: event queue object
	// :return: None
	// """
	let line_to_remove = event.Point.LineSegment;
	if (DEBUG_MODE) console.log("END POINT for line", line_to_remove.name);

	// # find the line segments prior and after the line to remove
	const prev_itr = sweep_line_status.OrderedBST.find(line_to_remove);
	prev_itr.prev();
	let predecessor_line = prev_itr.key;
	const next_itr = sweep_line_status.OrderedBST.find(line_to_remove);
	next_itr.next();
	let successor_line = next_itr.key;

	// # remove the line from the sweep line status
	if (DEBUG_MODE)
		console.log(
			"remove " + event.point.LineSegment.name + " from the sweep status"
		);
	sweep_line_status.OrderedBST.delete(line_to_remove);
	if (DEBUG_MODE) console.log(sweep_line_status.toString());
	// # check for the intersection of the lines that are now adjacent
	if (predecessor_line && successor_line)
		check_for_intersection(
			event_queue,
			predecessor_line,
			successor_line,
			sweep_line_status
		);
}

function handle_intersection(
	event,
	sweep_line_status,
	event_queue,
	line_intersections
) {
	// """
	// handles the processing of event if the event is intersection of points of two line segments
	// :param event: the current event object
	// :param sweep_line_status: sweep line status object
	// :param event_queue: event queue object
	// :param line_intersections: intersection points so far found
	// :return: None
	// """
	let l0 = event.Lines[0];
	let l1 = event.Lines[1];
	// # l0.name == "line2" and l1.name == "line4" or l0.name == "line4" and l1.name == "line2"
	if (DEBUG_MODE) {
		console.log("INTERSECTION for " + l0.name + " and " + l1.name);
		console.log(sweep_line_status.toString());
	}
	sweep_line_status.OrderedBST.delete(l0);
	sweep_line_status.OrderedBST.delete(l1);
	if (DEBUG_MODE) console.log(sweep_line_status.toString());
	// # l0.set_curr_y(sweep_line_status.x)
	// # l1.set_curr_y(sweep_line_status.x)
	sweep_line_status.OrderedBST.add(l1);
	sweep_line_status.OrderedBST.add(l0);
	if (DEBUG_MODE) console.log(sweep_line_status.toString());

	// # remove all the events from the queue
	// # add all of them with the reversed order for the intersection point lines
	// # check if after reversal, there is an intersection
	const prev_itr = sweep_line_status.OrderedBST.find(l1);
	prev_itr.prev();
	let new_predecessor_of_l1 = prev_itr.key;
	if (new_predecessor_of_l1)
		check_for_intersection(
			event_queue,
			l1,
			new_predecessor_of_l1,
			sweep_line_status
		);
	const next_itr = sweep_line_status.OrderedBST.find(l0);
	next_itr.next();
	let new_successor_of_l0 = next_itr.key;
	if (new_successor_of_l0)
		check_for_intersection(
			event_queue,
			l0,
			new_successor_of_l0,
			sweep_line_status
		);

	line_intersections.add(event.Point);
}

function handle_event(
	event,
	event_queue,
	sweep_line_status,
	line_intersections
) {
	// """
	// handles the current event
	// event could be one of the three event types

	// :param event: the event that occurred
	// :param event_queue: queue to add the event to
	// :param sweep_line_status: data structure for maintaining the line segments in sorted order of y at a given x
	// :param line_intersections: list of line intersections
	// :return: None
	// """
	// if (DEBUG_MODE) console.log(event.toString());
	if (event.Event_Type == EventType.START_POINT)
		handle_start(event, sweep_line_status, event_queue);
	else if (event.Event_Type == EventType.END_POINT)
		handle_end(event, sweep_line_status, event_queue);
	else
		handle_intersection(
			event,
			sweep_line_status,
			event_queue,
			line_intersections
		);
}

function cmp_points_tuples(t1, t2) {
	// """
	// comparison function to compare two points from a tuple containing the point and line segments intersecting at that point
	// :param t1: first tuples
	// :param t2: second typle
	// :return: 0 if points are the same. 1 if the first tuple is greater than the second -1 if otherwise
	// """
	if (
		parseFloat(t1[0].X.toFixed(5)) == parseFloat(t2[0].X.toFixed(5)) &&
		parseFloat(t1[0].Y.toFixed(5)) == parseFloat(t2[0].Y.toFixed(5))
	)
		return 0;
	else return t1[0].X > t2[0].X ? 1 : -1;
}

function cmp_points(p1, p2) {
	// """
	// compares two points
	// :param p1: first point
	// :param p2: second point
	// :return: 0 if two points are same upto 5 places after decimal
	// """
	if (parseFloat(p1.X.toFixed(5)) == parseFloat(p2.X.toFixed(5)) && parseFloat(p1.Y.toFixed(5)) == parseFloat(p2.Y.toFixed(5)))
		return 0;
	else return p1.X > p2.X ? 1 : -1;
}

function update_all_lines(line_segments, sweep_line_status) {
	// """
	// sets the current y value for the line segments based on the current x vlaue in the sweep line status
	// :param line_segments: list of line segments to update
	// :param sweep_line_status: sweep line status
	// :return: None
	// """
	for (let line_segment of line_segments)
		if (
			line_segment.Point1.X <= sweep_line_status.X &&
			sweep_line_status.X <= line_segment.Point2.X
		)
			line_segment.set_curr_y(sweep_line_status.X);
}

function find_intersections(line_segments) {
	// """
	// find the intersections between all the line segments using the plane sweep algorithm
	// :param line_segments: list of line segments to find the intersections for
	// :return: list of intersections between these lines
	// """
	let line_intersections = new TreeSet();
	line_intersections.compareFunc = cmp_points;
	let event_queue = new TreeSet();
	event_queue.compareFunc = cmp_event;
	let sweep_line_status = new SweepLineStatus(cmp_line);

	for (let line_segment of line_segments) {
		let points = line_segment.get_points();

		event_queue.add(new MyEvent(points[0], EventType.START_POINT));
		event_queue.add(new MyEvent(points[1], EventType.END_POINT));
	}

	while (event_queue.size != 0) {
		s = "["
		// if (DEBUG_MODE) console.log("[ ", (end = ""));
		if (DEBUG_MODE)
			for (let event of event_queue)
				s+=event.toString() + ", "
				// console.log(event.toString(), (end = ", "));
		s+=" ]"
		if (DEBUG_MODE) console.log(s);
		let forward_event_iterator = event_queue.begin();
		let event = forward_event_iterator.key;
		event_queue.erase(forward_event_iterator);

		// # if event.event_type != EventType.INTERSECTION:
		sweep_line_status.set_status(event.Point.X);
		update_all_lines(line_segments, sweep_line_status);
		handle_event(event, event_queue, sweep_line_status, line_intersections);
	}
	return line_intersections;
}

function find_intersections_brute_force(line_segments) {
	// """
	// finds the intersections between every line using the brute force approach
	// :param line_segments: list of line segments to find the intersections for
	// :return: list of line intersections
	// """
	let intersections = [];
	for (let l1 of line_segments)
		for (let l2 of line_segments)
			if (l1 != l2) {
				let [intersecting_in_range, intersection_point] =
					check_if_intersecting_in_range(l1, l2);
				if (intersecting_in_range)
					intersections.push([intersection_point, l1.Name, l2.Name]);
			}
	let line_intersections = new TreeSet();
	line_intersections.compareFunc = cmp_points_tuples;

	for (let intersection of intersections) line_intersections.add(intersection);
	for (let point of line_intersections)
		if (DEBUG_MODE) console.log(point[0], point[1], point[2]);
}

function main() {
	// ""5
	// driver function
	// :return: None
	// """
	/* 
		10
		10 57 79 46
		12 32 95 19
		44 8 14 70
		97 74 68 17
		43 25 14 65
		61 11 16 6
		26 94 53 31
		100 53 25 21
		81 99 16 98
		35 78 70 93 
	*/
	let line_segments = [
		new LineSegment(
			new Point(10, 57, EventType.START_POINT),
			new Point(79, 46, EventType.END_POINT),
			"line0"
		),
		new LineSegment(
			new Point(12, 32, EventType.START_POINT),
			new Point(95, 19, EventType.END_POINT),
			"line1"
		),
		new LineSegment(
			new Point(44, 8, EventType.START_POINT),
			new Point(14, 70, EventType.END_POINT),
			"line2"
		),
		new LineSegment(
			new Point(97, 74, EventType.START_POINT),
			new Point(68, 17, EventType.END_POINT),
			"line3"
		),
		new LineSegment(
			new Point(43, 25, EventType.START_POINT),
			new Point(14, 65, EventType.END_POINT),
			"line4"
		),
		new LineSegment(
			new Point(61, 11, EventType.START_POINT),
			new Point(16, 6, EventType.END_POINT),
			"line5"
		),
		new LineSegment(
			new Point(26, 94, EventType.START_POINT),
			new Point(53, 31, EventType.END_POINT),
			"line6"
		),
		new LineSegment(
			new Point(100, 53, EventType.START_POINT),
			new Point(25, 21, EventType.END_POINT),
			"line7"
		),
		new LineSegment(
			new Point(81, 99, EventType.START_POINT),
			new Point(16, 98, EventType.END_POINT),
			"line8"
		),
		new LineSegment(
			new Point(35, 78, EventType.START_POINT),
			new Point(70, 93, EventType.END_POINT),
			"line9"
		),
	];

	for (let line of line_segments) {
		line.Point1.Segment = line;
		line.Point2.Segment = line;
	}

	let intersections = find_intersections(line_segments);
	// # find_intersections_brute_force(line_segments)
	// console.log("intersection points:")
	// for (const point of intersections) console.log(point);
	// let it = intersections.begin();
	let div_to_show_intersections = document.getElementById(
		"intersection_points"
	);
	div_to_show_intersections.innerText = "Intersection Points:\n";
	for (
		let it = intersections.begin();
		!it.equals(intersections.end());
		it.next()
	) {
		div_to_show_intersections.innerText += `${it.key}\n`;
		console.log(`key: ${it.key}, value: ${it.value}`);
	}

	// plot_lines_and_intersections(line_segments, intersections)
}

function showGraph() {
	/* 
		10 57 79 46
		12 32 95 19
		44 8 14 70
		97 74 68 17
		43 25 14 65
		61 11 16 6
		26 94 53 31
		100 53 25 21
		81 99 16 98
		35 78 70 93 
		 */
	const s = (p) => {
		let x = 100;
		let y = 100;

		p.setup = function () {
			p.createCanvas(700, 550);
		};

		p.draw = function () {
			p.background(0);
			p.fill(255);
			// p.rect(x, y, 50, 50);
			p.stroke(255);
			p.line(10 * 5, 57 * 5, 79 * 5, 46 * 5);
			p.line(12 * 5, 32 * 5, 95 * 5, 19 * 5);
			p.line(44 * 5, 8 * 5, 14 * 5, 70 * 5);
			p.line(97 * 5, 74 * 5, 68 * 5, 17 * 5);
			p.line(43 * 5, 25 * 5, 14 * 5, 65 * 5);
			p.line(61 * 5, 11 * 5, 16 * 5, 6 * 5);
			p.line(26 * 5, 94 * 5, 53 * 5, 31 * 5);
			p.line(100 * 5, 53 * 5, 25 * 5, 21 * 5);
			p.line(81 * 5, 99 * 5, 16 * 5, 98 * 5);
			p.line(35 * 5, 78 * 5, 70 * 5, 93 * 5);
		};
	};

	let myp5 = new p5(s, "plot_graph");
}

// main();
