import openai
import os
from dotenv import load_dotenv, find_dotenv
_= load_dotenv(find_dotenv())
from langchain.text_splitter import TokenTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings

openai.api_key = os.getenv('OPENAI_API_KEY')

model = "gpt-4-0125-preview"

age = f"""9"""
text = f"""Let's talk about clothes."""
prompt = f"""I am an English teacher who conducts conversations in English with non-native English learners around the age of "{age}". So, I need to lead the conversation considering the student's intellectual abilities and background knowledge. If the student gives inappropriate responses or makes grammatical errors, I should point out what was incorrect and provide example sentences in the correct context. The topic for conversation with the student is "{text}". We should only discuss topics relevant to this theme during our conversation."""

def generate_response(prompt, model):
    completions = openai.chat.completions.create(
        model = model,
        prompt = prompt,
        max_tokens=1024,
        stop = None,
        temperature=0.8,
        top_p=1,
    )

    message = completions['choices'][0]['text'].replace("\n","")
    return message


embeddings_model = OpenAIEmbeddings()

def get_completion( prompt, model):
    messages = [
    #{"role":"system", "content":""},
    {"role":"user", "content":prompt}
    ]

    response = openai.chat.completions.create(
        model = model,
        max_tokens=1000,
        messages=messages,
        temperature=0.8 
   )
    
    return response

response = get_completion(prompt, model)

print(response)
