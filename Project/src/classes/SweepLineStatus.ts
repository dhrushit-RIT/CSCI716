class SweepLineStatus {
	// """
	// sweep line status class
	// ordered_BST: the ordered BST that holds the line segments in order
	// x : the current value of x when processing a given event
	// """
	private ordered_BST: TreeSet;
	private x: number;

	toString() {
		return this.x + " " + this.ordered_BST;
	}

	constructor(comp) {
		this.ordered_BST = new TreeSet(comp);
		this.x = -9999999999;
	}

	get OrderedBST(): TreeSet {
		return this.ordered_BST;
	}

	get X(): number {
		return this.x;
	}

	set_status(x: number) {
		this.x = x;
	}

	get_sequenced_line_segments(l1: LineSegment, l2: LineSegment) {
		if (this.ordered_BST.contains(l1) && this.ordered_BST.contains(l2)) {
			if (this.ordered_BST.lower(l1) == l2) {
				return [l2, l1];
			} else {
				return [l1, l2];
			}
		}
	}
}
