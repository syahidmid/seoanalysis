def word_counter(text):
    try:
        word_count = len(text.split())
        return word_count
    except Exception as e:
        return f"Unable to get word count: {str(e)}"


def character_counter(text):
    try:
        character_count = len(text)
        return character_count
    except Exception as e:
        return f"Unable to get character count: {str(e)}"
