import itertools
import os
import re
import sys
import time

from CiperOperations import frequentAnalysis, check_ifenglish

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
NUM_MOST_FREQ_LETTERS = 4
MAX_KEY_LENGTH = 16
NONLETTERS_PATTERN = re.compile('[^A-Z]')


def findRepeatSequencesSpacings(message):
    message = NONLETTERS_PATTERN.sub('', message.upper())
    seqSpacings = {}
    for seqLen in range(3, 6):
        for seqStart in range(len(message) - seqLen):
            seq = message[seqStart:seqStart + seqLen]
            for i in range(seqStart + seqLen, len(message) - seqLen):
                if message[i:i + seqLen] == seq:
                    if seq not in seqSpacings:
                        seqSpacings[seq] = []
                    seqSpacings[seq].append(i - seqStart)
    return seqSpacings


def getUsefulFactors(num):
    if num < 2:
        return []
    factors = []
    for i in range(2, MAX_KEY_LENGTH + 1):
        if num % i == 0:
            factors.append(i)
            otherFactor = int(num / i)
            if otherFactor < MAX_KEY_LENGTH + 1 and otherFactor != 1:
                factors.append(otherFactor)
    return list(set(factors))


def getItemAtIndexOne(items):
    return items[1]


def getMostCommonFactors(seqFactors):
    factorCounts = {}
    for seq in seqFactors:
        factorList = seqFactors[seq]
        for factor in factorList:
            if factor not in factorCounts:
                factorCounts[factor] = 0
            factorCounts[factor] += 1
    factorsByCount = []
    for factor in factorCounts:
        if factor <= MAX_KEY_LENGTH:
            factorsByCount.append((factor, factorCounts[factor]))
    factorsByCount.sort(key=getItemAtIndexOne, reverse=True)
    return factorsByCount


def kasiskiExamination(ciphertext):
    repeatedSeqSpacings = findRepeatSequencesSpacings(ciphertext)
    seqFactors = {}
    for seq in repeatedSeqSpacings:
        seqFactors[seq] = []
        for spacing in repeatedSeqSpacings[seq]:
            seqFactors[seq].extend(getUsefulFactors(spacing))
    factorsByCount = getMostCommonFactors(seqFactors)
    allLikelyKeyLengths = []
    for twoIntTuple in factorsByCount:
        allLikelyKeyLengths.append(twoIntTuple[0])
    return allLikelyKeyLengths


def getNthSubkeysLetters(nth, keyLength, message):
    message = NONLETTERS_PATTERN.sub('', message)
    i = nth - 1
    letters = []
    while i < len(message):
        letters.append(message[i])
        i += keyLength
    return ''.join(letters)


def attemptHackWithKeyLength(ciphertext, mostLikelyKeyLength):
    ciphertextUp = ciphertext.upper()
    allFreqScores = []
    for nth in range(1, mostLikelyKeyLength + 1):
        nthLetters = getNthSubkeysLetters(nth, mostLikelyKeyLength, ciphertextUp)
        freqScores = []
        for possibleKey in LETTERS:
            decryptedText, length = string_process('D', nthLetters, possibleKey)
            keyAndFreqMatchTuple = (possibleKey, frequentAnalysis.englishFreqMatchScore(decryptedText))
            freqScores.append(keyAndFreqMatchTuple)
        freqScores.sort(key=getItemAtIndexOne, reverse=True)
        allFreqScores.append(freqScores[:NUM_MOST_FREQ_LETTERS])
    for indexes in itertools.product(range(NUM_MOST_FREQ_LETTERS), repeat=mostLikelyKeyLength):
        possibleKey = ''
        for i in range(mostLikelyKeyLength):
            possibleKey += allFreqScores[i][indexes[i]][0]
        decryptedText,length = string_process('D', ciphertextUp, possibleKey)
        if check_ifenglish.check_ifenglish(decryptedText):
            origCase = []
            for i in range(len(ciphertext)):
                if ciphertext[i].isupper():
                    origCase.append(decryptedText[i].upper())
                else:
                    origCase.append(decryptedText[i].lower())
            decryptedText = ''.join(origCase)

            print('Possible encryption hack with key %s:' % (possibleKey))
            print(decryptedText[:200])
            print('Enter S if done, anything else to continue hacking:')
            response = input('> ')
            if response.strip().upper().startswith('D'):
                return decryptedText
    return None


