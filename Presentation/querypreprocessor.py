import re
import json
def expand_query(query, step = 1, mode = 1, context = ""):

    detailed_query = ""

    if(mode == 1):
        detailed_query = expand_query1(query, int(step))
    elif(mode == 3):
        detailed_query = expand_query2(query, int(step), context)

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
    elif (step == 4):
        detailed_query = query_accompagny_user(query, context)

    return detailed_query




def query_bullet_point(query):
    detailed_query = (
        f"I will write a description of the way I want you to answer to the following question."
        f"The question that the user wants to learn about (studying about it context) will be : {query}"
        f"Identify the three most important ideas required before being able to answer this question. These idea should be such that if the user understands them all, he can answer the question by himself, not directly give him the answer."
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
        f"I want you to build three hint ideas for answering the question \"{query}\". These hints should help the user come up himself with the answer, not give it to him."
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
        f"Identify the three most important ideas required before being able to answer this question. These idea should be such that if the user understands them all, he can answer the question by himself, not directly give him the answer."
        f"The template of the answer would be:"
        f"- Start your answer with word \" START \" and end with \" END \"."
        f"- For each one of the important ideas selected write a difficult question about an aspect of it, that the user should know after looking up for that idea + three answers to that question, first one being true and second two being completely false."
        f"- Express them on one line as \" STARTLINE \" + the question + \" ANSFI \" + the correct answer + \" ANSSE \" + first completely wrong answer + \" ANSTHI \" + second completely wrong answer. All this without line break."
    )
    return detailed_query

def querry_QAs2(query, context = ""):
    detailed_query = (
        f"I will write a description of the way I want you to answer to the following question."
        f"Based mainly on this document: {context}"
        f"Identify the three most important ideas required before being able to answer this question. These idea should be such that if the user understands them all, he can answer the question by himself, not directly give him the answer."
        f"The template of the answer would be:"
        f"- Start your answer with word \" START \" and end with \" END \"."
        f"- For each one of the important ideas selected write a difficult question about an aspect of it, that the user should know after looking up for that idea + three answers to that question, first one being true and second two being completely false."
        f"- Express them on one line as \" STARTLINE \" + the question + \" ANSFI \" + the correct answer + \" ANSSE \" + first completely wrong answer + \" ANSTHI \" + second completely wrong answer. All this without line break."
    )
    return detailed_query

def query_summary_sheet(query):
    detailed_query = (
        f"I will write a description of the way I want you to answer to the following question."
        f"The question will be : {query}"
        f"Identify the most important idea that this question tackles."
        f"The template of the answer would be:"
        f"- Start your answer with word \"START\"."
        f"- First paragraph expressed without a line break as \"IDEPAR\" + a short title of the most important idea that this question tackles + \"IDEDESCO \" +  a detailed description of the idea you chose. One line."
        f"- The next paragraphs will be for two key aspects concerning this idea"
        f"They will be expressed without line break as \"PARTIT\" + a short title of the idea chosen +  explanations in many details of that aspect. On the same line] ."
        f"- Next paragraph will start by \"SUMALL\" + a summary about the information presented"
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
        f"- First paragraph expressed without a line break as \"IDEPAR\" + a short title of the most important idea that this question tackles + \"IDEDESC \" +  a detailed description of the idea you chose."
        f"- The next paragraphs will be for two or three key aspects concerning this idea"
        f"They will be expressed without line break as \"PARTIT\" + a short title of the idea chosen +  explanations in many details of that aspect] ."
        f"- Next paragraph will start by \"SUMALL\" + a summary about the information presented"
        f"It should end with the word \"END\""
    )
    return detailed_query

def query_accompagny_user(query, context = ""):
    detailed_query = (
        f"I will write a description of the way I want you to answer to the following question."
        f"Based mainly on this document: {context}"
        f"The question will be : {query}"
        f"I want you to make a roadmap to tutor the user on how to read the document. It should include:"
        f"What points to pay attention to, regarding the query"
        f"And what needs to be researched from external sources for comprehension."
    )
    return detailed_query


