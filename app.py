from flask import Flask, render_template, request
import re
import pandas as pd
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="IO2024",
    user="nofluffjobs",
    password=""
)

app = Flask(__name__)

def custom_function(skin_type, age, discolorations, acne, max_budget, skin_irritations):
    query = f"""
        SELECT nazwa
        FROM skladniki
        WHERE 
            typ_skory = '{skin_type}' AND
            wiek = '{age}' AND
            przebarwienia {'=' if discolorations == 'Yes' else '!='} TRUE AND
            tradzik {'=' if acne == 'Yes' else '!='} TRUE AND
            podraznienia {'=' if skin_irritations == 'Yes' else '!='} TRUE
    """
    skladniki_df = pd.read_sql_query(query, conn)
    print(skladniki_df)

    if not skladniki_df.empty:
        skladniki_list = skladniki_df['nazwa'].tolist()
        query = f"""
            SELECT zdjecie, nazwa, url, cena
            FROM produkty
            WHERE
                cena <= {max_budget} AND
                ARRAY[{', '.join([f"'{skladnik}'" for skladnik in skladniki_list])}] && string_to_array(skladniki, ', ')
        """
        produkty_df = pd.read_sql_query(query, conn)

        products = [["Zdjęcie", "Nazwa", "Kup produkt", "Cena"]]
        for _, row in produkty_df.iterrows():
            products.append([row['zdjecie'], row['nazwa'], row['url'], row['cena']])
        
        print(products)
        return products
    else:
        return []
    # print(skin_type, age, discolorations, acne, max_budget, skin_irritations)
    # products = [
    #     ["Zdjęcie", "Nazwa", "Kup produkt", "Cena"],
    #     ['https://pro-fra-s3-productsassets.rossmann.pl/product_7_medium/390630_360_350.png', 'L\'ORÉAL PARIS Age Perfect Cell Renew', 'https://www.rossmann.pl/Produkt/Kremy-pod-oczy/LOreal-Paris-Age-Perfect-Cell-Renew-krem-pod-oczy-rozswietlajacy-15-ml,390630,9224', 56.99],
    #     ['https://pro-fra-s3-productsassets.rossmann.pl/product_7_medium/317887_360_350.png', 'CHRISTIAN LAURENT Edition de Luxe', 'https://www.rossmann.pl/Produkt/Serum/Christian-Laurent-Edition-de-Luxe-serum-do-twarzy-superskoncentrowane-diamentowe-napinajace-30-,317887,9225', 76.99],
    #     ['https://pro-fra-s3-productsassets.rossmann.pl/product_7_medium/199467_360_350.png', 'DERMIKA Luxury Neocollagen', 'https://www.rossmann.pl/Produkt/Kremy-do-twarzy/Dermika-Luxury-Neocollagen-krem-do-twarzy-kolagenowy-odzywczy-70-dzien-noc-50-ml,199467,9223', 69.99],
    #     ['https://pro-fra-s3-productsassets.rossmann.pl/product_1_medium/250871_360_350.png', 'L\'ORÉAL PARIS Age Perfect Złoty Wiek', 'https://www.rossmann.pl/Produkt/Kremy-do-twarzy/LOreal-Paris-Age-Perfect-Zloty-Wiek-krem-do-twarzy-chlodzacy-wzmacniajacy-na-noc-50-ml,250871,9223', 58.99],
    #     ['https://pro-fra-s3-productsassets.rossmann.pl/product_7_medium/331796_360_350.png', 'JANDA Collagen Reconstructor', 'https://www.rossmann.pl/Produkt/Serum/Janda-Collagen-Reconstructor-serum-odzywka-do-twarzy-odmladzajace-Naturalny-Kolagen-50-ml,331796,9225', 58.99]
    # ]
    # return products

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        skin_type = request.form.get('skin_type')
        age = request.form.get('age')
        discolorations = 'Yes' if request.form.get('discolorations') else 'No'
        skin_irritations = 'Yes' if request.form.get('skin_irritations') else 'No'
        acne = 'Yes' if request.form.get('acne') else 'No'
        max_budget = request.form.get('max_budget')

        if max_budget and not re.match(r'^\d+(\.\d{1,2})?$', max_budget):
            return render_template('index.html', error='Max budget must be a valid number.')

        result = custom_function(skin_type, age, discolorations, acne, max_budget, skin_irritations)
        headers = result[0]
        data = result[1:]

        return render_template('index.html', headers=headers, data=data)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
