import openai
from dotenv import load_dotenv
import os
import querypreprocessor
import chroma_db_integration as db
import file_handlers
from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()


load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY


def setup_openai_client():
    return openai.OpenAI(api_key=API_KEY)


def generate_response(query, client, messages, step, mode, context=""):

    #if context:
        #query = f"Based on the following document content: '{context[:500]}'\n\n{query}"
    preprocessed_query = querypreprocessor.expand_query(query, step, int(mode), context[:500])
    try:
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages +
            [{"role": "user", "content": preprocessed_query}]
        )
        response = chat_completion.choices[0].message.content
        messages.append({"role": "user", "content": preprocessed_query})
        messages.append({"role": "assistant", "content": response})
        return response
    except Exception as e:
        print(f"An error occurred while generating response: {e}")
        return f"An error occurred: {e}"


def search_past_queries():
    conn = db.create_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, query FROM queries")
    rows = cur.fetchall()
    conn.close()
    return rows


def follow_up_question(id):
    conn = db.create_connection()
    cur = conn.cursor()
    cur.execute("SELECT query, response FROM queries WHERE id = ?", (id,))
    result = cur.fetchone()
    conn.close()
    return result


def download_file_from_google_drive(shared_link):
    # Extract the file ID from the shared link
    start = shared_link.find('/d/') + 3
    end = shared_link.find('/view')
    file_id = shared_link[start:end]

    # Construct the direct download URL
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

    # Initial request to fetch the file
    with requests.Session() as session:
        response = session.get(download_url, stream=True)
        token = get_confirm_token(response)

        # If there's a "confirm" token in the initial response, it's a large file warning
        if token:
            # Construct the URL to confirm the download
            download_url = f"https://drive.google.com/uc?export=download&id={file_id}&confirm={token}"
            response = session.get(download_url, stream=True)

        # Save the content to a file
        finalstring = save_response_content(response, 'downloaded_file.txt')  # Name your file appropriately
        return finalstring


def get_confirm_token(response):
    # Check for the presence of the "confirm" token in the cookie
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None


def save_response_content(response, destination):
    # Write the response content to a file in chunks
    finalString = ""
    CHUNK_SIZE = 32768  # 32KB chunks
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                finalString = finalString +  chunk.decode('utf-8')

    return finalString

# Use the direct download URL
file_url = 'https://drive.google.com/file/d/1zwfys7t5KHLFPIaO591Zg96rJ5vKfKWu/view?usp=sharing'



