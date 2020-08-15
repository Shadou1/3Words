import requests
from html.parser import HTMLParser
import re

WORD_TYPES = ['Noun', 'Verb', 'Adjective', 'Adverb']

class WiktioaryParser(HTMLParser):

    def __init__(self):
        super().__init__()

        self.descriptions = []

        self.current_word_type = ''
        self.current_description = ''

        self.found_english = False
        self.found_description_list = False
        self.found_single_description = False
        # self.current_description_number = 0

    def handle_starttag(self, tag, attrs):

        # print(attrs)
        # print(*zip(*attrs))
        # print(dict(attrs))

        if tag == 'span' and ('class', 'mw-headline') in attrs:
            
            if ('id', 'English') in attrs:
                self.found_english = True
                print('Found English')
            
            elif "Etymology" in dict(attrs)['id']:
                if self.found_english:
                    
                    # Adding new Etymology
                    self.descriptions.append({})
                    print('Found etymology')

            if self.found_english and self.descriptions:
                for wt in WORD_TYPES:
                    if wt in dict(attrs)['id']:

                        # Adding new Word Type
                        self.descriptions[-1][wt] = []
                        self.current_word_type = wt
                        print('Current word type is', wt)

        elif tag == 'ol' and self.current_word_type:

            self.found_description_list = True
            print('Found desription list')

        elif tag == 'li' and self.found_description_list:
            
            self.found_single_description = True

    def handle_endtag(self, tag):

        if tag == 'li' and self.found_single_description:

            # Add description for current word type of current etymology
            self.descriptions[-1][self.current_word_type].append(self.current_description)

            self.found_single_description = False
            self.current_description = ''

        elif tag == 'ol' and self.current_word_type:

            self.found_description_list = False
            # print(self.current_description)
            print('Found the end of description list')


    def handle_data(self, data):
        
        if self.found_single_description:
            self.current_description += data
            # print('Added current description')

    def error(self, message):
        pass

if __name__ == '__main__':
    parser = WiktioaryParser()
    req = requests.get(f'https://en.wiktionary.org/wiki/staple')
    # print(req.text)
    parser.feed(req.text)
    print(parser.descriptions)