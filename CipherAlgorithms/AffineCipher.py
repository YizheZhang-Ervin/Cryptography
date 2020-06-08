import os
import random
import sys
import time

from CiperOperations.check_ifenglish import check_ifenglish
from CiperOperations.cryptMath import gcd, findModInverse


def getRandomKey(allowedchar):
    while True:
        keyA, keyB = random.randint(2, len(allowedchar)), random.randint(2, len(allowedchar))
        if gcd(keyA, len(allowedchar)) == 1:
            return keyA * len(allowedchar) + keyB


def split2Keys(key, allowedchar):
    keyA = key // len(allowedchar)
    keyB = key % len(allowedchar)
    return keyA, keyB


def checkKeys(keyA, keyB, mode, allowedchar):
    if keyA == 1 and mode == 'encrypt':
        print('Weak keyA')
        return False
    elif keyB == 0 and mode == 'encrypt':
        print('Weak keyB')
        return False
    elif keyA < 0 or keyB < 0 or keyB > len(allowedchar) - 1:
        print('Key should > 0 ')
        return False
    elif gcd(keyA, len(allowedchar)) != 1:
        print('keyA,keyB invalid')
        return False
    else:
        return True


def string_process(processType, message, allowedchar, keyA, keyB):
    # encrypt
    if processType.upper().startswith('E'):
        ciphertext = ''
        for m in message:
            if m in allowedchar:
                index = allowedchar.find(m)
                ciphertext += allowedchar[(index * keyA + keyB) % len(allowedchar)]
            else:
                ciphertext += m
        return ciphertext, len(ciphertext)
    # decrypt
    elif processType.upper().startswith('D'):
        plaintext = ''
        modeInverseOfKeyA = findModInverse(keyA, len(allowedchar))
        for m in message:
            if m in allowedchar:
                index = allowedchar.find(m)
                plaintext += allowedchar[(index - keyB) * modeInverseOfKeyA % len(allowedchar)]
            else:
                plaintext += m
        return plaintext, len(plaintext)
    elif processType.upper().startswith('H'):
        rst_set = []
        for k in range(len(allowedchar) ** 2):
            keyA, keyB = split2Keys(k, allowedchar)
            if gcd(keyA, len(allowedchar)) != 1:
                continue
            text = string_process('D', message, allowedchar, keyA, keyB)
            rst_set.append(text)
            if check_ifenglish(text):
                choice = input('Find possible result, Stop decrypt?(Y/N)')
                if choice.lower().startswith('y'):
                    return text, 1
        return rst_set, len(rst_set)


def file_process(processType, inputFile, outputFile, allowedchar, keyA, keyB):
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
    text, text_length = string_process(processType, content, allowedchar, keyA, keyB)
    totaltime = round(time.time() - starttime, 3)
    fileObj2 = open(outputFile, 'w')
    fileObj2.write(text)
    fileObj2.close()
    return totaltime


def affineCipher(objType, processType, **kwargs):
    """
        :param objType: String/File
        :param processType: Encrypt/Decrypt/Hacker
        :param kwargs: message/key
        :return: text,length
    """

    # Default values
    message, inputFile, outputFile, key, keyA, keyB = '', '', '', 0, 0, 0
    allowedchar = ''.join([chr(a) for a in range(65, 91)]) \
                  + ''.join([chr(a) for a in range(97, 123)]) \
                  + ''.join([chr(i) for i in range(48, 58)])

    # Enter values
    if kwargs:
        message = kwargs.get('message')
        key = kwargs.get('key')
        if processType.upper().startswith('E'):
            key = int(key) if key != 'R' else getRandomKey(allowedchar)
            print(f'Now key:{key}')
    else:
        if objType.upper().startswith('S'):
            message = input('Enter Message:')
        if objType.upper().startswith('F'):
            inputFile = input('Enter InputFile:')
            outputFile = input('Enter OutputFile:')
        # encrypt & decrypt
        if not processType.upper().startswith('H'):
            key = input('Enter key (positive integer):')
            # encrypt
            if processType.upper().startswith('E'):
                if key.upper().startswith('R'):
                    key = getRandomKey(allowedchar)
                    print(f'Auto generate Random key:{key}')
                else:
                    key = int(key)
        extrachar = input('Enter extra characters:')
        allowedchar += extrachar
    # check if enter invalid key
    keyA, keyB = split2Keys(key, allowedchar)
    while not checkKeys(keyA, keyB, 'encrypt', allowedchar):
        key = getRandomKey(allowedchar)
        keyA, keyB = split2Keys(key, allowedchar)
    print(f'Auto generate Random key:{key}')

    # String
    if objType.upper().startswith('S'):
        return string_process(processType, message, allowedchar, keyA, keyB)

    # File
    elif objType.upper().startswith('F'):
        if processType.upper().startswith('E'):
            return 'Encrypt Succeed', file_process('E', inputFile, outputFile, allowedchar, keyA, keyB)
        elif processType.upper().startswith('D'):
            return 'Decrypt Succeed', file_process('D', inputFile, outputFile, allowedchar, keyA, keyB)
        elif processType.upper().startswith('H'):
            return 'Hacker Succeed', file_process('H', inputFile, outputFile, allowedchar, keyA, keyB)
        else:
            sys.exit('Enter Encrypt / Decrypt / Hacker')
    else:
        sys.exit('Enter String / File')
