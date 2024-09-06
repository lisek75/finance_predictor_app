import streamlit as st
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go


def plot_data(data):
    # Allow users to select which columns to plot
    default_selection = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    selected_columns = st.multiselect(
        r"$\textsf{\normalsize Select\ columns\ to\ plot:}$",
        options=default_selection, 
        default=['Close']
    )

    # Add instruction for interacting with the chart
    st.markdown(
        """
        <div class="tip-box">
            ℹ️ <i>Tip: Hover over the chart and click the box icon to view it in full screen.</i>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Add space
    st.markdown("<br>", unsafe_allow_html=True)

    if selected_columns:
        fig = go.Figure()

        for column in selected_columns:
            fig.add_trace(go.Scatter(x=data['Date'], y=data[column], mode='lines', name=column))

        # If only one column is selected, add a trend line
        if len(selected_columns) == 1:
            # Linear Regression for Trend Analysis
            X = np.arange(len(data)).reshape(-1, 1)  # Time as an independent variable
            y = data[selected_columns[0]].values  # Selected column as the dependent variable

            # Create and fit the model
            model = LinearRegression()
            model.fit(X, y)

            # Predict the trend
            trend = model.predict(X)

            # Add the trend line to the figure
            fig.add_trace(go.Scatter(x=data['Date'], y=trend, mode='lines', name='Trend Line', line=dict(color='red', width=2)))

        # Customize layout to match your theme
        fig.update_layout(
            title='Historical Financial Data',
            xaxis_title='Date',
            yaxis_title='Value',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False)
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please select at least one column to plot.")