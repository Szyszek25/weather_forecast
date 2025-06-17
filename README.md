# Aplikacja Pogody

To prosta aplikacja w Pythonie, która pobiera i wyświetla aktualną pogodę dla wybranego miasta, korzystając z darmowego API Open-Meteo (https://open-meteo.com/). Nie wymaga klucza API ani rejestracji. Projekt został rozbudowany o prosty interfejs graficzny (Tkinter), obsługę prognozy na kilka dni oraz przykładowy skrypt w Node.js.

## Uruchomienie
1. Zainstaluj wymagane biblioteki Pythona:
   ```bash
   pip install -r requirements.txt
   ```
2. Aby uruchomić aplikację w trybie tekstowym:
   ```bash
   python main.py Warszawa -d 3
   ```
   Możesz pominąć nazwę miasta, aby podać ją podczas działania programu.
3. (Opcjonalnie) uruchom prosty interfejs graficzny:
   ```bash
   python gui.py
   ```
4. (Opcjonalnie) przykład w Node.js:
   ```bash
   node weather.js Warszawa
   ```

## Jak to działa?
- Program pobiera współrzędne geograficzne miasta przez OpenStreetMap (Nominatim).
- Następnie pobiera aktualną pogodę z Open-Meteo na podstawie tych współrzędnych.

## Funkcjonalności
- Pobieranie aktualnej pogody dla wybranego miasta.
- Wyświetlanie temperatury, prędkości wiatru i podstawowych informacji.
- Prognoza na dowolną liczbę dni (parametr `-d`).
- Prosty interfejs graficzny (Tkinter).
- Dodatkowy skrypt `weather.js` pokazujący, jak pobrać dane w Node.js.
- Brak potrzeby rejestracji ani klucza API.

---

Projekt startowy utworzony automatycznie. Aktualizacja: czerwiec 2025.
