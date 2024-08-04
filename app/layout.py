import streamlit as st

def initialize_app():
    st.set_page_config(
        page_title="Finance Predictor App",
        page_icon="💶",
        initial_sidebar_state="expanded"
    )

def display_header():
    st.title("💶 Finance Predictor App")
    st.write("""
        Predict assets like stocks, currencies, world indices, cryptocurrencies, and futures 
        using the Facebook Prophet model. A full list of these assets can be found [here](https://finance.yahoo.com/trending-tickers).
    """)
    st.divider()

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def initialize_session_state():
    if 'running' not in st.session_state:
        st.session_state.running = False
    if 'predict_button' not in st.session_state:
        st.session_state.predict_button = False
