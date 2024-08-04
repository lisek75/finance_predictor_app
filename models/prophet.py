from prophet import Prophet
from prophet.diagnostics import cross_validation
import warnings
import altair as alt

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
    Perform cross-validation on the provided Prophet model.

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
    Plot the forecast using Altair.

    Args:
        m (Prophet): Fitted Prophet model.
        forecast (pd.DataFrame): Forecasted values.

    Returns:
        chart (alt.Chart): Altair chart object.
    """
    try:
        # Get the historical data
        df = m.history.copy()

        # Create a color scale for the legend
        color_scale = alt.Scale(
            domain=['Actual', 'Predicted', 'Uncertainty'],
            range=['black', '#4494be', '#FFB6C1']
        )

        # Actual data points
        actual = alt.Chart(df).mark_point(size=5).encode(
            x=alt.X('ds:T', axis=alt.Axis(title='date', tickCount="year")),
            y=alt.Y('y:Q', title='forecast'),
            tooltip=[alt.Tooltip('ds:T', title='Date'), alt.Tooltip('y:Q', title='Actual Value', format='.2f')],
            color=alt.value('black')
        ).transform_calculate(
            legend_label='"Actual"'
        ).encode(
            color=alt.Color('legend_label:N', scale=color_scale)
        )

        # Forecast line
        forecast_line = alt.Chart(forecast).mark_line(strokeWidth=3).encode(
            x='ds:T',
            y='yhat:Q',
            tooltip=[alt.Tooltip('ds:T', title='Date'), alt.Tooltip('yhat:Q', title='Predicted Value', format='.2f')],
            color=alt.value('#4494be')
        ).transform_calculate(
            legend_label='"Predicted"'
        ).encode(
            color=alt.Color('legend_label:N', scale=color_scale)
        )

        # Uncertainty interval
        uncertainty = alt.Chart(forecast).mark_area(opacity=0.3).encode(
            x='ds:T',
            y='yhat_lower:Q',
            y2='yhat_upper:Q',
            tooltip=[alt.Tooltip('ds:T', title='Date'), alt.Tooltip('yhat_lower:Q', title='Lower Bound'), alt.Tooltip('yhat_upper:Q', title='Upper Bound')],
            color=alt.value('#FFB6C1')
        ).transform_calculate(
            legend_label='"Uncertainty"'
        ).encode(
            color=alt.Color('legend_label:N', scale=color_scale)
        )

        # Combine the layers
        chart = alt.layer(
            uncertainty,
            forecast_line,
            actual
        ).properties(
            width=800,
            height=400
        ).configure_legend(
            title=None,
            orient='bottom',
            direction='vertical',
            strokeColor='gray',
            fillColor='#EEEEEE',
            padding=10,
            cornerRadius=10,
        ).interactive()

        return chart
    except Exception as e:
        print(f"Error plotting forecast: {e}")
        return None