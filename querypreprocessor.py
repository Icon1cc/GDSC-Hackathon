import re
def expand_query(query, step = 1, mode = 1, context = ""):

    detailed_query = ""

    if(mode == 1):
        detailed_query = expand_query1(query, int(step))
    elif(mode == 4):
        detailed_query = expand_query2(query, int(step), context)
    else:
        detailed_query = query + "?"

    return detailed_query


def expand_query1(query, step = 1):
    query = query.strip().capitalize()
    if not query.endswith('?'):
        query += '?'

    detailed_query = ""

    if (step == 1):
        detailed_query = query_bullet_point(query)
    elif (step == 2):
        detailed_query = querry_QAs(query)
    elif (step == 3):
        detailed_query = query_summary_sheet(query)

    return detailed_query


def expand_query2(query, step = 1, context = ""):
    query = query.strip().capitalize()
    if not query.endswith('?'):
        query += '?'

    detailed_query = ""

    if (step == 1):
        detailed_query = query_bullet_point2(query, context)
    elif (step == 2):
        detailed_query = querry_QAs2(query, context)
    elif (step == 3):
        detailed_query = query_summary_sheet2(query, context)

    return detailed_query




def query_bullet_point(query):
    detailed_query = (
        f"I will write a description of the way I want you to answer to the following question."
        f"The question that the user wants to learn about (studying about it context) will be : {query}"
        f"Identify the three to five most important ideas required before being able to answer this question. These idea should be such that if the user understands them all, he can answer the question by himself, not directly give him the answer."
        f"The template of the answer would be:"
        f"- Start your answer with word \"START\" and end with \"END\"."
        f"- Create a bullet point list of:"
        f"- For each one of the important ideas selected start the line with \"TITIDE\" + a short title of the idea + \"DESCIDE\" + a very brief description of the goal of the user when looking this point up."
        f"Example : TITIDE learning different positions and roles of players DESCIDE The user should understand the responsibilities and duties of each player on the team to know how to best contribute to the game. All on one line."
    )
    return detailed_query

def query_bullet_point2(query, context):

    detailed_query = (
        f"I will write a description of the way I want you to answer to the following question."
        f"Based mainly on this document: {context}"
        f"I want you to build three - five hint ideas for answering the question \"{query}\". These hints should help the user come up himself with the answer, not give it to him."
        f"The template of the answer would be:"
        f"- Start your answer with word \"START\" and end with \"END\"."
        f"- Create a bullet point list of:"
        f"- For each one of the selected hints start the line with \"TITIDE\" + a short title of the hint + \"DESCIDE\" + a very brief description of the goal of the user when looking this point up."
        f"Example : TITIDE learning different positions and roles of players DESCIDE The user should understand the responsibilities and duties of each player on the team to know how to best contribute to the game. All on one line."
    )

    return detailed_query


def querry_QAs(query):
    detailed_query = (
        f"I will write a description of the way I want you to answer to the following question."
        f"The question that the user wants to learn about (studying about its context) will be : {query}"
        f"Identify the three to five most important ideas required before being able to answer this question. These idea should be such that if the user understands them all, he can answer the question by himself, not directly give him the answer."
        f"The template of the answer would be:"
        f"- Start your answer with word \"START\" and end with \"END\"."
        f"- For each one of the important ideas selected write three questions about aspects that the user should know after looking up for that idea + well detailed answers to those questions"
        f"- Express them as \"STARTLINE\" + the question + \"ANSLINE\" + the answer."
    )
    return detailed_query

def querry_QAs2(query, context = ""):
    detailed_query = (
        f"I will write a description of the way I want you to answer to the following question."
        f"Based mainly on this document: {context}"
        f"The question that the user wants to learn about (studying about its context) will be : {query}"
        f"Identify the three to five most important ideas required before being able to answer this question. These idea should be such that if the user understands them all, he can answer the question by himself, not directly give him the answer."
        f"The template of the answer would be:"
        f"- Start your answer with word \"START\" and end with \"END\"."
        f"- For each one of the important ideas selected write three questions about aspects that the user should know after looking up for that idea + well detailed answers to those questions"
        f"- Express them as \"STARTLINE\" + the question + \"ANSLINE\" + the answer."
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

def query_summary_sheet2(query, context = ""):
    detailed_query = (
        f"I will write a description of the way I want you to answer to the following question."
        f"Based mainly on this document: {context}"
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

def parse_bullet_answer(answer):
    list_titles = []
    list_descs = []
    list_lines = []

    titles = []
    descrs = []


    title_sep = "TITIDE "
    desc_sep = " DESCIDE "

    start = 0  # initial search position
    end = 0
    while True:
        start = answer.find(title_sep, start)
        end = answer.find(desc_sep, end)
        line = answer.find("\n", end)
        if start == -1:  # no more occurrences found
            break

        list_titles.append(start)
        list_descs.append(end)
        list_lines.append(line)
        start += 1
        end += 1

    for i in range(0, len(list_titles)):

        tempTitle = answer[list_titles[i] + len(title_sep): list_descs[i]]
        tempDesc = answer[list_descs[i] + len(desc_sep): list_lines[i]]
        titles.append(tempTitle)
        titles.append(tempDesc)

    print(titles)

    return titles
