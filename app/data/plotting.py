import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


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
            ℹ️ <i>Tip: Hover over the chart and click the expand icon to view it in full screen..</i>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Add space
    st.markdown("<br>", unsafe_allow_html=True) 

    if selected_columns:
        if len(selected_columns) == 1:
            # Linear Regression for Trend Analysis
            X = np.arange(len(data)).reshape(-1, 1)  # Time as an independent variable
            y = data[selected_columns[0]].values  # Selected column as the dependent variable

            # Create and fit the model
            model = LinearRegression()
            model.fit(X, y)

            # Predict the trend
            trend = model.predict(X)

            # Convert the trend to a DataFrame
            trend_df = pd.DataFrame({'Date': data['Date'], 'Trend': trend})

            # Plot the actual data and the trend line together
            chart = alt.Chart(data, title=f"{selected_columns[0]} with Trend Line in Red").mark_line(strokeWidth=3).encode(
                x=alt.X('Date:T', axis=alt.Axis(title='Date')),
                y=alt.Y(f'{selected_columns[0]}:Q', axis=alt.Axis(title=selected_columns[0])),
                tooltip=[alt.Tooltip('Date:T', title='Date'), alt.Tooltip(f'{selected_columns[0]}:Q', title=selected_columns[0], format='.2f')]
            )

            trend_line = alt.Chart(trend_df).mark_line(color='red', strokeWidth=2).encode(
                x=alt.X('Date:T'),
                y=alt.Y('Trend:Q')
            )

            st.altair_chart(chart + trend_line, use_container_width=True)

        else:
            # Prepare the Altair chart with selected columns (no trend)
            chart = alt.Chart(data, title="Historical Data").transform_fold(
                selected_columns,
                as_=['Metric', 'Value']
            ).mark_line(strokeWidth=3).encode(
                x=alt.X('Date:T', axis=alt.Axis(title='Date')),
                y=alt.Y('Value:Q', axis=alt.Axis(title='Value')),
                color='Metric:N',  # Color the lines by metric (Open, Close, etc.)
                tooltip=[alt.Tooltip('Date:T', title='Date'), alt.Tooltip('Value:Q', title='Value', format='.2f')]
            )

            st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("Please select at least one column to plot.")