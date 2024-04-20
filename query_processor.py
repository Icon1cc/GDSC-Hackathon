import re


def expand_query(query):
    query = query.strip().capitalize()
    if not query.endswith('?'):
        query += '?'

    # Expand the query to request detailed educational information
    detailed_query = (
        f"Can you provide a comprehensive explanation of {query} "
        f"Please include its history, current applications, various types, "
        f"and any relevant social or economic implications."
    )
    return detailed_query
