import copy
import os
import random
import sys
import time
import re

from CiperOperations import make_wordpatterns, wordPatterns

letterList = [chr(a) for a in range(65, 91)]
letterStr = ''.join(letterList)
nonLettersOrSpacePattern = re.compile(r'[^A-Z\s]')


def checkKeyValid(key):
    keyList = list(key)
    return sorted(keyList) == sorted(letterList)


def getRandomKey():
    random.shuffle(letterList)
    return ''.join(letterList)


def getBlankCipherletterMapping():
    # Returns a dictionary value that is a blank cipherletter mapping.
    return {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': [], 'K': [], 'L': [],
            'M': [], 'N': [], 'O': [], 'P': [], 'Q': [], 'R': [], 'S': [], 'T': [], 'U': [], 'V': [], 'W': [], 'X': [],
            'Y': [], 'Z': []}


def addLettersToMapping(letterMapping, cipherword, candidate):
    for i in range(len(cipherword)):
        if candidate[i] not in letterMapping[cipherword[i]]:
            letterMapping[cipherword[i]].append(candidate[i])


def intersectMappings(mapA, mapB):
    intersectedMapping = getBlankCipherletterMapping()
    for letter in letterStr:
        if not mapA[letter]:
            intersectedMapping[letter] = copy.deepcopy(mapB[letter])
        elif not mapB[letter]:
            intersectedMapping[letter] = copy.deepcopy(mapA[letter])
        else:
            for mappedLetter in mapA[letter]:
                if mappedLetter in mapB[letter]:
                    intersectedMapping[letter].append(mappedLetter)
    return intersectedMapping


def removeSolvedLettersFromMapping(letterMapping):
    loopAgain = True
    while loopAgain:
        loopAgain = False
        solvedLetters = []
        for cipherletter in letterStr:
            if len(letterMapping[cipherletter]) == 1:
                solvedLetters.append(letterMapping[cipherletter][0])
        for cipherletter in letterStr:
            for s in solvedLetters:
                if len(letterMapping[cipherletter]) != 1 and s in letterMapping[cipherletter]:
                    letterMapping[cipherletter].remove(s)
                    if len(letterMapping[cipherletter]) == 1:
                        loopAgain = True
    return letterMapping


def decryptWithCipherletterMapping(ciphertext, letterMapping):
    key = ['x'] * len(letterStr)
    for cipherletter in letterStr:
        if len(letterMapping[cipherletter]) == 1:
            keyIndex = letterStr.find(letterMapping[cipherletter][0])
            key[keyIndex] = cipherletter
        else:
            ciphertext = ciphertext.replace(cipherletter.lower(), '_')
            ciphertext = ciphertext.replace(cipherletter.upper(), '_')
    key = ''.join(key)
    return string_process('D', ciphertext, key)


def hackSimpleSub(message):
    intersectedMap = getBlankCipherletterMapping()
    cipherwordList = nonLettersOrSpacePattern.sub('', message.upper()).split()
    for cipherword in cipherwordList:
        candidateMap = getBlankCipherletterMapping()
        wordPattern = make_wordpatterns.getWordPattern(cipherword)
        if wordPattern not in wordPatterns.allPatterns:
            continue
        for candidate in wordPatterns.allPatterns[wordPattern]:
            addLettersToMapping(candidateMap, cipherword, candidate)
        intersectedMap = intersectMappings(intersectedMap, candidateMap)
    return removeSolvedLettersFromMapping(intersectedMap)


def hacker(message):
    letterMapping = hackSimpleSub(message)
    print(letterMapping)
    text, length = decryptWithCipherletterMapping(message, letterMapping)
    return text, length


def string_process(processType, message, key):
    text = ''
    charA = letterStr
    charB = key
    # encrypt / decrypt
    if processType.upper().startswith('D'):
        charA, charB = charB, charA
    if processType.upper().startswith('E') or processType.upper().startswith('D'):
        for m in message:
            if m.upper() in charA:
                index = charA.find(m.upper())
                if m.isupper():
                    text += charB[index].upper()
                else:
                    text += charB[index].lower()
            else:
                text += m
        return text, len(text)
    # hacker
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


def substitutionCipher(objType, processType, **kwargs):
    """
        :param objType: String/File
        :param processType: Encrypt/Decrypt/Hacker
        :param kwargs: message/key
        :return: text,length
    """

    # Default values
    message, inputFile, outputFile, key = '', '', '', 0

    # Enter values
    if kwargs:
        message = kwargs.get('message')
        key = kwargs.get('key')
        if processType.upper().startswith('E'):
            key = getRandomKey() if key == 'R' or len(set(key)) != 26 else key
            print(f'Now key:{key}')
    else:
        if objType.upper().startswith('S'):
            message = input('Enter Message:')
        if objType.upper().startswith('F'):
            inputFile = input('Enter InputFile:')
            outputFile = input('Enter OutputFile:')
        # encrypt & decrypt
        if not processType.upper().startswith('H'):
            key = input('Enter key (26 unique words):')
            if key.upper().startswith('R'):
                key = getRandomKey()
                print(f'Generated random key:{key}')

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
