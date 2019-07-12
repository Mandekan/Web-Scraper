import sys
import json
from classes.Author import Author
from classes.Book import Book
from classes.Press import Press


def open_book():
    mas = []

    with open('PageData.json', encoding="utf8") as json_data:
        json_data = json.load(json_data)
    for index, i in enumerate(json_data):
        book = Book(json_data[index]['author'], json_data[index]['title'], json_data[index]['press'],
                    json_data[index]['year'], json_data[index]['pages'], json_data[index]['price'])
        mas.append(book)
    return mas


def connect(number):
    a = ""
    if number == len(sys.argv) - 1:
        a = sys.argv[number]
    elif len(sys.argv) - 1 > number:
        for x in range(number, len(sys.argv)):
            if x < len(sys.argv) - 1:
                a = a + sys.argv[x] + " "
            elif x == len(sys.argv) - 1:
                a = a + sys.argv[x]
    else:
        quit("Connection error")
    return a


if __name__ == '__main__':
    bookmas = open_book()
    ats = ""

    if sys.argv[1] == "cat":
        press = Press(connect(3))
        if sys.argv[2] == "countA":  # skaiciuoja kiek kategorija turi autoriu            cat countA Fairytale
            try:
                ats = (press.count_authors(bookmas))
            except:
                quit("Unsuccessful attempt")
        elif sys.argv[2] == "countB":  # skaiciuoja kiek kategorija turi knygu              cat countB Fairytale
            try:
                ats = (press.count_books(bookmas))
            except:
                quit("Unsuccessful attempt")
        elif sys.argv[2] == "printB":  # isspausdina visas kategorijos knygas(visa info)    cat printB Fairytale
            try:
                ats = press.print_books(bookmas)
            except:
                quit("Unsuccessful attempt")
        else:
            quit("Function is not found")

    elif sys.argv[1] == "aut":
        author = Author(connect(3))
        if sys.argv[2] == "countB":  # skaiciuoja kiek autorius turi knygu                aut countB Lucy Lee
            try:
                ats = (author.count_books(bookmas))
            except:
                quit("Unsuccessful attempt")
        elif sys.argv[2] == "findN":  # randa naujausia autoriaus knyga                    aut findN Lucy Lee
            try:
                ats = author.find_newest(bookmas)
            except:
                quit("Unsuccessful attempt")
        elif sys.argv[2] == "findO":  # randa seniausia autoriaus knyga                    aut findO Lucy Lee
            try:
                ats = author.find_oldest(bookmas)
            except Exception as e:
                quit(e)
        elif sys.argv[2] == "printB":  # isspausdina visas autoriaus knygas(visa info)      aut printB Lucy Lee
            try:
                ats = author.print_books(bookmas)
            except:
                quit("Unsuccessful attempt")
        else:
            quit("Function is not found")

    elif sys.argv[1] == "book":
        if sys.argv[2] == "info":  # isspausdina visa info apie knyga                   book info Room
            try:
                book = Book(0, connect(3), 0, 0, 0, 0)
                ats = book.print_book_info(bookmas)
            except:
                quit("Unsuccessful attempt")
        elif sys.argv[2] == "findByY":  # randa ivestu metu knygas                           book findByY 2017
            try:
                int(sys.argv[3])
                book = Book(0, 0, 0, sys.argv[3], 0, 0)
                ats = book.find_by_year(bookmas)
            except:
                quit("Unsuccessful attempt")
        elif sys.argv[2] == "findN":  # randa naujausia knyga                              book findN
            try:
                book = Book(0, 0, 0, 0, 0, 0)
                ats = book.find_newest(bookmas)
            except:
                quit("Unsuccessful attempt")
        elif sys.argv[2] == "findO":  # randa seniausia knyga                              book findO
            try:
                book = Book(0, 0, 0, 0, 0, 0)
                ats = book.find_oldest(bookmas)
            except:
                quit("Unsuccessful attempt")
        elif sys.argv[2] == "findMinPa":  # randa knyga turincia maziausiai puslapiu           book findMinPa
            try:
                book = Book(0, 0, 0, 0, 0, 0)
                ats = book.find_least_pages(bookmas)
            except:
                quit("Unsuccessful attempt")
        elif sys.argv[2] == "findAveragePr":  # randa visu knygu kainu vidurki                     book findAveragePr
            try:
                book = Book(0, 0, 0, 0, 0, 0)
                ats = book.find_average_price(bookmas)
            except:
                quit("Unsuccessful attempt")
        elif sys.argv[2] == "findPr":  # randa kaina uzsakymo imant                         book findPr 5 Room
            try:
                book = Book(0, connect(4), 0, 0, 0, 0)  # kazkokia knyga kazkoki skaiciu vnt
                quantity = sys.argv[3]
                ats = book.find_price_by_quantity(bookmas, quantity)
            except:
                quit("Unsuccessful attempt")
        else:
            quit("Function is not found")
    else:
        quit("Selection is not found")

    file = open("Result.txt", "w")
    file.write(str(ats))
    file.close()
    print("Duomenys issaugoti testfile.txt faile")
    print(ats)