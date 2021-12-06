var DEBUG_MODE = true;
var autoNext = true;
var line_segments = [];

var scaleDownFactor = 0.8;
var timeout = 1000;

var newIntersectingLines = [];
var newIntersectingPoint = null;
var newIntersectionEvent = null;

var myp5;
var intersectionPoints = [];
var svgsl;
var svgeq;
var sweepline_x = 0;

var highlightLine = new LineSegment(
	new Point(0, 0, "highlightLine"),
	new Point(0, 0, "highlightLine")
);

var event_point = new Point(0, 0, null);

var event_queue_history = [];
var sweep_line_status_history = [];

function toggleAutoNext() {
	const elem = document.getElementById("autoNext");
	autoNext = elem.checked;
}

function reset_all() {
	scaleDownFactor = 0.8;
	intersectionPoints = [];
	sweepline_x = 0;

	sweepLineToHighlight = new LineSegment(
		new Point(0, 0, "highlightLine"),
		new Point(0, 0, "highlightLine")
	);

	event_point = new Point(0, 0, null);

	event_queue_history = [];
	sweep_line_status_history = [];
	myp5.draw();
	document.getElementById("resetBtn").disabled = true;
	document.getElementById("nextBtn").disabled = false;
	document.getElementById("runAlgorithm").disabled = false;
	document.getElementById("showgraph").disabled = true;

	let div_to_show_intersections = document.getElementById(
		"intersection_points"
	);
	div_to_show_intersections.innerText = "";
}

function describeAlgorithm(text) {
	const desc_box = document.getElementById("algorithm_description");
	desc_box.innerText = text;
}

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

function handleFiles(files) {
	let file = this.files[0];

	const reader = new FileReader();
	reader.onload = function (fileContent) {
		afterFileLoads(fileContent.target.result);
	};
	reader.readAsText(file);
}

function afterFileLoads(content) {
	line_segments = [];
	let lines = content.split("\n").map((item) => item.trim());
	lines = lines.slice(1);
	makeLines(lines);
	document.getElementById("showgraph").disabled = false;
	let div_to_show_intersections = document.getElementById(
		"intersection_points"
	);
	div_to_show_intersections.innerText = "";
}

function makeLines(lineStrArr) {
	let lineIndex = 0;
	for (let line of lineStrArr) {
		if (!line) {
			continue;
		}
		const points = line.split(/\s/).map((item) => parseFloat(item));
		line_segments.push(
			new LineSegment(
				new Point(points[0], points[1], EventType.START_POINT),
				new Point(points[2], points[3], EventType.END_POINT),
				"L" + lineIndex
			)
		);
		lineIndex++;
	}
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
				drawEventLineTree(event_queue.__t.head.root);
				newIntersectionEvent = intersection_event;
				newIntersectingPoint = intersection_point;
			}
		}
	}
}

async function handle_start(event, sweep_line_status, event_queue) {
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
	drawSweepLineTree(sweep_line_status.ordered_BST.__t.head.root);
	await awaitNextBtnOrTimeout();
	if (DEBUG_MODE) console.log(sweep_line_status.toString());
	// # check if it intersects with successor
	const next_itr = sweep_line_status.OrderedBST.find(event.Point.LineSegment);
	next_itr.next();
	let successor_line = next_itr.key;
	if (successor_line) {
		check_for_intersection(
			event_queue,
			event.Point.LineSegment,
			successor_line,
			sweep_line_status
		);

		newIntersectingLines = [event.Point.LineSegment, successor_line];
		myp5.draw();

		describeAlgorithm("check intersection with successor line");
		await awaitNextBtnOrTimeout();

		newIntersectingLines = [];
		newIntersectingPoint = null;
		newIntersectionEvent = null;
		myp5.draw();
	}

	// # check if it intersects with predecessor
	const prev_itr = sweep_line_status.OrderedBST.find(event.Point.LineSegment);
	prev_itr.prev();
	let predecessor_line = prev_itr.key;
	if (predecessor_line) {
		check_for_intersection(
			event_queue,
			event.Point.LineSegment,
			predecessor_line,
			sweep_line_status
		);

		newIntersectingLines = [event.Point.LineSegment, predecessor_line];
		myp5.draw();

		describeAlgorithm("check intersection with predecessor line");
		await awaitNextBtnOrTimeout();

		newIntersectingLines = [];
		newIntersectingPoint = null;
		newIntersectionEvent = null;
		myp5.draw();
	}
}

