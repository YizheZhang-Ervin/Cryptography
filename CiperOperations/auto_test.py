import random
from CipherAlgorithms import ReverseCipher, TranspositionCipher, CaesarCipher, AffineCipher


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
    tc_key = random.randint(2, len(allowedchar))

    # 倒置密码
    ciphertext1, l11 = ReverseCipher.reverseCipher('String', 'Encrypt', message=message, flag='Test')
    plaintext1, l12 = ReverseCipher.reverseCipher('String', 'Decrypt', message=ciphertext1, flag='Test')
    if message == plaintext1:
        print('ReverseCipher Succeed')
    else:
        print('ReverseCipher Fail')

    # 凯撒密码
    allowedchar = ''.join([chr(a) for a in range(65, 91)]) \
                  + ''.join([chr(a) for a in range(97, 123)]) \
                  + ''.join([chr(i) for i in range(48, 58)])
    ciphertext2, l21 = CaesarCipher.caesarCipher('String', 'Encrypt', message=message, flag='Test', key=tc_key)
    plaintext2, l22 = CaesarCipher.caesarCipher('String', 'Decrypt', message=ciphertext2, flag='Test', key=tc_key)
    if message == plaintext2:
        print('CaesarCipher Succeed')
    else:
        print('CaesarCipher Fail')

    # 错位密码
    ciphertext3, l31 = TranspositionCipher.transpositionCipher('String', 'Encrypt', message=message, flag='Test',
                                                               key=tc_key)
    plaintext3, l32 = TranspositionCipher.transpositionCipher('String', 'Decrypt', message=ciphertext3, flag='Test',
                                                              key=tc_key)
    if message == plaintext3:
        print('TranspositionCipher Succeed')
    else:
        print('TranspositionCipher Fail')

    # 仿射密码
    ciphertext4, l31, key = AffineCipher.affineCipher('String', 'Encrypt', message=message, flag='Test')
    plaintext4, l32 = AffineCipher.affineCipher('String', 'Decrypt', message=ciphertext4, flag='Test', key=key)
    if message == plaintext4:
        print('AffineCipher Succeed')
    else:
        print('AffineCipher Fail')