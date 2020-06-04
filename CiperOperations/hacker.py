def hacker(text, encrypt_name, extra_char):
    if encrypt_name == 'CaesarCipher':
        result_collection, collection_length = hacker_caesar(text, extrachar=extra_char)
        print(f'------Brute-force trials:{collection_length}')
        for i in result_collection:
            print(f'------Plain Text:{i[0]}, {i[1]}')


def hacker_caesar(message, **kwargs):
    allowedchar = ''.join([chr(a) for a in range(65, 91)]) \
                  + ''.join([chr(a) for a in range(97, 123)]) \
                  + ''.join([chr(i) for i in range(48, 58)])
    if kwargs:
        allowedchar += kwargs['extrachar']
    result_collection = []
    index = 0
    for key in range(len(allowedchar)):
        result = ''
        for mes in message:
            if mes in allowedchar:
                mes_index = allowedchar.find(mes)
                mes_index -= key
                if mes_index < 0:
                    mes_index += len(allowedchar)
                result += allowedchar[mes_index]
            else:
                result += mes
        result_collection.append((result, 'key='+str(index)))
        index += 1
    return result_collection, len(result_collection)


