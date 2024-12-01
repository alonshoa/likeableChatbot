import datetime
from openai import OpenAI
import streamlit as st
import anthropic
from utils import cases, image




def change_model():
    if not st.session_state.get("chatbot_api_key"):
        st.sidebar.info("Please provide an API key.")
    selected_value = st.session_state.model_selector
    if selected_value == "OpenAI":
        st.session_state.client = OpenAI(api_key=st.session_state.chatbot_api_key)
    elif selected_value == "Claude.ai":
        st.session_state.client = anthropic.Anthropic(api_key=st.session_state.chatbot_api_key)
    else:
        st.session_state.client = None

def case_changed():
    case = st.session_state.case_selector
    st.session_state["system_messages"] = [prompt for prompt in cases[case]]
    st.session_state["messages"].append({"role": "assistant", "content": "Hi!"})

def get_response(client, messages,sys_messages):
    try:
        if isinstance(client, OpenAI):
            response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
            return response.choices[0].message.content
        elif isinstance(client, anthropic.Anthropic):
            # response = client.messages.create(model="claude-3-5-sonnet-20241022", messages=messages,system=cases[st.session_state.case_selector],max_tokens=1024)
            response = client.messages.create(model="claude-3-haiku-20240307", messages=messages,system="".join(cases[st.session_state.case_selector]),max_tokens=128)
            print(response)
            print(messages)
            print(sys_messages)
            # return "Yey"
            return response.content[0].text
    except Exception as e:
        st.error(f"Error getting response: {e}")
        return "Error"

# Sidebar UI
with st.sidebar:
    st.text_input("User Id", key="user_id", type="default")
    st.text_input("API Key", key="chatbot_api_key", type="password")
    st.selectbox("Select model vendor", options=["OpenAI", "Claude.ai"], on_change=change_model, key="model_selector")
    st.selectbox("Select case", options=list(cases.keys()), on_change=case_changed, key="case_selector")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["system_messages"] = cases["case 1"] #[{"role": "system", "content": cases["case 1"]}]
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi!"}]

# Main chat interface
col1, col2 = st.columns([3, 1])
with col1:
    st.title("The 💗 Chatbot")
with col2:
    st.image("images/thumbsup.jpg", width=100)
st.caption(r"🚀 A Streamlit 💗 chatbot ")

# Display chat messages
for msg in st.session_state.messages:
    if msg["role"] in image:
        st.chat_message(msg["role"], avatar=image[msg["role"]]).write(msg["content"])

# Handle user input
if prompt := st.chat_input():
    if not st.session_state.get("user_id"):
        st.info("Please add your user identifier.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=image["user"]):
        st.write(prompt)

    msg = get_response(st.session_state.client, st.session_state.messages,st.session_state.system_messages)
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant", avatar=image["assistant"]).write(msg)

def collect_data_for_download():
    msg_list = [f"system: {c}" for c in cases[st.session_state.case_selector]]
    msg_list.extend([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
    return "\n".join(msg_list)

# Download chat history
def get_file_name():
    return f"chat_{st.session_state['user_id']}_{st.session_state.case_selector}_{datetime.datetime.now()}.txt"

if st.session_state.messages:
    with st.sidebar:
        st.download_button(
            label="Download chat as text",
            data=collect_data_for_download(),
            file_name=get_file_name(),
            mime="text/txt"
        )
