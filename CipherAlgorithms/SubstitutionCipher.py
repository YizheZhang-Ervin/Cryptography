import os
import random
import sys
import time

letterList = [chr(a) for a in range(65, 91)]
letterStr = ''.join(letterList)


def checkKeyValid(key):
    keyList = list(key)
    return sorted(keyList) == sorted(letterList)


def getRandomKey():
    random.shuffle(letterList)
    return ''.join(letterList)


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
        pass


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
        :param kwargs: flag/message/key
        :return: text,length
    """

    if kwargs:
        flag = kwargs.get('flag')
    else:
        flag = 'normal'
    # inputs
    key = 0
    if not flag.upper().startswith('T'):
        if not processType.upper().startswith('H'):
            key = input('Enter key (positive integer):')
            if key.upper().startswith('R'):
                key = getRandomKey()
                print(f'Generated random key:{key}')
    # String
    if objType.upper().startswith('S'):
        if flag.upper().startswith('T'):
            message = kwargs.get('message')
            key = kwargs.get('key')
        else:
            message = input('Enter Message:')
        return string_process(processType, message, key)

    # File
    elif objType.upper().startswith('F'):
        inputFile = input('Enter InputFile:')
        outputFile = input('Enter OutputFile:')
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