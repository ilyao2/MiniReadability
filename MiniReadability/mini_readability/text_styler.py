class TextStyler:
    def __init__(self):
        # All parameters can be in config.json
        # Default parameters for lenta.ru and gazeta.ru
        self.rows_size = 80
        self.words_wrap = True

    def set_text_style(self, text: str) -> str:
        pages = text.split('\n')
        styled_text = ''
        for page in pages:
            if len(page) < self.rows_size:
                styled_text += page + "\n"
                continue
            if self.words_wrap:
                words = page.split(' ')
                styled_text += self.__wrap_words(words)
            else:
                row = '\n'.join([page[i:i + self.rows_size] for i in range(0, len(page), self.rows_size)])
                styled_text += row + '\n'

        return styled_text

    def __wrap_words(self, words: list[str]) -> str:
        row = ''
        page = ''
        for word in words:
            if len(row) + len(word) > self.rows_size:
                if not row:
                    row = '\n'.join([word[i:i + self.rows_size] for i in range(0, len(word), self.rows_size)])
                    page += row + '\n'
                    row = ''
                    continue
                page += row + '\n'
                row = ''
            row += word + ' '
        if row:
            page += row + '\n'
        return page
