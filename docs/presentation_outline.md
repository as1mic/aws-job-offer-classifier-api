# Konspekt prezentacji

## Slajd 1. Temat i cel projektu

- Temat: API do klasyfikacji ofert pracy IT
- Cel: połączenie REST API, ML i usług AWS w prostym projekcie edukacyjnym
- Wynik: endpoint zwraca kategorię, poziom, confidence i flagę `recommended`

Co powiedzieć:
Projekt pokazuje pełny przepływ od danych do działającego API. Zależało mi na rozwiązaniu prostym, tanim i łatwym do obrony na zajęciach.

## Slajd 2. Architektura AWS

- S3 przechowuje dane i artefakty
- Glue kataloguje plik CSV
- Athena służy do prostych analiz SQL
- SageMaker Notebook służy do treningu modelu
- Lambda udostępnia logikę predykcji
- API Gateway wystawia endpoint HTTP

Co powiedzieć:
Architektura jest lekka. Nie używam drogich usług typu RDS lub pełny endpoint SageMaker, bo projekt działa w ramach budżetu AWS Academy.

## Slajd 3. Dataset

- Zbiór danych jest syntetyczny
- Zawiera co najmniej 500 ofert pracy
- Kolumny: `text`, `category`, `level`
- Kategorie: backend, frontend, data, devops, other
- Poziomy: internship, junior, regular, senior

Co powiedzieć:
Dane nie pochodzą z prawdziwych ogłoszeń, tylko zostały wygenerowane do celów edukacyjnych. Dzięki temu mogłem łatwo kontrolować balans klas.

## Slajd 4. ETL / preprocessing

- Generowanie CSV w Pythonie
- Czyszczenie tekstu: małe litery, usunięcie zbędnych znaków, normalizacja spacji
- Możliwość wczytania danych lokalnie lub z S3
- Wstępna analiza rozkładu klas w notebooku

Co powiedzieć:
ETL jest prosty, ale pokazuje prawdziwy proces przygotowania danych do modelu. To wystarcza do pokazania pracy z danymi w SageMaker Notebook.

## Slajd 5. Model ML

- TF-IDF zamienia tekst na cechy liczbowe
- Dwa modele `LogisticRegression`
- Model 1 przewiduje kategorię
- Model 2 przewiduje poziom
- Wyniki zapisane do `metrics.json`

Co powiedzieć:
Wybrałem lekkie modele klasyczne, bo są szybkie, tanie i łatwe do wyjaśnienia. To lepsze do projektu studenckiego niż ciężkie modele NLP.

## Slajd 6. REST API

- Endpoint `POST /predict`
- Wejście: tekst ogłoszenia
- Wyjście: kategoria, poziom, confidence, recommended
- Implementacja w AWS Lambda i API Gateway

Co powiedzieć:
API działa w prostym modelu serverless. Dzięki temu nie trzeba utrzymywać serwera i koszty są bardzo małe.

## Slajd 7. Wyniki i analiza

- Ocena przez accuracy, precision, recall i F1-score
- Dodatkowo raport klasyfikacji i macierz pomyłek
- Analiza rozkładu danych w Athena i notebooku
- Wysokie wyniki wynikają z dobrze rozdzielonych danych syntetycznych

Co powiedzieć:
Wyniki są dobre, ale trzeba pamiętać, że dane syntetyczne są prostsze niż dane z rynku. W raporcie zaznaczam to jako ograniczenie projektu.

## Slajd 8. Wnioski

- Projekt spełnia wymagania kursu
- Łączy Big Data, ML, ETL i REST API
- Jest tani w uruchomieniu i prosty do prezentacji
- Można go rozbudować o prawdziwe dane i lepszy model

Co powiedzieć:
Najważniejsze było pokazanie pełnego pipeline'u w AWS, a nie budowanie skomplikowanego produktu. Projekt jest dobrą bazą do dalszego rozwoju.