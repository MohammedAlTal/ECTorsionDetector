"""
Elliptic Curve Implementation

Implements elliptic curves in Weierstrass form: y^2 = x^3 + ax + b
Supports operations over rational numbers Q.
"""

from fractions import Fraction
from typing import Union, Optional, Tuple
from .modular_arithmetic import ModularArithmetic


class Point:
    """Represents a point on an elliptic curve."""
    
    def __init__(self, x: Optional[Union[int, Fraction]], 
                 y: Optional[Union[int, Fraction]], 
                 is_identity: bool = False):
        """
        Initialize a point.
        
        Args:
            x: x-coordinate (None for point at infinity)
            y: y-coordinate (None for point at infinity)
            is_identity: True if this is the identity element O
        """
        self.is_identity = is_identity
        
        if is_identity:
            self.x = None
            self.y = None
        else:
            self.x = ModularArithmetic.to_fraction(x) if x is not None else None
            self.y = ModularArithmetic.to_fraction(y) if y is not None else None
    
    def __eq__(self, other) -> bool:
        """Check equality of two points."""
        if not isinstance(other, Point):
            return False
        
        if self.is_identity and other.is_identity:
            return True
        
        if self.is_identity or other.is_identity:
            return False
        
        return self.x == other.x and self.y == other.y
    
    def __repr__(self) -> str:
        """String representation of point."""
        if self.is_identity:
            return "O (Identity)"
        return f"({self.x}, {self.y})"
    
    def __hash__(self) -> int:
        """Hash for using points in sets/dicts."""
        if self.is_identity:
            return hash(("identity",))
        return hash((self.x, self.y))
    
    @classmethod
    def identity(cls):
        """Create the identity element (point at infinity)."""
        return cls(None, None, is_identity=True)


class EllipticCurve:
    """
    Elliptic curve in Weierstrass form: y^2 = x^3 + ax + b
    """
    
    def __init__(self, a: Union[int, Fraction], b: Union[int, Fraction], 
                 field_mod: Optional[int] = None):
        """
        Initialize elliptic curve.
        
        Args:
            a: Coefficient of x term
            b: Constant term
            field_mod: If provided, curve is over F_p (finite field)
        """
        self.a = ModularArithmetic.to_fraction(a)
        self.b = ModularArithmetic.to_fraction(b)
        self.field_mod = field_mod
        
        discriminant = self.discriminant()
        if discriminant == 0:
            raise ValueError("Invalid curve: discriminant equals zero")
    
    def discriminant(self) -> Fraction:
        """Compute discriminant: -16(4a^3 + 27b^2)."""
        return -16 * (4 * self.a**3 + 27 * self.b**2)
    
    def is_on_curve(self, point: Point) -> bool:
        """
        Verify if a point satisfies the curve equation.
        
        Args:
            point: Point to check
            
        Returns:
            True if point is on curve
        """
        if point.is_identity:
            return True
        
        x, y = point.x, point.y
        lhs = y**2
        rhs = x**3 + self.a * x + self.b
        return lhs == rhs
    
    def add(self, P: Point, Q: Point) -> Point:
        """
        Add two points using the elliptic curve group law.
        
        Args:
            P: First point
            Q: Second point
            
        Returns:
            P + Q on the curve
        """
        if P.is_identity:
            return Q
        if Q.is_identity:
            return P
        
        x1, y1 = P.x, P.y
        x2, y2 = Q.x, Q.y
        
        if x1 == x2 and y1 == -y2:
            return Point.identity()
        
        if P == Q:
            if y1 == 0:
                return Point.identity()
            lambda_val = (3 * x1**2 + self.a) / (2 * y1)
        else:
            if x2 == x1:
                return Point.identity()
            lambda_val = (y2 - y1) / (x2 - x1)
        
        x3 = lambda_val**2 - x1 - x2
        y3 = lambda_val * (x1 - x3) - y1
        
        return Point(x3, y3)
    
    def double(self, P: Point) -> Point:
        """
        Double a point: compute 2P.
        
        Args:
            P: Point to double
            
        Returns:
            2P on the curve
        """
        return self.add(P, P)
    
    def scalar_multiply(self, P: Point, n: int) -> Point:
        """
        Compute nP using repeated addition.
        
        Args:
            P: Base point
            n: Scalar multiplier
            
        Returns:
            nP on the curve
        """
        if n == 0:
            return Point.identity()
        
        if n < 0:
            P_neg = Point(P.x, -P.y) if not P.is_identity else P
            return self.scalar_multiply(P_neg, -n)
        
        result = Point.identity()
        addend = P
        
        while n > 0:
            if n % 2 == 1:
                result = self.add(result, addend)
            addend = self.double(addend)
            n //= 2
        
        return result
    
    def find_order(self, P: Point, max_order: int = 12) -> Optional[int]:
        """
        Find the order of a point P (smallest n > 0 such that nP = O).
        
        Args:
            P: Point to analyze
            max_order: Maximum order to check (default 12 per Mazur)
            
        Returns:
            Order of P, or None if order > max_order
        """
        if P.is_identity:
            return 1
        
        current = P
        for n in range(1, max_order + 1):
            if current.is_identity:
                return n
            current = self.add(current, P)
        
        return None
    
    def is_torsion(self, P: Point, max_order: int = 12) -> Tuple[bool, Optional[int]]:
        """
        Check if a point is a torsion point.
        
        Args:
            P: Point to check
            max_order: Maximum order to check
            
        Returns:
            (is_torsion, order) where order is None if not torsion
        """
        order = self.find_order(P, max_order)
        return (order is not None, order)
    
    def __repr__(self) -> str:
        """String representation of curve."""
        return f"E: y^2 = x^3 + ({self.a})x + ({self.b})"

