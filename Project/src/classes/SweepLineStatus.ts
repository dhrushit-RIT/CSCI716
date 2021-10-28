// import jstreemap  from './../../node_modules/jstreemap';
import { TreeSet, TreeMap, TreeMultiSet, TreeMultiMap } from "jstreemap";
import { LineSegment } from "./LineSegment";

export class SweepLineStatus {
	// """
	// sweep line status class
	// ordered_BST: the ordered BST that holds the line segments in order
	// x : the current value of x when processing a given event
	// """
	private ordered_BST: TreeSet<LineSegment>;
	private x: number;

	toString() {
		return this.x + " " + this.ordered_BST;
	}

	constructor(comp: (l1: LineSegment, l2: LineSegment) => 0 | 1 | -1) {
		this.ordered_BST = new TreeSet<LineSegment>();
		this.ordered_BST.compareFunc = comp;
		this.x = -9999999999;
	}

	get OrderedBST(): TreeSet<LineSegment> {
		return this.ordered_BST;
	}

	get X(): number {
		return this.x;
	}

	set_status(x: number) {
		this.x = x;
	}

	get_sequenced_line_segments(l1: LineSegment, l2: LineSegment) {
		if (this.ordered_BST.has(l1) && this.ordered_BST.has(l2)) {
			let iterator_l1 = this.ordered_BST.find(l1);
			iterator_l1.prev();
			if (iterator_l1.key == l2) {
				return [l2, l1];
			} else {
				return [l1, l2];
			}
		}
	}
}
