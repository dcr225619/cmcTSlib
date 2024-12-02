# cmcTSlib
Time Series Analysis package cmcTSlib for DS5010 course project.
This README file includes a brief introduction to the module and usage instructions.

## Data Processing module
The Data Processing Module manages financial time series data intake and preparation. It includes the following functions:
1. __init__(self, file_path: str, file_format: str = "csv")
2. load_data(self)
3. resample_data(self, frequency: str = "D", agg_method: str = "mean")
4. detect_outliers(self, column: str, method: str = "zscore", threshold: float = 3.0)
5. smooth_data(self, column: str, window_size: int = 5)

### Function Description
1. __init__(self, file_path: str, file_format: str = "csv")
   
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
   
3. resample_data(self, frequency: str = "D", agg_method: str = "mean")

   This function resamples the time series data to a specified frequency.
   ```
   parameters: frequency - the desired frequency ('D' for daily, 'W' for weekly, 'M' for monthly) (using pd)
               agg_method - aggregation method ('mean', 'sum', 'last')
   returns: pd.DataFrame - resampled data
   raises: ValueError if data not loaded
           ValueError if the input aggregation method is not supported
   ```
   
4. detect_outliers(self, column: str, method: str = "zscore", threshold: float = 3.0)
   
   This function detects outliers in the data based on the specified method.
   ```
   parameters: column - the column to check for outliers
               method - outlier detection method (default is 'zscore')
               threshold - threshold for identifying outliers (default of 3.0 for z-score)
   returns: pd.Series - boolean series indicating outliers
   raises: ValueError if the input outlier detection method is not supported
           ValueError if input column not found in data
   ```
   
5. smooth_data(self, column: str, window_size: int = 5)
   
   This function smooths the data using a rolling average.
   ```
   parameters: column - the column to smooth
               window_size - the size of the moving window (default is 5)       
   returns: pd.Series - smoothed data as a rolling average
   raises: ValueError if input column not found in data
   ```

### Example Usage


## Statistical Summaries module
The Statistical Summaries Module provides users with essential metrics for analyzing trends, volatility, and other characteristics of stock market data. It includes the following functions:
1. __init__(self, data, price_column='close')
2. calculate_rolling_statistics(self, window=1, metrics=['mean', 'median', 'std'])
3. calculate_expanding_statistics(self, window=1, metrics=['mean', 'std'])
4. calculate_volatility(self, method='std', window=None)
5. calculate_rate_of_change(self, period)
6. simple_seasonal_decomposition(self, method = 'additive', freq = 12)
7. summary(self, rolling_window=20, roc_period=10, atr_window=14)

### Function Description
1. __init__(self, data, price_column='close')
   
   This function initializes the dataset for summary.
   ```
   parameters: data - DataFrame includes market data
               price_column - the name of price column
   raises: ValueError if the data index is not set to be a DatetimeIndex
   ```
   
2. calculate_rolling_statistics(self, window=1, metrics=['mean', 'median', 'std'])
   
   This function calculates the rolling window statistics.
   ```
   parameters: window - Window size for rolling calculations.
               metrics - List of metrics to calculate ('mean', 'median', 'std').
   returns: pd.DataFrame with rolling statistics.
   raises: ValueError if the input metrics are not supported
   ```
   
3. calculate_expanding_statistics(self, window=1, metrics=['mean', 'std'])
   
   This function calculates expanding window statistics.
   ```
   parameters: metrics - List of metrics to calculate ('mean', 'std').
   returns: pd.DataFrame with expanding statistics.
   raises: ValueError if the input metrics are not supported
   ```

4. calculate_volatility(self, method='std', window=None)
   
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
6. simple_seasonal_decomposition(self, method = 'additive', freq = 12)
    
   This function performs simple seasonal decomposition.
   ```
   parameters: freq - Frequency of the data for seasonal decomposition.
   returns: Seasonal decomposition result.
   raises: ValueError if the input method is not supported
   ```
7. summary(self, rolling_window=20, roc_period=10, atr_window=14)
    
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
