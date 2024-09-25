import streamlit as st
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go

def plot_data(data):
    """
    Plot selected financial data columns, allowing the user to choose which columns to display.
    Adds a trend line if only one column is selected.

    Args:
        data (pd.DataFrame): The DataFrame containing historical financial data.
    """

    # Check if all values in the 'Volume' column are 0
    if data['Volume'].sum() == 0:
        default_selection = ['Open', 'High', 'Low', 'Close', 'Adj Close']
    else:
        default_selection = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']

    # Allow users to select which columns to plot, default to 'Close'
    selected_columns = st.multiselect(
        r"$\textsf{\normalsize Select\ columns\ to\ plot:}$",
        options=default_selection, 
        default=['Close']  # Default selection to 'Close'
    )

    # Add a tip for users on how to interact with the chart
    st.markdown(
        """
        <div class="tip-box">
            ℹ️ <i>Tip: Hover over the chart and click the box icon to view it in full screen.</i>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Add space for layout purposes
    st.markdown("<br>", unsafe_allow_html=True)

    # If columns are selected for plotting
    if selected_columns:
        fig = go.Figure()

        # Plot each selected column as a line chart
        for column in selected_columns:
            fig.add_trace(go.Scatter(x=data['Date'], y=data[column], mode='lines', name=column))

        # If only one column is selected, add a trend line
        if len(selected_columns) == 1:
            # Linear Regression for Trend Analysis
            X = np.arange(len(data)).reshape(-1, 1)  # Time as an independent variable
            y = data[selected_columns[0]].values  # Selected column as the dependent variable

            # Create and fit the linear regression model
            model = LinearRegression()
            model.fit(X, y)

            # Predict the trend line
            trend = model.predict(X)

            # Add the trend line to the figure in red
            fig.add_trace(go.Scatter(x=data['Date'], y=trend, mode='lines', name='Trend Line', line=dict(color='red', width=2)))

        # Customize layout of the plot
        fig.update_layout(
            title='Historical Data Over 5 Years',  # Chart title
            xaxis_title='Date',  # X-axis label
            yaxis_title='Value',  # Y-axis label
            xaxis=dict(showgrid=False),  # Hide gridlines on the X-axis
            yaxis=dict(showgrid=False)   # Hide gridlines on the Y-axis
        )

        # Display the plot using Plotly in Streamlit
        st.plotly_chart(fig, use_container_width=True)
    else:
        # Show a warning if no columns are selected
        st.warning("Please select at least one column to plot.")