def main_loop():
    client = setup_openai_client()
    messages = []
    last_extracted_text = ""
    print("Welcome to Latti Macchiati Simulator")
    while True:
        print("\n1. Input Query\n2. Upload File\n3. Search Past Queries\n4. Interact with Last Extracted Text\n5. Exit")
        choice = input("Please select an option: ")
        if choice == '1':
            print("\nFormat choices:")
            print(" 1 - Bullet Points: Provide a bullet-pointed summary of the answer.")
            print(" 2 - Q&A: Answer in a question and answer format.")
            print(" 3 - Summary Sheet: Provide a detailed summary as the response.")
            format_choice = input("Select the response format (1-3): ")
            if format_choice.lower() == 'exit':
                break
            try:
                format_step = int(format_choice)
                if format_step not in [1, 2, 3]:
                    print("Invalid format choice. Please enter 1, 2, or 3.")
                    continue
            except ValueError:
                print("Please enter a valid number (1, 2, or 3).")
                continue
            input_query = input("Please enter your question: ")
            if input_query.lower() == 'exit':
                break
            response = generate_response(
                input_query, client, messages, format_step, choice)
            conn = db.create_connection()
            db.insert_query_response(conn, input_query, response, format_step)
            conn.close()
            print("Latti Macchiatti Simulator:", response)
        elif choice == '2':
            file_path = input("Enter the file path: ")
            if file_path.lower().endswith('.pdf'):
                text = file_handlers.extract_text_from_pdf(file_path)
            elif file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                text = file_handlers.extract_text_from_image(file_path)
                if text.strip() == "":
                    print("No text could be extracted from the image.")
                else:
                    print(
                        "Text extracted from the image. You can now interact with it.")
            elif file_path.lower().endswith('.docx'):
                text = file_handlers.extract_text_from_docx(file_path)
            elif file_path.lower().endswith('.txt'):
                text = file_handlers.extract_text_from_txt(file_path)
            else:
                print("Unsupported file type.")
                continue
            last_extracted_text = text
            conn = db.create_connection()
            db.insert_query_response(
                conn, "File uploaded: " + file_path, "Text stored for interaction", 0)
            conn.close()
        elif choice == '3':
            rows = search_past_queries()
            if rows:
                print("Past Queries:")
                for row in rows:
                    print(f"{row[0]}: {row[1]}")
                query_id = input("Enter ID to follow up or 'back' to return: ")
                if query_id.lower() == 'back':
                    continue
                try:
                    id = int(query_id)
                    query_details = follow_up_question(id)
                    if query_details:
                        print("Selected Query:", query_details[0])
                        print("Previous Response:", query_details[1])
                        follow_up = input("Enter your follow-up question: ")
                        if follow_up.lower() == 'exit':
                            break
                        response = generate_response(
                            follow_up, client, messages, 1, choice, query_details[1])
                        conn = db.create_connection()
                        db.insert_query_response(conn, follow_up, response, 1)
                        conn.close()
                        print("Latti Macchiatti Simulator:", response)
                    else:
                        print("No query found with that ID.")
                except ValueError:
                    print("Please enter a valid ID.")
            else:
                print("No past queries found.")
        elif choice == '4':
            if last_extracted_text:
                print("Ready to interact with the extracted text. Type your query:")
                query = input()
                if query.lower() == 'exit':
                    break
                response = generate_response(
                    query, client, messages, 1, int(choice), last_extracted_text)
                conn = db.create_connection()
                db.insert_query_response(conn, query, response, 1)
                conn.close()
                print("Response:", response)
            else:
                print(
                    "No extracted text available. Please upload a file and ensure text was successfully extracted.")
        elif choice == '5' or choice.lower() == 'exit':
            print("Exiting the Simulator.")
            break
        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    #print(download_file_from_google_drive(file_url))
    main_loop()

@app.get("/get-bullet1/")
def get_bullet1(query):
    client = setup_openai_client()
    messages = []
    response = generate_response(
        query, client, messages, 1, 1)
    conn = db.create_connection()
    db.insert_query_response(conn, query, response, 1)
    conn.close()

    json_string = querypreprocessor.parse_bullet_answer(response)
    return json_string

@app.get("/get-bullet2/")
def get_bullet2(query, file_url):
    client = setup_openai_client()
    messages = []

    fileContent = download_file_from_google_drive(file_url)

    response = generate_response(
        query, client, messages, 1, 2, fileContent)
    conn = db.create_connection()
    db.insert_query_response(conn, query, response, 1)
    conn.close()

    json_string = querypreprocessor.parse_bullet_answer(response)
    return json_string


@app.get("/get-QA1/")
def get_QA1(query):
    client = setup_openai_client()
    messages = []
    response = generate_response(
        query, client, messages, 2, 1)
    conn = db.create_connection()
    db.insert_query_response(conn, query, response, 2)
    conn.close()

    json_string = querypreprocessor.parse_QA_answer(response)
    return json_string

@app.get("/get-QA2/")
def get_QA2(query, file):
    client = setup_openai_client()
    messages = []
    response = generate_response(
        query, client, messages, 2, 2)
    conn = db.create_connection()
    db.insert_query_response(conn, query, response, 2)
    conn.close()

    json_string = querypreprocessor.parse_QA_answer(response)
    return json_string

@app.get("/get-summarry-1/")
def get_summary1(query):
    client = setup_openai_client()
    messages = []
    response = generate_response(
        query, client, messages, 3, 1)
    conn = db.create_connection()
    db.insert_query_response(conn, query, response, 3)
    conn.close()

    json_string = querypreprocessor.parse_summary_answer(response)
    return json_string

@app.get("/get-summary-2/")
def get_summary2(query, file):
    client = setup_openai_client()
    messages = []
    response = generate_response(
        query, client, messages, 3, 2)
    conn = db.create_connection()
    db.insert_query_response(conn, query, response, 3)
    conn.close()

    json_string = querypreprocessor.parse_summary_answer(response)
    return json_string

