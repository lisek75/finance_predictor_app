from prophet import Prophet
from prophet.diagnostics import cross_validation
from prophet.plot import plot_plotly
import plotly.graph_objs as go
import warnings

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

# Plot the forecast
def plot_forecast(m, forecast):
    forecast_fig = plot_plotly(m, forecast)

    # Remove existing legend entries
    for trace in forecast_fig['data']:
        trace['showlegend'] = False

    # Add custom legend entries for clarity
    legend_entries = [
        go.Scatter(x=[None], y=[None], mode='markers', marker=dict(size=10, color='black'),
                   legendgroup='Actual Data', showlegend=True, name='Actual Data'),
        go.Scatter(x=[None], y=[None], mode='lines', line=dict(color='#4494be'),
                   legendgroup='Forecast', showlegend=True, name='Forecast'),
        go.Scatter(x=[None], y=[None], mode='lines', fill='toself', fillcolor='#c0eaf8',
                   line=dict(color='#c0eaf8'), legendgroup='Uncertainty', showlegend=True, name='Uncertainty Interval')
    ]

    forecast_fig.add_traces(legend_entries)

    forecast_fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Forecasted Value",
        xaxis=dict(rangeslider=dict(visible=False), type="date"),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5)
    )
    return forecast_fig
