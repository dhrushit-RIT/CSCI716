from typing import List, Set
from Trapezoid import Trapezoid

class TrapezoidHolder:
    lst: List[Trapezoid]
    trap_set: Set[Trapezoid]

    def __init__(self) -> None:
        self.lst = []
        self.trap_set = set()
        pass

    def add_or_get_trapezoid(self, trapezoid: Trapezoid):
        
        for trap in self.lst:
            if trap == trapezoid:
                return trap

        self.lst.append(trapezoid)
        return trapezoid
    
    def remove_trapezoid_from_lst(self, trapezoid: Trapezoid):
        trapezoid.parents = []
        for trap in self.lst:
            if trap == trapezoid:
                self.lst.remove(trap)

    def get_trapezoids(self):
        return self.lst