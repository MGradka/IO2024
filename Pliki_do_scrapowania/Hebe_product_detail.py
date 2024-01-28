import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

df = pd.read_excel("Hebe_produkty.xlsx")
start_list = df.values.tolist()
# for line in start_list:print(line)

df_cały = pd.DataFrame()
for link in start_list:
    try:
        r = requests.get(link[1])
        # print(r.text)
        soup = BeautifulSoup(r.text)
        # with open("output.html", "w", encoding="utf-8") as file:
        #     file.write(soup.prettify())
        cena_src = soup.find("div", {'class':'price-product__wrapper'}).get_text().strip().split('\n')
        cena = float(cena_src[0]+"."+cena_src[2])
        print(cena)
        skladniki = soup.find("div", {'id':'product-ingredients'}).find("div", {'class':'ui-expandable__inner'}).get_text().strip()
        print(skladniki)
        df_start = pd.DataFrame({'Nazwa':[link[0]],'Cena':[cena],'Skaładniki':[skladniki],'URL':[link[1]]})
        dodatkowe_informacje_dane = []
        dodatkowe_informacje_etykiety = []
        dodatkowe_informacje_src_total = soup.find("div", {'id':'product-additional-info'})
        dodatkowe_informacje_src = dodatkowe_informacje_src_total.find_all("div", {'class':'product-attributes__row'})
        for element in dodatkowe_informacje_src: 
            # print(element)
            dodatkowe_informacje_etykiety.append(element.find("span", {'class':'product-attributes__label'}).get_text().strip())
            dodatkowe_informacje_dane.append(element.find("span", {'class':'product-attributes__value'}).get_text().strip())
        df = pd.DataFrame(dodatkowe_informacje_dane,index=dodatkowe_informacje_etykiety)
        df = df.transpose()
        df_resoult_iter = pd.concat([df_start,df], axis=1)
        df_cały = pd.concat([df_cały,df_resoult_iter])
        df_cały.to_excel("Hebe_detale.xlsx")
        try:
            df_check = pd.read_excel("Hebe_detale.xlsx")
            print(f"Plik Hebe_detale.xlsx został pomyślnie utworzony i otwarty.")
        except Exception as e:
            print(f"Błąd podczas otwierania pliku Hebe_detale.xlsx: {e}")
            os.system("""osascript -e 'display notification "Błąd Scrapera" with title "Błąd"'""")
            input("Naciśnij Enter zeby kontynować")
    except:
        pass

print(df_cały)