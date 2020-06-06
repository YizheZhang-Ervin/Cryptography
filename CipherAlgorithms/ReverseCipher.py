import os
import sys
import time


def file_process(processType, inputFile, outputFile):
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
    text, text_length = string_process(processType, content)
    totaltime = round(time.time() - starttime, 3)
    fileObj2 = open(outputFile, 'w')
    fileObj2.write(text)
    fileObj2.close()
    return totaltime


def string_process(processType, message):
    if processType.upper().startswith('E'):
        return message[::-1], len(message[::-1])
    elif processType.upper().startswith('D'):
        return message[::-1], len(message[::-1])
    elif processType.upper().startswith('H'):
        return message[::-1], len(message[::-1])


def reverseCipher(objType, processType, **kwargs):
    """
    :param objType: String/File
    :param processType: Encrypt/Decrypt/Hacker
    :return: text,length
    """

    if kwargs:
        flag = kwargs.get('flag')
    else:
        flag = 'normal'
    # String
    if objType.upper().startswith('S'):
        if flag.upper().startswith('T'):
            message = kwargs.get('message')
        else:
            message = input('Enter Message:')
        return string_process(processType, message)

    # File
    elif objType.upper().startswith('F'):
        inputFile = input('Enter InputFile:')
        outputFile = input('Enter OutputFile:')
        if processType.upper().startswith('E'):
            return 'Encrypt Succeed', file_process('E', inputFile, outputFile)
        elif processType.upper().startswith('D'):
            return 'Decrypt Succeed', file_process('D', inputFile, outputFile)
        elif processType.upper().startswith('H'):
            return 'Hacker Succeed', file_process('H', inputFile, outputFile)
