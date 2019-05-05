from os import urandom
import random

DEBUG = False
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
        #print(str(type(num)) + ":" + str(num))
        print('.', end="")
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
Uses pseudocode from Wikipedia
'''
def __euclideanGCD(num, mod):
    div = mod // num
    rem = mod % num
    if DEBUG:
        print(str(mod) + " = " + str(div) + " * " + str(num) + " + " + str(rem))
    if rem == 0:
        return num, list()
    else:
        a, eqs = __euclideanGCD(rem, num)
        eqs.append([mod, div, num])
        return a, eqs

def __modInverse(num, mod):
    gcd, eqlist = __euclideanGCD(num, mod)
    
    if gcd != 1:
        return -1

    factorA = (1, eqlist[0][0])
    factorB = (-eqlist[0][1], eqlist[0][2])
    if DEBUG:
        print(str(gcd), end="")
        print(" = " + str(factorA[0]) + " * " + str(factorA[1]), end="")
        print(" + " + str(factorB[0]) + " * " + str(factorB[1]))
    
    for i in range(len(eqlist) - 1):
        eq = eqlist[i + 1]
        factorB = (factorB[0], eq[0])
        factorA = (factorA[0] - eq[1] * factorB[0], factorA[1])
        if DEBUG:
            print(str(gcd), end="")
            print(" = " + str(factorA[0]) + " * " + str(factorA[1]), end="")
            print(" + " + str(factorB[0]) + " * " + str(factorB[1]))
        if(factorA[1] < factorB[1]):
            temp = tuple(factorA)
            factorA = tuple(factorB)
            factorB = tuple(temp)

    inv = factorA[0] if factorA[1] != mod else factorB[0]
    return inv if inv > 0 else inv + mod

'''
Returns a secure RSA keypair and modulus.

'''
def getRSAKeypair(keylen):
    p = __getLargeRandomPrime(keylen)
    q = __getLargeRandomPrime(keylen)
    
    n = p * q
    mod = (p-1)*(q-1)
    pub = 65537
    priv = __modInverse(pub, mod)
    return pub, mod, priv

if __name__ == "__main__":
    #print(str(__modInverse(42, 2017)))
    #print(str(__modInverse(11, 14)))
    #print(str(__modInverse(17, 780)))
    print(getRSAKeypair(1024))
    #print(getAESKey(128))
