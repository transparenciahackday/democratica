Syntax Highlighter
==================

.. py:module:: djutils.utils.highlighter

Contains utilities for syntax highlighting code snippets.

.. note:: requires the "pygments" package

.. py:function:: highlight(data, language=None, default='python')
    
    Simple wrapper around pygments syntax highlighter.  Returns HTML.
