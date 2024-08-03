import streamlit as st
from datetime import date
import re
from utils.data_utils import load_data, get_ticker_info
from utils.validation_utils import validate_ticker, mean_absolute_percentage_error
import models.prophet_model as prophet_model
import altair as alt
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

# Define the start and end dates for data collection
START = "2010-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

# Configure the Streamlit app header
st.set_page_config(
    page_title="Finance Predictor App",
    page_icon="💶",
    initial_sidebar_state="expanded"
)

st.title("💶 Finance Predictor App")
st.write(
    """
    Predict assets like stocks, currencies, world indices, cryptocurrencies, and futures 
    using the Facebook Prophet model. A full list of these assets can be found [here](https://finance.yahoo.com/trending-tickers).
    """
)
st.divider()

# Load CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("static/styles.css")

if 'predict_button' in st.session_state and st.session_state.predict_button == True:
    st.session_state.running = True
else:
    st.session_state.running = False

# Cache the data loading function
@st.cache_data(show_spinner=False)
def load_data_cached(ticker, start, end):
    return load_data(ticker, start, end)

# User input for the ticker symbol
user_ticker_input = st.text_input(
    r"$\textsf{\normalsize Enter\ a\ ticker\ }$",
    label_visibility="visible",
    disabled=st.session_state.running,
    placeholder="e.g. AAPL, BTC=F, EURUSD=X",
).upper()

# Main process after the user inputs a valid ticker
if user_ticker_input:
    tickers = re.split(r'\s+', user_ticker_input.strip())

    if len(tickers) != 1:
        st.error("❌ Please provide one ticker. You can find a full list of tickers [here](https://finance.yahoo.com/trending-tickers). 🧐")
    else:
        ticker = tickers[0]
        if validate_ticker(ticker):
            selected_stock = ticker
            ticker_info = get_ticker_info(selected_stock)
            st.write(f"{ticker_info} ({selected_stock})")

            # Display a loading spinner while data is being loaded
            with st.spinner('📈 Loading data... Hold tight! 🚀'):
                data = load_data_cached(selected_stock, START, TODAY)  # Use cached data

            with st.expander("🔍 Explore"):
                st.write("#####")

                # Create an Altair chart
                chart = alt.Chart(data, title="Historical Close Price").mark_line(strokeWidth=3).encode(
                    x=alt.X('Date:T', axis=alt.Axis(title='date', tickCount="year")),
                    y=alt.Y('Close:Q', axis=alt.Axis(title='close price')),
                    tooltip=[alt.Tooltip('Date:T', title='Date'), alt.Tooltip('Close:Q', title='Close', format='.2f')],
                ).interactive()
                st.altair_chart(chart, use_container_width=True)

                st.markdown("🤖 This bot can answer questions about the average, high, and low price, volume, trends, and other financial metrics for the selected ticker. 📈")

                # User input for the OpenAI API key
                openai_api_key = st.text_input(
                    r"$\textsf{\normalsize Enter\ your\ OpenAI\ API:}$",
                    type="password",
                    placeholder="sk-...",
                    disabled=st.session_state.running
                )

                st.markdown("[Get an OpenAI API key](https://platform.openai.com/signup)", unsafe_allow_html=True)

                # Prompt the user to enter their question
                user_prompt = st.text_area(
                    r"$\textsf{\normalsize Enter\ your\ prompt:}$", 
                    placeholder="e.g. What is the average closing price?",
                    disabled=st.session_state.running
                )

                if st.button("Generate", disabled=st.session_state.running):
                    if openai_api_key:
                        if user_prompt:
                            with st.spinner("Generating response...🤖"):
                                # Initialize the ChatOpenAI instance and data agent
                                llm = ChatOpenAI(api_key=openai_api_key, temperature=0.5)
                                agent = create_pandas_dataframe_agent(llm, data, verbose=True, allow_dangerous_code=True)

                                # Run the agent with the user prompt
                                response = agent.run(user_prompt)
                                st.write(response)
                        else:
                            st.warning("⚠️ Please enter a prompt.")
                    else:
                        st.warning("⚠️ Please enter your OpenAI API key.")


            with st.expander("🔮 Forecast", expanded=False):
                st.write("#####")

                # Slider for selecting the number of years for prediction
                n_years = st.slider(
                    r"$\textsf{\normalsize Years\ of\ prediction:}$", 
                    1, 4, disabled=st.session_state.running
                )
                period = n_years * 365

                # Trigger fitting process
                if st.button('Predict', disabled=st.session_state.running, key='predict_button'):
                    with st.spinner('🔮 Fitting the crystal ball... 🧙‍♂️'):
                        m, forecast = prophet_model.fit_prophet_model(data, period)

                    with st.spinner('🤹‍♂️ Juggling some numbers... 🤔'):
                        df_cv = prophet_model.cross_validate_model(m)
                    global_mape = mean_absolute_percentage_error(df_cv['y'], df_cv['yhat'])
                    m_accuracy = 100 - global_mape

                    forecast_fig = prophet_model.plot_forecast(m, forecast)
                    
                    # Store the output in session state
                    st.session_state.output = (forecast_fig, m_accuracy)
                    st.rerun()

                # Display the output if it exists in session state
                if 'output' in st.session_state:
                    forecast_fig, m_accuracy = st.session_state.output
                    st.altair_chart(forecast_fig, use_container_width=True)
                    st.markdown(f"<p class='model-accuracy'>Model Accuracy: {m_accuracy:.2f}%</p>", unsafe_allow_html=True)

        else:
            st.error("❌ Please provide a valid ticker. You can find a full list of tickers [here](https://finance.yahoo.com/trending-tickers). 🧐")
