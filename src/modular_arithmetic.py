"""
Modular Arithmetic Utilities

Provides operations for rational and modular arithmetic used in elliptic curve computations.
"""

from fractions import Fraction
from typing import Union


class ModularArithmetic:
    """Utilities for arithmetic operations in rational and modular contexts."""
    
    @staticmethod
    def rational_add(a: Fraction, b: Fraction) -> Fraction:
        """Add two rational numbers."""
        return a + b
    
    @staticmethod
    def rational_multiply(a: Fraction, b: Fraction) -> Fraction:
        """Multiply two rational numbers."""
        return a * b
    
    @staticmethod
    def rational_divide(a: Fraction, b: Fraction) -> Fraction:
        """Divide two rational numbers."""
        if b == 0:
            raise ValueError("Division by zero")
        return a / b
    
    @staticmethod
    def extended_gcd(a: int, b: int) -> tuple:
        """
        Extended Euclidean Algorithm.
        
        Returns (gcd, x, y) where gcd = ax + by
        """
        if a == 0:
            return b, 0, 1
        
        gcd, x1, y1 = ModularArithmetic.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        
        return gcd, x, y
    
    @staticmethod
    def modular_inverse(a: int, m: int) -> int:
        """
        Compute modular multiplicative inverse of a modulo m.
        
        Returns x such that (a * x) % m == 1
        """
        gcd, x, _ = ModularArithmetic.extended_gcd(a, m)
        
        if gcd != 1:
            raise ValueError(f"Modular inverse does not exist for {a} mod {m}")
        
        return (x % m + m) % m
    
    @staticmethod
    def mod_divide(a: int, b: int, m: int) -> int:
        """
        Compute (a / b) mod m = a * b^(-1) mod m
        """
        b_inv = ModularArithmetic.modular_inverse(b, m)
        return (a * b_inv) % m
    
    @staticmethod
    def is_coprime(a: int, b: int) -> bool:
        """Check if two numbers are coprime."""
        gcd, _, _ = ModularArithmetic.extended_gcd(a, b)
        return gcd == 1
    
    @staticmethod
    def to_fraction(value: Union[int, float, Fraction]) -> Fraction:
        """Convert value to Fraction for exact rational arithmetic."""
        if isinstance(value, Fraction):
            return value
        return Fraction(value).limit_denominator()

