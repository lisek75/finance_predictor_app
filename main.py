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

    # Process the user input to validate the ticker
    valid_ticker = validate_input(user_ticker_input)

    if valid_ticker is not None:
        st.write(get_ticker_name(valid_ticker))
        data = load_data(valid_ticker)
        st.divider()

        # Select action: Explore, Ask AI, or Forecast
        action_selector(data)


if __name__ == "__main__":
    main()
