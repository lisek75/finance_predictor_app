import streamlit as st

def initialize_app():
    st.set_page_config(
        page_title="Finance Predictor App",
        page_icon="💶",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def display_header():
    st.title("💶 Finance Predictor App")
    st.write("""
        Predict assets like stocks, currencies, world indices, cryptocurrencies, and futures 
        using the Facebook Prophet model. A full list of these assets can be found [here](https://finance.yahoo.com/trending-tickers).
    """)

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def initialize_session_state():
    if 'running' not in st.session_state:
        st.session_state.running = False
    if "output_predict" not in st.session_state:
        st.session_state.output_predict = None
    if 'output_warning' not in st.session_state:
        st.session_state.output_warning = None
    if 'output_generate' not in st.session_state:
        st.session_state.output_generate = None


