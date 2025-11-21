"""
Example Curves for Torsion Detection

Predefined curves for easy testing and demonstration.
"""

EXAMPLE_CURVES = [
    {
        "name": "y² = x³ - x (Klein Four-Group)",
        "a": -1,
        "b": 0,
        "test_point": {"x": 0, "y": 0},
        "description": "Classic example with Z/2Z × Z/2Z structure"
    },
    {
        "name": "y² = x³ - 2x + 1 (Simple 2-Torsion)",
        "a": -2,
        "b": 1,
        "test_point": {"x": 1, "y": 0},
        "description": "Simple curve with Z/2Z structure"
    },
    {
        "name": "y² = x³ - 4 (Interesting Structure)",
        "a": 0,
        "b": -4,
        "test_point": {"x": 2, "y": 2},
        "description": "Explore torsion on this curve"
    },
    {
        "name": "y² = x³ + x (Different Example)",
        "a": 1,
        "b": 0,
        "test_point": {"x": 0, "y": 0},
        "description": "Compare with y² = x³ - x"
    },
    {
        "name": "y² = x³ - 3x + 2 (Custom Example)",
        "a": -3,
        "b": 2,
        "test_point": {"x": 1, "y": 0},
        "description": "Another interesting curve to explore"
    }
]

