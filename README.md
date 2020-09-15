# 3Words

> Web / Terminal application to facilitate smooth word learning.

## Features
* Keep a record of all your learned words with relevant stats
* Repeat words that you learned based on
    * How long ago did you repeated it
    * How many times did you repeated it
* Get new words to learn from different sites

If `getkey` module gives `TypeError: can only concatenate str (not "bytes") to str`, then go to `"path-to-your-virtual-environment\lib\site-packages\getkey\platforms.py" line 40` and change `buffer += c` to `buffer += str(c, 'utf-8')`.
Probably will replace `getkey` module later.