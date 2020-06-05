import math
import os
import sys
import time


def transposition_cipher(message, **kwargs):
    """
    :param message: plaintext
    :param kwargs: key=0 / mode=encrypt
    :return: ciphertext,len(ciphertext)
    """

    if kwargs:
        key = kwargs.get('key')
        mode = kwargs.get('mode')
    else:
        key, mode = 0, 'encrypt'
    # 加密
    if mode == 'encrypt':
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
    # 解密
    elif mode == 'decrypt':
        if key != 0 and key is not None and key != '':
            return decryptTC(message, int(key)), len(decryptTC(message, key))
        rst = []
        for possible_key in range(2, len(message)):
            rst.append(decryptTC(message, possible_key))
        return rst, len(rst)


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


def transposition_cipher_file(inputFile, outputFile, **kwargs):
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
    text, text_length = transposition_cipher(content, key=kwargs.get('key', 0), mode=kwargs.get('mode', 'encrypt'))
    totaltime = round(time.time() - starttime, 2)
    fileObj2 = open(outputFile, 'w')
    fileObj2.write(text)
    fileObj2.close()
    print(f'{kwargs.get("mode")} Succeed, Time Consumption:{totaltime}')
