import random
import shutil

import getkey

import dataio
from parsers.scpparser import SCPWordsParser

commands = {}
scpwp = SCPWordsParser()


def initiate(dh: dataio.DataIO):
    global data_handler
    data_handler = dh


def add_command(*names):
    def inner(command):
        for name in names:
            commands[name] = command
        return command

    return inner


@add_command("help")
def help(*args):
    print(*commands.keys(), sep=", ")


@add_command("print_word", "print")
def print_word(*args):
    if args:
        print(data_handler.get_reviewed_word(args[0]))
    else:
        print(random.choice(data_handler.reviewed_words))


@add_command("add_reviewed_word", "addrw")
def add_reviewed_word(*args):
    if len(args):
        data_handler.add_reviewed_word(args[0])
        data_handler.write('reviewed')
        if args[0] in data_handler.awaiting_review_words:
            data_handler.awaiting_review_words.remove(args[0])
            data_handler.write('awaiting_review')
    else:
        print("No word supplied.")


@add_command("add_awaiting_word", "addaw")
def add_awaiting_word(*args):
    if len(args):
        data_handler.add_awaiting_review_word(args[0])
        data_handler.write('awaiting_review')
    else:
        print("No word supplied.")

@add_command("extract_words", "extract")
def extract_words(*args):
    if not args:
        print("please supply site and additional info")
        return

    if args[0] == 'scp':
        if len(args) > 1:
            scp_num = args[1] or random.randint(1, 5000)
        else:
            scp_num = random.randint(1, 5000)

        scp_num = '{:0>3}'.format(scp_num)

        if len(args) > 2:
            words_num = int(args[2]) or 100
        else:
            words_num = 100


        unique_words = scpwp.get_all_unique_words(scp_num)

        all_known_words = set()
        all_known_words.update(data_handler.basic_words,
                               data_handler.known_words,
                               data_handler.awaiting_review_words,
                               data_handler.other_words,
                               {word.word for word in data_handler.reviewed_words})

        unique_words -= all_known_words
        unique_words = list(unique_words)[:words_num]

        print(f"Extracting words from scp-{scp_num}")
        print("Press 'A' to add word to reviews, "
              "'B' to add word to basic words, "
              "'K' to add word to known words, "
              "and 'O' to add word to other words.")

        for word in unique_words:
            print(word)
            key = getkey.getkey()
            while key not in 'abko':
                print("please, enter 'a', 'b', 'k', or 'o'")
                key = getkey.getkey()
            if key == 'a':
                data_handler.add_awaiting_review_word(word)
            elif key == 'b':
                data_handler.add_basic_word(word)
            elif key == 'k':
                data_handler.add_known_word(word)
            elif key == 'o':
                data_handler.add_other_word(word)

        data_handler.write()


@add_command("review_words", "review")
def review_words(*args):
    args = list(args) or [3]
    args[0] = int(args[0])
    num_to_review = args[0]
    if len(data_handler.awaiting_review_words) <= args[0]:
        print(f'Too much words to review, try less than {len(data_handler.awaiting_review_words) + 1}')

    words_to_review = []
    for word in data_handler.awaiting_review_words:
        words_to_review.append(word)
        num_to_review -= 1
        if num_to_review <= 0:
            break

    print("Review these words:")
    print(*words_to_review, sep=', ')
    inp = input("(enter 'ok' when done or enter 'another' to get new words)\n")
    while inp == 'another':
        words_to_review.clear()
        num_to_review = args[0]
        for word in random.sample(list(data_handler.awaiting_review_words), args[0]):
            words_to_review.append(word)
            num_to_review -= 1
            if num_to_review <= 0:
                break
        print("Review these words:")
        print(*words_to_review, sep=', ')
        inp = input("(enter 'ok' when done or enter 'another' to get new words)\n")

    if inp == "ok":
        for word in words_to_review:
            data_handler.awaiting_review_words.remove(word)
            data_handler.add_reviewed_word(word)
        data_handler.write()


@add_command("review_difficulty", "reviewd")
def review_difficulty(*args):
    args = list(args) or [30]
    args[0] = int(args[0])
    for word in data_handler.reviewed_words:
        if not word.difficulty:
            dif = int(input(f"Word: {word.word}, Difficulty: "))
            word.set_difficulty(dif)
            args[0] -= 1
        if not args[0]:
            data_handler.write("reviewed")
            print("That's it!")
            break
    else:
        print("No more 0 difficulty words")