function awaitNextBtnOrTimeout() {
	return new Promise((resolve, reject) => {
		var nextbutton = document.getElementById("nextBtn");
		if (autoNext) {
			setTimeout(() => resolve(), timeout);
		} else {
			Rx.Observable.fromEvent(nextbutton, "click").subscribe(() => resolve());
		}
	});
}

async function handle_end(event, sweep_line_status, event_queue) {
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
	if (predecessor_line && successor_line) {
		check_for_intersection(
			event_queue,
			predecessor_line,
			successor_line,
			sweep_line_status
		);
		newIntersectingLines = [predecessor_line, successor_line];
		myp5.draw();

		describeAlgorithm(
			"END POINT : check intersection between predecessor and successor"
		);
		await awaitNextBtnOrTimeout();

		newIntersectingLines = [];
		newIntersectingPoint = null;
		newIntersectionEvent = null;
		myp5.draw();
	}
}

async function handle_intersection(
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
	// drawSweepLineTree(sweep_line_status.ordered_BST.__t.head.root);
	highlightSweeptNode(l0, "lightblue");
	highlightSweeptNode(l1, "lightgreen");
	describeAlgorithm("INTERSECTION EVENT: Swapping the line order");
	await awaitNextBtnOrTimeout();

	sweep_line_status.OrderedBST.delete(l0);
	sweep_line_status.OrderedBST.delete(l1);
	if (DEBUG_MODE) console.log(sweep_line_status.toString());
	// # l0.set_curr_y(sweep_line_status.x)
	// # l1.set_curr_y(sweep_line_status.x)
	sweep_line_status.OrderedBST.add(l1);
	sweep_line_status.OrderedBST.add(l0);
	if (DEBUG_MODE) console.log(sweep_line_status.toString());

	drawSweepLineTree(sweep_line_status.ordered_BST.__t.head.root);
	await new Promise((resolve, reject) => {
		setTimeout(() => {
			resolve();
		}, 10);
	});
	highlightSweeptNode(l0, "lightblue");
	highlightSweeptNode(l1, "lightgreen");
	describeAlgorithm("INTERSECTION EVENT: Line order swapped");
	await awaitNextBtnOrTimeout();
	drawSweepLineTree(sweep_line_status.ordered_BST.__t.head.root);
	// # remove all the events from the queue
	// # add all of them with the reversed order for the intersection point lines
	// # check if after reversal, there is an intersection
	const prev_itr = sweep_line_status.OrderedBST.find(l1);
	prev_itr.prev();
	let new_predecessor_of_l1 = prev_itr.key;
	if (new_predecessor_of_l1) {
		check_for_intersection(
			event_queue,
			l1,
			new_predecessor_of_l1,
			sweep_line_status
		);

		newIntersectingLines = [l1, new_predecessor_of_l1];
		myp5.draw();

		describeAlgorithm(
			"INTERSECTION EVENT: check intersection with new predecessor"
		);
		await awaitNextBtnOrTimeout();

		newIntersectingLines = [];
		newIntersectingPoint = null;
		newIntersectionEvent = null;
		myp5.draw();
	}
	const next_itr = sweep_line_status.OrderedBST.find(l0);
	next_itr.next();
	let new_successor_of_l0 = next_itr.key;
	if (new_successor_of_l0) {
		check_for_intersection(
			event_queue,
			l0,
			new_successor_of_l0,
			sweep_line_status
		);

		newIntersectingLines = [l0, new_successor_of_l0];
		myp5.draw();

		describeAlgorithm(
			"INTERSECTION EVENT: check intersection with new successor"
		);
		await awaitNextBtnOrTimeout();

		newIntersectingLines = [];
		newIntersectingPoint = null;
		newIntersectionEvent = null;
		myp5.draw();
	}
	line_intersections.add(event.Point);
	intersectionPoints.push(event.Point);
	myp5.draw();
}

