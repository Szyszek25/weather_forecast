"""Command line weather application."""

import argparse

from weather import get_lat_lon, get_current_weather, get_daily_forecast


def display_current(city: str, data: dict):
    """Pretty print current weather information."""
    if not data or "current_weather" not in data:
        print("Nie udało się pobrać danych pogodowych.")
        return
    weather = data["current_weather"]
    print(f"\nPogoda w {city}:")
    print(f"Temperatura: {weather['temperature']}°C")
    print(f"Wiatr: {weather['windspeed']} km/h")


def display_forecast(forecast: dict):
    """Display simple daily forecast."""
    days = forecast.get("daily", {})
    dates = days.get("time", [])
    tmax = days.get("temperature_2m_max", [])
    tmin = days.get("temperature_2m_min", [])
    if not dates:
        return
    print("\nPrognoza:")
    for date, mx, mn in zip(dates, tmax, tmin):
        print(f"{date}: {mn}°C - {mx}°C")


def main():
    parser = argparse.ArgumentParser(description="Aplikacja pogodowa")
    parser.add_argument("city", nargs="?", help="Nazwa miasta")
    parser.add_argument("-d", "--days", type=int, default=0,
                        help="Liczba dni prognozy (0 = tylko bieżąca pogoda)")
    args = parser.parse_args()

    city = args.city or input("Podaj nazwę miasta: ")
    lat, lon = get_lat_lon(city)
    if lat is None or lon is None:
        print("Nie znaleziono miasta.")
        return

    current = get_current_weather(lat, lon)
    display_current(city, current)

    if args.days > 0:
        forecast = get_daily_forecast(lat, lon, args.days)
        display_forecast(forecast)


if __name__ == "__main__":
    main()
