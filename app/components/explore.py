from ..data import plot_data
import streamlit as st

def explore_section(data):
    st.write("#####")
    plot_data(data)