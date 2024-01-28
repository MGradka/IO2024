import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import openpyxl
import time

# start_list = [['Missha M Perfect Cover','https://www.hebe.pl/missha-krem-bb-z-filtrem-spf42-pa-do-twarzy-23-natural-beige-20-ml-000000000000301819.html'],['Tołpa Dermo Face Enzyme','https://www.hebe.pl/tolpa-peeling-3-enzymy-8-ml-000000000000364564.html']]

df = pd.read_excel("Rossman_produkty.xlsx")
start_list = df.values.tolist()
driver = webdriver.Firefox(executable_path='geckodriver 2')
# for line in start_list:print(line)
driver.get('https://www.rossmann.pl/Produkt/Kremy-do-twarzy/Dermika-Luxury-Caviar-krem-do-twarzy-kawiorowy-wypelniajacy-zmarszczki-50-dzien-noc-50-ml,381350,9223')
time.sleep(10)

end_list = []
for link in start_list:
    il_iteracji = 1
    while True:
        try:
            driver.get(link[1])
            html_source = driver.page_source
            soup = BeautifulSoup(html_source)
            cena = soup.find("div", {'class':'product-price'}).get_text().strip() #.find("span")
            print(cena)
            r = requests.get(link[1])
            soup = BeautifulSoup(r.text)
            skladniki = soup.find_all('div',{"class":"accordion"})[1].get_text().strip()
            print(skladniki)
            end_list.append([link[0],link[1],cena,skladniki])
            arkusz = openpyxl.Workbook()
            arkusz_aktualny = arkusz.active
            for wiersz in end_list:arkusz_aktualny.append(wiersz)
            arkusz.save("Rossman_produkty_detale.xlsx")
            break
        except:
            try:
                driver.refresh()
                time.sleep(2)
                driver.get(link[1])
                html_source = driver.page_source
                soup = BeautifulSoup(html_source)
                cena = soup.find("div", {'class':'product-price'}).get_text().strip() #.find("span")
                print(cena)
                r = requests.get(link[1])
                soup = BeautifulSoup(r.text)
                skladniki = soup.find_all('div',{"class":"accordion"})[1].get_text().strip()
                print(skladniki)
                end_list.append([link[0],link[1],cena,skladniki])
                arkusz = openpyxl.Workbook()
                arkusz_aktualny = arkusz.active
                for wiersz in end_list:arkusz_aktualny.append(wiersz)
                arkusz.save("Rossman_produkty_detale.xlsx")
                break
            except:
                pass
        il_iteracji += 1
        if il_iteracji == 1000:break