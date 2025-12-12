"""
Flask Web Application for Torsion Point Detection

Provides a browser-based interface for elliptic curve torsion analysis.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, jsonify
from fractions import Fraction
from src.elliptic_curve import EllipticCurve, Point
from src.torsion_finder import TorsionFinder
from app.examples_data import EXAMPLE_CURVES

app = Flask(__name__)


@app.route('/')
def index():
    """Render main interface."""
    return render_template('index.html')


@app.route('/api/check_torsion', methods=['POST'])
def check_torsion():
    """
    Endpoint to check if a point is torsion.
    """
    try:
        data = request.get_json()
        
        a = Fraction(data['a']).limit_denominator()
        b = Fraction(data['b']).limit_denominator()
        curve = EllipticCurve(a, b)

        if not curve.is_integral_model():
            return jsonify({
                'success': False,
                'error': 'Nagell–Lutz requires integer coefficients a and b'
            })

        x = Fraction(data['x']).limit_denominator()
        y = Fraction(data['y']).limit_denominator()
        point = Point(x, y)
        
        if not curve.is_on_curve(point):
            return jsonify({
                'success': False,
                'error': f'Point ({x}, {y}) is not on the curve'
            })
        
        finder = TorsionFinder(curve)
        result = finder.check_torsion(point)
        
        multiples_str = []
        for i, p in enumerate(result['multiples'], 1):
            multiples_str.append({
                'n': i,
                'point': str(p)
            })
        
        return jsonify({
            'success': True,
            'curve': str(curve),
            'point': str(point),
            'is_torsion': result['is_torsion'],
            'order': result['order'],
            'multiples': multiples_str
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        })


@app.route('/api/find_torsion_subgroup', methods=['POST'])
def find_torsion_subgroup():
    """
    Endpoint to find all torsion points on a curve.
    """
    try:
        data = request.get_json()
        
        a = Fraction(data['a']).limit_denominator()
        b = Fraction(data['b']).limit_denominator()
        search_range = int(data.get('search_range', 20))
        
        curve = EllipticCurve(a, b)

        if not curve.is_integral_model():
            return jsonify({
                'success': False,
                'error': 'Nagell–Lutz requires integer coefficients a and b'
            })

        finder = TorsionFinder(curve)
        result = finder.find_torsion_subgroup(search_range)
        
        torsion_points_data = []
        for point in result['torsion_points']:
            order = result['orders'].get(point, 'Unknown')
            torsion_points_data.append({
                'point': str(point),
                'order': order
            })
        
        return jsonify({
            'success': True,
            'curve': str(curve),
            'size': result['size'],
            'group_structure': result['group_structure'],
            'torsion_points': torsion_points_data
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        })


@app.route('/api/examples', methods=['GET'])
def get_examples():
    """Return predefined example curves."""
    return jsonify({'examples': EXAMPLE_CURVES})


if __name__ == '__main__':
    PORT = 5050
    print(f"Starting Torsion Point Detection Server")
    print(f"Navigate to: http://localhost:{PORT}")
    app.run(debug=True, host='0.0.0.0', port=PORT)
