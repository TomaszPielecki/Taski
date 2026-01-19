"""
Zadanie rekrutacyjne - Backend Python Junior
Autor: Tomasz Pielecki
"""


# Cache dla nagłówków - klucz to pierwsza linia danych
_header_cache = {}


def _normalize_data(data: str) -> str:
    """Normalizuje line endings do \n."""
    return data.replace('\r\n', '\n').replace('\r', '\n')


def _parse_header(data: str) -> tuple[dict[str, int], int, int]:
    """
    Parsuje nagłówek i zwraca indeksy kolumn oraz pozycję początku danych.
    Zwraca: (column_indexes, value_index, data_start_position)
    """
    newline_pos = data.index('\n')
    header_line = data[:newline_pos]
    columns = header_line.split(',')
    
    column_indexes = {col: idx for idx, col in enumerate(columns)}
    value_index = column_indexes['value']
    
    return column_indexes, value_index, newline_pos + 1


def _get_cached_header(data: str) -> tuple[dict[str, int], int, int]:
    """
    Cachuje sparsowany nagłówek na podstawie pierwszej linii.
    """
    global _header_cache
    
    newline_pos = data.index('\n')
    header_key = data[:newline_pos]
    
    if header_key not in _header_cache:
        _header_cache[header_key] = _parse_header(data)
    
    return _header_cache[header_key]


def task1(search: dict, data: str) -> str:
    """
    Znajduje pierwszy wiersz pasujący do wszystkich par klucz-wartość z search.
    Zwraca wartość z kolumny 'value' lub '-1' jeśli nie znaleziono.
    
    Args:
        search: Słownik z parami klucz-wartość do wyszukania
        data: Dane w formacie CSV jako string
        
    Returns:
        Wartość z kolumny 'value' jako string lub '-1'
        
    Raises:
        Exception: Gdy klucz z search nie istnieje w nagłówku
    """
    # Normalizuj line endings
    data = _normalize_data(data)
    
    column_indexes, value_index, data_start = _get_cached_header(data)
    
    # Walidacja kluczy - sprawdź czy wszystkie klucze z search są w nagłówku
    for key in search:
        if key not in column_indexes:
            raise Exception("Key mismatch")
    
    # Przygotuj listę (indeks_kolumny, oczekiwana_wartość) dla szybkiego porównania
    search_pairs = [(column_indexes[k], str(v)) for k, v in search.items()]
    num_columns = len(column_indexes)
    
    # Iteruj linia po linii bez ładowania całości do pamięci
    pos = data_start
    data_len = len(data)
    
    while pos < data_len:
        # Znajdź koniec linii
        newline_pos = data.find('\n', pos)
        if newline_pos == -1:
            newline_pos = data_len
        
        # Pomiń puste linie
        if newline_pos == pos:
            pos = newline_pos + 1
            continue
        
        line = data[pos:newline_pos]
        pos = newline_pos + 1
        
        # Parsuj wiersz - split tylko raz
        values = line.split(',')
        
        # Sprawdź czy wszystkie warunki są spełnione
        match = True
        for col_idx, expected_val in search_pairs:
            if col_idx >= len(values) or values[col_idx] != expected_val:
                match = False
                break
        
        if match:
            return values[value_index]
    
    return '-1'


