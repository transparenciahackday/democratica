try:
    from pygments import formatters, lexers
    from pygments import highlight as syntax_highlight
    from pygments.lexers import guess_lexer, get_lexer_by_name

    def highlight(data, language=None, default='python'):
        """Simple wrapper around pygments"""
        try:
            lexer = get_lexer_by_name(language, stripall=True, encoding='UTF-8')
        except ValueError:
            lexer = get_lexer_by_name(default, stripall=True, encoding='UTF-8')
        
        formatter = formatters.HtmlFormatter()
        return syntax_highlight(data, lexer, formatter)

except ImportError:
    pass
