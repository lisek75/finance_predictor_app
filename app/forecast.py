import streamlit as st
from models import *

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
        global_mape = mean_absolute_percentage_error(df_cv['y'], df_cv['yhat'])
        m_accuracy = 100 - global_mape

        forecast_fig = plot_forecast(m, forecast)

        st.session_state.output_predict = (forecast_fig, m_accuracy)
        st.session_state.running = False
        st.rerun()

    if "output_predict" in st.session_state and st.session_state.output_predict:
        forecast_fig, m_accuracy = st.session_state.output_predict
        st.markdown(f"<p class='model-accuracy'>Model Accuracy: {m_accuracy:.2f}%</p>", unsafe_allow_html=True)
        st.altair_chart(forecast_fig, use_container_width=True)