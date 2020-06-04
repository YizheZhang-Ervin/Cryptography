import re
from CiperOperations.encrypt_decrypt import encrypt_decrypt
from CiperOperations.hacker import hacker


def main():
    try:
        # enter things
        text = input('--1--Enter plain/cipher text here:')
        encrypt_name = input('--2--Enter Encrypt function(RC/CC/TC) name:')
        mode = input('--3--Enter Mode(E/D/H) here:')
        extra_char = input('--4--Enter extra char need to be encrypted:')

        # choose hacker or encrypt or decrypt
        if bool(re.match(r'(?:hacker|H)', mode, re.IGNORECASE)):
            mode = 'hacker'
            hacker(text, encrypt_name, extra_char)

        elif bool(re.match(r'(?:E|encrypt|D|decrypt)', mode, re.IGNORECASE)):
            if bool(re.match(r'(?:E|encrypt)', mode, re.IGNORECASE)):
                mode = 'encrypt'
            elif bool(re.match(r'(?:D|decrypt)', mode, re.IGNORECASE)):
                mode = 'decrypt'

            # process key
            key = input('--5--Enter key here:')
            try:
                key = int(key)
            except Exception as e:
                key = str(key)
            encrypt_decrypt(text, encrypt_name, mode=mode, key=key, extrachar=extra_char)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