def hackVigenere(ciphertext):
    allLikelyKeyLengths = kasiskiExamination(ciphertext)
    hackedMessage = None
    for keyLength in allLikelyKeyLengths:
        hackedMessage = attemptHackWithKeyLength(ciphertext, keyLength)
        if hackedMessage is not None:
            break
    if hackedMessage is None:
        for keyLength in range(1, MAX_KEY_LENGTH + 1):
            if keyLength not in allLikelyKeyLengths:
                hackedMessage = attemptHackWithKeyLength(ciphertext, keyLength)
                if hackedMessage is not None:
                    break
    return hackedMessage


def hacker(message):
    hackedMessage = hackVigenere(message)
    if hackedMessage is not None:
        return hackedMessage, len(hackedMessage)
    else:
        print('Failed to hack encryption.')


def string_process(processType, message, key):
    if processType.upper().startswith('E') or processType.upper().startswith('D'):
        translated = []
        keyIndex = 0
        key = key.upper()
        for symbol in message:
            num = LETTERS.find(symbol.upper())
            if num != -1:
                if processType.upper().startswith('E'):
                    num += LETTERS.find(key[keyIndex])
                elif processType.upper().startswith('D'):
                    num -= LETTERS.find(key[keyIndex])
                num %= len(LETTERS)
                if symbol.isupper():
                    translated.append(LETTERS[num])
                elif symbol.islower():
                    translated.append(LETTERS[num].lower())
                keyIndex += 1
                if keyIndex == len(key):
                    keyIndex = 0
            else:
                translated.append(symbol)
        return ''.join(translated), len(''.join(translated))
    elif processType.upper().startswith('H'):
        return hacker(message)


def file_process(processType, inputFile, outputFile, key):
    if not os.path.exists(inputFile):
        print('Input File not exists')
        sys.exit()
    if os.path.exists(outputFile):
        choice = input('Output File exists, Overwrite it?(Y/N)')
        if not choice.lower().startswith('y'):
            sys.exit()
    fileObj = open(inputFile)
    content = fileObj.read()
    fileObj.close()
    starttime = time.time()
    text, text_length = string_process(processType, content, key)
    totaltime = round(time.time() - starttime, 3)
    fileObj2 = open(outputFile, 'w')
    fileObj2.write(text)
    fileObj2.close()
    return totaltime


def vigenereCipher(objType, processType, **kwargs):
    """
        :param objType: String/File
        :param processType: Encrypt/Decrypt/Hacker
        :param kwargs: message/key
        :return: text,length
    """

    # Default values
    message, inputFile, outputFile, key = '', '', '', ''

    if kwargs:
        message = kwargs.get('message')
        key = kwargs.get('key')
    else:
        if objType.upper().startswith('S'):
            message = input('Enter Message:')
        if objType.upper().startswith('F'):
            inputFile = input('Enter InputFile:')
            outputFile = input('Enter OutputFile:')
        # encrypt & decrypt
        if not processType.upper().startswith('H'):
            key = input('Enter key (words):')

    # String
    if objType.upper().startswith('S'):
        return string_process(processType, message, key)

    # File
    elif objType.upper().startswith('F'):
        if processType.upper().startswith('E'):
            return 'Encrypt Succeed', file_process('E', inputFile, outputFile, key)
        elif processType.upper().startswith('D'):
            return 'Decrypt Succeed', file_process('D', inputFile, outputFile, key)
        elif processType.upper().startswith('H'):
            return 'Hacker Succeed', file_process('H', inputFile, outputFile, key)
        else:
            sys.exit('Enter Encrypt / Decrypt / Hacker')
    else:
        sys.exit('Enter String / File')
