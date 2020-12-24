import requests
from mini_readability.HTML_formatter import HTMLFormatter


class MiniReadabilityManager:
    """
    This class manage readability HTML
    it can:
    - read html from url
    - format html to readability text
    - save readability text in local file
    """

    def __init__(self, URL: str = "") -> None:
        self.__text: str = ""
        self.__HTML: str = ""
        self.__URL: str = URL
        self.__formatter = HTMLFormatter()
        if str:
            self.read_url(URL)

    @property
    def text(self) -> str:
        """
        :return: mini readable string
        """
        return self.__text

    @property
    def URL(self) -> str:
        return self.__URL

    @property
    def HTML(self) -> str:
        return self.__HTML

    def save_in_file(self) -> None:
        """
        save mini readable text in file
        path =  [CUR_DIR]/[URL].txt
        """
        # TODO: save in file
        pass

    def read_url(self, URL: str) -> str:
        """
        read url, parse html, create readability text
        :return: mini readable string
        """
        self.__URL = URL

        try:
            response = requests.get(URL, timeout=(3, 10))
        except requests.exceptions.RequestException:
            print("Can't read URL")
            self.__HTML = ""
            self.__text = ""
            return self.__text

        self.__HTML = response.text

        self.__text = self.__formatter.format(self.__HTML)

        return self.__text
