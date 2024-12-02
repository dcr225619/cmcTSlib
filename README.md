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
   '''
   parameters: file_path - path to the data file
               file_format - format of the data file (default is 'csv')
   '''
2. load_data(self)
   This function loads the data based on the file format.
   '''
   returns: self.data - loaded dataset
   raises: ValueError if the file format is not supported
   '''
   
4. resample_data(self, frequency: str = "D", agg_method: str = "mean")
   This function resamples the time series data to a specified frequency.
   '''
   parameters: frequency - the desired frequency ('D' for daily, 'W' for weekly, 'M' for monthly) (using pd)
               agg_method - aggregation method ('mean', 'sum', 'last')
   returns: pd.DataFrame - resampled data
   raises: ValueError if data not loaded
           ValueError if the input aggregation method is not supported
   '''
   
5. detect_outliers(self, column: str, method: str = "zscore", threshold: float = 3.0)
   This function detects outliers in the data based on the specified method.
   '''
   parameters: column - the column to check for outliers
               method - outlier detection method (default is 'zscore')
               threshold - threshold for identifying outliers (default of 3.0 for z-score)
   returns: pd.Series - boolean series indicating outliers
   raises: ValueError if the input outlier detection method is not supported
           ValueError if input column not found in data
   '''
   
7. smooth_data(self, column: str, window_size: int = 5)
   This function smooths the data using a rolling average.
   '''
   parameters: column - the column to smooth
               window_size - the size of the moving window (default is 5)       
   returns: pd.Series - smoothed data as a rolling average
   raises: ValueError if input column not found in data
   '''

### Example Usage


## Statistical Summaries module
The Statistical Summaries Module provides users with essential metrics for analyzing trends, volatility, and other characteristics of stock market data. It includes the following functions:

## Visualization module
The Visualization Module is designed to help users interpret stock market trends through clear, informative visualizations. It includes the following functions:
