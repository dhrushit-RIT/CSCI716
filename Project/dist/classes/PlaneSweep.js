import { TreeSet } from "./../../node_modules/jstreemap";
import { SweepLineStatus } from "./SweepLineStatus";
import { Point } from "./Point";
import { EventType } from "./EventType";
import { LineSegment } from "./LineSegment";
import { MyEvent } from "./MyEvent";
function cmp_event(e1, e2) {
    if (e1.Point.X < e2.Point.X) {
        return -1;
    }
    else if (e1.Point.X > e2.Point.X) {
        return 1;
    }
    else {
        if (e1.Event_Type == EventType.INTERSECTION &&
            e2.Event_Type != EventType.INTERSECTION) {
            return -1;
        }
        else if (e2.Event_Type == EventType.INTERSECTION &&
            e1.Event_Type != EventType.INTERSECTION) {
            return 1;
        }
        else {
            if (e1.Event_Type == EventType.START_POINT &&
                e2.Event_Type == EventType.END_POINT) {
                return -1;
            }
            else if (e1.Event_Type == EventType.END_POINT &&
                e2.Event_Type == EventType.START_POINT) {
                return 1;
            }
            else {
                if (e1.Point.LineSegment != e2.Point.LineSegment) {
                    if (e1.Point.LineSegment.get_other_point(e1.Point).X <
                        e2.Point.LineSegment.get_other_point(e2.Point).X) {
                        return -1;
                    }
                    else {
                        return 1;
                    }
                }
                else {
                    return 0;
                }
            }
        }
    }
}
function cmp_line(l1, l2) {
    let y_1 = l1.CurrY.toFixed(5);
    let y_2 = l2.CurrY.toFixed(5);
    if (y_1 < y_2)
        return -1;
    else if (y_1 > y_2)
        return 1;
    else if (l1 == l2)
        return 0;
    else {
        let y_1_prev = l1.PrevY.toFixed(5);
        let y_2_prev = l2.PrevY.toFixed(5);
        if (y_1_prev != null && y_2_prev != null)
            if (y_1_prev > y_2_prev)
                return -1;
            else if (y_1_prev < y_2_prev)
                return 1;
            else
                return 0;
        else
            return 1;
    }
}
function check_if_intersecting_in_range(l1, l2) {
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
    let t1_in_range = t1_denominator != 0 &&
        0 <= t1_numerator / t1_denominator &&
        t1_numerator / t1_denominator <= 1;
    let t2_in_range = t2_denominator != 0 &&
        0 <= t2_numerator / t2_denominator &&
        t2_numerator / t2_denominator <= 1;
    let intersection_point = null;
    if (t1_in_range && t2_in_range) {
        t1 = t1_numerator / t1_denominator;
        t2 = t2_numerator / t2_denominator;
        intersection_point = new Point(x1 + t1 * (x2 - x1), y1 + t1 * (y2 - y1), EventType.INTERSECTION);
    }
    return [t1_in_range && t2_in_range, intersection_point];
}
function check_for_intersection(event_queue, l1, l2, sweep_line_status) {
    let [intersecting_in_range, intersection_point] = check_if_intersecting_in_range(l1, l2);
    if (intersecting_in_range) {
        if (intersection_point.X > sweep_line_status.X) {
            let intersection_event = new MyEvent(intersection_point, EventType.INTERSECTION);
            let lines_sorted_by_y = [l1, l2].sort((a, b) => b.CurrY - a.CurrY);
            intersection_event.set_event_lines(lines_sorted_by_y);
            if (!event_queue.has(intersection_event)) {
                event_queue.add(intersection_event);
            }
        }
    }
}
function handle_start(event, sweep_line_status, event_queue) {
    sweep_line_status.OrderedBST.add(event.Point.LineSegment);
    const next_itr = sweep_line_status.OrderedBST.find(event.Point.LineSegment);
    next_itr.next();
    let successor_line = next_itr.key;
    if (successor_line)
        check_for_intersection(event_queue, event.Point.LineSegment, successor_line, sweep_line_status);
    const prev_itr = sweep_line_status.OrderedBST.find(event.Point.LineSegment);
    prev_itr.prev();
    let predecessor_line = prev_itr.key;
    if (predecessor_line)
        check_for_intersection(event_queue, event.Point.LineSegment, predecessor_line, sweep_line_status);
}
function handle_end(event, sweep_line_status, event_queue) {
    let line_to_remove = event.Point.LineSegment;
    const prev_itr = sweep_line_status.OrderedBST.find(line_to_remove);
    prev_itr.prev();
    let predecessor_line = prev_itr.key;
    const next_itr = sweep_line_status.OrderedBST.find(line_to_remove);
    next_itr.next();
    let successor_line = next_itr.key;
    sweep_line_status.OrderedBST.delete(line_to_remove);
    if (predecessor_line && successor_line)
        check_for_intersection(event_queue, predecessor_line, successor_line, sweep_line_status);
}
function handle_intersection(event, sweep_line_status, event_queue, line_intersections) {
    let l0 = event.Lines[0];
    let l1 = event.Lines[1];
    sweep_line_status.OrderedBST.delete(l0);
    sweep_line_status.OrderedBST.delete(l1);
    sweep_line_status.OrderedBST.add(l1);
    sweep_line_status.OrderedBST.add(l0);
    const prev_itr = sweep_line_status.OrderedBST.find(l1);
    prev_itr.prev();
    let new_predecessor_of_l1 = prev_itr.key;
    if (new_predecessor_of_l1)
        check_for_intersection(event_queue, l1, new_predecessor_of_l1, sweep_line_status);
    const next_itr = sweep_line_status.OrderedBST.find(l0);
    next_itr.next();
    let new_successor_of_l0 = next_itr.key;
    if (new_successor_of_l0)
        check_for_intersection(event_queue, l0, new_successor_of_l0, sweep_line_status);
    line_intersections.add(event.Point);
}
function handle_event(event, event_queue, sweep_line_status, line_intersections) {
    if (event.Event_Type == EventType.START_POINT)
        handle_start(event, sweep_line_status, event_queue);
    else if (event.Event_Type == EventType.END_POINT)
        handle_end(event, sweep_line_status, event_queue);
    else
        handle_intersection(event, sweep_line_status, event_queue, line_intersections);
}
function cmp_points_tuples(t1, t2) {
    if (t1[0].X.toFixed(5) == t2[0].X.toFixed(5) &&
        t1[0].Y.toFixed(5) == t2[0].Y.toFixed(5))
        return 0;
    else
        return t1[0].X > t2[0].X ? 1 : -1;
}
function cmp_points(p1, p2) {
    if (p1.X.toFixed(5) == p2.X.toFixed(5) && p1.Y.toFixed(5) == p2.Y.toFixed(5))
        return 0;
    else
        return p1.X > p2.X ? 1 : -1;
}
function update_all_lines(line_segments, sweep_line_status) {
    for (let line_segment of line_segments)
        if (line_segment.Point1.X <= sweep_line_status.X &&
            sweep_line_status.X <= line_segment.Point2.X)
            line_segment.set_curr_y(sweep_line_status.X);
}
function find_intersections(line_segments) {
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
        let forward_event_iterator = event_queue.begin();
        let event = forward_event_iterator.key;
        event_queue.erase(forward_event_iterator);
        sweep_line_status.set_status(event.Point.X);
        update_all_lines(line_segments, sweep_line_status);
        handle_event(event, event_queue, sweep_line_status, line_intersections);
    }
    return line_intersections;
}
function find_intersections_brute_force(line_segments) {
    let intersections = [];
    for (let l1 of line_segments)
        for (let l2 of line_segments)
            if (l1 != l2) {
                let [intersecting_in_range, intersection_point] = check_if_intersecting_in_range(l1, l2);
                if (intersecting_in_range)
                    intersections.push([intersection_point, l1.Name, l2.Name]);
            }
    let line_intersections = new TreeSet();
    line_intersections.compareFunc = cmp_points_tuples;
    for (let intersection of intersections)
        line_intersections.add(intersection);
}
function main() {
    let line_segments = [
        new LineSegment(new Point(10, 57, EventType.START_POINT), new Point(79, 46, EventType.END_POINT)),
        new LineSegment(new Point(12, 32, EventType.START_POINT), new Point(95, 19, EventType.END_POINT)),
        new LineSegment(new Point(44, 8, EventType.START_POINT), new Point(14, 70, EventType.END_POINT)),
        new LineSegment(new Point(97, 74, EventType.START_POINT), new Point(68, 17, EventType.END_POINT)),
        new LineSegment(new Point(43, 25, EventType.START_POINT), new Point(14, 65, EventType.END_POINT)),
        new LineSegment(new Point(61, 11, EventType.START_POINT), new Point(16, 6, EventType.END_POINT)),
        new LineSegment(new Point(26, 94, EventType.START_POINT), new Point(53, 31, EventType.END_POINT)),
        new LineSegment(new Point(100, 53, EventType.START_POINT), new Point(25, 21, EventType.END_POINT)),
        new LineSegment(new Point(81, 99, EventType.START_POINT), new Point(16, 98, EventType.END_POINT)),
        new LineSegment(new Point(35, 78, EventType.START_POINT), new Point(70, 93, EventType.END_POINT)),
    ];
    let intersections = find_intersections(line_segments);
    for (const point of intersections)
        console.log(point);
    print();
}
main();
//# sourceMappingURL=PlaneSweep.js.map