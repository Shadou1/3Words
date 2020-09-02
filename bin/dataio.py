import pathlib
import json

from .word_data import ReviewedWord


class DataIO:
    def __init__(self,
                 basic_words_path,
                 known_words_path,
                 reviewed_words_path,
                 awaiting_review_words_path,
                 other_words_path):
        self.basic_words_path = pathlib.Path(basic_words_path)
        self.known_words_path = pathlib.Path(known_words_path)
        self.reviewed_words_path = pathlib.Path(reviewed_words_path)
        self.awaiting_review_words_path = pathlib.Path(awaiting_review_words_path)
        self.other_words_path = pathlib.Path(other_words_path)

        self.basic_words = set()
        self.known_words = set()
        self.reviewed_words = []
        self.awaiting_review_words = set()
        self.other_words = set()

    def add_basic_word(self, word):
        self.basic_words.add(word)

    def add_known_word(self, word):
        self.known_words.add(word)

    def add_awaiting_review_word(self, word):
        self.awaiting_review_words.add(word)

    def add_other_word(self, word):
        self.other_words.add(word)

    def add_reviewed_word(self, word):
        self.reviewed_words.append(ReviewedWord(word))

    def print_reviewed_words(self):
        for word in self.reviewed_words:
            print(word)

    def get_reviewed_word(self, w):
        for word in self.reviewed_words:
            if word.word == w:
                return word
        else:
            return(f"no such word {w}")

    def read(self):
        try:
            with open(self.basic_words_path, "r", encoding="utf-8") as file:
                self.basic_words = {word for word in json.load(file)}
            with open(self.known_words_path, "r", encoding="utf-8") as file:
                self.known_words = {word for word in json.load(file)}
            with open(self.awaiting_review_words_path, "r", encoding="utf-8") as file:
                self.awaiting_review_words = {word for word in json.load(file)}
            with open(self.other_words_path, "r", encoding="utf-8") as file:
                self.other_words = {word for word in json.load(file)}

            with open(self.reviewed_words_path, "r", encoding="utf-8") as file:
                self.reviewed_words = [ReviewedWord(word[0], word[1], word[2], word[3]) for word in json.load(file)]
        except FileNotFoundError as err:
            print("file not found", err)

    def write(self, what='all'):
        if what == 'basic' or what == 'all':
            with open(self.basic_words_path, "w", encoding="utf-8") as file:
                json.dump(sorted(self.basic_words), file, indent=4)
        if what == 'known' or what == 'all':
            with open(self.known_words_path, "w", encoding="utf-8") as file:
                json.dump(sorted(self.known_words), file, indent=4)
        if what == 'awaiting_review' or what == 'all':
            with open(self.awaiting_review_words_path, "w", encoding="utf-8") as file:
                json.dump(sorted(self.awaiting_review_words), file, indent=4)
        if what == 'other' or what == 'all':
            with open(self.other_words_path, "w", encoding="utf-8") as file:
                json.dump(sorted(self.other_words), file, indent=4)

        if what == 'reviewed' or what == 'all':
            with open(self.reviewed_words_path, "w", encoding="utf-8") as file:
                json.dump([word.get_list_data() for word in self.reviewed_words], file, indent=4)
