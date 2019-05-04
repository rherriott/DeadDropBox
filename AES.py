from os import urandom
import random

'''
'''
def __getRandomBitstream(bits):
    # print(type(bits))
    return urandom(bits//8)

def __isPrime(n, trials):
    """
    Miller-Rabin primality test.
 
    A return value of False means n is certainly not prime. A return value of
    True means n is very likely a prime.

    From rosettacode.com
    """
    if n!=int(n):
        return False
    n=int(n)

    s = 0
    d = n-1
    while d%2==0:
        d>>=1
        s+=1
    assert(2**s * d == n-1)
 
    def trial_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2**i * d, n) == n-1:
                return False
        return True  
 
    for i in range(trials):
        a = random.randrange(2, n)
        if trial_composite(a):
            return False
 
    return True 
        
'''
Generates a cryptographically random stream of bits.
Returns a str
'''    
def __getLargeRandom(keylen):
    key = "";
    keyarr = __getRandomBitstream(keylen)
    for i in range(keylen//8):
        key = key + str(bin(keyarr[i])[2:]).zfill(8)
    return int(key, 2)

def __getLargeRandomPrime(length):
    i = 0
    while(True):
        i += 1
        num = __getLargeRandom(length)
        print(str(type(num)) + ":" + str(num))
        if(__isPrime(num, 30)):
            print("Processed " + str(i) + " numbers.")
            return num
        
        
'''
Generates a cryptographically random stream of bits for use in the
AES encryption standard.
Recommended keylengths: 128, 192, 256
Returns a binary number
'''
def getAESKey(keylen):
    return __getLargeRandom(keylen)

'''
Returns a secure RSA keypair and modulus.

'''
def getRSAKeypair(keylen):
    p = __getLargeRandomPrime(1024)
    q = __getLargeRandomPrime(1024)
    
    n = p * q

    totient = (p-1)(q-1)

   #d = 
    
    e = 65537

print(__getLargeRandomPrime(1024))
