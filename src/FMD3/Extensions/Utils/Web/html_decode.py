import html

def html_decode(input_string):
    if not input_string:
        # Handle missing input
        return False

    # Decode HTML entities using html.unescape
    decoded_string = html.unescape(input_string)

    # Return the decoded string
    return decoded_string

def MangaInfoStatusIfPos(search_str, ongoing_str, completed_str):
    """
    Determine the manga status based on the search string and the provided ongoing and completed string conditions.

    Args:
        search_str (str): The search string to check against.
        ongoing_str (str): The ongoing manga status string.
        completed_str (str): The completed manga status string.

    Returns:
        str: The manga status (either 'Ongoing' or 'Completed').
    """

    if not search_str:
        return ''

    s = search_str.lower()
    o = ongoing_str.lower()
    c = completed_str.lower()

    if o:
        if o in s or search_many(o, s):
            return 'Ongoing'
        else:
            if not c:
                return 'Completed'
            elif search_many(c, s):
                return 'Completed'

    if c:
        if c in s or search_many(c, s):
            return 'Completed'
        elif search_many(o, s):
            return 'Ongoing'

    return ''

def search_many(str, search_str):
    """
    Checks if the `search_str` is found in the `str` or any of its substrings separated by '|'.

    Args:
        str (str): The string to search in.
        search_str (str): The search string to find.

    Returns:
        bool: True if `search_str` is found, False otherwise.
    """

    if '|' not in str:
        return str == search_str

    return any(s in str for s in search_str.split('|'))