import streamlit as st

def learn_more_page():

    st.markdown(f"<h2>🧠 Learn More About This Project</h2>", unsafe_allow_html=True)

    st.write("""
    The **Finance Predictor App** is designed to predict asset prices (stocks, cryptocurrencies, etc.) using **machine learning models** specifically tailored for **time series analysis**, such as **Prophet** and **ARIMA**. 
    Users can input a **ticker symbol** to explore **historical financial data**, ask **AI for insights**, or **forecast future prices**. 
    The app integrates these models to provide financial insights through **interactive charts** and **forecast accuracy metrics**.
    """)

    st.markdown(f"<h3>📋 Basic Knowledge Requirements</h3>", unsafe_allow_html=True)
    st.write("""
    - Basic **Python** Programming.
    - Experience with **Streamlit** Web App Development.
    - Familiarity with **SARIMA/Prophet models** and **cross-validation**.
    - Basic knowledge of **Machine Learning Libraries**: Pandas, pmdarima, scikit-learn, and Plotly.
    """)

    st.markdown(f"<h3>🔑 Key Learnings</h3>", unsafe_allow_html=True)
    st.write("""
    - Build advanced and interactive web apps with **Streamlit** (initialization, session states, dynamic updates …)
    - Fetch and validate financial data using **yfinance**.
    - Implement **SARIMA** and **Prophet** models for time series forecasting, with **automatic parameter selection** for SARIMA.
    - Apply **Rolling cross-validation (ARIMA)** and **time-based cross-validation (Prophet)** for model evaluation.
    - Visualize data with **Plotly** for interactive insights.
    - Calculate **evaluation metrics (MAE, MAPE, RMSE)** with scikit-learn.
    - Integrate **generative AI** with **OpenAI API** and **LangChain**.
    """)

    st.markdown(f"<h3>📖 Story Behind the Code</h3>", unsafe_allow_html=True)
    st.write("""
    - **Data Input and Validation**: Prompts users to enter a valid ticker symbol and validates the input by fetching data using the **yfinance** API.
    - **Explore Data**: Displays historical financial data and metrics for the selected ticker symbol.
    - **Ask AI** (Gen AI): Integrates with **OpenAI** and **LangChain** to provide AI-driven financial insights based on user prompts.
    - **Forecasting**: Allows users to select a prediction model and prediction period, generating future price forecasts along with accuracy metrics.
    - **Session State Management**: Tracks the selected section and ensures actions update dynamically, resetting data when necessary.
    """)

    st.markdown(f"<h3>⚙️Technical Architecture</h3>", unsafe_allow_html=True)
    st.image("app/static/tech_archi.png", caption="Architecture Diagram")

    st.markdown(f"<h3>🔗 GitHub Repository</h3>", unsafe_allow_html=True)
    st.write("""
        To explore the complete code and more detailed documentation, visit the [Fi-Predictor GitHub Repository](https://github.com/lisek75/finance_predictor_app).
    """)
    
