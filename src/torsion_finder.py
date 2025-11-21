"""
Torsion Subgroup Finder

Implements Mazur's Torsion Theorem to enumerate all rational torsion points
on an elliptic curve over Q.
"""

from typing import List, Set, Dict
from fractions import Fraction
from .elliptic_curve import EllipticCurve, Point


class TorsionFinder:
    """
    Finder for torsion points on elliptic curves.
    
    Uses Mazur's Theorem: Over Q, the torsion subgroup is one of:
    - Z/nZ for n = 1, 2, ..., 10, 12
    - Z/2Z × Z/2nZ for n = 1, 2, 3, 4
    """
    
    # Possible torsion group structures per Mazur
    MAZUR_CYCLIC_ORDERS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]
    MAZUR_MAX_ORDER = 12
    
    def __init__(self, curve: EllipticCurve):
        """
        Initialize torsion finder for a curve.
        
        Args:
            curve: EllipticCurve instance
        """
        self.curve = curve
        self.torsion_cache: Dict[Point, int] = {}
    
    def check_torsion(self, P: Point) -> Dict[str, any]:
        """
        Check if a point is torsion and return detailed information.
        
        Args:
            P: Point to check
            
        Returns:
            Dictionary with keys:
                - is_torsion: bool
                - order: int or None
                - multiples: list of points [P, 2P, 3P, ...]
        """
        if P in self.torsion_cache:
            order = self.torsion_cache[P]
            return {
                'is_torsion': True,
                'order': order,
                'multiples': self._compute_multiples(P, order)
            }
        
        if not self.curve.is_on_curve(P):
            raise ValueError(f"Point {P} is not on curve {self.curve}")
        
        multiples = []
        current = P
        
        for n in range(1, self.MAZUR_MAX_ORDER + 1):
            if current.is_identity:
                self.torsion_cache[P] = n
                return {
                    'is_torsion': True,
                    'order': n,
                    'multiples': multiples
                }
            multiples.append(current)
            current = self.curve.add(current, P)
        
        return {
            'is_torsion': False,
            'order': None,
            'multiples': multiples
        }
    
    def _compute_multiples(self, P: Point, order: int) -> List[Point]:
        """Compute [P, 2P, 3P, ..., (order-1)P]."""
        multiples = []
        current = P
        for _ in range(order - 1):
            multiples.append(current)
            current = self.curve.add(current, P)
        return multiples
    
    def find_rational_points_naive(self, x_range: int = 10) -> List[Point]:
        """
        Naively search for rational points by testing integer x-coordinates.
        
        Args:
            x_range: Search x in [-x_range, x_range]
            
        Returns:
            List of points found on the curve
        """
        points = [Point.identity()]
        
        for x in range(-x_range, x_range + 1):
            x_frac = Fraction(x)
            y_squared = x_frac**3 + self.curve.a * x_frac + self.curve.b
            
            if y_squared < 0:
                continue
            
            y_squared_float = float(y_squared)
            y_candidate = y_squared_float ** 0.5
            
            for denom in range(1, 11):
                for num in range(-100, 101):
                    y_frac = Fraction(num, denom)
                    if y_frac**2 == y_squared:
                        points.append(Point(x_frac, y_frac))
                        if y_frac != 0:
                            points.append(Point(x_frac, -y_frac))
                        break
        
        return list(set(points))
    
    def find_torsion_subgroup(self, search_range: int = 20) -> Dict[str, any]:
        """
        Find the complete torsion subgroup of the curve.
        
        Args:
            search_range: Range to search for rational points
            
        Returns:
            Dictionary containing:
                - torsion_points: List of all torsion points
                - orders: Dictionary mapping points to their orders
                - group_structure: Description of the group structure
        """
        candidate_points = self.find_rational_points_naive(search_range)
        
        torsion_points = []
        orders = {}
        
        for point in candidate_points:
            result = self.check_torsion(point)
            if result['is_torsion']:
                torsion_points.append(point)
                orders[point] = result['order']
        
        group_structure = self._analyze_group_structure(torsion_points, orders)
        
        return {
            'torsion_points': torsion_points,
            'orders': orders,
            'group_structure': group_structure,
            'size': len(torsion_points)
        }
    
    def _analyze_group_structure(self, points: List[Point], 
                                  orders: Dict[Point, int]) -> str:
        """
        Determine the group structure from torsion points.
        
        Args:
            points: List of torsion points
            orders: Dictionary of orders
            
        Returns:
            String describing group structure (e.g., "Z/2Z x Z/4Z")
        """
        if len(points) == 0:
            return "Trivial"
        
        if len(points) == 1:
            return "Z/1Z"
        
        order_counts = {}
        for order in orders.values():
            order_counts[order] = order_counts.get(order, 0) + 1
        
        max_order = max(orders.values())
        size = len(points)
        
        if size == max_order:
            return f"Z/{max_order}Z"
        
        if size % 2 == 0:
            order_2_count = sum(1 for o in orders.values() if o == 2)
            if order_2_count >= 3:
                return f"Z/2Z x Z/{max_order}Z"
        
        order_dist = ", ".join([f"{count} of order {order}" 
                               for order, count in sorted(order_counts.items())])
        return f"{size} points: {order_dist}"
    
    def verify_torsion_theorem(self) -> Dict[str, any]:
        """
        Verify that the torsion subgroup matches Mazur's theorem predictions.
        
        Returns:
            Verification results
        """
        torsion_data = self.find_torsion_subgroup()
        
        size = torsion_data['size']
        structure = torsion_data['group_structure']
        
        valid_sizes = self.MAZUR_CYCLIC_ORDERS + [4, 8, 12, 16]
        is_valid = size in valid_sizes or size == 1
        
        return {
            'is_valid': is_valid,
            'size': size,
            'structure': structure,
            'conforms_to_mazur': is_valid,
            'torsion_points': torsion_data['torsion_points']
        }

