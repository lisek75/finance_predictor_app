import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from ..models import *
import time 

def is_running():
    st.session_state.running = True

def check_openai_api_key(api_key):
    client = openai.OpenAI(api_key=api_key)
    try:
        client.models.list()
    except openai.AuthenticationError:
        return False
    else:
        return True

def ask_ai_section(data, ticker):
    st.markdown(f"<h2 style='text-align: center;'>🤖 Ask AI about {ticker}</h2>", unsafe_allow_html=True)
    st.markdown("🤖 Using LangChain and OpenAI (gpt-4o mini), this AI can answer questions about price, volume, trends, and other financial metrics  for the selected ticker.")

    openai_api_key = st.text_input(
        r"$\textsf{\normalsize Enter\ your\ OpenAI\ API:}$",
        type="password",
        placeholder="sk-...",
        disabled=st.session_state.running
    )

    st.markdown("[Get an OpenAI API key](https://platform.openai.com/signup)", unsafe_allow_html=True)

    user_prompt = st.text_area(
        r"$\textsf{\normalsize Enter\ your\ prompt:}$", 
        placeholder="e.g. What is the average closing price?",
        disabled=st.session_state.running
    )
    generate_pressed = st.button(
        "Generate",
        disabled=st.session_state.running,
        on_click=is_running
    )

    if generate_pressed:
        if openai_api_key:
            if check_openai_api_key(openai_api_key):
                if user_prompt.strip():
                    with st.spinner("Generating response...🤖"):
                        llm = ChatOpenAI(api_key=openai_api_key, temperature=0.9, model_name='gpt-4o-mini')
                        agent = create_pandas_dataframe_agent(llm, data, verbose=True, allow_dangerous_code=True)
                        response = agent.invoke(user_prompt)
                    st.session_state.output_generate = response["output"]
                    st.session_state.output_warning = None
                else:
                    time.sleep(0.01)
                    st.session_state.output_warning = "⚠️ Please enter a prompt."
            else:
                time.sleep(0.01)
                st.session_state.output_warning = "⚠️ Please enter a valid OpenAI API key."
        else:
            time.sleep(0.01)
            st.session_state.output_warning = "⚠️ Please enter your OpenAI API key."

        st.session_state.running = False
        st.rerun()

    if st.session_state.output_generate:
        st.write(st.session_state.output_generate)
    if st.session_state.output_warning:
        st.warning(st.session_state.output_warning)