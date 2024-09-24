import streamlit as st
from app.components.learn_more import *


def initialize_app():
    """
    Set up the initial configuration of the Streamlit app, including the title, icon, and sidebar state.
    """
    st.set_page_config(
        page_title="Finance Predictor App",  # Set the page title
        page_icon="💶",  # Set the icon for the page
        initial_sidebar_state="expanded"  # Expand the sidebar on app load
    )

def display_header():
    """
    Display the main header and description of the app with a brief introduction to its functionality.
    """
      # Display the app title
    st.title("💶 Finance Predictor App")

    # Description of the app's purpose
    st.write("""
        Predict asset prices (stocks, currencies, cryptocurrencies, etc.) using time series machine learning models.
    """)

    with st.sidebar.expander("🛠️ How to Use This App"):
        st.write("""
            1. 🔍 Enter a ticker symbol. Find a list of tickers [here](https://finance.yahoo.com/trending-tickers).

            2. 💰 Explore detailed financial information and historical data visualizations.
            5. 🤖 Enter your OpenAI API key, ask a financial question, and click 'Generate' for AI insights.
            4. 📊 Choose a prediction period and a forecasting model to view forecasted prices, metrics, and model accuracy.
    """)

    # Add space between expander and the input
    st.sidebar.markdown("<br>", unsafe_allow_html=True) 

    if st.session_state.page == "Homepage":
        if st.button("Learn More", disabled=st.session_state.running):
            st.session_state.page = "Learn More"
            st.session_state.output_predict = None
            st.session_state.selected_section = None
            st.rerun()

    elif st.session_state.page == "Learn More":
        if st.button("Back to Homepage"):
            st.session_state.page = "Homepage"
            st.session_state.output_predict = None
            st.session_state.selected_section = None
            st.rerun()
    
    st.divider()

def display_learn_more():
    if st.session_state.page == "Learn More":
        learn_more_page()

def display_homepage_instructions():
    if st.session_state.page == "Homepage":
        st.info("👈 Enter a ticker in the sidebar, select an action and follow the steps to complete it.")

        

def load_css(file_name):
    """
    Load a custom CSS file to style the Streamlit app.

    Args:
        file_name (str): Path to the CSS file.
    """
    with open(file_name) as f:
        # Inject custom CSS styles into the app
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def initialize_session_state():
    """
    Initialize the session state variables used in the app to keep track of the app's running state and outputs.
    """

    # Initialize navigation state (page)
    if 'page' not in st.session_state:
        st.session_state.page = "Homepage"

    # Initialize previous_ticker to track ticker changes
    if 'previous_ticker' not in st.session_state:
        st.session_state.previous_ticker = ''

    # Initialize a flag to indicate if the app is currently processing or running
    if 'running' not in st.session_state:
        st.session_state.running = False

    # Initialize the output storage for prediction results
    if "output_predict" not in st.session_state:
        st.session_state.output_predict = None

    # Initialize a variable to hold warnings for user input (AI)
    if 'output_warning' not in st.session_state:
        st.session_state.output_warning = None

    # Initialize the variable for storing AI-generated responses
    if 'output_generate' not in st.session_state:
        st.session_state.output_generate = None

    # Initialize a variable to track the previously selected model 
    if 'previous_model' not in st.session_state:
        st.session_state.previous_model = None

    # Initialize the selected section
    if 'selected_section' not in st.session_state:
        st.session_state.selected_section = None