async function handle_event(
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
		await handle_start(event, sweep_line_status, event_queue);
	else if (event.Event_Type == EventType.END_POINT)
		await handle_end(event, sweep_line_status, event_queue);
	else
		await handle_intersection(
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
	if (
		parseFloat(p1.X.toFixed(5)) == parseFloat(p2.X.toFixed(5)) &&
		parseFloat(p1.Y.toFixed(5)) == parseFloat(p2.Y.toFixed(5))
	)
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

function drawEventLineTree(eq) {
	let treeData = [buildCustomTree(eq)];
	var margin = { top: 20, right: 120, bottom: 20, left: 120 },
		width = 960 - margin.right - margin.left,
		height = 500 - margin.top - margin.bottom;

	var i = 0,
		duration = 0,
		root;

	var tree = d3.layout.tree().size([height, width]);

	var diagonal = d3.svg.diagonal().projection(function (d) {
		return [d.y, d.x];
	});

	// var svg; // = d3.select("body svg");
	// if (!svg)
	if (svgeq) {
		svgeq.selectAll("*").remove();
	}
	svgeq =
		svgeq ||
		d3
			.select("#myTreeEvent")
			.append("svg")
			.attr("width", width + margin.right + margin.left)
			.attr("height", height + margin.top + margin.bottom)
			.append("g")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
	// svg.selectAll("*").remove();
	// else
	// 	svg = d3.select("body svg")

	root = treeData[0];
	root.x0 = height / 2;
	root.y0 = 0;

	update(root);

	d3.select(self.frameElement).style("height", "500px");

	function update(source) {
		// d3.select("div.parent").html("");
		// d3.selectAll("g.node").selectAll("*").remove();
		// d3.selectAll("g.path.link").selectAll("*").remove();
		// Compute the new tree layout.
		var nodes = tree.nodes(root).reverse(),
			links = tree.links(nodes);

		// Normalize for fixed-depth.
		nodes.forEach(function (d) {
			d.y = d.depth * 100;
		});

		// Update the nodes…
		var node = svgeq.selectAll("g.node").data(nodes, function (d) {
			return d.id || (d.id = ++i);
		});

		// Enter any new nodes at the parent's previous position.
		var nodeEnter = node
			.enter()
			.append("g")
			.attr("class", "node")
			.attr("transform", function (d) {
				return "translate(" + source.y0 + "," + source.x0 + ")";
			})
			.on("click", click);

		// node.exit().remove();

		nodeEnter
			.append("circle")
			.attr("r", 1e-6)
			.style("fill", function (d) {
				return d._children ? "lightsteelblue" : "#fff";
			});

		nodeEnter
			.append("text")
			.attr(
				"x",
				0 /* function (d) {
				return d.children || d._children ? -13 : 13;
			} */
			)
			.attr("dy", ".35em")
			.attr(
				"text-anchor",
				"middle" /* function (d) {
						return d.children || d._children ? "end" : "start";
					} */
			)
			.text(function (d) {
				return d.name;
			})
			.style("fill-opacity", 1e-6);

		// Transition nodes to their new position.
		var nodeUpdate = node
			.transition()
			.duration(duration)
			.attr("transform", function (d) {
				return "translate(" + d.y + "," + d.x + ")";
			});

		nodeUpdate
			.select("circle")
			.attr("r", 25)
			.style("fill", function (d) {
				return d._children ? "lightsteelblue" : "#fff";
			});

		nodeUpdate
			.select("text")
			.style("fill-opacity", 1)
			.style("text-anchor", "middle");

		// Transition exiting nodes to the parent's new position.
		var nodeExit = node
			.exit()
			.transition()
			.duration(duration)
			.attr("transform", function (d) {
				return "translate(" + source.y + "," + source.x + ")";
			})
			.remove();

		nodeExit.select("circle").attr("r", 1e-6);

		nodeExit.select("text").style("fill-opacity", 1e-6);

		// Update the links…
		var link = svgeq.selectAll("path.link").data(links, function (d) {
			return d.target.id;
		});

		// Enter any new links at the parent's previous position.
		link
			.enter()
			.insert("path", "g")
			.attr("class", "link")
			.attr("d", function (d) {
				var o = { x: source.x0, y: source.y0 };
				return diagonal({ source: o, target: o });
			});

		// Transition links to their new position.
		link.transition().duration(duration).attr("d", diagonal);

		// Transition exiting nodes to the parent's new position.
		link
			.exit()
			.transition()
			.duration(duration)
			.attr("d", function (d) {
				var o = { x: source.x, y: source.y };
				return diagonal({ source: o, target: o });
			})
			.remove();

		// Stash the old positions for transition.
		nodes.forEach(function (d) {
			d.x0 = d.x;
			d.y0 = d.y;
		});
	}

	// Toggle children on click.
	function click(d) {
		if (d.children) {
			d._children = d.children;
			d.children = null;
		} else {
			d.children = d._children;
			d._children = null;
		}
		update(d);
	}
}

function highlightEventNode(node) {
	svgeq.selectAll("g.node").forEach((n) => {
		for (let nd of n) {
			if (nd.textContent == node.toString()) {
				nd.children[0].style.fill = "red";
			}
		}
	});
}

function highlightSweeptNode(node, color) {
	svgsl.selectAll("g.node").forEach((n) => {
		for (let nd of n) {
			if (nd.textContent == node.toString()) {
				nd.children[0].style.fill = color;
			}
		}
	});
}

async function find_intersections(line_segments) {
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

	await awaitNextBtnOrTimeout();

	for (let line_segment of line_segments) {
		let points = line_segment.get_points();

		event_queue.add(new MyEvent(points[0], EventType.START_POINT));
		event_queue.add(new MyEvent(points[1], EventType.END_POINT));

		highlightLine = line_segment;
		myp5.draw();

		let eqListElement = document.getElementById("eventQueueList");
		eqListElement.innerText = event_queue.toString();

		drawEventLineTree(event_queue.__t.head.root);

		describeAlgorithm("adding line segment " + line_segment.toString());
		await awaitNextBtnOrTimeout();
	}
	highlightLine = new LineSegment(
		new Point(0, 0, "highlightLine"),
		new Point(0, 0, "highlightLine")
	);

	while (event_queue.size != 0) {
		s = "[ ";
		// if (DEBUG_MODE) console.log("[ ", (end = ""));
		if (DEBUG_MODE) for (let event of event_queue) s += event.toString() + ", ";
		// console.log(event.toString(), (end = ", "));
		s += " ]";
		if (DEBUG_MODE) console.log(s);
		let forward_event_iterator = event_queue.begin();
		let event = forward_event_iterator.key;

		highlightEventNode(event);

		event_point = event.Point;
		sweep_line_status.set_status(event.Point.X);
		sweepline_x = event.Point.X;
		myp5.draw();
		describeAlgorithm("processing event: " + event.toString());
		await awaitNextBtnOrTimeout();

		event_queue.erase(forward_event_iterator);

		// # if event.event_type != EventType.INTERSECTION:
		update_all_lines(line_segments, sweep_line_status);
		await handle_event(
			event,
			event_queue,
			sweep_line_status,
			line_intersections
		);
		drawSweepLineTree(sweep_line_status.ordered_BST.__t.head.root);
		drawEventLineTree(event_queue.__t.head.root);

		const eqListElement = document.getElementById("eventQueueList");
		eqListElement.innerText = event_queue.toString();
		const sweeplineListElement = document.getElementById("sweepLineList");
		sweeplineListElement.innerText = sweep_line_status.toString();

		// describeAlgorithm("");
		myp5.draw();
		await awaitNextBtnOrTimeout();
	}
	document.getElementById("nextBtn").disabled = true;
	return line_intersections;
}

function buildCustomTree(node) {
	if (node.id) {
		return [];
	}

	let newNode = {
		name: node.key.name || node.key.toString(),
		children: [],
	};

	if (!node.id) {
		newNode.parent = "null";
	}

	if (node.left != null && !node.left.id) {
		let left_child = buildCustomTree(node.left);
		left_child.parent = newNode.name;
		newNode.children.push(left_child);
	} /* else {
		newNode.children.push(null);
	} */

	if (node.right != null && !node.right.id) {
		let right_child = buildCustomTree(node.right);
		right_child.parent = newNode.name;
		newNode.children.push(right_child);
	} /* else {
		newNode.children.push(null);
	} */

	return newNode;
}

function drawSweepLineTree(ssl) {
	let treeData = [buildCustomTree(ssl)];
	var margin = { top: 20, right: 120, bottom: 20, left: 120 },
		width = 960 - margin.right - margin.left,
		height = 500 - margin.top - margin.bottom;

	var i = 0,
		duration = 0,
		root;

	var tree = d3.layout.tree().size([height, width]);

	var diagonal = d3.svg.diagonal().projection(function (d) {
		return [d.y, d.x];
	});

	// var svg; // = d3.select("body svg");
	// if (!svg)
	if (svgsl) {
		svgsl.selectAll("*").remove();
	}
	svgsl =
		svgsl ||
		d3
			.select("#myTreeSweep")
			.append("svg")
			.attr("width", width + margin.right + margin.left)
			.attr("height", height + margin.top + margin.bottom)
			.append("g")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
	// svg.selectAll("*").remove();
	// else
	// 	svg = d3.select("body svg")

	root = treeData[0];
	root.x0 = height / 2;
	root.y0 = 0;

	update(root);

	d3.select(self.frameElement).style("height", "500px");

	function update(source) {
		// d3.select("div.parent").html("");
		// d3.selectAll("g.node").selectAll("*").remove();
		// d3.selectAll("g.path.link").selectAll("*").remove();
		// Compute the new tree layout.
		var nodes = tree.nodes(root).reverse(),
			links = tree.links(nodes);

		// Normalize for fixed-depth.
		nodes.forEach(function (d) {
			d.y = d.depth * 100;
		});

		// Update the nodes…
		var node = svgsl.selectAll("g.node").data(nodes, function (d) {
			return d.id || (d.id = ++i);
		});

		// Enter any new nodes at the parent's previous position.
		var nodeEnter = node
			.enter()
			.append("g")
			.attr("class", "node")
			.attr("transform", function (d) {
				return "translate(" + source.y0 + "," + source.x0 + ")";
			})
			.on("click", click);

		// node.exit().remove();

		nodeEnter
			.append("circle")
			.attr("r", 1e-6)
			.style("fill", function (d) {
				return d._children ? "lightsteelblue" : "#fff";
			});

		nodeEnter
			.append("text")
			.attr(
				"x",
				0 /* function (d) {
				return d.children || d._children ? -13 : 13;
			} */
			)
			.attr("dy", ".35em")
			.attr(
				"text-anchor",
				"middle" /* function (d) {
						return d.children || d._children ? "end" : "start";
					} */
			)
			.text(function (d) {
				return d.name;
			})
			.style("fill-opacity", 1e-6);

		// Transition nodes to their new position.
		var nodeUpdate = node
			.transition()
			.duration(duration)
			.attr("transform", function (d) {
				return "translate(" + d.y + "," + d.x + ")";
			});

		nodeUpdate
			.select("circle")
			.attr("r", 25)
			.style("fill", function (d) {
				return d._children ? "lightsteelblue" : "#fff";
			});

		nodeUpdate
			.select("text")
			.style("fill-opacity", 1)
			.style("text-anchor", "middle");

		// Transition exiting nodes to the parent's new position.
		var nodeExit = node
			.exit()
			.transition()
			.duration(duration)
			.attr("transform", function (d) {
				return "translate(" + source.y + "," + source.x + ")";
			})
			.remove();

		nodeExit.select("circle").attr("r", 1e-6);

		nodeExit.select("text").style("fill-opacity", 1e-6);

		// Update the links…
		var link = svgsl.selectAll("path.link").data(links, function (d) {
			return d.target.id;
		});

		// Enter any new links at the parent's previous position.
		link
			.enter()
			.insert("path", "g")
			.attr("class", "link")
			.attr("d", function (d) {
				var o = { x: source.x0, y: source.y0 };
				return diagonal({ source: o, target: o });
			});

		// Transition links to their new position.
		link.transition().duration(duration).attr("d", diagonal);

		// Transition exiting nodes to the parent's new position.
		link
			.exit()
			.transition()
			.duration(duration)
			.attr("d", function (d) {
				var o = { x: source.x, y: source.y };
				return diagonal({ source: o, target: o });
			})
			.remove();

		// Stash the old positions for transition.
		nodes.forEach(function (d) {
			d.x0 = d.x;
			d.y0 = d.y;
		});
	}

	// Toggle children on click.
	function click(d) {
		if (d.children) {
			d._children = d.children;
			d.children = null;
		} else {
			d.children = d._children;
			d._children = null;
		}
		update(d);
	}
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

async function runIntersectionAlgorithm() {
	document.getElementById("nextBtn").disabled = false;
	document.getElementById("runAlgorithm").disabled = true;

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

	const linesStr =
		"10 57 79 46\n12 32 95 19\n44 8 14 70\n97 74 68 17\n43 25 14 65\n61 11 16 6\n26 94 53 31\n100 53 25 21\n81 99 16 98\n35 78 70 93";

	// makeLines(linesStr.split("\n"));

	for (let line of line_segments) {
		line.Point1.Segment = line;
		line.Point2.Segment = line;
	}

	let intersections = await find_intersections(line_segments);

	document.getElementById("resetBtn").disabled = false;
	let div_to_show_intersections = document.getElementById(
		"intersection_points"
	);
	sweepline_x = 700 * scaleDownFactor;
	event_point = new Point(700 * scaleDownFactor, 0, null);
	div_to_show_intersections.innerText = "Intersection Points:\n";
	for (
		let it = intersections.begin();
		!it.equals(intersections.end());
		it.next()
	) {
		div_to_show_intersections.innerText += `${it.key}\n`;
		intersectionPoints.push(it.key);
		console.log(`key: ${it.key}, value: ${it.value}`);
	}
}

function drawGraph() {
	myp5.draw();
}

function drawLines(p) {
	for (let line of line_segments) {
		p.line(
			line.Point1.X * scaleFactor,
			line.Point1.Y * scaleFactor,
			line.Point2.X * scaleFactor,
			line.Point2.Y * scaleFactor
		);
	}
}

function drawIntersectingPoints(p) {
	p.stroke("red");
	p.strokeWeight(16);
	for (let pt of intersectionPoints) {
		p.point(pt.x * scaleFactor, pt.y * scaleFactor);
	}
	p.strokeWeight(1);
}

function highlightSweepLine(p) {
	p.stroke("yellow");
	p.line(
		sweepline_x * 5 * scaleDownFactor,
		0,
		sweepline_x * 5 * scaleDownFactor,
		550 * scaleDownFactor
	);
}

function highlightEventPoint(p) {
	p.strokeWeight(16);
	p.point(
		event_point.X * 5 * scaleDownFactor,
		event_point.Y * 5 * scaleDownFactor
	);
}

function highlightLineSegment(p) {
	p.strokeWeight(5);
	p.line(
		highlightLine.Point1.X * scaleFactor,
		highlightLine.Point1.Y * scaleFactor,
		highlightLine.Point2.X * scaleFactor,
		highlightLine.Point2.Y * scaleFactor
	);
	p.strokeWeight(1);
}

function highlightIntersectingLines(p) {
	p.strokeWeight(5);
	p.stroke("blue");
	for (let line of newIntersectingLines) {
		p.line(
			line.Point1.X * scaleFactor,
			line.Point1.Y * scaleFactor,
			line.Point2.X * scaleFactor,
			line.Point2.Y * scaleFactor
		);
	}

	defaultStrokes(p);
}

function highlightNewIntersectionPoint(p) {
	if (newIntersectingPoint != null) {
		p.strokeWeight(15);
		p.stroke("green");
		p.point(
			newIntersectingPoint.X * 5 * scaleDownFactor,
			newIntersectingPoint.Y * 5 * scaleDownFactor
		);
		defaultStrokes(p);
	}
}

function hightlightNewIntersectionEvent(p) {
	if (!svgeq || !newIntersectionEvent) return;
	svgeq.selectAll("g.node").forEach((n) => {
		for (let nd of n) {
			if (nd.textContent == newIntersectionEvent.toString()) {
				nd.children[0].style.fill = "green";
			}
		}
	});
	// highlightEventNode(intersection_event);
}

function defaultStrokes(p) {
	p.stroke("white");
	p.strokeWeight(1);
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

	document.getElementById("runAlgorithm").disabled = false;

	const s = (p) => {
		let x = 100;
		let y = 100;

		p.setup = function () {
			p.createCanvas(700 * scaleDownFactor, 550 * scaleDownFactor);
		};

		p.draw = function () {
			p.clear();
			scaleFactor = 5 * scaleDownFactor;

			p.background(100);
			p.fill(255);
			p.stroke(255);

			drawLines(p);
			drawIntersectingPoints(p);

			highlightSweepLine(p);
			highlightEventPoint(p);

			highlightLineSegment(p);
			highlightIntersectingLines(p);
			highlightNewIntersectionPoint(p);
			hightlightNewIntersectionEvent(p);
		};
	};

	if (!myp5) myp5 = new p5(s, "plot_graph");
	else myp5.draw();
}