def parse_bullet_answer(answer):
    list_titles = []
    list_descs = []
    list_lines = []

    titles = []

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

    listDics = []
    for i in range (0, int(len(titles)/2)):
        dic = {}
        dic['title'] = titles[2*i]
        dic['description'] = titles[2*i+1]
        listDics.append(dic)

    dicto = {
        "title1" : titles[0],
        "description1" : titles[1],
        "title2" : titles[2],
        "description2" : titles[3],
        "title3" : titles[4],
        "description3" : titles[5],
    }


    return dicto


def parse_QA_answer(answer):
    list_titles = []
    list_descs1 = []
    list_descs2 = []
    list_descs3 = []
    list_lines = []

    titles = []

    title_sep = "STARTLINE "
    desc_sep1 = " ANSFI "
    desc_sep2 = " ANSSE "
    desc_sep3 = " ANSTHI "

    start = 0  # initial search position
    while True:
        start = answer.find(title_sep, start)
        end1 = answer.find(desc_sep1, start)
        end2 = answer.find(desc_sep2, end1)
        end3 = answer.find(desc_sep3, end1)
        line = answer.find("\n", end3)
        if start == -1:  # no more occurrences found
            break

        list_titles.append(start)
        list_descs1.append(end1)
        list_descs2.append(end2)
        list_descs3.append(end3)
        list_lines.append(line)
        start += 1
        end1 += 1

    for i in range(0, len(list_titles)):

        tempTitle = answer[list_titles[i] + len(title_sep): list_descs1[i]]
        tempDesc1 = answer[list_descs1[i] + len(desc_sep1): list_descs2[i]]
        tempDesc2 = answer[list_descs2[i] + len(desc_sep2): list_descs3[i]]
        tempDesc3 = answer[list_descs3[i] + len(desc_sep3): list_lines[i]]
        titles.append(tempTitle)
        titles.append(tempDesc1)
        titles.append(tempDesc2)
        titles.append(tempDesc3)

    listDics = []
    for i in range(0, int(len(titles)/4)):
        dict = {}
        dict['title'] = titles[4*i]
        dict['correct'] = titles[4*i + 1]
        dict['incorrect1'] = titles[4*i + 2]
        dict['incorrect2'] = titles[4*i + 3]
        listDics.append(dict)

    dict={}

    dict['title1'] = titles[0]
    dict['correct1'] = titles[1]
    dict['incorrect11'] = titles[2]
    dict['incorrect12'] = titles[3]

    dict['title2'] = titles[4]
    dict['correct2'] = titles[5]
    dict['incorrect21'] = titles[6]
    dict['incorrect22'] = titles[7]

    dict['title3'] = titles[8]
    dict['correct3'] = titles[9]
    dict['incorrect31'] = titles[10]
    dict['incorrect32'] = titles[11]

    return dict

def parse_summary_answer(answer):

    #LES OUTPUTS CEST TITLEIDEA, DESCIDEA, TITLES, SUMALL
    titleIdea = ""
    descIdea = ""


    startIntro = "IDEPAR"
    titleIntro = "IDEDESCO"

    start = answer.find(startIntro, 0)
    end = answer.find(titleIntro, 0)
    descend = answer.find("\n", end)

    titleIdea = answer[start + len(startIntro): end]
    descIdea = answer[end + len(titleIntro): descend]

    list_titles = []
    list_descs = []
    list_lines = []

    titles = []

    title_sep = "PARTIT "
    desc_sep = " PARTEXP "

    start = 0  # initial search position
    end = 0
    while True:
        start = answer.find(title_sep, start)
        end = answer.find("\n", start)
        if start == -1:  # no more occurrences found
            break

        list_titles.append(start)
        list_descs.append(end)
        start += 1
        end += 1

    for i in range(0, len(list_titles)):

        tempTitle = answer[list_titles[i] + len(title_sep): list_descs[i]]
        titles.append(tempTitle)

    sepSumall = "SUMALL "
    indexSumall = answer.find(sepSumall)
    sumall = answer[indexSumall + len(sepSumall) : answer.find("\n",indexSumall)]

    print(titleIdea)
    print(descIdea)
    print(titles)
    print(sumall)

    dict = {}

    dict["titleData"] = titleIdea
    dict["descriptionIdea"] = descIdea
    dict["part1"] = titles[0]
    dict["part2"] = titles[1]
    dict["summary"] = sumall

    return dict