
import requests
from urllib.parse import quote

BASE_URL = "https://api.open-meteo.com/v1/forecast"


def get_lat_lon(city_name):
    """
    Pobiera szerokość i długość geograficzną miasta korzystając z Nominatim (OpenStreetMap).
    """
    url = f"https://nominatim.openstreetmap.org/search?q={quote(city_name)}&format=json&limit=1"
    try:
        response = requests.get(url, headers={"User-Agent": "weather-app"})
        response.raise_for_status()
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
        else:
            print("Nie znaleziono miasta.")
            return None, None
    except requests.RequestException as e:
        print(f"Błąd podczas pobierania współrzędnych: {e}")
        return None, None

def get_weather(city_name):
    """
    Pobiera dane pogodowe dla podanego miasta z Open-Meteo API.
    """
    lat, lon = get_lat_lon(city_name)
    if lat is None or lon is None:
        return None
    params = {
        'latitude': lat,
        'longitude': lon,
        'current_weather': 'true',
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        data['city'] = city_name
        return data
    except requests.RequestException as e:
        print(f"Błąd podczas pobierania danych pogodowych: {e}")
        return None


def display_weather(data):
    """
    Wyświetla dane pogodowe w czytelny sposób.
    """
    if data and data.get('current_weather'):
        city = data.get('city', 'Nieznane miasto')
        weather = data['current_weather']
        temp = weather['temperature']
        wind = weather['windspeed']
        desc = "Brak opisu (Open-Meteo nie udostępnia opisu)"
        print(f"\nPogoda w {city}:")
        print(f"Temperatura: {temp}°C")
        print(f"Opis: {desc}")
        print(f"Wiatr: {wind} km/h")
    else:
        print("Nie udało się pobrać danych pogodowych.")


def main():
    print("Witaj w aplikacji pogodowej!")
    city = input("Podaj nazwę miasta: ")
    data = get_weather(city)
    display_weather(data)


if __name__ == "__main__":
    main()
