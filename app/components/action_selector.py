import streamlit as st
from app.components.explore import explore_section
from app.components.forecast import forecast_section
from app.components.ask_ai import ask_ai_section

def action_selector(data, ticker):
    """
    Display buttons for the user to choose an action (Explore, Ask AI, or Forecast) 
    and navigate to the corresponding section.

    Args:
        data (pd.DataFrame): DataFrame containing the data to be used in each section.
        ticker (str): The ticker symbol of the stock or asset being analyzed.
    """
    st.sidebar.divider()

    # Header to instruct the user to choose an action
    st.sidebar.write ("😊 What would you like to do next?")

    selected_action = None # Initialize the selected action variable

    # Create three columns for the action buttons
    col1, col2, col3 = st.sidebar.columns(3)

    # First column: Button to explore data
    with col1:
        if st.button("🔍 Explore", disabled=st.session_state.running):
            selected_action = "🔍 Explore"

    # Second column: Button to ask AI for insights
    with col2:
        if st.button("🤖\n\nAsk AI", disabled=st.session_state.running):
            selected_action = "🤖 Ask AI"

    # Third column: Button to forecast data
    with col3:
        if st.button("🔮 Forecast", disabled=st.session_state.running):
            selected_action = "🔮 Forecast"

    # If an action is selected, store it in session state
    if selected_action:
        st.session_state.selected_section = selected_action

    # Check if a section was selected and navigate to the corresponding section
    if "selected_section" in st.session_state:
        section = st.session_state.selected_section
        if section == "🔍 Explore":
            explore_section(data, ticker)
        elif section == "🤖 Ask AI":
            ask_ai_section(data, ticker)
        elif section == "🔮 Forecast":
            forecast_section(data, ticker)
