# 💰Finance Predictor App

## 📋 Overview
Predict assets like currencies, cryptocurrencies, and stock prices using ML models (Facebook Prophet).

**Deployed App:** [Finance Predictor App](https://fi-predictor.streamlit.app/)

## Project Structure

- `main.py`: Entry point for the Streamlit app.
- `models/`: Contains the models used for this project.
- `utils/`: Utility functions for data handling and validation.
- `requirements.txt`: Python dependencies.
- `README.md`: Project documentation.

## 🛠️ Setup

### 📚 Prerequisites

- Python 3.8 or higher
- Proficiency in Python programming
- Advanced understanding of machine learning models
- Familiarity with time series analysis

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

1. Open your browser and navigate to the local Streamlit URL (usually `http://localhost:8501`).
2. Type the ticker symbol of the asset you want to predict.
3. Use the slider to choose the number of years for the prediction.
4. The app will display the historical data, forecasted prices, and model accuracy.
