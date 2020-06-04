def transposition_cipher(message, **kwargs):
    """
    :param message: plaintext
    :param kwargs: key=0 / mode=encrypt
    :return: ciphertext,len(ciphertext)
    """

    if kwargs:
        key = kwargs['key']
        mode = kwargs['mode']
    else:
        key, mode = 0, 'encrypt'

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
    elif mode == 'decrypt':
        return
