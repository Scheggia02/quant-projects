import unittest as unittest
import numpy as np
import pandas as pd
import scipy.stats as st
from Source.MathLibrary.math_library import *

class TestMathLibrary(unittest.TestCase):
    def setUp(self):
        self.confidence_level = 0.90
        self.returns = np.arange(-50, 50)
        self.asymmetric_values = np.array([1.0, 2.0, 3.0, 10.0])
        self.flat_values = np.array([5.0, 5.0, 5.0, 5.0])
        self.prices = pd.Series([100.0, 105.0, 110.0], index=pd.to_datetime([
            "2022-01-01", "2022-01-02", "2022-01-03"
        ]))

    def test_calculate_simple_returns_with_price_series(self):
        expected_returns = self.prices.pct_change().dropna()
        pd.testing.assert_series_equal(calculate_simple_returns(self.prices), expected_returns)

    def test_calculate_simple_returns_with_price_list(self):
        expected_returns = pd.Series([0.05, (110.0 / 105.0) - 1.0], index=[1, 2], dtype=float)
        pd.testing.assert_series_equal(calculate_simple_returns([100.0, 105.0, 110.0]), expected_returns)

    def test_calculate_log_returns_with_price_series(self):
        expected_returns = np.log(self.prices / self.prices.shift(1)).dropna()
        pd.testing.assert_series_equal(calculate_log_returns(self.prices), expected_returns)

    def test_calculate_log_returns_with_price_list(self):
        expected_returns = pd.Series(
            [np.log(105.0 / 100.0), np.log(110.0 / 105.0)],
            index=[1, 2],
            dtype=float,
        )
        pd.testing.assert_series_equal(calculate_log_returns([100.0, 105.0, 110.0]), expected_returns)

    def test_calculate_mean_with_numpy_array(self):
        self.assertAlmostEqual(calculate_mean(self.returns), np.mean(self.returns))

    def test_calculate_mean_with_list_input(self):
        self.assertAlmostEqual(calculate_mean([1.0, 2.0, 3.0, 4.0]), 2.5)

    def test_calculate_variance_matches_sample_variance(self):
        self.assertAlmostEqual(calculate_variance(self.returns), np.var(self.returns, ddof=1))

    def test_calculate_variance_returns_zero_for_single_value(self):
        self.assertEqual(calculate_variance(np.array([42.0])), 0.0)

    def test_calculate_skewness_matches_scipy_unbiased_result(self):
        expected_skewness = st.skew(self.asymmetric_values, bias=False)
        self.assertAlmostEqual(calculate_skewness(self.asymmetric_values), expected_skewness)

    def test_calculate_skewness_returns_zero_for_small_sample(self):
        self.assertEqual(calculate_skewness(np.array([1.0, 2.0])), 0.0)

    def test_calculate_skewness_returns_zero_for_flat_series(self):
        self.assertEqual(calculate_skewness(self.flat_values), 0.0)

    def test_calculate_kurtosis_matches_scipy_pearson_result(self):
        expected_kurtosis = st.kurtosis(self.asymmetric_values, fisher=False, bias=False)
        self.assertAlmostEqual(calculate_kurtosis(self.asymmetric_values), expected_kurtosis)

    def test_calculate_kurtosis_returns_zero_for_small_sample(self):
        self.assertEqual(calculate_kurtosis(np.array([1.0, 2.0, 3.0])), 0.0)

    def test_calculate_kurtosis_returns_zero_for_flat_series(self):
        self.assertEqual(calculate_kurtosis(self.flat_values), 0.0)

    def test_calculate_volatility(self):
        expected_volatility = np.std(self.returns)
        self.assertAlmostEqual(calculate_volatility(self.returns), expected_volatility)

    def test_calculate_parametric_var_with_zero_mean(self):
        alpha = 1 - self.confidence_level
        expected_var = calculate_volatility(self.returns) * st.norm.ppf(alpha)
        self.assertAlmostEqual(
            calculate_parametric_var(self.returns, self.confidence_level, zero_mean=True),
            expected_var,
        )

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