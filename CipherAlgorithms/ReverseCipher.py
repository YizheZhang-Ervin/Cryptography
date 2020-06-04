
def reverse_cipher(message='', **kwargs):
    """
    :param message: plaintext
    :param kwargs: mode=encrypt
    :return: cipher text,len(ciphertext)
    """

    if kwargs:
        mode = kwargs['mode']
    else:
        mode = 'encrypt'
    if mode == 'encrypt':
        return message[::-1], len(message[::-1])
    elif mode == 'decrypt':
        return message[::-1], len(message[::-1])
