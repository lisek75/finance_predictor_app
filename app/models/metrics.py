import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error


def calculate_metrics(actual, predicted):
    """
    Calculate evaluation metrics
    
    Args:
        actual: The actual values from the test data.
        predicted: The forecasted values by cross validation process.
        
    Returns:
        pd.DataFrame: DataFrame containing MAE, MAPE, and RMSE metrics.
    """
    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    mape = mean_absolute_percentage_error(actual, predicted) * 100
    
    metrics_df = pd.DataFrame({
        'Metrics': ['MAPE (Mean Absolute Percentage Error)', 'MAE (Mean Absolute Error)', 'RMSE (Root Mean Squared Error)'],
        'Value': [f"{mape:.2f}%", f"{mae:.2f}", f"{rmse:.2f}"]
    }).set_index('Metrics')

    return metrics_df

