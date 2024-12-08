import unittest
import pandas as pd
import numpy as np
import os
from io import StringIO
class TestDataProcessor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.csv_data = StringIO("""
        date,value
        2024-01-01,100
        2024-01-02,110
        2024-01-03,120
        2024-01-04,130
        2024-01-05,140
        2024-01-06,150
        2024-01-07,160
        """)
        cls.file_path = "test_data.csv"
        cls.csv_data.seek(0)
        with open(cls.file_path, "w") as f:
            f.write(cls.csv_data.getvalue())
        cls.processor = DataProcessor(cls.file_path, file_format="csv")
    
    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.file_path):
            os.remove(cls.file_path)

    def test_load_data(self):
        data = self.processor.load_data()
        self.assertEqual(len(data), 7)  
        self.assertIn("value", data.columns)  
    
    def test_resample_data(self):
        self.processor.load_data()
        resampled = self.processor.resample_data(frequency="2D", agg_method="mean")
        self.assertEqual(len(resampled), 4)  #
    
    def test_detect_outliers(self):
        self.processor.load_data()
        outliers = self.processor.detect_outliers(column="value", method="zscore", threshold=2.0)
        self.assertEqual(outliers.sum(), 0) 
        
    def test_smooth_data(self):
        self.processor.load_data()
        smoothed = self.processor.smooth_data(column="value", window_size=3)
        self.assertTrue(smoothed.isna().sum() > 0) 
    
    def test_handle_missing_data(self):
        self.processor.load_data()
        self.processor.data.loc["2024-01-03", "value"] = np.nan
        handled = self.processor.handle_missing_data(method="fill_mean")
        self.assertFalse(handled.isna().any().any())  
    
    def test_save_data(self):
        self.processor.load_data()
        output_path = "test_output.csv"
        self.processor.save_data(output_path, file_format="csv")
        self.assertTrue(os.path.exists(output_path))  
        os.remove(output_path)  

if __name__ == "__main__":
    unittest.main()
