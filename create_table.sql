-- CREATE TABLE skladniki (
--     id SERIAL PRIMARY KEY,
--     nazwa TEXT,
--     wiek VARCHAR(10) CHECK (wiek IN ('do 50 lat', 'od 50 lat')),
--     przebarwienia BOOLEAN,
--     podraznienia BOOLEAN,
--     tradzik BOOLEAN,
--     typ_skory VARCHAR(20) CHECK (typ_skory IN ('Sucha', 'Tlusta', 'Mieszana'))
-- );

-- COPY skladniki(id, nazwa, wiek, przebarwienia, podraznienia, tradzik, typ_skory)
-- FROM '/Users/nofluffjobs/Desktop/IO2024/Składniki.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE produkty (
    id SERIAL PRIMARY KEY,
    zrodlo VARCHAR(20) CHECK (zrodlo IN ('Hebe', 'Rossmann')),
    nazwa VARCHAR(255),
    cena NUMERIC,
    skladniki TEXT,
    url TEXT,
    zdjecie TEXT
);

COPY produkty(id, zrodlo, nazwa, cena, skladniki, url, zdjecie)
FROM '/Users/nofluffjobs/Desktop/IO2024/Produkty.csv' DELIMITER ',' CSV HEADER;