from mini_readability.HTML_required_getter import HTMLRequiredGetter
from mini_readability.text_styler import TextStyler


class HTMLFormatter:
    """
    This class format HTML to readability text
    """

    def __init__(self) -> None:
        # All parameters can be in config.json
        # Default parameters for lenta.ru and gazeta.ru
        self.getter = HTMLRequiredGetter()
        self.styler = TextStyler()

    def format(self, HTML: str) -> str:
        """ Format HTML to readability text with current parameters """
        text = self.getter.get_required_text(HTML)
        text = self.styler.set_text_style(text)

        return text
