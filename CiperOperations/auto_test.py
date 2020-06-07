import random
from CipherAlgorithms import ReverseCipher, TranspositionCipher, CaesarCipher, AffineCipher, SubstitutionCipher, \
    VigenereCipher


def autoTest():
    # random message
    random.seed(42)
    # truly random: random.SystemRandom.randint()
    allowedchar = ''.join([chr(a) for a in range(65, 91)]) \
                  + ''.join([chr(a) for a in range(97, 123)]) \
                  + ''.join([chr(i) for i in range(48, 58)])
    message = list(allowedchar) * random.randint(4, 40)
    random.shuffle(message)
    message = ''.join(message)
    # random keys
    digits_key = random.randint(2, len(allowedchar))
    words_key = ''.join([chr(random.randint(65, 90)) for i in range(random.randint(1, 50))])

    # 倒置密码
    ciphertext1, l11 = ReverseCipher.reverseCipher('String', 'Encrypt', message=message)
    plaintext1, l12 = ReverseCipher.reverseCipher('String', 'Decrypt', message=ciphertext1)
    if message == plaintext1:
        print('ReverseCipher Succeed')
    else:
        print('ReverseCipher Fail')

    # 凯撒密码
    allowedchar = ''.join([chr(a) for a in range(65, 91)]) \
                  + ''.join([chr(a) for a in range(97, 123)]) \
                  + ''.join([chr(i) for i in range(48, 58)])
    ciphertext2, l21 = CaesarCipher.caesarCipher('String', 'Encrypt', message=message, key=digits_key)
    plaintext2, l22 = CaesarCipher.caesarCipher('String', 'Decrypt', message=ciphertext2, key=digits_key)
    if message == plaintext2:
        print('CaesarCipher Succeed')
    else:
        print('CaesarCipher Fail')

    # 错位密码
    ciphertext3, l31 = TranspositionCipher.transpositionCipher('String', 'Encrypt', message=message, key=digits_key)
    plaintext3, l32 = TranspositionCipher.transpositionCipher('String', 'Decrypt', message=ciphertext3, key=digits_key)
    if message == plaintext3:
        print('TranspositionCipher Succeed')
    else:
        print('TranspositionCipher Fail')

    # 仿射密码(需要手动测试)
    print('AffineCipher need to be tested manually')
    # ciphertext4, l41 = AffineCipher.affineCipher('String', 'Encrypt', message=message, key='R')
    # plaintext4, l42 = AffineCipher.affineCipher('String', 'Decrypt', message=ciphertext4, key='R')
    # if message == plaintext4:
    #     print('AffineCipher Succeed')
    # else:
    #     print('AffineCipher Fail')

    # 代换密码
    print('SubstitutionCipher need to be tested manually')
    # ciphertext5, l51 = SubstitutionCipher.substitutionCipher('String', 'Encrypt', message=message, key='R')
    # plaintext5, l52 = SubstitutionCipher.substitutionCipher('String', 'Decrypt', message=ciphertext5, key='R')
    # if message == plaintext5:
    #     print('SubstitutionCipher Succeed')
    # else:
    #     print('SubstitutionCipher Fail')

    # 维吉尼亚密码
    ciphertext6, l61 = VigenereCipher.vigenereCipher('String', 'Encrypt', message=message, key='R')
    plaintext6, l62 = VigenereCipher.vigenereCipher('String', 'Decrypt', message=ciphertext6, key='R')
    if message == plaintext6:
        print('VigenereCipher Succeed')
    else:
        print('VigenereCipher Fail')