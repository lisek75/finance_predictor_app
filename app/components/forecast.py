import streamlit as st
from ..models import *
from .utils import *

def is_running():
    st.session_state.running = True

def forecast_section(data, ticker):
    """
    Fit a Prophet model to the provided data and forecast for the given period.

    Args:
        data (pd.DataFrame): DataFrame with historical data for the ticker, including 'Date' and 'Close'.

    Functionality:
        - Allows the user to set a prediction period in years.
        - Fits a Prophet model and returns forecasted data.
        - Displays model accuracy and relevant performance metrics.
    """

    st.sidebar.write("####")

    # Slider to allow the user to select the number of years for prediction
    n_years = st.sidebar.slider(
        r"$\textsf{\normalsize Years\ of\ prediction:}$", 
        1, 4, disabled=st.session_state.running
    )

    # Calculate the forecast period in days
    period = n_years * 365

    # Button to trigger the prediction process
    predict_pressed = st.sidebar.button(
        "Predict",
        disabled=st.session_state.running,
        on_click=is_running, key='predict_button'
    )

    if predict_pressed:
        # Display a loading spinner while fitting the model
        with st.spinner('🔮 Fitting the crystal ball... 🧙‍♂️'):
            m, forecast = fit_prophet_model(data, period) # Fit the Prophet model

        # Display a spinner while performing cross-validation
        with st.spinner('🤹‍♂️ Juggling some numbers... 🤔'):
            df_cv = cross_validate_model(m) # Cross-validate the model

        # Calculate model performance metrics
        metrics_df = calculate_metrics(df_cv['y'], df_cv['yhat'])

        # Extract and calculate the model accuracy from MAPE
        global_mape = metrics_df.loc['MAPE (Mean Absolute Percentage Error)', 'Value']
        m_accuracy = 100 - float(global_mape.strip('%')) 

        # Generate the forecast plot
        forecast_fig = plot_forecast(m, forecast)

        # Store the results in session state to display later
        st.session_state.output_predict = (forecast_fig, m_accuracy, metrics_df, forecast, data)
        st.session_state.running = False
        st.rerun() # Refresh the page to update the displayed results

    # Check if the forecast results are stored in session state
    if "output_predict" in st.session_state and st.session_state.output_predict:
        # Retrieve the stored forecast results
        forecast_fig, m_accuracy, metrics_df, forecast, data = st.session_state.output_predict

        st.markdown(f"<h2 style='text-align: center;'>🔮 Forecast Data for {ticker}</h2>", unsafe_allow_html=True)

        # Display the forecasted data
        display_data(data, forecast, "forecast")

        st.write('######')

        # Display the model accuracy
        st.markdown(f"<h5 class='model-accuracy'>Model Accuracy: {m_accuracy:.2f}%</h5>", unsafe_allow_html=True)

        # Tip for interacting with the chart
        st.markdown(
            """
            <div class="tip-box">
                ℹ️ <i>Tip: Hover over the chart and click the box icon to view it in full screen.</i>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write('#####')

        # Display the forecast plot
        st.plotly_chart(forecast_fig, use_container_width=True)

        st.write("**Metrics**")

        # Expandable section for showing metric definitions
        with st.expander("Metric Definitions"):
            st.markdown("""
            - **MAPE**: Mean Absolute Percentage Error<br>
                - Measures how far off the model's predictions are from the actual values, expressed as a percentage.<br>
                - For example, a MAPE of 16% means the model's predictions are off by an average of 16% from the actual values.<br>
                - Lower MAPE values indicate better model accuracy.
            <br><br>
            - **MAE**: Mean Absolute Error<br>
                - Measures the average absolute difference between predicted and actual values.<br>
                - Lower MAE indicates better model performance.
            <br><br>
            - **RMSE**: Root Mean Squared Error<br>
                - Measures the square root of the average squared differences between predictions and actual values.<br>
                - Lower RMSE means better accuracy.
            """, unsafe_allow_html=True)

        # Display the metrics DataFrame
        st.dataframe(metrics_df, width=800)




