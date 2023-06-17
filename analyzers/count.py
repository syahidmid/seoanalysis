def count_title_length(title):
    """
    Count the length of the title.
    """
    titleLength = len(title)
    return f"{titleLength} characters"
    
def count_meta_description(meta_description):

    meta_description_length = len(meta_description)
    return f"{meta_description_length} characters"


def count_words(content):
    """
    Count the number of words in the given content.

    Parameters:
    content (str): The content to count words in.

    Returns:
    str: A string representing the number of words in the content.
    """
    words = content.split()
    num_words = len(words)
    return f"{num_words} words*"