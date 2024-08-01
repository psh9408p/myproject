import os
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st

api_key1 = st.secrets["openai"]["api_key"]
api_key = api_key1
load_dotenv()
# api_key = os.getenv('API_KEY')
client = OpenAI(api_key=api_key)

file_path = "file/web2x.pdf"

def fileUpload(file_path):
    file = client.files.create(
        file=open(file_path, "rb"),
        purpose="assistants"
    )
    return file.id  # 파일 ID 반환


# 파일 업로드 및 ID 획득
# uploaded_file_id = fileUpload(file_path)
# 벡터 스토어 생성 및 ID 획득

# vector_store = client.beta.vector_stores.create(
#   name="LH GUIDE Support FAQ"
# )

# vector_store_file = client.beta.vector_stores.files.create(
#   vector_store_id=vector_store.id,
#   file_id=uploaded_file_id
# )

def assistant_creator():
    my_assistant = client.beta.assistants.create(
        instructions="이 챗봇은 WEB2X 문서기반으로 질의응답하는 bot.",
        name="web2x Helper",
        tools=[{"type": "file_search"}],
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
        model="gpt-4o"
      # gpt-4o	
        
    )
    return my_assistant.id

# print(assistant_creator())


# my_assistant_id = assistant_creator()

# empty_thread = client.beta.threads.create()

