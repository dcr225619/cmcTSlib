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

    