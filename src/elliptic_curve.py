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
        self.is_identity = is_identity

        if is_identity:
            self.x = None
            self.y = None
        else:
            self.x = ModularArithmetic.to_fraction(x) if x is not None else None
            self.y = ModularArithmetic.to_fraction(y) if y is not None else None

    def __eq__(self, other) -> bool:
        if not isinstance(other, Point):
            return False
        if self.is_identity and other.is_identity:
            return True
        if self.is_identity or other.is_identity:
            return False
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return "O (Identity)" if self.is_identity else f"({self.x}, {self.y})"

    def __hash__(self) -> int:
        if self.is_identity:
            return hash(("identity",))
        return hash((self.x, self.y))

    @classmethod
    def identity(cls):
        return cls(None, None, is_identity=True)


class EllipticCurve:
    """
    Elliptic curve in Weierstrass form: y^2 = x^3 + ax + b
    """

    def __init__(self, a: Union[int, Fraction], b: Union[int, Fraction],
                 field_mod: Optional[int] = None):
        self.a = ModularArithmetic.to_fraction(a)
        self.b = ModularArithmetic.to_fraction(b)
        self.field_mod = field_mod

        # ORIGINAL CHECK (unchanged)
        if self.discriminant() == 0:
            raise ValueError("Invalid curve: discriminant equals zero")

    def discriminant(self) -> Fraction:
        """
        Elliptic curve discriminant Δ_E = -16(4a^3 + 27b^2)
        """
        return -16 * (4 * self.a**3 + 27 * self.b**2)

    def discriminant_cubic(self) -> Fraction:
        """
        Cubic polynomial discriminant Δ_f = -(4a^3 + 27b^2)
        """
        return -(4 * self.a**3 + 27 * self.b**2)

    def is_integral_model(self) -> bool:
        """
        Required for Nagell–Lutz:
        a, b ∈ Z
        """
        return self.a.denominator == 1 and self.b.denominator == 1

    def is_on_curve(self, point: Point) -> bool:
        if point.is_identity:
            return True
        x, y = point.x, point.y
        return y**2 == x**3 + self.a * x + self.b

    def add(self, P: Point, Q: Point) -> Point:
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
            if x1 == x2:
                return Point.identity()
            lambda_val = (y2 - y1) / (x2 - x1)

        x3 = lambda_val**2 - x1 - x2
        y3 = lambda_val * (x1 - x3) - y1
        return Point(x3, y3)

    def double(self, P: Point) -> Point:
        return self.add(P, P)

    def scalar_multiply(self, P: Point, n: int) -> Point:
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
        if P.is_identity:
            return 1

        current = P
        for n in range(1, max_order + 1):
            if current.is_identity:
                return n
            current = self.add(current, P)
        return None

    def is_torsion(self, P: Point, max_order: int = 12) -> Tuple[bool, Optional[int]]:
        order = self.find_order(P, max_order)
        return (order is not None, order)

    def __repr__(self) -> str:
        return f"E: y^2 = x^3 + ({self.a})x + ({self.b})"
