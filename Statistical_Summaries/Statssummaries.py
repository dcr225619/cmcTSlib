import pandas as pd
import numpy as np

class Statssummaries:
    def __init__(self, data, datetime_column='date', price_column='close'):
        """
        Initializations
        :param data: DataFrame includes market data
        :param datetime_column: the name of date column
        :param price_column: the name of price column
        """
        self.data = data.copy()
        self.price_column = price_column

        # transfer the datetimes as indices
        self.data[datetime_column] = pd.to_datetime(self.data[datetime_column])
        self.data.set_index(datetime_column, inplace=True)

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
                results['Rolling_Mean'] = self.data[self.price_column].rolling(window).mean()
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
        return self.data[self.price_column].pct_change(periods=period) * 100

    def simple_seasonal_decomposition(self, freq):
        """
        Perform simple seasonal decomposition
        :param freq: Frequency of the data for seasonal decomposition.
        :return: Seasonal decomposition result.
        """
        # trend
        trend = self.data[self.price_column].rolling(window=freq, center=True).mean()

        # seasonal decomposition
        detrended = self.data[self.price_column] - trend
        seasonal = detrended.groupby(self.data.index.to_period(f"{freq}D").strftime('%d')).transform('mean')

        # residual
        residual = self.data[self.price_column] - trend - seasonal

        return {
            'trend': trend,
            'seasonal': seasonal,
            'residual': residual
        }

    def summary(self, rolling_window=20, roc_period=10, atr_window=14):
        summary = self.data.copy()
        
        rolling_stats = self.calculate_rolling_statistics(rolling_window, metrics=['mean', 'std'])
        summary = summary.join(rolling_stats)
        
        summary['Rate_of_Change(%)'] = self.calculate_rate_of_change(roc_period)
        
        summary['ATR'] = self.calculate_volatility(method='atr', window=atr_window)
        
        summary.fillna(0, inplace=True)  # 

        return summary


if __name__ == "__main__":

    file_path = "000001.csv"
    #
    data = pd.read_csv(file_path)

    analysis_tools = Statssummaries(data, datetime_column="date", price_column="close")
    
    # rolling_stats = analysis_tools.calculate_rolling_statistics(window=20, metrics=['mean', 'std'])
    # print("Rolling Statistic:")
    # print(rolling_stats)
    
    # expanding_stats = analysis_tools.calculate_expanding_statistics(metrics=['mean'])
    # print("Expanding Statistic:")
    # print(expanding_stats)
    
    # atr = analysis_tools.calculate_volatility(method='atr', window=14)
    # print("ATR:")
    # print(atr)
    
    # roc = analysis_tools.calculate_rate_of_change(period=10)
    # print("ROC:(%)")
    # print(roc)
    
    decomposition = analysis_tools.simple_seasonal_decomposition(freq=12)
    print("Trend:")
    print(decomposition['trend'].head(24))
    print("Seasonal:")
    print(decomposition['seasonal'].head(24))
    print("Residual:")
    print(decomposition['residual'].head(24))

    summary_table = analysis_tools.summary(rolling_window=20, roc_period=10, atr_window=14)
    print("Summary:")
    print(summary_table.head(24))
