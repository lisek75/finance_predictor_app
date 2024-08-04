import streamlit as st
import altair as alt

# Plot historical data using Altair
def plot_data(data):
    chart = alt.Chart(data, title="Historical Close Price").mark_line(strokeWidth=3).encode(
        x=alt.X('Date:T', axis=alt.Axis(title='date', tickCount="year")),
        y=alt.Y('Close:Q', axis=alt.Axis(title='close price')),
        tooltip=[alt.Tooltip('Date:T', title='Date'), alt.Tooltip('Close:Q', title='Close', format='.2f')],
    ).interactive()
    st.altair_chart(chart, use_container_width=True)