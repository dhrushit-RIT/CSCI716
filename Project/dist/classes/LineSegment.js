export class LineSegment {
    constructor(point1, point2, name = "") {
        this.point1 = point1;
        this.point2 = point2;
        if (this.point1.X > this.point2.X) {
            this.point1, (this.point2 = this.point2), this.point1;
        }
        if (this.point1.X - this.point2.X != 0) {
            this.slope =
                (this.point2.Y - this.point1.Y) / (this.point2.X - this.point1.X);
        }
        else {
            this.slope = undefined;
        }
        this.curr_y = undefined;
        this.prev_y = undefined;
        this.name = name;
        this.y_intercept =
            point1.Y - ((point2.Y - point1.Y) / (point2.X - point1.X)) * point1.X;
    }
    get_points() {
        return [this.point1, this.point2];
    }
    set_curr_y(x) {
        this.prev_y = this.curr_y;
        this.curr_y = this.slope * x + this.y_intercept;
    }
    get_curr_y() {
        return this.curr_y;
    }
    get_other_point(point) {
        if (point == this.point1) {
            return this.point2;
        }
        else {
            return this.point1;
        }
    }
    get CurrY() {
        return this.curr_y;
    }
    set CurrY(x) {
        this.prev_y = this.curr_y;
        this.curr_y = this.slope * x + this.y_intercept;
    }
    get PrevY() {
        return this.prev_y;
    }
    get Point1() {
        return this.point1;
    }
    get Point2() {
        return this.point2;
    }
    get Name() {
        return this.name;
    }
    toString() {
        return this.name;
    }
}
//# sourceMappingURL=LineSegment.js.map