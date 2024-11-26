import pandas as pd
import numpy as np


class DataProcessor:
    """
    for handling and preprocessing
    """
    def __init__(self, file_path: str, file_format: str = "csv"):
        """
        initialize the data processor with the file path and format
        parameters: file_path - path to the data file
        file_format - format of the data file (default is 'csv')
        """
        self.file_path = file_path
        self.file_format = file_format
        self.data = None

    def load_data(self):
        """
        load the data based on the file format
        """
        if self.file_format == "csv":
            self.data = pd.read_csv(self.file_path, parse_dates=True, index_col=0)
        elif self.file_format in ["xlsx", "xls"]:
            self.data = pd.read_excel(self.file_path, parse_dates=True, index_col=0)
        elif self.file_format == "jsonl":
            self.data = pd.read_json(self.file_path, lines=True)
        elif self.file_format == "parquet":
            self.data = pd.read_parquet(self.file_path)
        elif self.file_format == "hdf5":
            self.data = pd.read_hdf(self.file_path)
        else:
            raise ValueError(f"Unsupported file format: {self.file_format}")
        return self.data

    def resample_data(self, frequency: str = "D", agg_method: str = "mean"):
        """
        resample the time series data to a specified frequency
        parameters: frequency - the desired frequency ('D' for daily, 'W' for weekly, 'M' for monthly) (using pd)
        - agg_method - aggregation method ('mean', 'sum', 'last')
        returns: pd.DataFrame - resampled data
        """
        if self.data is None:
            raise ValueError("Data not loaded. Please load the data first.")
        
        if agg_method == "mean":
            resampled_data = self.data.resample(frequency).mean()
        elif agg_method == "sum":
            resampled_data = self.data.resample(frequency).sum()
        elif agg_method == "last":
            resampled_data = self.data.resample(frequency).last()
        else:
            raise ValueError(f"Unsupported aggregation method: {agg_method}")
        return resampled_data

    def detect_outliers(self, column: str, method: str = "zscore", threshold: float = 3.0):
        """
        detect outliers in the data based on the specified method
        parameters: column - the column to check for outliers
        method - outlier detection method (default is 'zscore')
        threshold - threshold for identifying outliers (default of 3.0 for z-score)
        returns: pd.Series - boolean series indicating outliers
        """
        if column not in self.data.columns:
            raise ValueError(f"Column {column} not found in data.")
        
        if method == "zscore":
            z_scores = (self.data[column] - self.data[column].mean()) / self.data[column].std()
            outliers = abs(z_scores) > threshold
        elif method == "iqr":
            Q1 = self.data[column].quantile(0.25)
            Q3 = self.data[column].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ~self.data[column].between(Q1 - 1.5 * IQR, Q3 + 1.5 * IQR)
        else:
            raise ValueError(f"Unsupported outlier detection method: {method}")
        return outliers

    def smooth_data(self, column: str, window_size: int = 5):
        """
        smooth the data using a rolling average
        parameters: column - the column to smooth
        window_size - the size of the moving window (default is 5)       
        Returns: pd.Series - smoothed data as a rolling average
        """
        if column not in self.data.columns:
            raise ValueError(f"Column {column} not found in data.")
        
        return self.data[column].rolling(window=window_size).mean()
