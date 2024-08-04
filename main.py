from app import *
from data import process_user_input, validate_and_load_data
import streamlit as st

def main():
    # Initialize the Streamlit app and settings
    initialize_app()
    display_header()
    load_css("static/styles.css")
    initialize_session_state()

    # Update session state based on user interactions
    if 'predict_button' in st.session_state and st.session_state.predict_button == True:
        st.session_state.running = True
    else:
        st.session_state.running = False

    # Get user input for the ticker symbol
    user_ticker_input = get_user_ticker()

    # Process the user input to validate and extract the ticker
    valid_ticker = process_user_input(user_ticker_input)

    if valid_ticker:
        # Validate the ticker and load the data
        ticker_info, data = validate_and_load_data(valid_ticker)
        if data is not None:
            st.write(ticker_info)
            if data is not None:
                with st.expander("🔍 Explore"):
                    explore(data)
                with st.expander("🔮 Forecast"):
                    forecast(data)

if __name__ == "__main__":
    main()
