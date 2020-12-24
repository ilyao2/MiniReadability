from mini_readability.HTML_required_getter import HTMLRequiredGetter
from mini_readability.text_styler import TextStyler


class HTMLFormatter:
    """
    This class format HTML to readability text
    """

    def __init__(self) -> None:
        # All parameters can be in config.json
        # Default parameters for lenta.ru and gazeta.ru
        self.__getter = HTMLRequiredGetter()
        self.__styler = TextStyler()

    def set_config(self, json):
        """ Set parameters from configure json """
        pass

    def format(self, HTML: str) -> str:
        """ Format HTML to readability text with current parameters """
        text = self.__getter.get_required_text(HTML)
        text = self.__styler.set_text_style(text)

        return text
