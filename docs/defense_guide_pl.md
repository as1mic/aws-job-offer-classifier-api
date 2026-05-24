# Przewodnik do obrony projektu

## Cel tego dokumentu

Ten dokument ma pomoc w praktycznej obronie projektu:

- jak zaczac prezentacje,
- co pokazac po kolei,
- jak wyjasnic architekture i kod,
- jak odpowiadac na typowe pytania,
- czego nie komplikowac podczas obrony.

Projekt:

- klasyfikuje oferty pracy IT,
- zwraca `category`, `level`, `confidence` i `recommended`,
- laczy machine learning, REST API i uslugi AWS.

## Jak zaczac obrone

Mozesz zaczac bardzo prosto:

> Dzien dobry. Moj projekt to serwis REST API do klasyfikacji ofert pracy IT.  
> Celem projektu bylo polaczenie przetwarzania danych tekstowych, modelu ML oraz uslug AWS w jednym, prostym i dzialajacym rozwiazaniu.  
> System przyjmuje tekst oferty pracy i zwraca przewidziana kategorie stanowiska, poziom seniority, confidence oraz prosta flage rekomendacji.

Jesli chcesz wersje jeszcze krotsza:

> Projekt sluzy do klasyfikacji ofert pracy IT na podstawie opisu tekstowego.  
> Zbudowalem pipeline danych, wytrenowalem model, a nastepnie udostepnilem predykcje przez API lokalne i przez AWS.

## Co powiedziec o celu projektu

Najbezpieczniej powiedziec tak:

- projekt mial pokazac pelny pipeline: dane -> preprocessing -> trening modelu -> zapis artefaktow -> endpoint API,
- projekt jest edukacyjny, ale oparty o realny dataset,
- nacisk byl na prostote, czytelnosc i mozliwosc uruchomienia w AWS Academy Learner Lab.

Mozesz dodac:

> Nie chcialem budowac bardzo ciezkiego modelu NLP, tylko lekkie, tanie i latwe do obrony rozwiazanie, ktore naprawde dziala end-to-end.

## Jak pokazac projekt krok po kroku

Najlepsza kolejnosc na obronie:

1. Powiedz w 2-3 zdaniach, jaki jest cel projektu.
2. Pokaz krotko architekture AWS.
3. Powiedz, skad sa dane i jak zostaly przygotowane.
4. Powiedz, jak dziala model.
5. Pokaz AWS.
6. Pokaz dzialajaca predykcje przez lokalny web app lub AWS API.
7. Na koncu powiedz o ograniczeniach i mozliwych rozbudowach.

## Kolejnosc ekranow podczas obrony

Praktyczna kolejnosc:

1. GitHub repo
2. `README.md`
3. S3
4. Glue
5. Athena
6. SageMaker notebook
7. Lambda
8. API Gateway
9. lokalny web app
10. ewentualnie `docs/demo_job_cases.md`

Jesli prowadzacy chce szybciej:

1. architektura,
2. Lambda + API Gateway,
3. web app demo,
4. notebook i metryki.

## Jak wyjasnic architekture

Mozesz powiedziec:

> Architektura jest lekka i tania.  
> Dane treningowe trzymam w Amazon S3.  
> AWS Glue kataloguje dane, a Athena pozwala wykonac podstawowe zapytania SQL bez stawiania bazy danych.  
> W SageMaker Notebook pokazuje przygotowanie i analize danych oraz trening modelu.  
> Sama logika inferencji zostala wdrozona w AWS Lambda, a HTTP endpoint udostepnia API Gateway.

Krotko o rolach uslug:

- `S3` - przechowywanie danych i artefaktow modelu,
- `Glue` - katalog danych,
- `Athena` - analiza danych w SQL,
- `SageMaker Notebook` - eksperymenty, preprocessing i trening,
- `Lambda` - inferencja serverless,
- `API Gateway` - publiczny endpoint REST,
- `FastAPI` - lokalne demo aplikacji.

## Jak wyjasnic dane

Aktualna, dobra odpowiedz:

