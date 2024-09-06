import numpy as np
import pandas as pd


def calculate_metrics(y_true, y_pred):
    # Calculate metrics
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    mae = np.mean(np.abs(y_true - y_pred))
    rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))

    # Create a DataFrame with metrics
    metrics_df = pd.DataFrame({
        'Metrics': ['MAPE (Mean Absolute Percentage Error)', 'MAE (Mean Absolute Error)', 'RMSE (Root Mean Squared Error)'],
        'Value': [f"{mape:.2f}%", f"{mae:.2f}", f"{rmse:.2f}"]
    }).set_index('Metrics')

    return metrics_df
