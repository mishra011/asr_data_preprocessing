import shutil
import re
import num2words

def transInt(num, mode=None):
    # Changes the mode of the translation to 
    # correctly translate ordinal numbers.
    if mode:
        mode = "ordinal"
    else:
        mode = "cardinal"

    # translates the number to either float
    # or int, so the translation works correctly.
    if "." in num:
        num = float(num)
    else:
        num = int(num)
    return num2words.num2words(num, to=mode)

def replaceInt(string):
    # Matches numbers, followed by optional ordinal-characters after it.
    return re.sub(r"(\d+\.*\d*)(st|nd|rd|th)*", lambda x: transInt(*x.groups()), string)

# word = 'so do 1st or do 2nd or 3rd byte 4th so do 5th longest word 3765 word 50 but 7th'
# word = "hi there"
# print(word)
# print(replaceInt(word))