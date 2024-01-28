import requests
from bs4 import BeautifulSoup
import openpyxl

finlist = []
iterator = 1

for i in range(0,12001,1000):
    r = requests.get("https://www.hebe.pl/twarz/?start="+str(i)+"&sz=1000")
    soup = BeautifulSoup(r.text)
    # with open("output.html", "w", encoding="utf-8") as file:
    #     file.write(soup.prettify())
    resoultlist = soup.find_all("li", {'class':'product-grid__item'})

    for line in resoultlist: 
        print(iterator)
        # print(line.prettify())
        # print("\n"+90*"_"+'\n')
        try:
            dataformline = [
                "https://www.hebe.pl"+line.find("a",{'class':'product-tile__clickable js-product-link'})['href'],
                line.find("div", {'class':'product-tile__image'}).find('picture',{'class':'tile-image__container'}).find('source')['data-srcset']
            ]
            finlist.append(dataformline)
        except Exception as e:
            print("nie znalazło zdjęcia")
            print(line.find("div", {'class':'product-tile__image'}).prettify())
            print(e)
            input("naciśnij Enter")
        iterator += 1
    
print(len(finlist))
for line in finlist: print(line)

arkusz = openpyxl.Workbook()
arkusz_aktualny = arkusz.active
for wiersz in finlist:arkusz_aktualny.append(wiersz)
arkusz.save("Hebe_produkty_img.xlsx")
    