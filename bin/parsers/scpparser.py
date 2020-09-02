import requests
from html.parser import HTMLParser
import re


class SCPHTMLParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.div_count = 0
        self.start_count = False
        self.page_content_data = ''

    def handle_starttag(self, tag, attrs):
        if self.start_count and tag == 'div':
            self.div_count += 1
        elif tag == 'div' and len(attrs) and attrs[0] == ('id', 'page-content'):
            self.start_count = True
            self.div_count += 1

    def handle_endtag(self, tag):
        if self.start_count and tag == 'div':
            self.div_count -= 1
            if not self.div_count:
                self.start_count = False

    def handle_data(self, data):
        if self.start_count:
            self.page_content_data += data

    def error(self, message):
        pass


class SCPWordsParser:

    def __init__(self):
        self.word_re = re.compile(r'\w+')
        self.parser = SCPHTMLParser()

    def get_all_unique_words(self, scp_number):
        words = set()

        req = requests.get(f'http://www.scp-wiki.net/scp-{scp_number}')
        self.parser.feed(req.text)

        for word in self.word_re.findall(self.parser.page_content_data):
            words.add(word.lower())

        return words
