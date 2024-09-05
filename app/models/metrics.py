import numpy as np
import pandas as pd


def calculate_metrics(y_true, y_pred):
    # Calculate MAPE
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100

    # Calculate MSE
    mse = np.mean((y_true - y_pred) ** 2)

    # Calculate RMSE
    rmse = np.sqrt(mse)

    # Create a DataFrame with metrics
    metrics_df = pd.DataFrame({
        'Metrics': ['MAPE (Mean Absolute Percentage Error)', 'MSE (Mean Squared Error)', 'RMSE (Root Mean Squared Error)'],
        'Value': [f"{mape:.2f}%", f"{mse:.2f}", f"{rmse:.2f}"]
    }).set_index('Metrics')

    return metrics_df
