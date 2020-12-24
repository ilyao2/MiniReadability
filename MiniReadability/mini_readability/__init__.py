import requests
import json
import re
import os
from mini_readability.HTML_formatter import HTMLFormatter


class MiniReadabilityManager:
    """
    This class manage readability HTML
    it can:
    - read html from url
    - format html to readability text
    - save readability text in local file
    """

    def __init__(self) -> None:
        self.__text: str = ""
        self.__HTML: str = ""
        self.__URL: str = ""
        self.__formatter = HTMLFormatter()

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
        path = re.sub(r'(^.*//)|(//+$)', '', self.__URL)
        dirs = [i for i in path.split('/') if i]
        path = ''
        for d in dirs[:-1]:
            if d:
                path += d + '/'
                if not (os.path.exists(path) and os.path.isdir(path)):
                    os.mkdir(path)
        with open(path + dirs[-1] + '.txt', 'w') as f:
            f.write(self.__text)

    def use_config(self, path: str) -> None:
        """ Set parameters from configure json """
        data = {}
        try:
            with open(path, 'r') as f:
                data = json.load(f)
        except OSError:
            print("Can't read file: " + path)
            return

        if 'words_wrap' in data:
            self.__formatter.styler.words_wrap = data['words_wrap']
        if 'rows_size' in data:
            self.__formatter.styler.rows_size = data['rows_size']
        if 'except_class_list' in data:
            self.__formatter.getter.except_class_list = data['except_class_list']
        if 'except_id_list' in data:
            self.__formatter.getter.except_id_list = data['except_id_list']
        if 'except_tag_list' in data:
            self.__formatter.getter.except_tag_list = data['except_tag_list']
        if 'need_attr_list' in data:
            self.__formatter.getter.need_attr_list = data['need_attr_list']

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
