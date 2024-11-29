from processor import DataProcessor
from Statssummaries import Statssummaries

file_path = "000001.csv"
    
processor = DataProcessor(file_path=file_path, file_format="csv")
data = processor.load_data()

# print("Loaded Data (first 5 rows):")
# print(data.head())

analysis_tools = Statssummaries(data, price_column="close")
    
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
    
# decomposition = analysis_tools.simple_seasonal_decomposition(method = 'additive', freq=12)
# print("Trend:")
# print(decomposition['trend'].head(24))
# print("Seasonal:")
# print(decomposition['seasonal'].head(24))
# print("Residual:")
# print(decomposition['residual'].head(24))

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