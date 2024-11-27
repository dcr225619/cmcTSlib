import matplotlib.pyplot as plt


class VisualizationModule:
    def __init__(self, data, analysis_tools):  
        self.analysis_tools = analysis_tools
    
    def plot_price_with_moving_averages(self, window_short=50, window_long=200):
        '''
        @purpose: To plot closing prices with short-term and long-term moving averages.
        @parameters: 
            - Window size for short-term moving average. Defaults to 50.
            - Window size for long-term moving average. Defaults to 200.
        @return: A plot of closing prices with moving averages.
        '''
        rolling_stats_short = self.analysis_tools.calculate_rolling_statistics(window=window_short, metrics=['mean'])
        rolling_stats_long = self.analysis_tools.calculate_rolling_statistics(window=window_long, metrics=['mean'])
        
        plt.figure(figsize=(14, 8))
        plt.plot(self.analysis_tools.data['close'], label='Closing Price')
        plt.plot(rolling_stats_short['Rolling_Mean'], label=f'{window_short}-day MA')
        plt.plot(rolling_stats_long['Rolling_Mean'], label=f'{window_long}-day MA')
        plt.title('Stock Price with Moving Averages')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.show()
    
    def plot_volatility(self, atr_window=14, analysis_tools=None):
        '''
        @purpose: To plot the 0ATR for volatility.
        @parameters: 
            - Window size for ATR calculation. Defaults to 14.
        @return: plot 
        '''
        
        if analysis_tools is None:
            analysis_tools = self.analysis_tools  
        
        atr = analysis_tools.calculate_volatility(method='atr', window=atr_window)
        
        plt.figure(figsize=(14, 6))
        plt.plot(atr, label='ATR (Volatility)')
        plt.title('Volatility (ATR)')
        plt.xlabel('Date')
        plt.ylabel('ATR')
        plt.legend()
        plt.show()
    
    def plot_rate_of_change(self, period=10, analysis_tools=None):
        '''
        @purpose: To plot the RoC for a specified period.
        @parameters: 
            - Number of periods for calculating the RoC. Defaults to 10.
            - Statssummaries object. Defaults to None.
        @return: A plot 
        '''
        if analysis_tools is None:
            analysis_tools = self.analysis_tools  
        
        roc = analysis_tools.calculate_rate_of_change(period=period)
        
        plt.figure(figsize=(14, 6))
        plt.plot(roc, label=f'Rate of Change (%) - {period} periods')
        plt.title(f'Rate of Change (Period={period})')
        plt.xlabel('Date')
        plt.ylabel('RoC (%)')
        plt.legend()
        plt.show()
    
    def plot_seasonal_decomposition(self, freq=12, analysis_tools=None):
        '''
        @purpose: To plot the trend, seasonal, and residual components 
        @parameters: 
            - Frequency for seasonal decomposition. Defaults to 12.
            - Statssummaries object. Defaults to None.
        @return: plots 
        '''
        if analysis_tools is None:
            analysis_tools = self.analysis_tools 
        decomposition = analysis_tools.simple_seasonal_decomposition(freq=freq)
        
        plt.figure(figsize=(14, 10))
        plt.subplot(3, 1, 1)
        plt.plot(decomposition['trend'], label='Trend')
        plt.title('Trend')
        plt.legend()
        
        plt.subplot(3, 1, 2)
        plt.plot(decomposition['seasonal'], label='Seasonal')
        plt.title('Seasonal')
        plt.legend()
        
        plt.subplot(3, 1, 3)
        plt.plot(decomposition['residual'], label='Residual')
        plt.title('Residual')
        plt.legend()
        
        plt.tight_layout()
        plt.show()

