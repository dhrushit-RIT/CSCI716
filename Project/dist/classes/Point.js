export class Point {
    constructor(x, y, point_type) {
        this.x = x;
        this.y = y;
        this.pointType = point_type;
        this.lineSegment = undefined;
    }
    get X() {
        return this.x;
    }
    get Y() {
        return this.y;
    }
    get LineSegment() {
        return this.lineSegment;
    }
    set_segment(line) {
        this.lineSegment = line;
    }
    toString() {
        return "{" + this.x + ", " + this.y + "}";
    }
}
//# sourceMappingURL=Point.js.map