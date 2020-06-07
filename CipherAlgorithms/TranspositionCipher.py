import math
import os
import sys
import time
from CiperOperations.check_ifenglish import check_ifenglish


def decryptTC(message, possible_key):
    # abcdefghi -- adgbehcfi
    # abc --  adg
    # def --  beh
    # ghi --  cfi
    # 列数=明文长度/密钥长度
    cols = int(math.ceil(len(message) / float(possible_key)))
    # 行数=密钥长度
    rows = possible_key
    # 多余空格数 = 行列之和-明文长度
    cutboxs = (cols * rows) - len(message)
    plaintext = [''] * cols
    r, c = 0, 0
    # 按列取
    for m in message:
        plaintext[c] += m
        c += 1
        # 除首行外第一行开头 or 行末尾且当前行>满格的行数(即是否在多余的空格里)
        if c == cols or (c == cols - 1 and r >= rows - cutboxs):
            c = 0
            r += 1
    return ''.join(plaintext)


def string_process(processType, message, key):
    # 加密
    if processType.upper().startswith('E'):
        result_mes = [''] * key
        for column in range(key):
            index_mes = column
            while index_mes < len(message):
                # 原内容按列存入result_mes
                result_mes[column] += message[index_mes]
                # 原内容每行key个
                index_mes += key
        rst = ''.join(result_mes)
        return rst, len(rst)
    # 解密(已知key进行decrypt)
    elif processType.upper().startswith('D'):
        if key != 0 and key is not None and key != '':
            return decryptTC(message, int(key)), len(decryptTC(message, key))
    # 暴力穷举破解(乱猜key进行hacker)
    elif processType.upper().startswith('H'):
        rst = []
        for possible_key in range(1, len(message)):
            de_text = decryptTC(message, possible_key)
            rst.append(de_text)
            if check_ifenglish(de_text):
                choice = input('Find possible result, Stop decrypt?(Y/N)')
                if choice.lower().startswith('y'):
                    return de_text, 1
        return rst, len(rst)


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


def transpositionCipher(objType, processType, **kwargs):
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
