import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error

def calculate_metrics_prophet(y_true, y_pred):
    """
    Calculate common performance metrics for a model's predictions: MAPE, MAE, and RMSE.

    Args:
        y_true (np.ndarray or pd.Series): The actual values.
        y_pred (np.ndarray or pd.Series): The predicted values by the model.

    Returns:
        pd.DataFrame: A DataFrame containing the calculated MAPE, MAE, and RMSE metrics.
    """

    # Calculate MAPE (Mean Absolute Percentage Error)
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100

    # Calculate MAE (Mean Absolute Error)
    mae = np.mean(np.abs(y_true - y_pred))

    # Calculate RMSE (Root Mean Squared Error)
    rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))

    # Create a DataFrame to display the metrics
    metrics_df = pd.DataFrame({
        'Metrics': ['MAPE (Mean Absolute Percentage Error)', 'MAE (Mean Absolute Error)', 'RMSE (Root Mean Squared Error)'],
        'Value': [f"{mape:.2f}%", f"{mae:.2f}", f"{rmse:.2f}"]
    }).set_index('Metrics')

    return metrics_df

def calculate_metrics_arima(actual, predicted):
    """
    Calculate evaluation metrics for ARIMA model.
    
    Args:
        actual (pd.Series or list): The actual values from the test data.
        predicted (pd.Series or list): The forecasted values by the ARIMA model.
        
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

