from djutils.constants import STOP_WORDS_RE


def split_words_at(words, split_at, after=True):
    """
    Split the words string at a certain number of characters:

    >>> split_words_at('aa bb cc dd', 4, True)
    'aa bb'
    >>> split_words_at('aa bb cc dd', 4, False)
    'aa'
    """
    if len(words) < split_at:
        return words
    if after:
        tmp = words[split_at:]
        pos = tmp.find(' ')
        if pos >= 0:
            return words[:split_at + pos]
        else:
            return words
    else:
        tmp = words[:split_at + 1]
        pos = tmp.rfind(' ')
        if pos > 0:
            return tmp[:pos]
        else:
            return tmp[:split_at]

def clean_stop_words(text):
    return STOP_WORDS_RE.sub('', text).strip()
