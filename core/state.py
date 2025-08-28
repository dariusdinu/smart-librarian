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
    keys_to_reset = [
        "user_input", "title", "gpt_response", "summary", "show_output", "image_url"
    ]
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]
