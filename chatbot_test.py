import openai 
import os
from dotenv import load_dotenv, find_dotenv
_= load_dotenv(find_dotenv())

import streamlit as st
from streamlit_chat import message

openai.api_key = os.getenv('OPENAI_API_KEY')

model = "gpt-4-0125-preview"

instructions = """
# teacher's guide
- I'm an English teacher for 3rd grade elementary students in Korea.
- As an English teacher, I need to converse in English with students whose native language is not English. 
- It's important for me to consider the students' intellectual abilities and background knowledge while leading the conversation. 
- I should discourage students from speaking inappropriate content, and I shouldn't engage in inappropriate content myself. 
- When a student uses incorrect grammar, I should point out the mistake and provide a correct example sentence within the conversation context. 
- We'll be discussing "{text}" during our conversation, and we should stick to that topic.

# teacher's conversation examples
Teacher: Today, we are going to talk about clothes. What are you wearing now? 
Student: I am wearing a hoodie and shorts.
"""

st.header("GPT Test (Demo)")
st.markdown("[Educloud DigitalHuman T Park Hannah] ")
client = openai.api_key

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = model

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Let's start conversation!"):
    st.session_state.messages.append({"role" : "user", "content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        messages = [
            {"role" : m["role"], "content":m["content"]}
            for m in st.session_state.messages
        ]
        messages.insert(0, {"role":"system", "content":instructions})

        stream = client.chat.completions.create(
            model = st.session_state["openai_model"],
            messages = messages,
            stream = True,
        )
        for response in stream:
            full_response += response.choices[0].delta.content or ""
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role":"assistant", "content":full_response})
    