# TODO: rewrite repeat_last and repeat_last_random to be one command with common code (getting the words table)


@add_command("repeat_last", "repeatl", "rl")
def repeat_last(*args):
    args = list(args) or [3]
    args[0] = int(args[0])
    #words = [word.word for word in data_handler.words]
    words_inc = []
    i = len(data_handler.reviewed_words) - 1
    inc = 0
    while i > 0:
        if inc == 0:
            words_inc.extend(data_handler.reviewed_words[i:i - args[0] * 3:-1])
            i -= args[0] * 4
            inc = 2
        else:
            words_inc.extend(data_handler.reviewed_words[i:i - args[0]:-1])
            i -= args[0] * (inc + 1)
            inc *= 2

    #random.shuffle(words_inc)
    print("Explain these words:")
    for i in range(0, len(words_inc), 3):
        print(*[w.word for w in words_inc[i:i + 3]])
        input()
    else:
        for w in words_inc:
            w.update_data()
        data_handler.write("reviewed")
        print("That's it!")


@add_command("repeat_last_random", "repeatlr", "rlr")
def repeat_last_random(*args):
    args = list(args) or [3]
    args[0] = int(args[0])
    #words = [word.word for word in data_handler.words]
    words_inc = []
    i = len(data_handler.reviewed_words) - 1
    inc = 0
    while i > 0:
        if inc == 0:
            words_inc.extend(data_handler.reviewed_words[i:i - args[0] * 3:-1])
            i -= args[0] * 4
            inc = 2
        else:
            words_inc.extend(data_handler.reviewed_words[i:i - args[0]:-1])
            i -= args[0] * (inc + 1)
            inc *= 2

    random.shuffle(words_inc)
    print("Explain these words:")
    for i in range(0, len(words_inc), 3):
        print(*[w.word for w in words_inc[i:i + 3]])
        input()
    else:
        for w in words_inc:
            w.update_data()
        data_handler.write("reviewed")
        print("That's it!")


@add_command("repeat_all", "repeata", "ra")
def repeat_all(*args):
    words = [word for word in data_handler.reviewed_words]
    random.shuffle(words)
    print("Explain these words:")
    for i in range(0, len(words), 3):
        print(*[word.word for word in words[i:i + 3]])
        input()
    else:
        for w in words:
            w.update_data()
        data_handler.write("reviewed")
        print("That's it!")


@add_command("repeat_least", "repeatle")
def repeat_least(*args):
    args = list(args) or [30]
    args[0] = int(args[0])
    words = sorted(data_handler.reviewed_words, key=lambda word: word.count)[:args[0]]
    random.shuffle(words)
    print("Explain these least repeated words:")
    for i in range(0, args[0], 3):
        print(*[word.word for word in words[i:i + 3]])
        input()
    else:
        for w in words:
            w.update_data()
        data_handler.write("reviewed")
        print("That's it!")


@add_command("repeat_oldest", "repeat_old", "repeato")
def repeat_oldest(*args):
    args = list(args) or [30]
    args[0] = int(args[0])
    words = sorted(data_handler.reviewed_words, key=lambda word: word.last_date)[:args[0]]
    random.shuffle(words)
    print("Explain these oldest repeated words:")
    for i in range(0, args[0], 3):
        print(*[word.word for word in words[i:i + 3]])
        input()
    else:
        for w in words:
            w.update_data()
        data_handler.write("reviewed")
        print("That's it!")

@add_command("exit", "e")
def exit_and_save(*args):
    data_handler.write()
    shutil.copy(data_handler.basic_words_path, data_handler.basic_words_path.with_suffix('.json.bac'))
    shutil.copy(data_handler.known_words_path, data_handler.known_words_path.with_suffix('.json.bac'))
    shutil.copy(data_handler.awaiting_review_words_path, data_handler.awaiting_review_words_path.with_suffix('.json.bac'))
    shutil.copy(data_handler.other_words_path, data_handler.other_words_path.with_suffix('.json.bac'))

    shutil.copy(data_handler.reviewed_words_path, data_handler.reviewed_words_path.with_suffix('.json.bac'))
    exit()


def start_console():
    while True:
        command_parts = input().split(" ")
        command_parts[0] = command_parts[0].lower().strip()
        if command_parts[0] in commands.keys():
            commands[command_parts[0]](*command_parts[1:])
        else:
            print("no such command")
