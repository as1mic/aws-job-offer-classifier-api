# Pytania od prowadzacego i krotkie odpowiedzi

## Dlaczego wybrales ten temat?

To praktyczny temat laczacy analize tekstu, machine learning i REST API. Dodatkowo latwo go pokazac na AWS w prosty sposob.

## Jak dziala model?

Najpierw tekst jest czyszczony, potem TF-IDF zamienia go na wektor cech. Na koncu dwa modele Logistic Regression przewiduja kategorie i poziom stanowiska.

## Co oznacza TF-IDF?

To metoda reprezentacji tekstu. Pokazuje, jak wazne jest dane slowo w dokumencie wzgledem calego zbioru danych.

## Jakie uslugi AWS zostaly uzyte?

Amazon S3, AWS Glue, Amazon Athena, Amazon SageMaker Notebook, AWS Lambda oraz Amazon API Gateway.

## Gdzie tutaj jest Big Data?

Element Big Data pokazuje przez uzycie duzego zewnetrznego datasetu oraz uslug danych AWS: S3 jako data lake, Glue jako katalog danych i Athena do analizy SQL nad danymi w S3.

## Czy to sa prawdziwe Big Data?

Nie w sensie bardzo duzej skali produkcyjnej. To edukacyjna, uproszczona wersja architektury Big Data, dopasowana do budzetu AWS Academy.

## Skad pochodzi dataset?

Finalny dataset zostal przygotowany na bazie duzego zbioru opisow ofert pracy z Hugging Face. Nastepnie dane zostaly przeksztalcone do formatu potrzebnego do treningu modelu.

## Dlaczego wybrales wiekszy dataset?

Wiekszy dataset daje bardziej realistyczne przyklady i lepiej pokazuje zachowanie modelu na prawdziwych ofertach pracy. Dzieki temu projekt jest bardziej wiarygodny niz przy malym zbiorze testowym.

## Jak oceniales model?

Uzylem accuracy, precision, recall, F1-score, classification report oraz confusion matrix.

## Dlaczego Lambda zamiast SageMaker endpoint?

Lambda jest tansza i prostsza do projektu studenckiego. Model jest maly, wiec nie potrzebuje stalego endpointu inferencyjnego.

## Jak dziala recommended?

Flaga ma wartosc `true`, jesli model przewidzi kategorie `backend` oraz poziom `internship` albo `junior`.

## Jakie sa ograniczenia projektu?

Mimo duzego datasetu model nadal jest prosty i nie zawsze idealnie rozroznia role mieszane, na przyklad backend z elementami cloud lub data. Projekt jest celowo prosty, bo ma byc tani i latwy do wyjasnienia.
