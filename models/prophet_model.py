#prophet_model.py

from prophet import Prophet
from prophet.diagnostics import cross_validation
import warnings
import altair as alt

# Fit the model
def fit_prophet_model(data, period):
    df_train = data[['Date', 'Close']].rename(columns={"Date": "ds", "Close": "y"})
    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)
    return m, forecast

# Perform cross-validation
def cross_validate_model(m):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=FutureWarning)
        df_cv = cross_validation(m, initial='730 days', period='180 days', horizon='365 days')
    return df_cv

# Plot the forecast using Altair
def plot_forecast(m, forecast):
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
        direction='horizontal',
        strokeColor='gray',
        fillColor='#EEEEEE',
        padding=10,
        cornerRadius=10,
    ).interactive()

    return chart
