#  Python Project
# ○ Write a python program that takes a URL on the command line, fetches the page, and 
# outputs (one per line)
# ■ Page Title (without any HTML tags)
# ■ Page Body (without any html tags)
# ■ All the URLs that the page points/links to

# PART-1


import requests
import sys
from bs4 import BeautifulSoup

def fetch_data(url):
    
    user={"User-Agent":"Mozilla/5.0"}
    response=requests.get(url, headers=user, timeout=10)
    soup=BeautifulSoup(response.text,'html.parser')

    titles=soup.find('title')
    
    print("................Page Titles:...............\n",titles.string)

    text = soup.body.get_text(" ", strip=True)
    print()
    print("...............Body text:............\n")
    print(text)
    links = soup.find_all("a", href=True)
    print()
    print("...............Links:.............. \n")
    for link in links:
        href=link.get("href")
        print(href)

if __name__=="__main__":
    if len(sys.argv)!=2:
        print("Give input in correct format:\n eg: python script.py <url>") 
        sys.exit(1)  
    
    url =sys.argv[1]
    fetch_data(url)
# fetch_data('https://www.cricbuzz.com/')