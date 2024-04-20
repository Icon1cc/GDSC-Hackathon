import sys
from file_handlers import extract_text_from_pdf, extract_text_from_image
from query_processor import expand_query
from openai_integration import setup_openai, generate_response

def process_input(input_path, client, step = 1):
    if input_path.endswith('.pdf'):
        query = extract_text_from_pdf(input_path)
    elif input_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        query = extract_text_from_image(input_path)
    else:
        query = input_path 
    
    expanded_query = expand_query(query, step)
    return generate_response(expanded_query, client)

if __name__ == "__main__":
    if len(sys.argv) < 1 or len(sys.argv) > 2:
        print("Usage: python main.py <input_path_or_query>")
        sys.exit(1)

    input_path = input("What is your query: ")

    client = setup_openai()

    step = 1
    if(len(sys.argv) == 2):
        step = int(sys.argv[1])

    response = process_input(input_path, client, step)
    print(response)
