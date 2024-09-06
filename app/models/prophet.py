from prophet import Prophet
from prophet.diagnostics import cross_validation
import warnings
import plotly.graph_objects as go
import streamlit as st


def fit_prophet_model(data, period):
    """
    Fit a Prophet model to the provided data and forecast for the given period.

    Args:
        data (pd.DataFrame): DataFrame with columns 'Date' and 'Close'.
        period (int): Number of periods to forecast into the future.

    Returns:
        m (Prophet): Fitted Prophet model.
        forecast (pd.DataFrame): Forecasted values.
    """
    try:
        df_train = data[['Date', 'Close']].rename(columns={"Date": "ds", "Close": "y"})
        m = Prophet()
        m.fit(df_train)
        future = m.make_future_dataframe(periods=period)
        forecast = m.predict(future)
        return m, forecast
    except Exception as e:
        print(f"Error fitting model: {e}")
        return None, None

def cross_validate_model(m, initial='730 days', period='180 days', horizon='365 days'):
    """
    Cross-validation evaluates a model's performance and stability 
    across different data subsets to ensure robust predictions.

    Args:
        m (Prophet): Fitted Prophet model.
        initial (str): Initial training period.
        period (str): Period between successive validation sets.
        horizon (str): Forecast horizon.

    Returns:
        df_cv (pd.DataFrame): Cross-validation results.
    """
    try:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=FutureWarning)
            df_cv = cross_validation(m, initial=initial, period=period, horizon=horizon)
        return df_cv
    except Exception as e:
        print(f"Error during cross-validation: {e}")
        return None


def plot_forecast(m, forecast):
    """
    Plot the forecast using Plotly.

    Args:
        m (Prophet): Fitted Prophet model.
        forecast (pd.DataFrame): Forecasted values.

    Returns:
        fig (go.Figure): Plotly figure object.
    """

    try:
        # Common style dictionary for fonts
        common_font_style = dict(size=14, color='#ffffff')

        # Get the historical data
        df = m.history.copy()

        # Create figure
        fig = go.Figure()

        # Actual data points
        fig.add_trace(go.Scatter(
            x=df['ds'], 
            y=df['y'], 
            mode='lines',
            name='Actual',
            marker=dict(color='#87CEEB', size=3),
            hovertemplate='Actual: %{y:.2f}<extra></extra>' 
        ))

        # Forecast line
        fig.add_trace(go.Scatter(
            x=forecast['ds'], 
            y=forecast['yhat'], 
            mode='lines',
            name='Predicted',
            line=dict(color='#FF0000', width=6),
            hovertemplate='Predicted: %{y:.2f}<extra></extra>'
        ))

        # Customize layout
        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Value',
            margin=dict(t=20, b=0, l=0, r=0),
            font=common_font_style,  # Apply the common font to the whole chart
            hovermode='x',
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1,
                xanchor='center',
                x=0.5,
                font=common_font_style  # Use the same common font style for the legend
            )
        )

        return fig
    except Exception as e:
        st.error(f"Error plotting forecast: {e}")
        return None
