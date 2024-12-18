import pandas as pd
import numpy as np
from processor import DataProcessor

class Statssummaries:
    def __init__(self, data, price_column='close'):
        """
        Initializations
        :param data: DataFrame includes market data
        :param price_column: the name of price column
        """
        self.data = data.copy()
        self.price_column = price_column

        # Check if the index is datetime index already
        if not isinstance(self.data.index, pd.DatetimeIndex):
            raise ValueError("Index must be a DatetimeIndex. Ensure your data's index is properly set to datetime.")


    def calculate_rolling_statistics(self, window=1, metrics=['mean', 'median', 'std']):
        """
        Calculate the rolling window statistics.
        :param window: Window size for rolling calculations.
        :param metrics: List of metrics to calculate ('mean', 'median', 'std').
        :return: DataFrame with rolling statistics.
        """
        results = {}
        for metric in metrics:
            if metric == 'mean':
                results['Rolling_Mean'] = self.data[self.price_column].rolling(window).mean()  # moving average
            elif metric == 'median':
                results['Rolling_Median'] = self.data[self.price_column].rolling(window).median()
            elif metric == 'std':
                results['Rolling_Std'] = self.data[self.price_column].rolling(window).std()
            else:
                raise ValueError(f"Unsupported metric: {metric}")

        return pd.DataFrame(results)

    def calculate_expanding_statistics(self, window=1, metrics=['mean', 'std']):
        """
        Calculate expanding window statistics.
        :param metrics: List of metrics to calculate ('mean', 'std').
        :return: DataFrame with expanding statistics.
        """
        results = {}
        for metric in metrics:
            if metric == 'mean':
                results['Expanding_Mean'] = self.data[self.price_column].expanding(window).mean()
            elif metric == 'std':
                results['Expanding_Std'] = self.data[self.price_column].expanding(window).std()
            else:
                raise ValueError(f"Unsupported metric: {metric}")

        return pd.DataFrame(results)

    def calculate_volatility(self, method='std', window=None):
        """
        Calculate volatility metrics.
        :param method: 'std' (standard deviation) or 'atr' (average true range).
        :param window: Window size for rolling calculations (required for ATR).
        :return: Series with volatility metrics.
        """
        if method == 'std':
            return self.data[self.price_column].rolling(window).std()
        elif method == 'atr':
            if window is None:
                raise ValueError("ATR requires window size to be specified")
            
            high_low = self.data['high'] - self.data['low']
            high_close = np.abs(self.data['high'] - self.data[self.price_column].shift())
            low_close = np.abs(self.data['low'] - self.data[self.price_column].shift())
            tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
            atr = tr.rolling(window).mean()
            return atr
        else:
            raise ValueError(f"Unsupported method: {method}")

    def calculate_rate_of_change(self, period):
        """
        Calculate the rate of change (RoC) metric.
        :param period: Period for RoC calculation.
        :return: Series with RoC values.
        """
        return self.data[self.price_column].pct_change(periods=period) * 100 # Percentage change between neighboring data points

    def simple_seasonal_decomposition(self, method = 'additive', freq = 12):
        """
        Perform simple seasonal decomposition
        :param method: residual can be computed by 'additive' or 'multiplicative'
        :param freq: Frequency of the data for seasonal decomposition.
        :return: Seasonal decomposition result.
        """
        # trend
        trend = self.data[self.price_column].rolling(window=freq, center=True).mean()

        # seasonal decomposition
        if method == 'additive':
            detrended = self.data[self.price_column] - trend
        elif method == 'multiplicative':
            detrended = self.data[self.price_column] / trend
        else:
            raise ValueError("Unsupported method. Use 'additive' or 'multiplicative'.")

        seasonal = detrended.groupby(self.data.index.to_period(f"{freq}D").strftime('%d')).transform('mean')

        # residual
        if method == 'additive':
            residual = self.data[self.price_column] - trend - seasonal
        elif method == 'multiplicative':
            residual = self.data[self.price_column] / (trend * seasonal)

        return {
            'trend': trend,
            'seasonal': seasonal,
            'residual': residual
        }

    def summary(self, rolling_window=20, roc_period=10, atr_window=14):
        """
        Return a summary of rolling window statistics, volatility and rate of change.
        """
        summary = self.data.copy()
        
        rolling_stats = self.calculate_rolling_statistics(rolling_window, metrics=['mean', 'std'])
        summary = summary.join(rolling_stats)
        
        summary['Rate_of_Change(%)'] = self.calculate_rate_of_change(roc_period)
        
        summary['ATR'] = self.calculate_volatility(method='atr', window=atr_window)
        
        summary.fillna(0, inplace=True)  # 

        return summary
