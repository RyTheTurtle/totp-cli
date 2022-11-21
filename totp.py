from hashlib import sha1
from time import time, sleep 
from hmac import new as newHmac
from sys import argv 
from base64 import b32decode 

def getCurrentTimeInterval(split = 30):
    # divide the current epoch seconds by the 
    # size of the time window. RFC specifices 30 seconds as a 
    # default value 
    return int(time() / split) 

def getLongAsBigEndianByteArray(input): 
    result = [0x0  for i in range(8)] 
    i = 0
    while input > 0:
        result[i] = input & 0xFF 
        input >>= 8 
        i = i + 1
    result.reverse()
    return bytearray(result)

def getHmacSha1Hash(data, key): 
    digester = newHmac(key, data, sha1)
    return digester.digest()

def dynamicTruncate(hash):
    offsetBits = hash[19] & 0xF #0 <= offsetBits <= 15
    # returns last 31 bits from the offset 
    return [hash[offsetBits] & 0x7F,
             hash[offsetBits+1] & 0xff,
             hash[offsetBits+2] & 0xff,
             hash[offsetBits+3] & 0xff
            ]

def getBigEndianByteArrayAsNum(inputBytes):
    result = 0 
    for b in inputBytes:
        result <<= 8
        result |= b 
    return result 


def getTotp(currentTimeInterval, secretKey, digits=6):
    data = getLongAsBigEndianByteArray(currentTimeInterval)
    key  = b32decode(secretKey, casefold=True)
    hash = getHmacSha1Hash(data, key)
    truncatedHash = getBigEndianByteArrayAsNum(dynamicTruncate(hash))
    otp = truncatedHash % (10 ** digits)
    return otp 

if __name__ == "__main__":
    print("Python CLI for generating time-based OTPs")
    secretKey = argv[1]

    currentTimeInterval = getCurrentTimeInterval() 
    currentTotp = getTotp(currentTimeInterval, secretKey)
    print(f"Current OTP is {currentTotp}")
    while(True):
        sleep(3)
        
        if getCurrentTimeInterval() != currentTimeInterval:
            currentTimeInterval = getCurrentTimeInterval()
            currentTotp = getTotp(currentTimeInterval, secretKey)
            print(f"Current OTP is {currentTotp}")

