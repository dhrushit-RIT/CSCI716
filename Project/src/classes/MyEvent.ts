import { EventType } from "./EventType";
import { LineSegment } from "./LineSegment";
import { Point } from "./Point";

export class MyEvent {
	// """
	// defines the events class
	// point : the point associated with this event
	// event_type : the type of event (EventType)
	// lines : set if the point is an intersection point
	// """
	private point;
	private event_type;
	private lines:LineSegment[];

	constructor(point: Point, event_type: EventType) {
		this.point = point;
		this.event_type = event_type;
		this.lines = undefined;
	}

	set_event_lines(lines: LineSegment[]) {
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
				this.lines.sort((a, b) => (a.CurrY > b.CurrY ? 1 : -1));
			}
		}
	}

	get Point(): Point {
		return this.point;
	}

	get Event_Type(): EventType {
		return this.event_type;
	}

	get Lines(): LineSegment[]{
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
