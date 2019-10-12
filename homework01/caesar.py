def encrypt_caesar(plaintext: str) -> str:
    """
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    # PUT YOUR CODE HERE
    ciphertext = ''
    shift = 3
    for ch in plaintext:
        if 'a' <= ch <='z' or 'A' <= ch <= 'Z':
            newch = ord(ch) + shift
            if(chr(newch) > 'z'):
                newch -= 26
            elif(chr(newch) > 'Z' and chr(newch) < 'a'):
                newch -= 26
            ciphertext+=chr(newch)
        else:
            ciphertext+=ch
    return ciphertext


def decrypt_caesar(ciphertext: str) -> str:
    """
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    # PUT YOUR CODE HERE
    plaintext = ''
    shift = 3
    for ch in ciphertext:
        if('a' <= ch <= 'z' or 'A' <= ch <= 'Z'):
            newch = ord(ch) - shift
            if(chr(newch) < 'A'):
                newch +=26
            elif(chr(newch) > 'Z' and chr(newch) < 'a'):
                newch +=26
            plaintext+=chr(newch)
        else:
            plaintext+=ch
    return plaintext
