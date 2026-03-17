import unittest as unittest
import numpy as np
from Source.MathLibrary.math_library import (
    calculate_volatility, calculate_parametric_var, calculate_historical_var,
    calculate_monte_carlo_var, calculate_parametric_cvar, calculate_historical_cvar)

class TestMathLibrary(unittest.TestCase):
    def setUp(self):
        self.confidence_level = 0.90
        self.returns = np.arange(-50, 50)

    def test_calculate_volatility(self):
        expected_volatility = np.std(self.returns)
        self.assertAlmostEqual(calculate_volatility(self.returns), expected_volatility)

    def test_calculate_parametric_var(self):
        var = calculate_parametric_var(self.returns, self.confidence_level)
        self.assertIsInstance(var, float)
        self.assertAlmostEqual(var, -37.49, places=1)

    def test_calculate_historical_var(self):
        var = calculate_historical_var(self.returns, self.confidence_level)
        self.assertIsInstance(var, float)
        self.assertAlmostEqual(var, -40.1, places=1) #Linearly interpolated

    def test_calculate_monte_carlo_var(self):
        var = calculate_monte_carlo_var(self.returns, self.confidence_level, 100000)
        self.assertIsInstance(var, float)
        self.assertLessEqual(var, -37)
        self.assertGreaterEqual(var, -38)

    def test_calculate_parametric_cvar(self):
        cvar = calculate_parametric_cvar(self.returns, self.confidence_level)
        self.assertIsInstance(cvar, float)
        self.assertAlmostEqual(cvar, -51.16, places=1)

    def test_calculate_historical_cvar(self):
        cvar = calculate_historical_cvar(self.returns, self.confidence_level)
        self.assertIsInstance(cvar, float)
        self.assertAlmostEqual(cvar, -45.5, places=1)