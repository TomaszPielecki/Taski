# Zadanie Rekrutacyjne - Backend Python Junior

**Autor:** Tomasz Pielecki

## 📋 Opis projektu

Rozwiązanie zadania rekrutacyjnego obejmującego przetwarzanie danych CSV z wyszukiwaniem i obliczaniem średniej ważonej.

## 🗂️ Struktura projektu

```
Taski/
├── README.md
├── Task1/
│   ├── solution.py              # Główny kod z funkcjami task1() i task2()
│   ├── calculate_result.py      # Skrypt uruchamiający z danymi testowymi
│   └── find_match_average_v2.dat.lz4  # Skompresowane dane testowe
└── Task2/
    └── solution.py              # Kopia rozwiązania
```

## 🚀 Uruchomienie

### Wymagania
- Python 3.10+
- Biblioteka `lz4`

### Instalacja zależności
```bash
pip install lz4
```

### ⚠️ Plik danych
Plik `find_match_average_v2.dat.lz4` należy pobrać z linku podanego w zadaniu rekrutacyjnym i umieścić w folderze `Task1/`.

### Uruchomienie testów
```bash
cd Task1
python solution.py
```

### Obliczenie wyniku dla danych testowych
```bash
cd Task1
python calculate_result.py
```

## 📝 Funkcje

### `task1(search: dict, data: str) -> str`
Znajduje **pierwszy wiersz** pasujący do wszystkich par klucz-wartość z `search`.

**Przykład:**
```python
data = 'side,currency,value\nIN,PLN,1\nIN,EUR,2'
result = task1({'side': 'IN', 'currency': 'PLN'}, data)
# Wynik: '1'
```

### `task2(search_list: list, data: str) -> str`
Oblicza **średnią ważoną** dla wartości znalezionych wierszy.
- Waga = **10** dla wartości nieparzystych
- Waga = **20** dla wartości parzystych

**Przykład:**
```python
search_list = [
    {'side': 'IN', 'currency': 'PLN'},  # value=1 (nieparzyste, waga=10)
    {'side': 'IN', 'currency': 'EUR'},  # value=2 (parzyste, waga=20)
]
result = task2(search_list, data)
# Wynik: '1.7'  (średnia ważona: (1*10 + 2*20) / 30 = 1.667)
```

## ✅ Wynik zadania

**Wynik task2 dla pliku `find_match_average_v2.dat.lz4`:**

```
666172.0
```

**Klucze użyte do obliczeń:**
```python
{'a': 862984, 'b': 29105, 'c': 605280, 'd': 678194, 'e': 302120}
{'a': 20226, 'b': 781899, 'c': 186952, 'd': 506894, 'e': 325696}
```

## 🧪 Testy

Wszystkie testy jednostkowe przechodzą pomyślnie:
- ✅ task1 - wyszukiwanie istniejących wartości
- ✅ task1 - zwracanie '-1' dla nieistniejących
- ✅ task1 - walidacja "Key mismatch"
- ✅ task2 - średnia ważona z jednym wynikiem
- ✅ task2 - średnia ważona z wieloma wynikami

## ⚡ Optymalizacje

- **Cache nagłówków** - parsowanie nagłówka tylko raz
- **Jedno przejście przez dane** - dla task2 wszystkie wyszukiwania w jednej iteracji
- **Early exit** - zatrzymanie gdy wszystkie wartości znalezione