def task2(search_list: list, data: str) -> str:
    """
    Oblicza średnią ważoną dla wartości znalezionych wierszy.
    Waga = 10 dla wartości nieparzystych, 20 dla parzystych.
    
    Args:
        search_list: Lista słowników z warunkami wyszukiwania
        data: Dane w formacie CSV jako string
        
    Returns:
        Średnia ważona zaokrąglona do 1 miejsca po przecinku jako string
    """
    # Normalizuj line endings
    data = _normalize_data(data)
    
    column_indexes, value_index, data_start = _get_cached_header(data)
    
    # Walidacja wszystkich kluczy z góry
    for search in search_list:
        for key in search:
            if key not in column_indexes:
                raise Exception("Key mismatch")
    
    # Przygotuj wszystkie warunki wyszukiwania jako tuple (lista par indeks-wartość)
    search_conditions = []
    for search in search_list:
        pairs = tuple((column_indexes[k], str(v)) for k, v in search.items())
        search_conditions.append(pairs)
    
    # Set do śledzenia które wyszukiwania już znalazły dopasowanie
    # (każde wyszukiwanie znajduje tylko PIERWSZY pasujący wiersz)
    found_indices = set()
    found_values = []
    
    num_searches = len(search_conditions)
    
    # Iteruj przez dane tylko raz
    pos = data_start
    data_len = len(data)
    
    while pos < data_len and len(found_indices) < num_searches:
        # Znajdź koniec linii
        newline_pos = data.find('\n', pos)
        if newline_pos == -1:
            newline_pos = data_len
        
        # Pomiń puste linie
        if newline_pos == pos:
            pos = newline_pos + 1
            continue
        
        line = data[pos:newline_pos]
        pos = newline_pos + 1
        
        # Parsuj wiersz
        values = line.split(',')
        
        # Sprawdź każde nieznalezione wyszukiwanie
        for search_idx, search_pairs in enumerate(search_conditions):
            if search_idx in found_indices:
                continue
            
            # Sprawdź czy wszystkie warunki są spełnione
            match = True
            for col_idx, expected_val in search_pairs:
                if col_idx >= len(values) or values[col_idx] != expected_val:
                    match = False
                    break
            
            if match:
                found_indices.add(search_idx)
                found_values.append(int(values[value_index]))
    
    # Oblicz średnią ważoną
    if not found_values:
        return "0.0"
    
    weighted_sum = 0
    total_weight = 0
    
    for value in found_values:
        weight = 10 if value % 2 == 1 else 20  # 10 dla nieparzystych, 20 dla parzystych
        weighted_sum += value * weight
        total_weight += weight
    
    if total_weight == 0:
        return "0.0"
    
    result = weighted_sum / total_weight
    
    # Zaokrąglij do 1 miejsca po przecinku
    return f"{result:.1f}"


# Testy lokalne
if __name__ == "__main__":
    # Test task1
    data = 'side,currency,value\nIN,PLN,1\nIN,EUR,2\nOUT,ANY,3'
    
    assert task1({'side': 'IN', 'currency': 'PLN'}, data) == '1', "Test 1 failed"
    assert task1({'side': 'IN', 'currency': 'GBP'}, data) == '-1', "Test 2 failed"
    assert task1({'side': 'OUT', 'currency': 'ANY'}, data) == '3', "Test 3 failed"
    assert task1({'side': 'IN', 'currency': 'EUR'}, data) == '2', "Test 4 failed"
    
    # Test Key mismatch
    try:
        task1({'side': 'IN', 'invalid_key': 'X'}, data)
        assert False, "Should have raised exception"
    except Exception as e:
        assert str(e) == "Key mismatch", "Wrong exception message"
    
    # Test task2
    result = task2(
        [
            {'side': 'IN', 'currency': 'PLN'},
            {'side': 'OUT', 'currency': 'EUR'},
        ],
        data
    )
    # value=1 (odd, weight=10): 1*10 = 10
    # {'side': 'OUT', 'currency': 'EUR'} - nie istnieje, pomijamy
    # weighted_avg = 10 / 10 = 1.0
    assert result == "1.0", f"Test task2 failed: got {result}"
    
    # Test task2 z wieloma dopasowaniami
    result2 = task2(
        [
            {'side': 'IN', 'currency': 'PLN'},  # value=1 (odd, w=10)
            {'side': 'IN', 'currency': 'EUR'},  # value=2 (even, w=20)
        ],
        data
    )
    # weighted_avg = (1*10 + 2*20) / (10+20) = 50/30 = 1.666... ≈ 1.7
    assert result2 == "1.7", f"Test task2 multiple failed: got {result2}"
    
    print("Wszystkie testy lokalne przeszły pomyślnie!")
