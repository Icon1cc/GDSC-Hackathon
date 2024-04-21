import openai
from dotenv import load_dotenv
import os
import querypreprocessor
import chroma_db_integration as db
import file_handlers

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
    main_loop()
