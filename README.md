# 💶Finance Predictor App

## 📋 Overview
The Finance Predictor App is designed to predict asset prices (stocks, cryptocurrencies, etc.) using machine learning models specifically tailored for time series analysis, such as Prophet and ARIMA. Users can input a ticker symbol to explore historical financial data, ask AI for insights, or forecast future prices. The app integrates these models to provide financial insights through interactive charts and forecast accuracy metrics.

**Deployed App:** [Finance Predictor App](https://fi-predictor.streamlit.app/)

## Project Structure

- `main.py`: Entry point for the Streamlit app.
- `app`: Root directory.
    - `components/`: Contains scripts for UI elements, data exploration, forecasting, and Gen AI features.
    - `data/`: Utility functions for data handling and validation.
    - `models/`: Model scripts for forecasting and analytics.
    - `static/`: Static files like CSS.
- `requirements.txt`: Project dependencies.
- `README.md`: Project description and instructions.

## 🛠️ Setup

### 📚 Prerequisites

- Python 3.8+, proficient in Python programming.
- Experience with Streamlit for web apps.
- Knowledge of machine learning models for time series analysis, libraries, and evaluation metrics.
- OpenAI API key and familiarity with LangChain for integrating generative AI and building AI agents.

### 📥 Installation 

1. **Clone the repository**:
    ```sh
    git clone https://github.com/lisek75/finance_predictor_app.git
    cd finance_predictor_app
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv .venv
    .venv\Scripts\activate  # On Windows
    source .venv/bin/activate  # On MacOS/Linux
    ```

3. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

## 🚀 Run 

1. **Start the Streamlit application**:
    ```sh
    streamlit run main.py
    ```

## 💻 Usage

1. Open your browser and navigate to the local Streamlit URL.
2. Type the ticker symbol of the asset you want to predict.
3. Explore Data: Review historical data and key financial metrics.
4. Forecast Data: 
    - Select the prediction period and forecasting model (ARIMA or Prophet). 
    - The app will display forecasted prices, metrics, and model accuracy.
5. Ask AI: 
    - Enter your OpenAI API key and type a question about the financial data. 
    - Press "Generate" to receive AI-driven insights based on the data.