> Finalny dataset zostal przygotowany na bazie duzego zbioru opisow ofert pracy z Hugging Face.  
> Wybralem duzy dataset, bo daje bardziej realistyczne przyklady niz maly zbior testowy albo dane czysto syntetyczne.  
> Nastepnie przygotowalem dane do formatu potrzebnego w projekcie, czyli przede wszystkim pola `text`, `category` i `level`.

Mozesz dopowiedziec:

- kategorie: `backend`, `frontend`, `data`, `devops`, `other`,
- poziomy: `internship`, `junior`, `regular`, `senior`.

## Jak wyjasnic preprocessing

Najprostsza wersja:

> Tekst oferty jest czyszczony: zamieniany na male litery, usuwane sa zbedne znaki i normalizowane sa spacje.  
> To prosty, klasyczny preprocessing dla modelu tekstowego opartego o TF-IDF.

Jesli padnie pytanie "dlaczego tak prosto?":

> Bo celem bylo pokazanie dzialajacego i czytelnego pipeline'u, a nie budowanie bardzo ciezkiego modelu jezykowego.  
> Dla projektu studenckiego lekki preprocessing i klasyczne modele sa bardziej stabilne i latwiejsze do obrony.

## Jak wyjasnic model

Mozesz powiedziec:

> Uzywam klasycznego podejscia do klasyfikacji tekstu.  
> Najpierw TF-IDF zamienia tekst na wektor cech liczbowych.  
> Potem dwa osobne modele `LogisticRegression` przewiduja:
>
> - kategorie stanowiska,
> - poziom seniority.

Dlaczego dwa modele:

> Rozdzielilem problem na dwie predykcje, bo kategoria roli i poziom seniority to dwa rozne zadania klasyfikacyjne.

## Jak wyjasnic confidence i recommended

`confidence`:

> Confidence jest liczone na podstawie prawdopodobienstw zwracanych przez modele i pokazuje, jak pewna jest predykcja.

`recommended`:

> Flaga `recommended` ma wartosc `true`, gdy przewidziana oferta pasuje do profilu Junior Python Backend Developer, czyli przede wszystkim wtedy, gdy kategoria to `backend`, a poziom to `internship` albo `junior`.

## Jak wyjasnic kod

Najwazniejsze pliki:

- [src/predictor.py](/c:/Users/Asim/Desktop/aws-job-offer-classifier-api/src/predictor.py)
- [src/preprocessing.py](/c:/Users/Asim/Desktop/aws-job-offer-classifier-api/src/preprocessing.py)
- [scripts/train_model.py](/c:/Users/Asim/Desktop/aws-job-offer-classifier-api/scripts/train_model.py)
- [app/main.py](/c:/Users/Asim/Desktop/aws-job-offer-classifier-api/app/main.py)
- [lambda/lambda_function.py](/c:/Users/Asim/Desktop/aws-job-offer-classifier-api/lambda/lambda_function.py)

Jak to opisac:

### `src/preprocessing.py`

- czysci tekst oferty,
- przygotowuje go do wektoryzacji.

### `src/predictor.py`

- laduje wektoryzator i modele,
- wykonuje predykcje,
- liczy confidence,
- stosuje dodatkowe reguly korygujace dla kategorii i seniority.

### `scripts/train_model.py`

- wczytuje dataset,
- dzieli dane na train/test,
- trenuje modele,
- zapisuje artefakty do katalogu `model/`.

### `app/main.py`

- udostepnia lokalne API i prosty web interfejs,
- pozwala szybko pokazac projekt podczas obrony.

### `lambda/lambda_function.py`

- obsluguje request w AWS Lambda,
- pobiera artefakty modelu z S3,
- uruchamia predykcje,
- zwraca odpowiedz JSON.

## Jak wyjasnic deployment w AWS

Mozesz powiedziec:

> Wdrozylem model w architekturze serverless.  
> Artefakty modelu trzymam w S3, a Lambda pobiera je przy uruchomieniu.  
> API Gateway wystawia publiczny endpoint `POST /predict`.

Jesli prowadzacy zapyta, dlaczego model nie jest trzymany bezposrednio w zipie Lambdy:

> Bo artefakty modelu byly stosunkowo duze, a osobne trzymanie ich w S3 jest bardziej elastyczne i blizsze praktyce chmurowej.

## Jak zrobic live demo

