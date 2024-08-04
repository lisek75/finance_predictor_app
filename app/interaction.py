import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from models import *
from data import plot_data

def get_user_ticker():
    return st.text_input(
        r"$\textsf{\normalsize Enter\ a\ ticker\ }$",
        label_visibility="visible",
        disabled=st.session_state.running,
        placeholder="e.g. AAPL, BTC=F, EURUSD=X"
    ).upper()

def explore(data):
    st.write("#####")
    plot_data(data)

    st.markdown("🤖 Using GPT-4 and LangChain/OpenAI, this AI can answer questions about price, volume, trends, and other financial metrics.")

    openai_api_key = st.text_input(
        r"$\textsf{\small Enter\ your\ OpenAI\ API:}$",
        type="password",
        placeholder="sk-...",
        disabled=st.session_state.running
    )

    st.markdown("[Get an OpenAI API key](https://platform.openai.com/signup)", unsafe_allow_html=True)

    user_prompt = st.text_area(
        r"$\textsf{\small Enter\ your\ prompt:}$", 
        placeholder="e.g. What is the average closing price?",
        disabled=st.session_state.running
    )

    if st.button("Generate", disabled=st.session_state.running):
        if openai_api_key:
            if user_prompt:
                with st.spinner("Generating response...🤖"):
                    llm = ChatOpenAI(api_key=openai_api_key, temperature=0.5, model_name='gpt-3.5-turbo')
                    agent = create_pandas_dataframe_agent(llm, data, verbose=True, allow_dangerous_code=True)
                    response = agent.invoke(user_prompt)
                    st.write(response["output"])
            else:
                st.warning("⚠️ Please enter a prompt.")
        else:
            st.warning("⚠️ Please enter your OpenAI API key.")

def forecast(data):
    st.write("#####")
    n_years = st.slider(
        r"$\textsf{\small Years\ of\ prediction:}$", 
        1, 4, disabled=st.session_state.running
    )
    period = n_years * 365

    if st.button('Predict', disabled=st.session_state.running, key='predict_button'):
        with st.spinner('🔮 Fitting the crystal ball... 🧙‍♂️'):
            m, forecast = fit_prophet_model(data, period)

        with st.spinner('🤹‍♂️ Juggling some numbers... 🤔'):
            df_cv = cross_validate_model(m)
        global_mape = mean_absolute_percentage_error(df_cv['y'], df_cv['yhat'])
        m_accuracy = 100 - global_mape

        forecast_fig = plot_forecast(m, forecast)

        st.session_state.output = (forecast_fig, m_accuracy)
        st.rerun()

    if 'output' in st.session_state:
        forecast_fig, m_accuracy = st.session_state.output
        st.markdown(f"<p class='model-accuracy'>Model Accuracy: {m_accuracy:.2f}%</p>", unsafe_allow_html=True)
        st.altair_chart(forecast_fig, use_container_width=True)
