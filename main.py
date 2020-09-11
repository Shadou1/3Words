import consoleio
import dataio

dio = dataio.DataIO("data/basic_words.json",
                    "data/known_words.json",
                    "data/reviewed_words.json",
                    "data/awaiting_review_words.json",
                    "data/other_words.json")
dio.read()

consoleio.initiate(dio)
consoleio.start_console()
