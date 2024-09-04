from app.components import *
from app.data import *
from app.models import *
import streamlit as st

def main():
    # Initialize the Streamlit app and settings
    initialize_app()
    display_header()
    load_css("app/static/styles.css")
    initialize_session_state()

    # Get user input for the ticker symbol
    user_ticker_input = get_user_ticker()

    # Process the user input to validate and extract the ticker
    valid_ticker = process_user_input(user_ticker_input)

    if valid_ticker:
        # Validate the ticker and load the data
        ticker_info, data = validate_and_load_data(valid_ticker)

        if data is not None:
            st.write(ticker_info)
            st.divider()

            # Select action: Explore, Ask AI, or Forecast
            action_selector(data)


if __name__ == "__main__":
    main()
