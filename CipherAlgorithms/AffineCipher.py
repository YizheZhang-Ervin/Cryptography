import os
import random
import sys
import time


def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b


def findModInverse(a, m):
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


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
        pass


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
        :return: text,length
    """

    if kwargs:
        flag = kwargs.get('flag')
    else:
        flag = 'normal'
    # initial
    allowedchar = ''.join([chr(a) for a in range(65, 91)]) \
                  + ''.join([chr(a) for a in range(97, 123)]) \
                  + ''.join([chr(i) for i in range(48, 58)])
    # inputs
    key, keyA, keyB = 0, 0, 0
    if not flag.upper().startswith('T'):
        if not processType.upper().startswith('H'):
            key = input('Enter key (positive integer):')
            if key.upper().startswith('R'):
                key = getRandomKey(allowedchar)
            else:
                key = int(key)
            keyA, keyB = split2Keys(key, allowedchar)
            while not checkKeys(keyA, keyB, 'encrypt', allowedchar):
                key = getRandomKey(allowedchar)
                keyA, keyB = split2Keys(key, allowedchar)
            print(f'Auto generate Random key:{key}')
        extrachar = input('Enter extra characters:')
        allowedchar += extrachar
    # String
    if objType.upper().startswith('S'):
        if flag.upper().startswith('T'):
            message = kwargs.get('message')
            if processType.upper().startswith('E'):
                while True:
                    key = getRandomKey(allowedchar)
                    keyA, keyB = split2Keys(key, allowedchar)
                    if checkKeys(keyA, keyB, 'encrypt', allowedchar):
                        break
                text, length = string_process(processType, message, allowedchar, keyA, keyB)
                return text, length, key
            elif processType.upper().startswith('D'):
                key = kwargs.get('key')
                keyA, keyB = split2Keys(key, allowedchar)
                return string_process(processType, message, allowedchar, keyA, keyB)
        else:
            message = input('Enter Message:')
        return string_process(processType, message, allowedchar, keyA, keyB)

    # File
    elif objType.upper().startswith('F'):
        inputFile = input('Enter InputFile:')
        outputFile = input('Enter OutputFile:')
        if processType.upper().startswith('E'):
            return 'Encrypt Succeed', file_process('E', inputFile, outputFile, allowedchar, keyA, keyB)
        elif processType.upper().startswith('D'):
            return 'Decrypt Succeed', file_process('D', inputFile, outputFile, allowedchar, keyA, keyB)
        elif processType.upper().startswith('H'):
            return 'Hacker Succeed', file_process('H', inputFile, outputFile, allowedchar, keyA, keyB)