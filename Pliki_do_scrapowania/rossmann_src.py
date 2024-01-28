import requests
from bs4 import BeautifulSoup
import openpyxl

finlist = []
iterator = 1

for i in range(1,26):
    r = requests.get(f"https://www.rossmann.pl/kategoria/twarz,8686?Page={i}&PageSize=100")
    soup = BeautifulSoup(r.text)
    # with open("output.html", "w", encoding="utf-8") as file:
    #     file.write(soup.prettify())
    resoultlist = soup.find_all("div", {'class':'product-list__col--thirds col-8 mb-6 item'})
    
    for line in resoultlist: 
        print(iterator)
        # print(line.prettify())
        # print("\n"+90*"_"+'\n')
        try:
            dataformline = [
                "https://www.rossmann.pl"+line.find("a",{'class':'tile-product__name'})['href'],
                line.find("a", {'class':'tile-product__img'}).find('img')['src']
            ]
            finlist.append(dataformline)
        except:
            print(line.find("a", {'class':'tile-product__name'}))
            if(line.find("a", {'class':'tile-product__name'}) == None):
                print(line)
        iterator += 1
    
print(len(finlist))
for line in finlist: print(line)

arkusz = openpyxl.Workbook()
arkusz_aktualny = arkusz.active
for wiersz in finlist:arkusz_aktualny.append(wiersz)
arkusz.save("Rossman_produkty_img.xlsx")