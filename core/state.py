import streamlit as st

def initialize_state():
    """Initialize all required Streamlit session state variables."""
    defaults = {
        "gpt_response": "",
        "summary": "",
        "title": "",
        "show_output": False,
        "user_input": ""
    }
    for key, default in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default

def reset_state():
    """Reset session state to initial state and rerun the app."""
    keys_to_reset = ["gpt_response", "summary", "title", "show_output", "user_input"]
    for key in keys_to_reset:
        st.session_state[key] = "" if key != "show_output" else False

    st.rerun()
