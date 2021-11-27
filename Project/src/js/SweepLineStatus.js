class SweepLineStatus {
	// """
	// sweep line status class
	// ordered_BST: the ordered BST that holds the line segments in order
	// x : the current value of x when processing a given event
	// """
	ordered_BST;
	x;

	toString() {
		return "x:" + this.x.toFixed(3) + " | " + this.ordered_BST;
	}

	constructor(comp) {
		this.ordered_BST = new TreeSet();
		this.ordered_BST.compareFunc = comp;
		this.x = -9999999999;
	}

	get OrderedBST() {
		return this.ordered_BST;
	}

	get X() {
		return this.x;
	}

	set_status(x) {
		this.x = x;
	}

	get_sequenced_line_segments(l1, l2) {
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
