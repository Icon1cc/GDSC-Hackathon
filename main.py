import openai
from dotenv import load_dotenv
import os
import querypreprocessor  # Ensure this is correctly named and accessible

# Load environment variables from a .env file
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client with your API key
openai.api_key = API_KEY

def setup_openai_client():
    return openai.OpenAI(api_key=API_KEY)

def generate_response(query, client, messages, step):
    preprocessed_query = querypreprocessor.expand_query(query, step)
    try:
        # Attempting to generate a response with the GPT model
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Adjust model as needed
            messages=messages + [{"role": "user", "content": preprocessed_query}]
        )
        # Access the response text correctly
        response = chat_completion.choices[0].message.content  # Accessing the 'content' attribute directly
        messages.append({"role": "user", "content": preprocessed_query})
        messages.append({"role": "assistant", "content": response})
        return response
    except Exception as e:
        # Print the exception if there's an error
        print(f"An error occurred: {e}")
        return f"An error occurred: {e}"

def main_loop():
    client = setup_openai_client()
    messages = []
    print("Welcome to Latti Macchiati Simulator (type 'exit' to quit)")
    while True:
        print("Select the response format: 1 for Bullet Points, 2 for Q&A, 3 for Summary Sheet")
        format_choice = input("Format choice (1-3): ")
        if format_choice.lower() == 'exit':
            print("Exiting the Simulator.")
            break

        try:
            format_step = int(format_choice)
            if format_step not in [1, 2, 3]:
                print("Invalid format choice. Please enter 1, 2, or 3.")
                continue
        except ValueError:
            print("Please enter a valid number (1, 2, or 3).")
            continue

        input_query = input("You: ")
        if input_query.lower() == 'exit':
            print("Exiting the Simulator.")
            break

        response = generate_response(input_query, client, messages, format_step)
        print("GPT:", response)

if __name__ == "__main__":
    main_loop()