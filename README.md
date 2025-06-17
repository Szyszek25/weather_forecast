# Aplikacja Pogody

To prosta aplikacja w Pythonie, która pobiera i wyświetla aktualną pogodę dla wybranego miasta, korzystając z darmowego API Open-Meteo (https://open-meteo.com/). Nie wymaga klucza API ani rejestracji.

## Uruchomienie
1. Zainstaluj wymagane biblioteki:
   ```bash
   pip install requests
   ```
2. Uruchom skrypt:
   ```bash
   python main.py
   ```

## Jak to działa?
- Program pobiera współrzędne geograficzne miasta przez OpenStreetMap (Nominatim).
- Następnie pobiera aktualną pogodę z Open-Meteo na podstawie tych współrzędnych.

## Funkcjonalności
- Pobieranie aktualnej pogody dla wybranego miasta.
- Wyświetlanie temperatury, prędkości wiatru i podstawowych informacji.
- Brak potrzeby rejestracji ani klucza API.

---

Projekt startowy utworzony automatycznie. Aktualizacja: czerwiec 2025.
