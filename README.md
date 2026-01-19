# Zadanie Rekrutacyjne - Backend Python Junior

**Autor:** Tomasz Pielecki

## Opis

Rozwiązanie zadania rekrutacyjnego - przetwarzanie danych CSV z wyszukiwaniem i obliczaniem średniej ważonej.

## Funkcje

### `task1(search: dict, data: str) -> str`
Znajduje pierwszy wiersz pasujący do wszystkich par klucz-wartość z `search`.
- Zwraca wartość z kolumny `value` jako string
- Zwraca `'-1'` jeśli nie znaleziono
- Rzuca `Exception("Key mismatch")` gdy klucz nie istnieje w nagłówku

### `task2(search_list: list, data: str) -> str`
Oblicza średnią ważoną dla wartości znalezionych wierszy.
- Waga = **10** dla wartości nieparzystych
- Waga = **20** dla wartości parzystych
- Zwraca wynik zaokrąglony do 1 miejsca po przecinku jako string

## Wynik

```
666172.0
```

## Wymagania

- Python 3.10+
- Tylko biblioteka standardowa
