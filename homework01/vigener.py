def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    # PUT YOUR CODE HERE
    ciphertext = ''
    shift = 0
    for ch in plaintext:
        if 'a' <= ch <= 'z' or 'A' <= ch <= 'Z':
            if ('a' <= ch <= 'z'):
                newch = ord(ch) + ord(keyword[shift % len(keyword)]) - ord('a')
                if (chr(newch) > 'z'):
                    newch -= 26
            else:
                newch = ord(ch) + ord(keyword[shift % len(keyword)]) - ord('A')
                if (chr(newch) > 'Z'):
                    newch -= 26
            ciphertext += chr(newch)
        else:
            ciphertext += ch
        shift += 1
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    # PUT YOUR CODE HERE
    plaintext = ''
    shift = 0
    for ch in ciphertext:
        if ('a' <= ch <= 'z' or 'A' <= ch <= 'Z'):
            if ('a' <= ch <= 'z'):
                newch = ord(ch) - ord(keyword[shift % len(keyword)]) + ord('a')
                if (chr(newch) < 'a'):
                    newch += 26
            else:
                newch = ord(ch) - ord(keyword[shift % len(keyword)]) + ord('A')
                if (chr(newch) < 'A'):
                    newch += 26
            plaintext += chr(newch)
        else:
            plaintext += ch
        shift += 1
    return plaintext
