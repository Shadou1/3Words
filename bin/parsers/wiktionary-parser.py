import requests
from html.parser import HTMLParser
import re
import json

WORD_TYPES = ['Noun', 'Verb', 'Adjective', 'Adverb']

class WiktioaryParser(HTMLParser):

    def __init__(self):
        super().__init__()

        self.descriptions = []

        self.current_word_type = ''
        self.current_description = ''
        self.current_examples = []

        self.found_english = False
        self.found_description_list = False
        self.found_single_description = False

        # Found examples in <dl> element
        # self.found_examples_description = False

        # Found examples in <span> with class="HQToggle"
        # self.found_examples_toggle = False

        # Found example in either form
        self.found_example = False
        self.example_in_HQToggle = False

        # self.current_description_number = 0

    def handle_starttag(self, tag, attrs):

        # print(attrs)
        # print(*zip(*attrs))
        # print(dict(attrs))

        # print(attrs)

        if tag == 'span':
            
            # print(attrs)

            if ('class', 'mw-headline') in attrs:
            
                if ('id', 'English') in attrs:

                    self.found_english = True
                    print('Found English')
                
                elif self.found_english and "Etymology" in dict(attrs)['id']: 

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

            # elif ('class', 'HQToggle') in attrs:
                
            #     self.found_examples_toggle = True
            #     self.current_examples.append('')
            #     print('Found examples toggle')

        elif tag == 'h2' and self.found_english:

            # Stop Parsing Data
            self.current_word_type = ''
            self.current_description = ''
            self.found_english = False
            self.found_description_list = False
            self.found_single_description = False
            print('Found the end ot the English section')

        elif tag == 'ol' and self.current_word_type:

            self.found_description_list = True
            print('Found description list')

        elif tag == 'li':

            if self.found_description_list and not self.found_single_description:
            
                self.found_single_description = True
                print("Found single description")

            elif self.found_description_list and self.found_single_description:

                self.found_example = True
                self.example_in_HQToggle = True
                self.current_examples.append('')
                print("Found example in toggle")

        elif tag == 'dd' and self.found_single_description and not self.found_example:

            self.found_example = True
            self.example_in_HQToggle = False
            self.current_examples.append('')
            print("Found example")

    def handle_data(self, data):
        
        if self.found_single_description:

            if self.found_example:

                self.current_examples[-1] += data

            # if self.found_examples_toggle or self.found_examples_description:

            #     self.current_examples[-1] += data

            else:

                self.current_description += data
                # print('Added current description')

    def handle_endtag(self, tag):

        if tag == 'li':

            if self.found_single_description and not self.found_example:

                # Add description for current word type of current etymology
                self.descriptions[-1][self.current_word_type].append((self.current_description, self.current_examples))

                # Descriptions and Examples are again not found
                self.current_description = ''
                self.current_examples = []

                self.found_single_description = False
                # self.found_examples_description = False
                # self.found_examples_toggle = False
                self.found_example = False

                print("Found the end of a single description")

            elif self.found_single_description and self.found_example and self.example_in_HQToggle:

                self.found_example = False
                # self.example_in_HQToggle = False
                print("Found the end of a single example")

        elif tag == 'ol' and self.current_word_type:

            self.found_description_list = False
            # print(self.current_description)
            print('Found the end of description list')

        # elif tag == 'dl' and self.found_examples_description:

        #     self.found_examples_description = False

        # Crudely handel both types of examples
        # elif tag == 'dd' and self.found_examples_description or self.found_examples_toggle:

        #     self.current_examples.append('')

        elif tag == 'dd' and self.found_single_description and self.found_example and not self.example_in_HQToggle:

            self.found_example = False
            # self.example_in_HQToggle = False

    def error(self, message):
        pass

if __name__ == '__main__':
    parser = WiktioaryParser()
    req = requests.get(f'https://en.wiktionary.org/wiki/staple')
    # print(req.text)
    # json.dump(req.text, 'dump.json')
    # with open('test.txt', 'w', encoding='utf-8') as f:
    #     f.write(req.text)

    parser.feed(req.text)
    req.close()
    # print(parser.descriptions)
    with open('test.json', 'w', encoding='utf-8') as f:
        json.dump(parser.descriptions, f, indent=2)