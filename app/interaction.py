import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from models import *
from data import plot_data

import time 

def is_running():
    st.session_state.running = True

def get_user_ticker():
    return st.text_input(
        r"$\textsf{\normalsize Enter\ a\ ticker\ }$",
        label_visibility="visible",
        disabled=st.session_state.running,
        placeholder="e.g. AAPL, BTC=F, EURUSD=X"
    ).upper()

def explore_section(data):
    st.write("#####")
    plot_data(data)

    st.markdown("🤖 Using GPT-4 and LangChain/OpenAI, this AI can answer questions about price, volume, trends, and other financial metrics.")

    openai_api_key = st.text_input(
        r"$\textsf{\normalsize Enter\ your\ OpenAI\ API:}$",
        type="password",
        placeholder="sk-...",
        disabled=st.session_state.running
    )

    st.markdown("[Get an OpenAI API key](https://platform.openai.com/signup)", unsafe_allow_html=True)

    user_prompt = st.text_area(
        r"$\textsf{\normalsize Enter\ your\ prompt:}$", 
        placeholder="e.g. What is the average closing price?",
        disabled=st.session_state.running
    )
    generate_pressed = st.button(
        "Generate",
        disabled=st.session_state.running,
        on_click=is_running
    )

    if generate_pressed:
        if openai_api_key:
            if user_prompt.strip():
                with st.spinner("Generating response...🤖"):
                    llm = ChatOpenAI(api_key=openai_api_key, temperature=0.9, model_name='gpt-3.5-turbo')
                    agent = create_pandas_dataframe_agent(llm, data, verbose=True, allow_dangerous_code=True)
                    response = agent.invoke(user_prompt)
                st.session_state.output_generate = response["output"]
                st.session_state.output_warning = None
            else:
                time.sleep(0.01)
                st.session_state.output_warning = "⚠️ Please enter a prompt."
        else:
            time.sleep(0.01)
            st.session_state.output_warning = "⚠️ Please enter your OpenAI API key."

        st.session_state.running = False
        st.rerun()

    if st.session_state.output_generate:
        st.write(st.session_state.output_generate)
    if st.session_state.output_warning:
        st.warning(st.session_state.output_warning)

def forecast_section(data):
    st.write("#####")
    n_years = st.slider(
        r"$\textsf{\small Years\ of\ prediction:}$", 
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

def interaction(data):
    # Radio button for selecting between 'Explore' and 'Forecast'
    section = st.radio(
        r"$\textsf{\normalsize Choose\ an \ action:}$",
        ("🔍 Explore", "🔮 Forecast"),
        disabled=st.session_state.running,
    )

    if section == "🔍 Explore":
        explore_section(data)
    elif section == "🔮 Forecast":
        forecast_section(data)
