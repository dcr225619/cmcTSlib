# cmcTSlib
Time Series Analysis package cmcTSlib for DS5010 course project.

This README file includes a brief introduction to the module and usage instructions.

## Getting Started

### Dependencies
> Python3:
> * Numpy
> * Pandas
> * Matplotlib
  
### Running the code
> Clone the repo to your local machine
>
> Run each module (data processing, statistical summaries, visualization) individually
>
> Run run_test for unit testing

### Dataset
The dataset '000001.csv' for example usage can be downloaded from https://github.com/onewaymyway/stockdata

## Data Processing module
The Data Processing Module manages financial time series data intake and preparation. It includes the following functions:
1. __init__(self, file_path, file_format)
2. load_data(self)
3. resample_data(self, frequency, agg_method)
4. detect_outliers(self, column, method, threshold)
5. smooth_data(self, column, window_size)

### Function Description
1. __init__(self, file_path: str, file_format)
   
   This function initializes the data processor with the file path and format.
   ```
   parameters: file_path - path to the data file
               file_format - format of the data file (default is 'csv')
   ```
2. load_data(self)

   This function loads the data based on the file format.
   ```
   returns: self.data - loaded dataset
   raises: ValueError if the file format is not supported
   ```
   
3. resample_data(self, frequency, agg_method)

   This function resamples the time series data to a specified frequency.
   ```
   parameters: frequency - the desired frequency ('D' for daily, 'W' for weekly, 'M' for monthly) (using pd)
               agg_method - aggregation method ('mean', 'sum', 'last')
   returns: pd.DataFrame - resampled data
   raises: ValueError if data not loaded
           ValueError if the input aggregation method is not supported
   ```
   
4. detect_outliers(self, column, method, threshold)
   
   This function detects outliers in the data based on the specified method.
   ```
   parameters: column - the column to check for outliers
               method - outlier detection method (default is 'zscore')
               threshold - threshold for identifying outliers (default of 3.0 for z-score)
   returns: pd.Series - boolean series indicating outliers
   raises: ValueError if the input outlier detection method is not supported
           ValueError if input column not found in data
   ```
   
5. smooth_data(self, column, window_size)
   
   This function smooths the data using a rolling average.
   ```
   parameters: column - the column to smooth
               window_size - the size of the moving window (default is 5)       
   returns: pd.Series - smoothed data as a rolling average
   raises: ValueError if input column not found in data
   ```

### Example Usage
```
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
```

## Statistical Summaries module
The Statistical Summaries Module provides users with essential metrics for analyzing trends, volatility, and other characteristics of stock market data. It includes the following functions:
1. __init__(self, data, price_column)
2. calculate_rolling_statistics(self, window, metrics)
3. calculate_expanding_statistics(self, window, metrics)
4. calculate_volatility(self, method, window)
5. calculate_rate_of_change(self, period)
6. simple_seasonal_decomposition(self, method, freq)
7. summary(self, rolling_window, roc_period, atr_window)

### Function Description
1. __init__(self, data, price_column)
   
   This function initializes the dataset for summary.
   ```
   parameters: data - DataFrame includes market data
               price_column - the name of price column
   raises: ValueError if the data index is not set to be a DatetimeIndex
   ```
   
2. calculate_rolling_statistics(self, window, metrics)
   
   This function calculates the rolling window statistics.
   ```
   parameters: window - Window size for rolling calculations.
               metrics - List of metrics to calculate ('mean', 'median', 'std').
   returns: pd.DataFrame with rolling statistics.
   raises: ValueError if the input metrics are not supported
   ```
   
3. calculate_expanding_statistics(self, window, metrics)
   
   This function calculates expanding window statistics.
   ```
   parameters: metrics - List of metrics to calculate ('mean', 'std').
   returns: pd.DataFrame with expanding statistics.
   raises: ValueError if the input metrics are not supported
   ```

4. calculate_volatility(self, method, window)
   
   This function calculates volatility metrics.
   ```
   parameters: method - 'std' (standard deviation) or 'atr' (average true range).
               window - Window size for rolling calculations (required for ATR).
   returns: pd.Series with volatility metrics.
   raises: ValueError if the window is not specified when using atr method
           ValueError if the input method is not supported
   ```

5. calculate_rate_of_change(self, period)

   This function calculates the rate of change (RoC) metric.
   ```
   parameters: period - Period for RoC calculation.
   returns: pd.Series with RoC values.
   ```
6. simple_seasonal_decomposition(self, method, freq)
    
   This function performs simple seasonal decomposition.
   ```
   parameters: method - 'additive' or 'multiplicative'
               freq - Frequency of the data for seasonal decomposition.
   returns: Seasonal decomposition result.
   raises: ValueError if the input method is not supported
   ```
7. summary(self, rolling_window, roc_period, atr_window)
    
   This function returns a summary of rolling window statistics, volatility, and rate of change.
      
