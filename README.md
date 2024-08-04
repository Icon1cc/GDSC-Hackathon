# GDSC PoliMi @ START HACK

This is the repository for the Google Developer Student Club Start Hackaton. The main folder is './presentation' as it holds all the necessary files during the showcase of our project in front of the jury. This project displays a trivia mobile application using openAI chatGPT system as motor engine in order to generate the data/information. 

## Installation

To get started, follow these simple steps:

### Clone the Repository

```bash
git clone https://github.com/Icon1cc/GDSC-Hackathon.git
cd presentation/hackatonApp
```

### Install Dependencies

```bash
npm install
pip3 install python-dotenv
pip3 install --upgrade openai
pip3 install openai pillow PyMuPDF pytesseract
pipenv install
pipenv shell
python3 main.py
python3 chroma_db_integration.py
pip3 install python-docx
```

### Run the app

```bash
npx expo start -c
```

## Backend

This project uses a local backend. It is mandatory to create a personal account at OpenAI and configure the .env.local file accordingly. Furthermore, a detailed step-by-step guide is given on both services website in order to embed them together.

