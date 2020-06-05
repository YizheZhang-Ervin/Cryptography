import random
from CiperOperations.hacker import hacker_caesar
from CipherAlgorithms import ReverseCipher, TranspositionCipher, CaesarCipher


def autoTest():
    # random message
    random.seed(42)
    # truly random: random.SystemRandom.randint()
    message = list((''.join([chr(a) for a in range(65, 91)])
                    + ''.join([chr(a) for a in range(97, 123)])
                    + ''.join([chr(i) for i in range(48, 58)])) * random.randint(4, 40))
    random.shuffle(message)
    message = ''.join(message)
    # random keys
    tc_key = random.randint(2, len(message))

    # 倒置密码
    ciphertext1, l11 = ReverseCipher.reverse_cipher(message=message, mode='encrypt')
    plaintext1, l12 = ReverseCipher.reverse_cipher(message=ciphertext1, mode='decrypt')
    if message == plaintext1:
        print('ReverseCipher Succeed')
    else:
        print('ReverseCipher Fail')

    # 凯撒密码
    allowedchar = ''.join([chr(a) for a in range(65, 91)]) \
                  + ''.join([chr(a) for a in range(97, 123)]) \
                  + ''.join([chr(i) for i in range(48, 58)])
    ciphertext2, l21 = CaesarCipher.caesar_cipher(message=message, key=len(allowedchar), mode='encrypt')
    plaintext21, l21 = CaesarCipher.caesar_cipher(message=ciphertext2, key=len(allowedchar), mode='decrypt')
    plaintext22, l22 = hacker_caesar(message=ciphertext2)
    if message in plaintext22[0] and message == plaintext21:
        print('CaesarCipher Succeed')
    else:
        print('CaesarCipher Fail')

    # 错位密码
    ciphertext3, l31 = TranspositionCipher.transposition_cipher(message=message, key=tc_key, mode='encrypt')
    plaintext3, l32 = TranspositionCipher.transposition_cipher(message=ciphertext3, key=tc_key, mode='decrypt')
    if message in plaintext3:
        print('TranspositionCipher Succeed')
    else:
        print('TranspositionCipher Fail')
