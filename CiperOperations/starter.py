import re
import sys

from CiperOperations.auto_test import autoTest
from CipherAlgorithms.AffineCipher import affineCipher
from CipherAlgorithms.CaesarCipher import caesarCipher
from CipherAlgorithms.RSACiper import rsaCipher
from CipherAlgorithms.ReverseCipher import reverseCipher
from CipherAlgorithms.SubstitutionCipher import substitutionCipher
from CipherAlgorithms.TranspositionCipher import transpositionCipher
from CipherAlgorithms.VigenereCipher import vigenereCipher


def function_choice(function, objType, processType):
    if function == 'ReverseCipher' or bool(re.match(r'[R][C]', function, re.IGNORECASE)):
        return reverseCipher(objType, processType)
    elif function == 'CaesarCipher' or bool(re.match(r'[C][C]', function, re.IGNORECASE)):
        return caesarCipher(objType, processType)
    elif function == 'TranspositionCipher' or bool(re.match(r'[T][C]', function, re.IGNORECASE)):
        return transpositionCipher(objType, processType)
    elif function == 'AffineCipher' or bool(re.match(r'[A][C]', function, re.IGNORECASE)):
        return affineCipher(objType, processType)
    elif function == 'SubstitutionCipher' or bool(re.match(r'[S][C]', function, re.IGNORECASE)):
        return substitutionCipher(objType, processType)
    elif function == 'VigenereCipher' or bool(re.match(r'[V][C]', function, re.IGNORECASE)):
        return vigenereCipher(objType, processType)
    elif function == 'RSACipher' or bool(re.match(r'[R][S][A]', function, re.IGNORECASE)):
        return rsaCipher(objType, processType)
    else:
        sys.exit('no this function')


def usagemode():
    # initial Cipher Algorithms
    N = ['RC', 'CC', 'TC', 'AC']
    testmode = input('Enter Usage Mode (Manual/Auto):')
    # Manual mode
    if testmode.upper().startswith('M'):
        objType = input('Enter Object type (String/File):')
        processType = input('Enter Processing Type (Encrypt/Decrypt/Hacker):')
        function = input('Enter Encrypt Function (if applicable):')
        if len(function) == 0 and processType.upper().startswith('H'):
            resultSet = []
            for i in N:
                resultSet.append(function_choice(i, objType, processType))
            return resultSet, 'several', processType
        text, length = function_choice(function, objType, processType)
        return text, length, processType

    # Auto mode
    elif testmode.upper().startswith('A'):
        try:
            times = int(input('--1--Enter test times:'))
        except Exception:
            sys.exit('Please enter positive integer test times')
        for i in range(times):
            print(f'----Test {i}----')
            autoTest()
        return 'All Auto Tests Succeed', times, 'AutoTest'
    else:
        sys.exit('Please enter (Manual/Auto)')


def main():
    text, length, processType = usagemode()
    if processType.upper().startswith('E'):
        print(f'--Encrypt Text:{text}, Length:{length}')
    elif processType.upper().startswith('D'):
        print(f'--Decrypt Text:{text}, Length:{length}')
    elif processType.upper().startswith('H'):
        print(f'--Hacker Text:{text}, Length:{length}')