Najbezpieczniejszy scenariusz:

1. Otworz lokalny web app.
2. Wklej oferte pracy.
3. Pokaz wynik klasyfikacji.
4. Potem pokaz AWS Lambda test albo API Gateway response.

Mozesz powiedziec:

> Tutaj pokazuje dzialanie systemu od strony uzytkownika.  
> Wklejam tekst oferty, a aplikacja zwraca wynik klasyfikacji wraz z confidence.

## Jak mowic o wynikach

Najbezpieczniej:

> Model daje sensowne wyniki dla wielu ofert, szczegolnie gdy opis jest techniczny i jednoznaczny.  
> Trzeba jednak pamietac, ze role mieszane, na przyklad backend + cloud albo backend + data, sa trudniejsze do rozroznienia.

Mozesz dodac:

> Dlatego poza samym modelem dodalem tez warstwe lekkich regul heurystycznych w `predictor.py`, ktora pomaga poprawic wynik dla praktycznych przypadkow.

## Jak mowic o ograniczeniach

To bardzo wazne, bo brzmi dojrzale:

> Projekt ma kilka ograniczen:
>
> - model jest klasyczny, a nie oparty o nowoczesne embeddingi lub LLM,
> - klasyfikacja ofert mieszanych jest trudniejsza,
> - labelowanie danych treningowych bylo przygotowywane pod potrzeby projektu,
> - to rozwiazanie edukacyjne, a nie produkcyjne.

Ale od razu dodaj:

> Mimo tego projekt spelnia cel dydaktyczny: pokazuje pelny pipeline danych, model ML, wdrozenie API i integracje z AWS.

## Typowe pytania i dobre odpowiedzi

### Dlaczego wybrales Logistic Regression?

> Bo to lekki, szybki i czytelny model do klasyfikacji tekstu.  
> Dobrze pasuje do projektu studenckiego i do danych reprezentowanych przez TF-IDF.

### Dlaczego nie uzyles LLM albo BERT?

> Chcialem zbudowac rozwiazanie tansze, prostsze i latwiejsze do wdrozenia w AWS Academy.  
> Celem bylo pokazanie calego pipeline'u, a nie tylko wysokiej jakosci modelu.

### Gdzie tutaj jest Big Data?

> W projekcie Big Data jest pokazane przez uzycie duzego datasetu oraz uslug danych AWS: S3, Glue i Athena.  
> To uproszczona architektura edukacyjna, ale zgodna z idea pracy na danych w chmurze.

### Dlaczego Lambda zamiast SageMaker endpoint?

> Model jest maly i nie wymaga stalego endpointu inferencyjnego.  
> Lambda jest tansza i prostsza do takiego projektu.

### Jak dziala endpoint?

> Endpoint `POST /predict` przyjmuje JSON z polem `text`, uruchamia preprocessing i model, a potem zwraca wynik klasyfikacji w JSON.

### Co bys poprawil w przyszlosci?

> Uzylbym lepszego modelu tekstowego, bardziej precyzyjnego labelowania danych oraz dodal porzadny monitoring i testowanie endpointu produkcyjnego.

## Jak zakonczyc obrone

Bezpieczne zakonczenie:

> Podsumowujac, projekt spelnia wymagania kursu, bo laczy dane, ETL, machine learning, REST API i wdrozenie w AWS.  
> Najwazniejsze bylo dla mnie pokazanie dzialajacego rozwiazania end-to-end, a nie tylko samego modelu.

Krotsza wersja:

> Projekt dziala od danych do endpointu i pokazuje praktyczne polaczenie ML oraz AWS w jednej aplikacji.

## Czego nie robic na obronie

- nie zaczynaj od bardzo szczegolowego kodu,
- nie tlumacz od razu kazdej biblioteki,
- nie obiecuj, ze model jest idealny,
- nie komplikuj opisu AWS,
- nie pokazuj za duzo ekranow naraz.

## Najlepsza strategia

Najlepiej broni sie ten projekt tak:

- prosto,
- spokojnie,
- technicznie,
- bez przesadnego chwalenia,
- z uczciwym wskazaniem ograniczen.

To brzmi dojrzale i profesjonalnie.
