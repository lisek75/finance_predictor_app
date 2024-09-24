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
        - Allows the user to select the ML model.
        - Allows the user to set a prediction period in years.
        - Fits the selected model and returns forecasted data.
        - Displays model accuracy and relevant performance metrics.
    """

    st.sidebar.write("####")

    # Slider to allow the user to select the number of years for prediction
    n_years = st.sidebar.slider(
        r"$\textsf{\normalsize Years\ of\ prediction:}$", 
        1, 5, disabled=st.session_state.running
    )

    st.sidebar.write('######')

    # Calculate the forecast period in days
    period = n_years * 365

    # Checkbox to select between Prophet and ARIMA
    model_selection = st.sidebar.radio(
        r"$\textsf{\normalsize Select\ ML\ model:}$", 
        ("Prophet", "ARIMA"),
        disabled=st.session_state.running
    )

    # Check if the selected model has changed
    if st.session_state.previous_model != model_selection:
        # If the model has changed, reset session state for output prediction
        st.session_state.output_predict = None  # Clear the stored prediction data
        st.session_state.running = False  # Reset the running flag if needed

        # Store the current selected model as the previous one for future comparisons
        st.session_state.previous_model = model_selection

    st.sidebar.write('######')

    # Button to trigger the prediction process
    predict_pressed = st.sidebar.button(
        "Predict",
        disabled=st.session_state.running,
        on_click=is_running, key='predict_button'
    )

    if predict_pressed:

        if model_selection == "Prophet":
            # Display a loading spinner while fitting the model
            with st.spinner('🔮 Fitting the crystal ball... 🧙‍♂️'):
                m, forecast = fit_prophet_model(data, period) # Fit the Prophet model

            # Display a spinner while performing cross-validation
            with st.spinner('🤹‍♂️ Juggling some numbers... 🤔'):
                df_cv = cross_validate_prophet(m) # Cross-validate the model

            # Calculate model performance metrics
            metrics_df = calculate_metrics(df_cv['y'], df_cv['yhat'])

            # Extract and calculate the model accuracy from MAPE
            global_mape = metrics_df.loc['MAPE (Mean Absolute Percentage Error)', 'Value']
            m_accuracy = 100 - float(global_mape.strip('%')) 

            # Generate the forecast plot
            forecast_fig = plot_prophet_forecast(m, forecast)

            # Store the results in session state to display later
            st.session_state.output_predict = (forecast_fig, m_accuracy, metrics_df, forecast, data)
            st.session_state.running = False
            st.rerun() # Refresh the page to update the displayed results

        elif model_selection == "ARIMA":

            # Drop unecessary columns
            data = data.drop(['Open', 'High', 'Low', 'Volume', 'Adj Close'], axis= 1)

            # Display a loading spinner while fitting the model
            with st.spinner('🔮 Fitting the ARIMA model...'):
                m, forecast = fit_arima_model(data, period)  # Fit ARIMA model

            # Display a spinner while performing cross-validation
            with st.spinner('🤹‍♂️ Juggling some numbers... 🤔'):
                df_cv = cross_validation_arima(data, m) # Cross-validate the model

            # Calculate ARIMA model metrics
            metrics_df = calculate_metrics(df_cv['Actual'], df_cv['Predicted'])

            # Accuracy
            mape_value = metrics_df.loc['MAPE (Mean Absolute Percentage Error)', 'Value'].strip('%')
            m_accuracy = 100 - float(mape_value)

            # Generate the ARIMA forecast plot
            forecast_fig = plot_arima_forecast(data, forecast)

            # Store the results in session state
            st.session_state.output_predict = (forecast_fig, m_accuracy, metrics_df, forecast, data)
            st.session_state.running = False
            st.rerun()  # Refresh the page


    # Display the prophet forecast results
    if "output_predict" in st.session_state and st.session_state.output_predict:
        # Retrieve the stored forecast results
        forecast_fig, m_accuracy, metrics_df, forecast, data = st.session_state.output_predict

        st.markdown(f"<h2>🔮 Forecast Data for {ticker} with {model_selection}</h2>", unsafe_allow_html=True)

        st.write('######')

        st.write(f"{model_selection} Forecast Data")
        # Display the forecasted data
        display_data(data, forecast, "forecast", model_selection)

        # Display the model accuracy
        st.markdown(f"<h5 class='model-accuracy'>{model_selection} Model Accuracy: {m_accuracy:.2f}%</h5>", unsafe_allow_html=True)

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
        # st.pyplot(forecast_fig)

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




