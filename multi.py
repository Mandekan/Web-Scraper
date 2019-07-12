import math
import threading

from bs4 import BeautifulSoup
import requests
import json
import io, time

ats = []
b = []
url = "https://www.patogupirkti.lt/"
response = requests.get(url, timeout = 5)
soup = BeautifulSoup(response.content, "html.parser")

firstt = soup.find('a', class_='arrow-right pull-right mt5')
if firstt.has_attr('href'):
    b.append(firstt.attrs['href']+"&limit=36")
    b.append(b[0]+"&p=2")

lock = threading.Lock()
for index,i in enumerate(b):
    url = b[index]
    response = requests.get(url, timeout = 5)
    soup = BeautifulSoup(response.content, "html.parser")
    for link in soup.find_all('a') :
        k = 0
        if link.has_attr('href'):
            a = link.attrs['href']
            if(a.endswith(".html")):
                for index, l in enumerate (ats):
                    try:
                        lock.acquire(True)
                        print(l, " - Lock acquired")
                        if ats[index] == a:
                            k=k+1
                    finally:
                        lock.release()
                        print(l, " - Lock released")
                if k == 0:
                    ats.append(a)

data = []  # create a list to store the items
def get_info(start, end):
    for link in range(start, end):
        url = ats[link]
        response = requests.get(url, timeout = 5)
        soup = BeautifulSoup(response.text, "html.parser")


        if soup.find(class_="author").find('h2'):
            author = soup.find(class_="author").find('h2').text
        else:
            author = "-"

        if soup.find('h1'):
            title = soup.find('h1').text
        else:
            title = "-"

        if soup.find('span', itemprop = "name"):
            press = soup.find('span', itemprop = "name").text
        else:
            press = "-"

        if soup.find(itemprop = "copyrightYear"):
            year = soup.find(itemprop = "copyrightYear").text
        else:
            year = "0"

        if soup.find(itemprop = "numberOfPages"):
            pages = soup.find(itemprop = "numberOfPages").text
        else:
            pages = "0"

        if soup.find('span', class_ = "font-16"):
            pr = soup.find('span', class_ = "font-16").text[0:-2]
            pr = pr.split(",")
            price = pr[0]+"."+pr[1]
        else:
            price = "0"

        item = {}
        item['author'] = author
        item['title'] = title
        item['press'] = press
        item['year'] = year
        item['pages'] = pages
        item['price'] = price
        data.append(item)  # add the item to the list

start_time = time.time()
thread_count = 16
book_count = len(ats)-1
thread_list = []

for i in range(thread_count):
    start = math.floor(i * book_count / thread_count) + 1
    end = math.floor((i + 1) * book_count / thread_count) + 1
    thread_list.append(threading.Thread(target=get_info, args=(start, end)))

for thread in thread_list:
    thread.start()

for thread in thread_list:
    thread.join()

with io.open('PageData.json', 'w', encoding='utf8') as json_file:
    json_file.write(
        '[' +
        ',\n'.join(json.dumps(i, ensure_ascii=False) for i in data) +
        ']\n')

end_time = time.time()
print("OK")
print("Time taken: " + str(end_time - start_time) + "sec")
