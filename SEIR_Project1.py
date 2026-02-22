
import requests
import re
import sys
from bs4 import BeautifulSoup

def word_frequency(url):
    response= requests.get(url)
    soup=BeautifulSoup(response.text, "html.parser")
    text=soup.body.get_text(" ",strip=True)

    words = re.findall(r"[A-Za-z0-9]+", text.lower())
    frequency={}
    for word in words:
        frequency[word]=frequency.get(word, 0)+1
    # print(frequency)
    return frequency

def calc_polynomial_rolling_hash_fn(word):
    p=53      
    hash_value=0
    power=1

    for character in word:
        hash_value=(hash_value + ord(character)*power)%2**64
        # print(hash_value)
        power=(power*p)%2**64
    return hash_value


def calc_simhash(frequency):
    vector=[0]*64

    for word, weight  in frequency.items():
        hash_value=calc_polynomial_rolling_hash_fn(word)

        for i in range(64):
            bit=(hash_value>>i)&1 
            if bit==1:
                vector[i]+=weight
            else:
                vector[i]-=weight

    fingerprint=0
    for i in range(64):
        if vector[i]>0:
            fingerprint = fingerprint|(1<<i)
    return fingerprint


def count_common_bits(hash1, hash2):
    xor = hash1^hash2
    diff_bits_count=0
    while xor>0:
        diff_bits_count= diff_bits_count + (xor)&1
        xor>>=1
    # print(diff_bits_count)
    return 64 - diff_bits_count



if __name__=="__main__":
    if len(sys.argv)!=3:
        print("Give the input in correct format \n eg: python script.py <url1> <url2>")
        sys.exit(1)
    url1=sys.argv[1]
    url2=sys.argv[2]

    frequency1=word_frequency(url1)
    frequency2=word_frequency(url2)

    hash1=calc_simhash(frequency1)
    hash2=calc_simhash(frequency2)

    num_of_common_bits=count_common_bits(hash1,hash2)
    print(f"Number of common bits in Simhash of url {url1} & {url2} \n:", num_of_common_bits)

# word_frequency('https://www.cricbuzz.com/')