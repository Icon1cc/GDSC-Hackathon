import re


def expand_query(query, step = 1):
    query = query.strip().capitalize()
    if not query.endswith('?'):
        query += '?'

    # Expand the query to request detailed educational information

    detailed_query = ""

    if(step == 1):
        detailed_query = query_bullet_point(query)
    elif(step == 2):
        detailed_query = querry_QAs(query)
    elif(step == 3):
        detailed_query = query_summary_sheet(query)

    return detailed_query


def query_bullet_point(query):
    detailed_query = (
        f"I will write a description of the way I want you to answer to the following question."
        f"The question that the user wants to learn about (studying about it context) will be : {query}"
        f"Identify the three to five most important ideas required before being able to answer this question. These idea should be such that if the user understands them all, he can answer the question by himself, not directly give him the answer."
        f"The template of the answer would be:"
        f"- Start your answer with word \"START\" and end with \"END\"."
        f"- Create a bullet point list of:"
        f"- For each one of the important ideas selected start the line with \"IDEA_TITLE\" + a short title of the idea + \"DESC\" + a very brief description of the goal of the user when looking this point up."
    )
    return detailed_query

def querry_QAs(query):
    detailed_query = (
        f"I will write a description of the way I want you to answer to the following question."
        f"The question that the user wants to learn about (studying about it context) will be : {query}"
        f"Identify the three to five most important ideas required before being able to answer this question. These idea should be such that if the user understands them all, he can answer the question by himself, not directly give him the answer."
        f"The template of the answer would be:"
        f"- Start your answer with word \"START\" and end with \"END\"."
        f"- For each one of the important ideas selected write three questions about aspects that the user should know after looking up for that idea + well detailed answers to those questions"
        f"- Express them as \"QUESTION\" + the question + \"ANSWER\" + the answer."
    )
    return detailed_query

def query_summary_sheet(query):
    detailed_query = (
        f"I will write a description of the way I want you to answer to the following question."
        f"The question will be : {query}"
        f"Identify the most important idea that this question tackles."
        f"The template of the answer would be:"
        f"- Start your answer with word \"START\"."
        f"- First paragraph \"IDEA\" + One paragraph will be a short title of the idea chosen + \": \" +  a detailed description of the idea you chose."
        f"- The next paragraphs will be for two or three  key aspects concerning this idea: [\"PAR_TITLE\" + a short title of the idea chosen + \"EXP\" +  explanations in many details of that aspect] ."
        f"- Next paragraph will start by \"SUMMARY\" + a summary about the information presented"
        f"It should end with the word \"END\""
    )
    return detailed_query

