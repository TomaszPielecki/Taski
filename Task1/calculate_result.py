"""
Skrypt do obliczenia wyniku dla zadania rekrutacyjnego.
Wymaga pliku: find_match_average_v2.dat.lz4

Instalacja lz4 (jeśli potrzebna): pip install lz4

WYNIK: 666172.0
"""

import lz4.frame
import os
from solution import task2


def main():
    # Wczytaj i dekompresuj plik
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'find_match_average_v2.dat.lz4')
    
    with open(file_path, 'rb') as f:
        compressed_data = f.read()
    
    data = lz4.frame.decompress(compressed_data).decode('utf-8')
    
    # Klucze z zadania
    search_list = [
        {'a': 862984, 'b': 29105, 'c': 605280, 'd': 678194, 'e': 302120},
        {'a': 20226, 'b': 781899, 'c': 186952, 'd': 506894, 'e': 325696}
    ]
    
    # Oblicz wynik
    result = task2(search_list, data)
    
    print(f"Wynik task2: {result}")
    return result


if __name__ == "__main__":
    main()
