from app.components import *
from app.data import *
from app.models import *
import streamlit as st

def main():
    """
    The main function to run the Streamlit app. It initializes the app, handles user input, 
    validates the ticker symbol, loads the corresponding data, and presents the user 
    with various actions (Explore, Ask AI, Forecast).
    """

    # Initialize the Streamlit app with settings (title, page icon, sidebar)
    initialize_app()

    # Display the header and description of the app
    display_header()

    # Load custom CSS for styling the app
    load_css("app/static/styles.css")

    # Initialize session state variables to manage app state
    initialize_session_state()

    # Get user input for the ticker symbol
    user_ticker_input = get_user_ticker()

    # Validate the user-provided ticker symbol
    valid_ticker = validate_input(user_ticker_input)

    # If the ticker is valid, proceed with data loading and action selection
    if valid_ticker is not None:
        # Display the long name (company name) for the valid ticker
        st.sidebar.write(get_ticker_name(valid_ticker))

        # Load the historical financial data for the ticker
        data = load_data(valid_ticker)

        # Allow the user to choose between exploring data, asking AI, or forecasting
        action_selector(data, valid_ticker)


# Execute the main function when the script is run
if __name__ == "__main__":
    main()

