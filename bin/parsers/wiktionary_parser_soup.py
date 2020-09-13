import re
from urllib.request import urlopen
from urllib.error import HTTPError

from bs4 import BeautifulSoup

def get_wiktionary_word(word, english_only=True):

    try:

        with urlopen(f'https://en.wiktionary.org/wiki/{word}') as client:
            html = client.read()
        
    except HTTPError as e:
        print(f'no such word {word}')
        return None

    soup = BeautifulSoup(html, 'html.parser')

    word_dictionary = parse_dictionary(soup, english_only)

    return word_dictionary

def parse_dictionary(soup: BeautifulSoup, english_only=True):

    dictionary = {}

    re_etymology = re.compile(r'Etymology.*')
    re_part_of_speech = re.compile(r'Noun|Verb|Adjective|Adverb|' +
                                r'Numeral|Pronoun|Conjunction|Preposition|Interjection|Romanization')

    # english = soup.find('span', {'id': 'English'})

    all_elements = soup.find_all(True)

    h2_list = soup.findAll(lambda elem: elem.name == 'h2' and elem.string != 'Contents' and elem.string != 'Navigation menu')
    languages_list = [lang.find('span') for lang in h2_list]
    etymology_list = soup.findAll('span', id = re_etymology)
    parts_of_speech_list = soup.findAll('span', id = re_part_of_speech)
    descriptions_list = soup.findAll('ol')
    translations_list = soup.findAll('table', class_='translations')

    # TODO Optimize the adding of etymology

    lang_range = 1 if english_only and len(languages_list) > 1 else len(languages_list) - 1
    for i in range(lang_range):
        for etymology in etymology_list:
            if etymology in all_elements[
                all_elements.index(languages_list[i]):
                all_elements.index(languages_list[i + 1])]:
                # print('Etymology in', languages_list[i]['id'])
                break
        else:
            # print('No etymology in', languages_list[i]['id'])
            someEtymology = soup.new_tag('span', id='Etymology')
            languages_list[i].insert_after(someEtymology)
            etymology_list.append(someEtymology)

    if not english_only:
        for etymology in etymology_list:
            if etymology in all_elements[all_elements.index(languages_list[-1]):]:
                # print('Etymology in', languages_list[-1]['id'])
                break
        else:
            # print('No etymology in', languages_list[-1]['id'])
            someEtymology = soup.new_tag('span', id='Etymology')
            languages_list[i].insert_after(someEtymology)
            etymology_list.append(someEtymology)

    # Find Language
    for language in languages_list:
        if english_only and language['id'] != "English": continue

        dictionary[language['id']] = {}

        # Add etymology if etymology is not found
        # print(all_elements.index(language))

        # Find Etymology
        for next_etymology in language.next_elements:
            if next_etymology in etymology_list:

                dictionary[language['id']][next_etymology['id']] = {}

                # Find part of speech
                for next_part_of_speech in next_etymology.next_elements:
                    if next_part_of_speech in parts_of_speech_list:

                        dictionary[language['id']][next_etymology['id']][next_part_of_speech['id']] = []

                        # Find description list <li> elements
                        for next_description in next_part_of_speech.next_elements:
                            if next_description in descriptions_list:

                                descriptions = next_description.findAll('li', recursive=False)

                                for desc in descriptions:

                                    # Remove maintenance-line class elements from the tree
                                    for maintenance_line in desc.findAll(class_='maintenance-line'):
                                        maintenance_line.extract()

                                    # Get examples
                                    examples = [d.get_text() for d in desc.findAll('dd') if d.get_text()]

                                    # Remove examples from the tree
                                    for li in desc.findAll('li'):
                                        li.extract()

                                    for dd in desc.findAll('dd'):
                                        dd.extract()

                                    # TODO Get Translations

                                    # Add the rest of the text as a description
                                    desc_text = desc.get_text().strip()

                                    # TODO find out while somethimes desc_text is empty
                                    if desc_text:
                                        dictionary[language['id']][next_etymology['id']][next_part_of_speech['id']].append([desc_text, examples])

                                break

                    # If next part of speech element is etymology or language, break
                    elif next_part_of_speech in etymology_list or next_part_of_speech in languages_list:
                        break

            # If next etymology element is language, break
            elif next_etymology in languages_list:
                break

    return dictionary


if __name__ == "__main__":

    import json
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("word", help="word from wiktionary", default='staple')
    parser.add_argument("--file", help="json file to write to")
    parser.add_argument("--english-only", help="only search for English definitions", default='yes')
    args = parser.parse_args()
    if not args.file: args.file = args.word + '.json'

    word_dictionary = get_wiktionary_word(args.word, True if args.english_only == 'yes' else False)

    with open(args.file, 'w', encoding='utf-8') as f:
        json.dump(word_dictionary, f, indent=2, ensure_ascii=False)