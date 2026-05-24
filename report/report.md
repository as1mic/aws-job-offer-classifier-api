# Raport projektu: AWS Job Offer Classifier API

## 1. Cel projektu

Celem projektu bylo stworzenie prostego systemu REST API, ktory klasyfikuje oferty pracy na podstawie tekstu ogloszenia. Aplikacja przewiduje kategorie stanowiska, poziom seniority, poziom pewnosci predykcji oraz flage `recommended` dla profilu Junior Python Backend Developer.

Projekt zostal przygotowany jako rozwiazanie edukacyjne na kurs AWS i mial spelniac wymagania zwiazane z uzyciem uslug chmurowych, przetwarzaniem danych, elementem Big Data oraz modelem Machine Learning.

## 2. Opis rozwiazania

Rozwiazanie sklada sie z kilku etapow. Najpierw pobierany jest duzy zbior opisow ofert pracy z platformy Hugging Face. Nastepnie dane sa przeksztalcane do formatu projektu, czyszczone i przygotowywane do uczenia modelu. W kolejnym kroku trenowane sa dwa modele klasyfikacyjne: pierwszy przewiduje kategorie oferty, a drugi poziom stanowiska.

Gotowe artefakty modelu sa zapisywane do plikow i wykorzystywane przez funkcje AWS Lambda. Lambda jest polaczona z API Gateway, dzieki czemu uzytkownik moze wyslac zadanie HTTP i otrzymac odpowiedz JSON.

## 3. Architektura AWS

Architektura projektu zostala zaprojektowana jako lekka i tania w utrzymaniu. Dane wejsciowe sa przechowywane w Amazon S3. Metadane o zbiorze sa budowane w AWS Glue. Analiza SQL jest wykonywana w Amazon Athena. Trening modelu i analiza danych odbywaja sie w SageMaker Notebook. Model inferencyjny jest uruchamiany w AWS Lambda, a endpoint publiczny jest wystawiony przez API Gateway.

Takie podejscie pozwala pokazac pelny pipeline danych i ML bez uzycia drogich uslug infrastrukturalnych.

## 4. Wykorzystane uslugi AWS

- Amazon S3 do przechowywania danych i artefaktow modelu
- AWS Glue do katalogowania danych
- Amazon Athena do analizy danych z uzyciem SQL
- Amazon SageMaker Notebook do przetwarzania danych i treningu modelu
- AWS Lambda do uruchamiania predykcji
- Amazon API Gateway do udostepnienia REST API

## 5. Dataset

W finalnej wersji projektu wykorzystano duzy zbior danych pochodzacy z Hugging Face: `lang-uk/recruitment-dataset-job-descriptions-english`. Zbior zawiera opisy prawdziwych ofert pracy w jezyku angielskim i zostal przeksztalcony do formatu projektu.

Na potrzeby modelu przygotowano plik treningowy zawierajacy pola `text`, `category` i `level`. Kategorie obejmuja: backend, frontend, data, devops i other. Poziomy obejmuja: internship, junior, regular oraz senior.

Zaleta tego podejscia jest znacznie wieksza liczba rekordow i wiekszy realizm danych niz w malych zbiorach testowych czy danych syntetycznych.

## 6. Proces ETL / przetwarzanie danych

Proces ETL obejmuje pobranie surowego zbioru z Hugging Face, zapis do pliku CSV, wybor rekordow anglojezycznych, przeksztalcenie ich do wspolnego formatu projektu oraz przygotowanie etykiet `category` i `level`.

Tekst jest nastepnie czyszczony, zamieniany na male litery, usuwane sa zbedne znaki oraz nadmiarowe spacje. Na koncu dane sa dzielone na zbiory treningowe i testowe.

W warstwie AWS dane moga zostac przeslane do S3, skatalogowane przez Glue i analizowane w Athena przed treningiem modelu w SageMaker Notebook.

## 7. Model ML

W projekcie wykorzystano klasyczne podejscie do klasyfikacji tekstu. Tekst jest reprezentowany za pomoca TF-IDF, a nastepnie przetwarzany przez modele `LogisticRegression`. Zastosowano dwa osobne modele: dla kategorii oferty oraz dla poziomu stanowiska.

Dodatkowo zastosowano prosty warstwowy post-processing oparty na regulach, aby lepiej rozrozniac poziom stanowiska i czesc mieszanych kategorii.

## 8. REST API

REST API przyjmuje tekst ogloszenia pracy i zwraca wynik klasyfikacji w formacie JSON. Odpowiedz zawiera przewidywana kategorie, poziom, wartosc confidence oraz pole `recommended`. Logika `recommended` jest prosta: ma wartosc `true`, gdy przewidywana kategoria to backend, a poziom to internship lub junior.

API zostalo przygotowane do dzialania lokalnie oraz w srodowisku AWS poprzez Lambda + API Gateway.

## 9. Testy endpointu

Endpoint moze byc testowany lokalnie na przykladowych tekstach oraz w AWS przez test event funkcji Lambda lub przez zadanie HTTP do API Gateway. Dodatkowo przygotowano testy jednostkowe `pytest`, ktore sprawdzaja poprawnosc preprocessingu oraz strukture wynikow predykcji.

## 10. Analiza wynikow

Model byl oceniany przy uzyciu accuracy, precision, recall oraz F1-score. Dodatkowo zapisano classification report i confusion matrix. Wyniki sa nizsze niz w przypadku prostych danych syntetycznych, ale lepiej oddaja rzeczywiste zachowanie modelu na prawdziwych ofertach pracy.

To podejscie jest bardziej wartosciowe edukacyjnie, poniewaz pokazuje zarowno mocne strony modelu, jak i jego ograniczenia przy pracy z realnymi, bardziej zroznicowanymi danymi.

## 11. Wnioski

Projekt spelnia wymagania kursowe i pokazuje polaczenie uslug AWS, przetwarzania danych, analizy oraz modelu ML w jednym rozwiazaniu. Architektura zostala swiadomie uproszczona, aby byla tania, czytelna i mozliwa do uruchomienia w AWS Academy Learner Lab.

W przyszlosci projekt mozna rozbudowac o lepsze mapowanie etykiet, reczna walidacje czesci rekordow, bardziej zaawansowany model oraz monitoring predykcji.

## 12. Link do repozytorium

Tutaj nalezy wkleic link do zdalnego repozytorium GitHub po jego utworzeniu.
