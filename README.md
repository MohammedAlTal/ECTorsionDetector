# Detecting Torsion Points on Elliptic Curves

A Python implementation for detecting and analyzing torsion points on elliptic curves over the rational numbers.

## Overview

This project implements detection of torsion points on elliptic curves defined by:

```
E: y² = x³ + ax + b
```

A point P is **torsion** if nP = O for some positive integer n ≤ 12 (bounded by Mazur's Torsion Theorem).

## Features

- Complete elliptic curve group law implementation
- Torsion point detection with order computation
- Full torsion subgroup enumeration
- Interactive web interface
- Pre-loaded example curves
- Jupyter notebook demonstrations

## Installation

Navigate to the project directory:

```bash
cd Project.5.AlTal
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Web Application

Start the Flask server:

```bash
python app/server.py
```

Navigate to http://localhost:5050

The web interface provides:
- Example curve selector with 5 pre-loaded curves
- Input fields for curve parameters (a, b)
- Input fields for test point coordinates (x, y)
- Torsion detection for individual points
- Complete torsion subgroup enumeration

### Jupyter Notebook

Launch the interactive notebook:

```bash
jupyter notebook notebooks/demo.ipynb
```

### Python API

```python
from src.elliptic_curve import EllipticCurve, Point
from src.torsion_finder import TorsionFinder

# Create curve y² = x³ - x
curve = EllipticCurve(a=-1, b=0)

# Test point (0, 0)
P = Point(0, 0)

# Check if point is torsion
finder = TorsionFinder(curve)
result = finder.check_torsion(P)

print(f"Is torsion: {result['is_torsion']}")
print(f"Order: {result['order']}")

# Find complete torsion subgroup
subgroup = finder.find_torsion_subgroup(search_range=20)
print(f"Group size: {subgroup['size']}")
print(f"Structure: {subgroup['group_structure']}")
```

## Project Structure

```
Project.5.AlTal/
├── app/                      # Web application
│   ├── server.py             # Flask backend
│   ├── examples_data.py      # Pre-loaded examples
│   ├── templates/            # HTML templates
│   └── static/               # CSS styles
├── src/                      # Core implementation
│   ├── elliptic_curve.py     # Curve operations
│   ├── torsion_finder.py     # Torsion detection
│   ├── modular_arithmetic.py # Utilities
│   └── __init__.py
├── notebooks/                # Interactive demos
│   └── demo.ipynb
├── requirements.txt
└── README.md
```

## Example Curves

**y² = x³ - x**
- Torsion subgroup: Z/2Z × Z/2Z
- 4 points: O, (0,0), (1,0), (-1,0)
- All points have order 2

**y² = x³ - 2x + 1**
- Torsion subgroup: Z/2Z
- 2 points: O, (1,0)
- Point (1,0) has order 2

**y² = x³ - 4**
- Torsion subgroup varies
- Test with the application

## Mathematical Background

### Group Law

**Point Addition (P ≠ Q):**
```
λ = (y₂ - y₁) / (x₂ - x₁)
x₃ = λ² - x₁ - x₂
y₃ = λ(x₁ - x₃) - y₁
```

**Point Doubling (P = Q):**
```
λ = (3x₁² + a) / (2y₁)
x₃ = λ² - 2x₁
y₃ = λ(x₁ - x₃) - y₁
```

### Mazur's Torsion Theorem

Over Q, the torsion subgroup is one of:
- **Cyclic:** Z/nZ for n = 1, 2, ..., 10, 12
- **Product:** Z/2Z × Z/2nZ for n = 1, 2, 3, 4

This theorem bounds the search space to orders ≤ 12.

## Implementation Details

- **Exact Arithmetic:** Uses Python's Fraction class for precision
- **Efficient Algorithms:** Double-and-add for scalar multiplication
- **Bounded Search:** Mazur's theorem limits order checking
- **Clean Architecture:** Modular design with separation of concerns

## Author

Mohammed Al-Tal  
MATH 312 - Elliptic Curves and Cryptography  
November 13, 2025

## References

1. Silverman, J. H. (2009). The Arithmetic of Elliptic Curves. Springer.
2. Washington, L. C. (2008). Elliptic Curves: Number Theory and Cryptography.
3. Mazur, B. (1977). "Modular curves and the Eisenstein ideal".
