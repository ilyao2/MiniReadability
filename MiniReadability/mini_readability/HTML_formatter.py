class HTMLFormatter:
    """
    This class format HTML to readability text
    """
    def __init__(self):
        self.rows_size = 80
        self.words_wrap = True

    def set_config(self, json):
        """ Set parameters from configure json """
        pass

    def format(self, HTML: str) -> str:
        """ Format HTML to readability text with current parameters """
        text = self.__get_required_text(HTML)
        text = self.__set_text_style(text)

        return text

    def __get_required_text(self, HTML: str) -> str:
        req_text = HTML + "req"
        return req_text

    def __set_text_style(self, text):
        styled_text = text + "styled"
        return styled_text
