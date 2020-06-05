import re
from CiperOperations.auto_test import autoTest
from CiperOperations.encrypt_decrypt import encrypt_decrypt
from CiperOperations.hacker import hacker
from CipherAlgorithms.TranspositionCipher import transposition_cipher_file


def start_string():
    try:
        mode = input('--2--Enter Mode(E/D/H) here:')
        re_hacker = bool(re.match(r'(?:hacker|H)', mode, re.IGNORECASE))
        re_encrypt = bool(re.match(r'(?:E|encrypt)', mode, re.IGNORECASE))
        re_decrypt = bool(re.match(r'(?:D|decrypt)', mode, re.IGNORECASE))
        re_encrypt_decrypt = bool(re.match(r'(?:E|encrypt|D|decrypt)', mode, re.IGNORECASE))
        if re_hacker:
            # 输入
            text = input('--3--Enter plain/cipher text here:')
            encrypt_name = input('--4--Enter Encrypt function(RC/CC/TC) name:')
            extra_char = input('--5--Enter extra char need to be encrypted:')
            hacker(text, encrypt_name, extra_char)

        # choose hacker or encrypt or decrypt
        if re_encrypt_decrypt:
            if re_encrypt:
                mode = 'encrypt'
            if re_decrypt:
                mode = 'decrypt'

            text = input('--3--Enter plain/cipher text here:')
            encrypt_name = input('--4--Enter Encrypt function(RC/CC/TC) name:')
            extra_char = input('--5--Enter extra char need to be encrypted:')
            # process key
            key = input('--6--Enter key here:')
            try:
                key = int(key)
            except Exception as e:
                key = str(key)
            encrypt_decrypt(text, encrypt_name, mode=mode, key=key, extrachar=extra_char)
    except Exception as e:
        print(e)


def start_file():
    inputFile = input('--2--Enter File name need to be encrypted/decrypted:')
    outputFile = input('--3--Enter Output File name:')
    key = input('--4--Enter key:')
    try:
        key = int(key)
    except Exception:
        key = str(key)
    mode = input('--5--Enter mode(encrypt/decrypt):')
    transposition_cipher_file(inputFile, outputFile, key=key, mode=mode)


def main():
    tmode = input('--0--Enter Testing mode(Manual/Auto):')
    if tmode == 'Manual':
        things = input('--1--Enter encrypt object(String/File):')
        if things.lower().startswith('string'):
            start_string()
        elif things.lower().startswith('file'):
            start_file()
    elif tmode == 'Auto':
        times = int(input('--1--Enter test times:'))
        for i in range(times):
            print(f'----Test {i}----')
            autoTest()
    else:
        print('Please enter "Manual" or "Auto"')


if __name__ == '__main__':
    main()
