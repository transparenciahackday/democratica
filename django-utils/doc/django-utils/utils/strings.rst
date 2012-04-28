Strings
=======

.. py:module:: djutils.utils.strings

A collection of utilities for dealing with strings.

.. py:function:: split_words_at(words, split_at, after=True)

    Split the words string at a certain number of characters
    
    :param words: an arbitrary string to truncate
    :param split_at: number of characters to treat as the boundary
    :param after: whether to break up string before or after the boundary
    
    Example::

        >>> split_words_at('aa bb cc dd', 4, True)
        'aa bb'
        >>> split_words_at('aa bb cc dd', 4, False)
        'aa'

.. py:function:: clean_stop_words(text)

    Remove all instances of stop words from text.  Stop words are defined
    in :mod:`djutils.constants`
