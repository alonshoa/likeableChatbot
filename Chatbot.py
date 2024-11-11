from openai import OpenAI
import streamlit as st

with st.sidebar:
    user_id = st.text_input("User Id", key="user_id", type="default")
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

st.title("The 💗 Chatbot")
st.caption("🚀 A Streamlit 💗 chatbot <small> powered by OpenAI </small>")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not user_id:
        st.info("Please add your user identifier")
        st.stop()

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

with st.sidebar:
    if not user_id:
        st.info("Please add your user identifier")
        st.stop()

    if st.session_state.messages:
        st.download_button(
            label="Download data as text",
            data="\n".join([f"{msg['role']} : {msg['content']}" for msg in st.session_state["messages"]]),
            file_name=f"chat_{user_id}.txt",
            mime="text/txt",
        )
