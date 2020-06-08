import math
import sys

SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.'


def getBlocksFromText(message, blockSize):
    for character in message:
        if character not in SYMBOLS:
            print('ERROR: The symbol set does not have the character %s' % (character))
            sys.exit()
    blockInts = []
    for blockStart in range(0, len(message), blockSize):
        blockInt = 0
        for i in range(blockStart, min(blockStart + blockSize, len(message))):
            blockInt += (SYMBOLS.index(message[i])) * (len(SYMBOLS) ** (i % blockSize))
        blockInts.append(blockInt)
    return blockInts


def getTextFromBlocks(blockInts, messageLength, blockSize):
    message = []
    for blockInt in blockInts:
        blockMessage = []
        for i in range(blockSize - 1, -1, -1):
            if len(message) + i < messageLength:
                charIndex = blockInt // (len(SYMBOLS) ** i)
                blockInt = blockInt % (len(SYMBOLS) ** i)
                blockMessage.insert(0, SYMBOLS[charIndex])
        message.extend(blockMessage)
    return ''.join(message)


def encryptMessage(message, key, blockSize):
    encryptedBlocks = []
    n, e = key
    for block in getBlocksFromText(message, blockSize):
        encryptedBlocks.append(pow(block, e, n))
    return encryptedBlocks


def decryptMessage(encryptedBlocks, messageLength, key, blockSize):
    decryptedBlocks = []
    n, d = key
    for block in encryptedBlocks:
        decryptedBlocks.append(pow(block, d, n))
    return getTextFromBlocks(decryptedBlocks, messageLength, blockSize)


def readKeyFile(keyFilename):
    fo = open(keyFilename)
    content = fo.read()
    fo.close()
    keySize, n, EorD = content.split(',')
    return int(keySize), int(n), int(EorD)


def encryptAndWriteToFile(messageFilename, keyFilename, message, blockSize=None):
    keySize, n, e = readKeyFile(keyFilename)
    if blockSize is None:
        blockSize = int(math.log(2 ** keySize, len(SYMBOLS)))
    if not (math.log(2 ** keySize, len(SYMBOLS)) >= blockSize):
        sys.exit('ERROR: Block size is too large for the key and symbol set size. Did you specify the correct key '
                 'file and encrypted file?')
    encryptedBlocks = encryptMessage(message, (n, e), blockSize)
    for i in range(len(encryptedBlocks)):
        encryptedBlocks[i] = str(encryptedBlocks[i])
    encryptedContent = ','.join(encryptedBlocks)
    encryptedContent = '%s_%s_%s' % (len(message), blockSize, encryptedContent)
    fo = open(messageFilename, 'w')
    fo.write(encryptedContent)
    fo.close()
    return encryptedContent


def readFromFileAndDecrypt(messageFilename, keyFilename):
    keySize, n, d = readKeyFile(keyFilename)
    fo = open(messageFilename)
    content = fo.read()
    messageLength, blockSize, encryptedMessage = content.split('_')
    messageLength = int(messageLength)
    blockSize = int(blockSize)
    if not (math.log(2 ** keySize, len(SYMBOLS)) >= blockSize):
        sys.exit('ERROR: Block size is too large for the key and symbol set size. Did you specify the correct key '
                 'file and encrypted file?')
    encryptedBlocks = []
    for block in encryptedMessage.split(','):
        encryptedBlocks.append(int(block))
    return decryptMessage(encryptedBlocks, messageLength, (n, d), blockSize)


def rsaCipher(objType, processType, **kwargs):
    """
        :param objType: String/File
        :param processType: Encrypt/Decrypt
        :param kwargs: message/mesfilename/keyfilename
        :return: text,length
    """

    # Default values
    message, mesfilename, keyfilename = '', '', ''

    # Enter values
    if kwargs:
        message = kwargs.get('message')
        mesfilename = int(kwargs.get('mesfilename'))
        keyfilename = int(kwargs.get('keyfilename'))
    else:
        if objType.upper().startswith('S'):
            message = input('Enter Message:')
            mesfilename = input('Enter Message Filename (*.txt):')
            keyfilename = input('Enter Key Filename (*.txt):')
            if keyfilename.upper().startswith('DEFAULTENCRYPT'):
                keyfilename = 'al_sweigart_pubkey.txt'
            elif keyfilename.upper().startswith('DEFAULTDECRYPT'):
                keyfilename = 'al_sweigart_privkey.txt'
        if objType.upper().startswith('F'):
            sys.exit('Sorry, you have to choose String')
    if processType.upper().startswith('E'):
        encryptedText = encryptAndWriteToFile(mesfilename, keyfilename, message)
        return encryptedText, len(encryptedText)
    elif processType.upper().startswith('D'):
        decryptedText = readFromFileAndDecrypt(mesfilename, keyfilename)
        return decryptedText, len(decryptedText)
    elif processType.upper().startswith('H'):
        sys.exit('Sorry, you can not hacker it')
    else:
        sys.exit('Enter Encrypt / Decrypt')
