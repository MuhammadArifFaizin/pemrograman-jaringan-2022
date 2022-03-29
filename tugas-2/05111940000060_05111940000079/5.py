# get short tutorial here: http://www.pythonforbeginners.com/python-on-the-web/beautifulsoup-4-python/
from urllib.request import urlopen
from bs4 import BeautifulSoup

response = urlopen('https://classroom.its.ac.id').read()
soup = BeautifulSoup(response)

# print(soup.title.string)
# print(soup.get_text())

p = soup.get_text().split('\n')
p = list(filter(('').__ne__, p))[2:9]
for i in p:
    print(i)