import time
import math

class BasicWord:
    def __init__(self, word):
        self.word = word


class ReviewedWord:

    min_difficulty = 0
    max_difficulty = 5

    def __init__(self, word, count=0, last_date=time.time(), difficulty=0):
        self.word = word.lower()
        self.count = count
        self.last_date = last_date
        self.difficulty = max(min(difficulty, ReviewedWord.max_difficulty), ReviewedWord.min_difficulty)

    def set_difficulty(self, difficulty):
        self.difficulty = max(min(difficulty, ReviewedWord.max_difficulty), ReviewedWord.min_difficulty)

    def update_data(self):
        self.count += 1
        self.last_date = time.time()

    def get_str_data(self):
        return f"{self.word}; {self.count}; {self.last_date}; {self.difficulty};"

    def get_list_data(self):
        return [self.word, self.count, self.last_date, self.difficulty]

    def __str__(self):
        return f"Word: {self.word}; Repeated amount: {self.count}; Difficulty: {self.difficulty}\n" \
               f"Last repeated on {time.asctime(time.localtime(self.last_date))}"