import random


def is_prime(n):
    """
    Tests to see if a number is prime.

    >>> is_prime(2)
    True
    >>> is_prime(11)
    True
    >>> is_prime(8)
    False
    """
    # PUT YOUR CODE HERE
    i = 2
    while (i <= n ** 0.5):
        if (n % i == 0):
            return False
        i += 1
    return True


def gcd(a, b):
    """
    Euclid's algorithm for determining the greatest common divisor.

    >>> gcd(12, 15)
    3
    >>> gcd(3, 7)
    1
    """
    # PUT YOUR CODE HERE
    while (b != 0):
        a, b = b, a % b
    return a


def multiplicative_inverse(e, phi):
    """
    Euclid's extended algorithm for finding the multiplicative
    inverse of two numbers.

    >>> multiplicative_inverse(7, 40)
    23
    """
    # PUT YOUR CODE HERE
    i = 0
    exphi = phi
    vec = []
    while (exphi % e != 0):
        vec.append(exphi // e)
        exphi, e = e, exphi % e
        i += 1
    x, y = 0, 1
    while i > 0:
        x, y = y, x - (y * vec[i - 1])
        i -= 1
    return y % phi


def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')

    # n = pq
    # PUT YOUR CODE HERE
    n = p * q

    # phi = (p-1)(q-1)
    # PUT YOUR CODE HERE
    phi = (p - 1) * (q - 1)

    # Choose an integer e such that e and phi(n) are coprime
    e = 27179

    # Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = 36459
    while g != 1:
        e = 27179
        if (is_prime(e)):
            g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = 36459
    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))


def encrypt(pk, plaintext):
    # Unpack the key into it's components
    key, n = pk
    # Convert each letter in the plaintext to numbers based on
    # the character using a^b mod m
    cipher = [(ord(char) ** key) % n for char in plaintext]
    # Return the array of bytes
    return cipher


def decrypt(pk, ciphertext):
    # Unpack the key into its components
    key, n = pk
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr(char ** key % n) for char in ciphertext]
    # Return the array of bytes as a string
    return ''.join(plain)


if __name__ == '__main__':
    print("RSA Encrypter/ Decrypter")
    a=0.15
    a1=0.85
    b=0.2
    b1=0.8
    c=0.2
    c1=0.8
    d=0.05
    d1=0.95
    e=0.21
    e1=0.79
    z=0
    x = [0.09, 0.91]
    x1 = [0.25, 0.75]
    x2 = [0.79, 0.21]
    for i in range(2):
        for j in range(2):
            #for k in range(2):
                #for v in range(2):
                    for m in range(2):
                        z+=(x[i]*x1[j]*x2[m])
    z-=(0.91*0.75*0.79)
    z = 1 - z
    print(z)
    p = int(input("Enter a prime number (17, 19, 23, etc): "))
    q = int(input("Enter another prime number (Not one you entered above): "))
    print("Generating your public/private keypairs now . . .")
    public, private = generate_keypair(p, q)
    print("Your public key is ", public, " and your private key is ", private)
    message = input("Enter a message to encrypt with your private key: ")
    encrypted_msg = encrypt(private, message)
    print("Your encrypted message is: ")
    print(''.join(map(lambda x: str(x), encrypted_msg)))
    print("Decrypting message with public key ", public, " . . .")
    print("Your message is:")
    print(decrypt(public, encrypted_msg))
