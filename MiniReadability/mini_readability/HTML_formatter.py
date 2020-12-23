from bs4 import BeautifulSoup


class HTMLFormatter:
    """
    This class format HTML to readability text
    """

    def __init__(self):
        # All parameters can be in config.json
        # Default parameters for lenta.ru and gazeta.ru
        self.rows_size = 80
        self.words_wrap = True
        self.except_tag_list = ['nav', 'footer', 'header']
        self.except_class_list = ['b-topic-sidebar', 'b-socials', 'b-topic-addition', 'b-tabloid',
                                  'b_audio_wrapper', 'b_social_sharing', 'adcenter-wrapper',
                                  'closebtn', 'voice-over__label']
        self.except_id_list = ['header', 'footer', 'recommender', 'article_main_video', 'article_pants', 'right']
        self.need_attr_list = ['href', 'src']

    def set_config(self, json):
        """ Set parameters from configure json """
        pass

    def format(self, HTML: str) -> str:
        """ Format HTML to readability text with current parameters """
        text = self.__get_required_text(HTML)
        text = self.__set_text_style(text)

        return text

    def __get_required_text(self, HTML: str) -> str:
        soup = BeautifulSoup(HTML, 'lxml')
        root = soup.html

        req_text = self.__get_dom_child_text(root)

        return req_text

    def __set_text_style(self, text):
        styled_text = text + "styled"
        return styled_text

    def __get_dom_child_text(self, node):
        """ Recursive func for deep-check html dom-tree """
        text = ''
        child_list = [e for e in node.children if e.name is not None and e.text != '']
        if child_list:
            # Excepting elements
            for child in child_list:
                if child.name in self.except_tag_list:
                    child.decompose()
                    continue
                elif 'class' in child.attrs and set(child.attrs['class']) & set(self.except_class_list):
                    child.decompose()
                    continue
                elif 'id' in child.attrs and child.attrs['id'] in self.except_id_list:
                    child.decompose()
                    continue
                # Recursive appending elements
                text += self.__get_dom_child_text(child)

        blank_line_flag = False

        # Saving required text
        if node.text.strip() != '':
            text += ' '.join(node.text.split()) + '\n'
            blank_line_flag = True

        for attr in self.need_attr_list:
            if attr in node.attrs:
                text += '[' + node.attrs[attr] + ']\n'
                blank_line_flag = True

        if blank_line_flag:
            text += '\n'

        node.decompose()

        return text
