# cipher wheel
import os
import sys
import time


def string_process(processType, message, allowedchar, key):
    if processType.upper().startswith('E') or processType.upper().startswith('D'):
        result_mes = ''
        for mes in message:
            if mes in allowedchar:
                mes_index = allowedchar.find(mes)
                newmes_index = 0
                if processType.upper().startswith('E'):
                    newmes_index = mes_index + key
                elif processType.upper().startswith('D'):
                    newmes_index = mes_index - key
                if newmes_index >= len(allowedchar):
                    newmes_index -= len(allowedchar)
                elif newmes_index < 0:
                    newmes_index += len(allowedchar)
                result_mes += allowedchar[newmes_index]
            else:
                result_mes += mes
        return result_mes, len(result_mes)
    elif processType.upper().startswith('H'):
        result_collection = []
        index = 0
        for k in range(len(allowedchar)):
            result = ''
            for mes in message:
                if mes in allowedchar:
                    mes_index = allowedchar.find(mes)
                    mes_index -= k
                    if mes_index < 0:
                        mes_index += len(allowedchar)
                    result += allowedchar[mes_index]
                else:
                    result += mes
            result_collection.append((result, 'key=' + str(index)))
            index += 1
        return result_collection, len(result_collection)


def file_process(processType, inputFile, outputFile, allowedchar, key):
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
    text, text_length = string_process(processType, content, allowedchar, key)
    totaltime = round(time.time() - starttime, 3)
    fileObj2 = open(outputFile, 'w')
    fileObj2.write(text)
    fileObj2.close()
    return totaltime


def caesarCipher(objType, processType, **kwargs):
    """
        :param objType: String/File
        :param processType: Encrypt/Decrypt/Hacker
        :param kwargs: message/key
        :return: text,length
    """

    # Default values
    message, inputFile, outputFile, key = '', '', '', 0
    allowedchar = ''.join([chr(a) for a in range(65, 91)]) \
                  + ''.join([chr(a) for a in range(97, 123)]) \
                  + ''.join([chr(i) for i in range(48, 58)])

    # Enter values
    if kwargs:
        message = kwargs.get('message')
        key = int(kwargs.get('key'))
    else:
        if objType.upper().startswith('S'):
            message = input('Enter Message:')
        if objType.upper().startswith('F'):
            inputFile = input('Enter InputFile:')
            outputFile = input('Enter OutputFile:')
        # encrypt & decrypt
        if not processType.upper().startswith('H'):
            key = int(input('Enter key (positive integer):'))
        extrachar = input('Enter extra characters:')
        allowedchar += extrachar

    # String
    if objType.upper().startswith('S'):
        return string_process(processType, message, allowedchar, key)

    # File
    elif objType.upper().startswith('F'):
        if processType.upper().startswith('E'):
            return 'Encrypt Succeed', file_process('E', inputFile, outputFile, allowedchar, key)
        elif processType.upper().startswith('D'):
            return 'Decrypt Succeed', file_process('D', inputFile, outputFile, allowedchar, key)
        elif processType.upper().startswith('H'):
            return 'Hacker Succeed', file_process('H', inputFile, outputFile, allowedchar, key)
        else:
            sys.exit('Enter Encrypt / Decrypt / Hacker')
    else:
        sys.exit('Enter String / File')
