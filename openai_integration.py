import os
from dotenv import load_dotenv
from openai import OpenAI

def setup_openai():
    load_dotenv()  # This loads the environment variables from the .env file into os.environ
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set in .env file")
    return OpenAI(api_key=api_key)

def generate_response(query, client):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": query
            }
        ],
        model="gpt-3.5-turbo"
    )
    return chat_completion.choices[0].message.content
