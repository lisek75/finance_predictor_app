import streamlit as st
from ..models import *
from .utils import *

def is_running():
    st.session_state.running = True

def forecast_section(data):
    st.write("#####")
    n_years = st.slider(
        r"$\textsf{\normalsize Years\ of\ prediction:}$", 
        1, 4, disabled=st.session_state.running
    )
    period = n_years * 365

    predict_pressed = st.button(
        "Predict",
        disabled=st.session_state.running,
        on_click=is_running, key='predict_button'
    )

    if predict_pressed:
        with st.spinner('🔮 Fitting the crystal ball... 🧙‍♂️'):
            m, forecast = fit_prophet_model(data, period)

        with st.spinner('🤹‍♂️ Juggling some numbers... 🤔'):
            df_cv = cross_validate_model(m)

        metrics_df = calculate_metrics(df_cv['y'], df_cv['yhat'])

        # Calculate model accuracy
        global_mape = metrics_df.loc['MAPE (Mean Absolute Percentage Error)', 'Value']
        m_accuracy = 100 - float(global_mape.strip('%')) 

        forecast_fig = plot_forecast(m, forecast)

        st.session_state.output_predict = (forecast_fig, m_accuracy, metrics_df, forecast, data)
        st.session_state.running = False
        st.rerun()

    if "output_predict" in st.session_state and st.session_state.output_predict:
        forecast_fig, m_accuracy, metrics_df, forecast, data = st.session_state.output_predict

        st.write('#####')
        st.markdown(f"<p class='model-accuracy'>Model Accuracy: {m_accuracy:.2f}%</p>", unsafe_allow_html=True)

        # Add instruction for interacting with the chart
        st.markdown(
            """
            <div class="tip-box">
                ℹ️ <i>Tip: Hover over the chart and click the box icon to view it in full screen.</i>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.write('#####')
        st.plotly_chart(forecast_fig, use_container_width=True)

        st.write("**Metrics**")
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
                - Gives an error metric in the same units as the data.<br>
                - Lower RMSE means better accuracy.
            """, unsafe_allow_html=True)
        st.dataframe(metrics_df, width=800)

        display_data(data, forecast, "forecast")


