import unittest
import pandas as pd
import numpy as np
from data_processing import DataProcessor

class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        """
        set up test environment with sample data and files
        """
        self.sample_data = pd.DataFrame(
            {"Date": pd.date_range(start="2024-01-01", periods=10, freq="D"),
            "Close": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],})
        self.sample_data.set_index("Date", inplace=True)
        self.sample_data.to_csv("test_data.csv")

    def tearDown(self):
        """
        clean up after tests by removing temporary files
        """
        import os
        if os.path.exists("test_data.csv"):
            os.remove("test_data.csv")

    def test_load_data_csv(self):
        """
        test loading data from a CSV file
        """
        processor = DataProcessor(file_path="test_data.csv", file_format="csv")
        data = processor.load_data()
        self.assertTrue(isinstance(data, pd.DataFrame))
        self.assertEqual(data.shape, self.sample_data.shape)
        pd.testing.assert_frame_equal(data, self.sample_data)

    def test_resample_data(self):
        """
        test resampling data to weekly frequency with mean aggregation
        """
        processor = DataProcessor(file_path="test_data.csv", file_format="csv")
        data = processor.load_data()
        resampled_data = processor.resample_data(frequency="W", agg_method="mean")
        expected_data = self.sample_data.resample("W").mean()
        pd.testing.assert_frame_equal(resampled_data, expected_data)

    def test_detect_outliers_zscore(self):
        """
        test detecting outliers using the z-score method
        """
        processor = DataProcessor(file_path="test_data.csv", file_format="csv")
        data = processor.load_data()
        processor.data.loc["2024-01-01", "Close"] = 1000
        outliers = processor.detect_outliers(column="Close", method="zscore", threshold=3.0)
        self.assertTrue(outliers.loc["2024-01-01"])
        self.assertFalse(outliers.loc["2024-01-02"])

    def test_detect_outliers_iqr(self):
        """
        test detecting outliers using the IQR method
        """
        processor = DataProcessor(file_path="test_data.csv", file_format="csv")
        data = processor.load_data()
        processor.data.loc["2024-01-01", "Close"] = 1000
        outliers = processor.detect_outliers(column="Close", method="iqr")
        self.assertTrue(outliers.loc["2024-01-01"])
        self.assertFalse(outliers.loc["2024-01-02"])

    def test_smooth_data(self):
        """
        test smoothing data using a rolling average
        """
        processor = DataProcessor(file_path="test_data.csv", file_format="csv")
        data = processor.load_data()
        smoothed_data = processor.smooth_data(column="Close", window_size=3)
        expected_data = self.sample_data["Close"].rolling(window=3).mean()
        pd.testing.assert_series_equal(smoothed_data, expected_data)

    def test_invalid_file_format(self):
        """
        test handling of unsupported file formats
        """
        with self.assertRaises(ValueError):
            processor = DataProcessor(file_path="test_data.csv", file_format="unsupported")
            processor.load_data()

    def test_invalid_column(self):
        """
        test handling of invalid column names in functions
        """
        processor = DataProcessor(file_path="test_data.csv", file_format="csv")
        processor.load_data()
        with self.assertRaises(ValueError):
            processor.detect_outliers(column="InvalidColumn", method="zscore")
        with self.assertRaises(ValueError):
            processor.smooth_data(column="InvalidColumn", window_size=3)

if __name__ == "__main__":
    unittest.main()
