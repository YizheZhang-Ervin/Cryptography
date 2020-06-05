# cipher wheel


def caesar_cipher(message='', **kwargs):
    """
    :param message: plaintext
    :param kwargs: extrachar=none / key=0 / mode=encrypt
    :return: ciphertext,len(ciphertext)
    """

    allowedchar = ''.join([chr(a) for a in range(65, 91)]) \
                  + ''.join([chr(a) for a in range(97, 123)]) \
                  + ''.join([chr(i) for i in range(48, 58)])
    if kwargs:
        allowedchar += kwargs.get('extrachar', '')
        key = kwargs.get('key')
        mode = kwargs.get('mode')
    else:
        key, mode = 0, 'encrypt'

    result_mes = ''
    for mes in message:
        if mes in allowedchar:
            mes_index = allowedchar.find(mes)
            newmes_index = 0
            if mode == 'encrypt':
                newmes_index = mes_index + key
            elif mode == 'decrypt':
                newmes_index = mes_index - key
            if newmes_index >= len(allowedchar):
                newmes_index -= len(allowedchar)
            elif newmes_index < 0:
                newmes_index += len(allowedchar)
            result_mes += allowedchar[newmes_index]
        else:
            result_mes += mes
    return result_mes, len(result_mes)
