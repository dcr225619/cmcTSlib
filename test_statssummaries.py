import unittest
import pandas as pd
import numpy as np
from Statssummaries import Statssummaries

class TestStatssummaries(unittest.TestCase):
    def setUp(self):
        """
        Setup test environment with sample data.
        """
        self.sample_data = pd.DataFrame({
            'date': pd.date_range(start="2024-01-01", periods=10, freq="D"),
            'close': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
            'high': [15, 25, 35, 45, 55, 65, 75, 85, 95, 105],
            'low': [5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
        })
        self.sample_data.set_index('date', inplace=True)

    def test_calculate_rolling_statistics(self):
        """
        Test rolling statistics calculation.
        """
        stats = Statssummaries(data=self.sample_data, price_column='close')
        result = stats.calculate_rolling_statistics(window=3, metrics=['mean', 'std'])

        expected_mean = self.sample_data['close'].rolling(3).mean()
        expected_mean.name = 'Rolling_Mean'
        expected_std = self.sample_data['close'].rolling(3).std()
        expected_std.name = 'Rolling_Std'

        pd.testing.assert_series_equal(result['Rolling_Mean'], expected_mean, check_dtype=False)
        pd.testing.assert_series_equal(result['Rolling_Std'], expected_std, check_dtype=False)

    def test_calculate_expanding_statistics(self):
        """
        Test expanding statistics calculation.
        """
        stats = Statssummaries(data=self.sample_data, price_column='close')
        result = stats.calculate_expanding_statistics(metrics=['mean', 'std'])

        expected_mean = self.sample_data['close'].expanding().mean()
        expected_mean.name = 'Expanding_Mean'
        expected_std = self.sample_data['close'].expanding().std()
        expected_std.name = 'Expanding_Std'

        pd.testing.assert_series_equal(result['Expanding_Mean'], expected_mean, check_dtype=False)
        pd.testing.assert_series_equal(result['Expanding_Std'], expected_std, check_dtype=False)

    def test_calculate_volatility_atr(self):
        """
        Test volatility calculation using ATR.
        """
        stats = Statssummaries(data=self.sample_data, price_column='close')
        result = stats.calculate_volatility(method='atr', window=3)

        # Calculate expected ATR
        high_low = self.sample_data['high'] - self.sample_data['low']
        high_close = np.abs(self.sample_data['high'] - self.sample_data['close'].shift())
        low_close = np.abs(self.sample_data['low'] - self.sample_data['close'].shift())
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        expected_atr = true_range.rolling(window=3).mean()

        pd.testing.assert_series_equal(result, expected_atr, check_dtype=False)

    def test_calculate_rate_of_change(self):
        """
        Test rate of change calculation.
        """
        stats = Statssummaries(data=self.sample_data, price_column='close')
        result = stats.calculate_rate_of_change(period=3)

        # Calculate expected rate of change
        expected_roc = self.sample_data['close'].pct_change(periods=3) * 100

        pd.testing.assert_series_equal(result, expected_roc, check_dtype=False)

    def test_perform_seasonal_decomposition(self):
        """
        Test seasonal decomposition.
        """
        stats = Statssummaries(data=self.sample_data, price_column='close')
        decomposition = stats.simple_seasonal_decomposition(freq=3, method='additive')

        # Validate decomposition components
        self.assertIn('trend', decomposition)
        self.assertIn('seasonal', decomposition)
        self.assertIn('residual', decomposition)

        trend = decomposition['trend']
        seasonal = decomposition['seasonal']
        residual = decomposition['residual']

        # Validate length of components matches data length
        self.assertEqual(len(trend), len(self.sample_data))
        self.assertEqual(len(seasonal), len(self.sample_data))
        self.assertEqual(len(residual), len(self.sample_data))

    def test_summary(self):
        """
        Test summary statistics combining multiple metrics.
        """
        stats = Statssummaries(data=self.sample_data, price_column='close')
        result = stats.summary(rolling_window=3, roc_period=3, atr_window=3)

        # Ensure required columns exist
        self.assertIn('Rolling_Mean', result.columns)
        self.assertIn('Rolling_Std', result.columns)
        self.assertIn('Rate_of_Change(%)', result.columns)
        self.assertIn('ATR', result.columns)


if __name__ == "__main__":
    unittest.main()