### Example Usage
```
from processor import DataProcessor
from Statssummaries import Statssummaries

file_path = "000001.csv"
    
processor = DataProcessor(file_path=file_path, file_format="csv")
data = processor.load_data()

# print("Loaded Data (first 5 rows):")
# print(data.head())

analysis_tools = Statssummaries(data, price_column="close")
    
rolling_stats = analysis_tools.calculate_rolling_statistics(window=20, metrics=['mean', 'std'])
print("Rolling Statistic:")
print(rolling_stats)
    
expanding_stats = analysis_tools.calculate_expanding_statistics(metrics=['mean'])
print("Expanding Statistic:")
print(expanding_stats)
    
atr = analysis_tools.calculate_volatility(method='atr', window=14)
print("ATR:")
print(atr)
    
roc = analysis_tools.calculate_rate_of_change(period=10)
print("ROC:(%)")
print(roc)
    
decomposition = analysis_tools.simple_seasonal_decomposition(method = 'additive', freq=12)
print("Trend:")
print(decomposition['trend'].head(24))
print("Seasonal:")
print(decomposition['seasonal'].head(24))
print("Residual:")
print(decomposition['residual'].head(24))

decomposition = analysis_tools.simple_seasonal_decomposition(method = 'multiplicative', freq=12)
print("Trend:")
print(decomposition['trend'].head(24))
print("Seasonal:")
print(decomposition['seasonal'].head(24))
print("Residual:")
print(decomposition['residual'].head(24))

summary_table = analysis_tools.summary(rolling_window=6, roc_period=6, atr_window=6)
print("Summary:")
print(summary_table.head(48))
```

## Visualization module
The Visualization Module is designed to help users interpret stock market trends through clear, informative visualizations. It includes the following functions:
1. __init__(self, data, analysis_tools)
2. plot_price_with_moving_averages(self, window_short, window_long)
3. plot_volatility(self, atr_window, analysis_tools)
4. plot_rate_of_change(self, period, analysis_tool)
5. plot_seasonal_decomposition(self, freq, analysis_tools)

### Function Description
1. __init__(self, data, analysis_tools)

   This function initializes the dataset and the analysis tools.

2. plot_price_with_moving_averages(self, window_short, window_long)

   This function plots closing prices with short-term and long-term moving averages.
   ```
   parameters: window_short - Window size for short-term moving average. Defaults to 50
               window_long - Window size for long-term moving average. Defaults to 200
   returns: A plot of closing prices with moving averages.
   ```

3. plot_volatility(self, atr_window, analysis_tools)

   This function plots the 0ATR for volatility.
   ```
   parameters: atr_window - Window size for ATR calculation. Defaults to 14
               analysis_tools - Statssummaries object. Defaults to None
   return: plot
   ```
4. plot_rate_of_change(self, period, analysis_tools)

   This function plots the RoC for a specified period.
   ```
   parameters: period - Number of periods for calculating the RoC. Defaults to 10
               analysis_tools - Statssummaries object. Defaults to None
   returns: plot
   ```
5. plot_seasonal_decomposition(self, freq, analysis_tools)

   This function plots the trend, seasonal, and residual components.
   ```
   parameters: freq - Frequency for seasonal decomposition. Defaults to 12.
               analysis_tools - Statssummaries object. Defaults to None.
   returns: plots
   ```
   
### Example Usage

```
import unittest
from unittest.mock import patch
from Visualization import VisualizationModule
from statssummaries import Statssummaries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class TestVisualizationModule(unittest.TestCase):
    def setUp(self):
        '''
         @purpose: To set up sample dataset (date and close) for the tests and initialzes the mock analysis tools.
        '''
        self.data = pd.DataFrame({
            'date': pd.date_range(start='2023-01-01', periods=100, freq='D'),
            'close': np.random.randn(100) + 100
        })
        self.mock_analysis_tools = MockAnalysisTools(self.data)
        self.visualization_module = VisualizationModule(self.data, self.mock_analysis_tools)
    
    def test_plot_price_with_moving_averages(self):
        '''
        @purpose: Verifies that the plot function `plot_price_with_moving_averages` calls plt.show() once with the given window parameters.
        '''
        with patch('matplotlib.pyplot.show') as mock_show:
            self.visualization_module.plot_price_with_moving_averages(window_short=20, window_long=50)
        
        mock_show.assert_called_once()  
    
    def test_plot_volatility(self):
        '''Tests the plotting volatility function.'''
        with patch('matplotlib.pyplot.show') as mock_show:
            self.visualization_module.plot_volatility(atr_window=14)
        mock_show.assert_called_once()  


class MockAnalysisTools:
    '''Imitates the methods calculate_rolling_statistics and calculate_volatility for testing the visualization module and returns mock data iin the functions'''
    def __init__(self, data):
        self.data = data
    
    def calculate_rolling_statistics(self, window, metrics):
        
        return {'Rolling_Mean': [1, 2, 3]}
    
    def calculate_volatility(self, method, window):
        
        return [0.1, 0.2, 0.3]
```
