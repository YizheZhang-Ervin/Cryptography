import os
import sys
import time

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def string_process(processType, message, key):
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
