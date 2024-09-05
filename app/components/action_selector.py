import streamlit as st
from app.components.explore import explore_section
from app.components.forecast import forecast_section
from app.components.ask_ai import ask_ai_section

def action_selector(data, ticker):
    st.markdown("##### Please choose an action to proceed:")

    selected_action = None

    # Create three columns for horizontal button layout
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔍 Explore", disabled=st.session_state.running):
            selected_action = "🔍 Explore"

    with col2:
        if st.button("🤖 Ask AI", disabled=st.session_state.running):
            selected_action = "🤖 Ask AI"

    with col3:
        if st.button("🔮 Forecast", disabled=st.session_state.running):
            selected_action = "🔮 Forecast"

    if selected_action:
        st.session_state.selected_section = selected_action

    if "selected_section" in st.session_state:
        section = st.session_state.selected_section
        if section == "🔍 Explore":
            explore_section(data, ticker)
        elif section == "🤖 Ask AI":
            ask_ai_section(data)
        elif section == "🔮 Forecast":
            forecast_section(data)
