import streamlit as st
from ..models import *

def is_running():
    st.session_state.running = True

def get_user_ticker():
    return st.text_input(
        r"$\textsf{\normalsize Enter\ a\ ticker\ }$",
        label_visibility="visible",
        disabled=st.session_state.running,
        placeholder="e.g. AAPL, BTC=F, EURUSD=X"
    ).upper()