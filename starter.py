import re
from CiperOperations.auto_test import autoTest
from CiperOperations.encrypt_decrypt import encrypt_decrypt
from CiperOperations.hacker import hacker


def start():
    try:
        mode = input('--1--Enter Mode(E/D/H) here:')
        re_hacker = bool(re.match(r'(?:hacker|H)', mode, re.IGNORECASE))
        re_encrypt = bool(re.match(r'(?:E|encrypt)', mode, re.IGNORECASE))
        re_decrypt = bool(re.match(r'(?:D|decrypt)', mode, re.IGNORECASE))
        re_encrypt_decrypt = bool(re.match(r'(?:E|encrypt|D|decrypt)', mode, re.IGNORECASE))
        if re_hacker:
            # 输入
            text = input('--2--Enter plain/cipher text here:')
            encrypt_name = input('--3--Enter Encrypt function(RC/CC/TC) name:')
            extra_char = input('--4--Enter extra char need to be encrypted:')
            hacker(text, encrypt_name, extra_char)

        # choose hacker or encrypt or decrypt
        if re_encrypt_decrypt:
            if re_encrypt:
                mode = 'encrypt'
            if re_decrypt:
                mode = 'decrypt'

            text = input('--2--Enter plain/cipher text here:')
            encrypt_name = input('--3--Enter Encrypt function(RC/CC/TC) name:')
            extra_char = input('--4--Enter extra char need to be encrypted:')
            # process key
            key = input('--5--Enter key here:')
            try:
                key = int(key)
            except Exception as e:
                key = str(key)
            encrypt_decrypt(text, encrypt_name, mode=mode, key=key, extrachar=extra_char)
    except Exception as e:
        print(e)


def main():
    tmode = input('Enter Testing mode(Manual/Auto):')
    if tmode == 'Manual':
        start()
    elif tmode == 'Auto':
        times = int(input('Enter test times:'))
        for i in range(times):
            print(f'----Test {i}----')
            autoTest()
    else:
        print('Please enter "Manual" or "Auto"')


if __name__ == '__main__':
    main()
