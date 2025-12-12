"""
Torsion Subgroup Finder

Implements Mazur's Torsion Theorem to enumerate all rational torsion points
on an elliptic curve over Q.

"""

from typing import List, Set, Dict
from fractions import Fraction
import math
from .elliptic_curve import EllipticCurve, Point

def _integer_divisors(n: int) -> Set[int]:
    n = abs(n)
    divs = set()
    for d in range(1, int(math.isqrt(n)) + 1):
        if n % d == 0:
            divs.add(d)
            divs.add(n // d)
    out = set()
    for d in divs:
        out.add(d)
        out.add(-d)
    return out

class TorsionFinder:
    """
    Finder for torsion points on elliptic curves.

    Uses Mazur's Theorem:
    - Z/nZ for n = 1,2,...,10,12
    - Z/2Z × Z/2nZ for n = 1,2,3,4
    """

    MAZUR_CYCLIC_ORDERS = [1,2,3,4,5,6,7,8,9,10,12]
    MAZUR_MAX_ORDER = 12

    def __init__(self, curve: EllipticCurve):
        self.curve = curve
        self.torsion_cache: Dict[Point, int] = {}

        if not curve.is_integral_model():
            raise ValueError("Nagell–Lutz requires integral Weierstrass model")

    def check_torsion(self, P: Point) -> Dict[str, any]:
        """
        Check if a point is torsion and return detailed information.
        """
        if not self.curve.is_on_curve(P):
            raise ValueError(f"Point {P} is not on curve {self.curve}")

        if P in self.torsion_cache:
            order = self.torsion_cache[P]
            return {
                "is_torsion": True,
                "order": order,
                "multiples": self._compute_multiples(P, order)
            }

        current = P
        multiples = []

        for n in range(1, self.MAZUR_MAX_ORDER + 1):
            if current.is_identity:
                self.torsion_cache[P] = n
                return {
                    "is_torsion": True,
                    "order": n,
                    "multiples": multiples
                }
            multiples.append(current)
            current = self.curve.add(current, P)

        return {
            "is_torsion": False,
            "order": None,
            "multiples": multiples
        }

    def _compute_multiples(self, P: Point, order: int) -> List[Point]:
        multiples = []
        current = P
        for _ in range(order - 1):
            multiples.append(current)
            current = self.curve.add(current, P)
        return multiples

    def find_rational_points_naive(self, x_range: int = 10) -> List[Point]:
        """
        DEPRECATED — kept only for compatibility.
        """
        return self._nagell_lutz_candidates()

    def _nagell_lutz_candidates(self) -> List[Point]:
        """
        Generate all possible torsion points using Nagell–Lutz.
        """
        A = int(self.curve.a)
        B = int(self.curve.b)
        Delta = abs(int(self.curve.discriminant()))

        candidates: Set[Point] = {Point.identity()}

        # y = 0 always allowed
        y_values = {0}

        # y^2 divides Δ
        for d in _integer_divisors(Delta):
            if d != 0 and Delta % (d * d) == 0:
                y_values.add(d)

        for y in y_values:
            bound = int(abs(y)**(2/3) + abs(A) + abs(B) + 10)
            for x in range(-bound, bound + 1):
                if y*y == x*x*x + A*x + B:
                    P = Point(x, y)
                    if self.curve.is_on_curve(P):
                        candidates.add(P)

        return list(candidates)

    def find_torsion_subgroup(self, search_range: int = 20) -> Dict[str, any]:
        """
        Find the complete torsion subgroup of the curve.
        """
        candidate_points = self._nagell_lutz_candidates()

        torsion_points = []
        orders = {}

        for P in candidate_points:
            result = self.check_torsion(P)
            if result["is_torsion"]:
                torsion_points.append(P)
                orders[P] = result["order"]

        group_structure = self._analyze_group_structure(torsion_points, orders)

        return {
            "torsion_points": torsion_points,
            "orders": orders,
            "group_structure": group_structure,
            "size": len(torsion_points),
        }

    def _analyze_group_structure(
        self, points: List[Point], orders: Dict[Point, int]
    ) -> str:
        if len(points) == 0:
            return "Trivial"

        if len(points) == 1:
            return "Z/1Z"

        size = len(points)
        max_order = max(orders.values())

        # Cyclic case
        if size == max_order:
            return f"Z/{max_order}Z"

        # Product case: Z/2 x Z/2n
        order_2_count = sum(1 for o in orders.values() if o == 2)
        if order_2_count >= 3 and size == 2 * max_order:
            return f"Z/2Z x Z/{max_order}Z"

        return f"Unknown (size={size}, max_order={max_order})"

    def verify_torsion_theorem(self) -> Dict[str, any]:
        torsion_data = self.find_torsion_subgroup()
        size = torsion_data["size"]

        valid_sizes = self.MAZUR_CYCLIC_ORDERS + [4, 8, 12, 16]

        return {
            "is_valid": size in valid_sizes or size == 1,
            "size": size,
            "structure": torsion_data["group_structure"],
            "conforms_to_mazur": size in valid_sizes or size == 1,
            "torsion_points": torsion_data["torsion_points"],
        }
