from openai import OpenAI
import streamlit as st
import time
import os

from dotenv import load_dotenv
api_key = st.secrets["openai"]["API_KEY"]
assistant_id = st.secrets["openai"]["ASSISTANT_ID"]

load_dotenv()
# api_key = os.getenv('API_KEY')
# assistant_id = os.getenv('ASSISTANT_ID')

client = OpenAI(api_key=api_key)

# thread_id = "thread_UfwfQO5f0mIlVLMheDLYKR9u"
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password",value=api_key)
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    # "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"
    thread_id = st.text_input('Thread ID')
    thread_btn = st.button("Create a new Thread")
    if thread_btn:
        thread = client.beta.threads.create()
        thread_id = thread.id

        st.subheader(f"{thread_id}",divider="rainbow")
        st.info("스레드 생성 완")
st.title("💬 TEST: WEB2X Q&A ChatBot" )
st.caption("🚀 A Streamlit chatbot powered by OpenAI")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "무엇이든 물어보세용 : WEB2X"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
        
    if not thread_id:
        st.info("Please add your thread_id to continue.")
        st.stop()    

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = client.beta.threads.messages.create(
    thread_id,
    role="user",
    content=prompt, 
    )

    run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id
    )
    run_id = run.id

    while True:
        run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id
        )
        if run.status == "completed":
            break
        else:
            time.sleep(2)

    thread_messages = client.beta.threads.messages.list(thread_id)

    msg=thread_messages.data[0].content[0].text.value

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

    # response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    # msg = response.choices[0].message.content
  

    
        
