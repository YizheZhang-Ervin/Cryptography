from CipherAlgorithms import ReverseCipher, CaesarCipher, TranspositionCipher
import re


def encrypt_decrypt(plain_text, encrypt_name, **kwargs):
    ed_mode = kwargs.get('mode')
    ed_key = kwargs.get('key')
    ed_extrachar = kwargs.get('extrachar')
    cipher_text, text_length = encryptChoice(encrypt_name, plain_text, mode=ed_mode, key=ed_key, extrachar=ed_extrachar)
    print(f'------Cipher Text:{cipher_text}, Text Length:{text_length}')


def encryptChoice(name, plaintext, **kwargs):
    ed_mode = kwargs.get('mode')
    ed_key = kwargs.get('key')
    ed_extrachar = kwargs.get('extrachar')

    if name == 'ReverseCipher' or bool(re.match(r'[R][C]', name, re.IGNORECASE)):
        return ReverseCipher.reverse_cipher(message=plaintext, mode=ed_mode)
    elif name == 'CaesarCipher' or bool(re.match(r'[C][C]', name, re.IGNORECASE)):
        return CaesarCipher.caesar_cipher(message=plaintext, key=ed_key, mode=ed_mode, extrachar=ed_extrachar)
    elif name == 'TranspositionCipher' or bool(re.match(r'[T][C]', name, re.IGNORECASE)):
        return TranspositionCipher.transposition_cipher(message=plaintext, key=ed_key, mode=ed_mode)



