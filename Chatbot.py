import streamlit as st
from streamlit_server_state import server_state, server_state_lock, force_rerun_bound_sessions
from utils import image, cases  # Ensure `image` and `cases` are imported
import datetime

# Sidebar UI
with st.sidebar:
    st.text_input("User Id", key="user_id", type="default")
    st.text_input("API Key", key="chatbot_api_key", type="password")
    st.selectbox("Select model vendor", options=["OpenAI", "Claude.ai"], key="model_selector")
    st.selectbox("Select case", options=list(cases.keys()), key="case_selector")
    if not st.session_state.user_id:
        st.stop()
    else:
        if not st.session_state.user_id == "assistant":
            user_id = "user"
        else:
            user_id = "assistant"

# Initialize server state for messages
with server_state_lock["chat_messages"]:
    if "chat_messages" not in server_state:
        server_state["chat_messages"] = []



# Main chat UI
col1, col2 = st.columns([3, 1])
with col1:
    st.title("The 💗 Chatbot")
with col2:
    st.image("images/thumbsup.jpg", width=100)
st.caption(r"🚀 A Streamlit 💗 chatbot ")


# Initialize server state for chat messages
with server_state_lock["chat_messages"]:
    if "chat_messages" not in server_state:
        server_state["chat_messages"] = []

# Ensure session state for chat input
if "last_message" not in st.session_state:
    st.session_state.last_message = None  # Track the last submitted message

# Handle user input
user_input = st.chat_input("Type a message")
if user_input and user_input != st.session_state.last_message:
    # Update the last message to prevent duplicates
    st.session_state.last_message = user_input
    
    # Add new message to chat messages
    with server_state_lock["chat_messages"]:
        new_message = {"role": user_id, "text": user_input}
        server_state["chat_messages"].append(new_message)
    force_rerun_bound_sessions(key="chat_messages")
# Display chat messages
for msg in server_state["chat_messages"]:
    role = msg.get("role", "user")  # Default role to 'user' if not provided
    st.chat_message(role).write(msg["text"])


# Collect data for download
def collect_data_for_download():
    msg_list = [f"{msg['role']}: {msg['text']}" for msg in server_state["chat_messages"]]
    return "\n".join(msg_list)

# Download chat history
def get_file_name():
    return f"chat_{st.session_state.get('user_id', 'unknown')}_{st.session_state.get('case_selector', 'default')}_{datetime.datetime.now()}.txt"

if server_state["chat_messages"]:
    with st.sidebar:
        st.download_button(
            label="Download chat as text",
            data=collect_data_for_download(),
            file_name=get_file_name(),
            mime="text/txt"
        )
