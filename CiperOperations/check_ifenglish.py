upperletters = ''.join([chr(i) for i in range(65, 91)])
lowerletters = ''.join([chr(i) for i in range(97, 123)])


def loadDictionary():
    dict = open('dictionary.txt')
    englishwords = {}
    for w in dict.read().split('\n'):
        englishwords[w] = None
    dict.close()
    return englishwords


def remove_nonletters(message):
    # remove non letters
    filtermessage = []
    for i in message:
        if str(i) in upperletters + lowerletters + ' \t\n':
            filtermessage.append(i)
    filtermessage = ''.join(filtermessage)
    return filtermessage


def count_englishwords(message):
    filtermessage = remove_nonletters(message).upper()
    words_possibile = filtermessage.split()
    if not words_possibile:
        return 0.0
    match_num = 0
    for w in words_possibile:
        if w in loadDictionary():
            match_num += 1
    return float(match_num) / len(words_possibile)


def check_ifenglish(message, given_wordpercentage=20, given_letterpercentage=85):
    words_match = count_englishwords(message) * 100 >= given_wordpercentage
    letters_num = len(remove_nonletters(message))
    letters_percentage = float(letters_num) / len(message) * 100
    letters_match = letters_percentage >= given_letterpercentage
    return words_match and letters_match
