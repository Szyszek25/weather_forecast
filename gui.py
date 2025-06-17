
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageDraw
import io

from weather import get_lat_lon, get_current_weather

# Główna klasa aplikacji GUI
class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikacja Pogodowa")
        self.geometry("400x350")
        self.resizable(False, False)

        # Style
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 10))
        self.style.configure("TButton", font=("Helvetica", 10, "bold"))
        self.style.configure("Result.TLabel", font=("Helvetica", 12, "bold"))

        # Ramka główna
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill="both")

        # Wejście dla miasta
        ttk.Label(main_frame, text="Wpisz miasto:").pack(pady=5)
        self.city_entry = ttk.Entry(main_frame, width=30)
        self.city_entry.pack(pady=5)
        self.city_entry.bind("<Return>", self.fetch_weather)

        # Przycisk
        self.search_button = ttk.Button(main_frame, text="Sprawdź pogodę", command=self.fetch_weather)
        self.search_button.pack(pady=10)

        # Ramka na wyniki
        self.results_frame = ttk.Frame(main_frame, padding="10")
        self.results_frame.pack(pady=10)
        
        self.weather_icon_label = ttk.Label(self.results_frame)
        self.weather_icon_label.pack()

        self.result_city = ttk.Label(self.results_frame, text="", style="Result.TLabel")
        self.result_city.pack()
        self.result_temp = ttk.Label(self.results_frame, text="")
        self.result_temp.pack()
        self.result_wind = ttk.Label(self.results_frame, text="")
        self.result_wind.pack()

    def fetch_weather(self, event=None):
        city = self.city_entry.get()
        if not city:
            messagebox.showwarning("Uwaga", "Proszę wpisać nazwę miasta.")
            return

        lat, lon = get_lat_lon(city)
        if lat is None or lon is None:
            messagebox.showerror("Błąd", f"Nie znaleziono miasta: {city}")
            return

        try:
            weather_data = get_current_weather(lat, lon)
            self.display_weather(city, weather_data)
        except Exception as e:
            messagebox.showerror("Błąd", f"Błąd pobierania danych pogody: {e}")

    def display_weather(self, city, data):
        current_weather = data.get('current_weather', {})
        temp = current_weather.get('temperature', 'N/A')
        wind = current_weather.get('windspeed', 'N/A')
        
        self.result_city.config(text=f"Pogoda dla: {city.capitalize()}")
        self.result_temp.config(text=f"Temperatura: {temp}°C")
        self.result_wind.config(text=f"Wiatr: {wind} km/h")
        
        # Prosta ikona (placeholder)
        self.set_weather_icon(current_weather.get('weathercode', 0))

    def set_weather_icon(self, weather_code):
        # Prosta logika do wyboru ikony na podstawie kodu pogody
        # W przyszłości można to rozbudować o pobieranie ikon z sieci
        icon_data = self.get_icon_for_code(weather_code)
        
        try:
            image = Image.open(io.BytesIO(icon_data))
            image = image.resize((100, 100), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.weather_icon_label.config(image=photo)
            self.weather_icon_label.image = photo
        except Exception as e:
            # Jeśli wystąpi błąd z ikoną, po prostu go ignorujemy
            print(f"Błąd ładowania ikony: {e}")


    def get_icon_for_code(self, code):
        # Zwraca dane binarne prostej ikony w zależności od kodu pogody
        # Słonecznie
        if code in [0, 1]:
            return self.create_sun_icon()
        # Pochmurno
        if code in [2, 3]:
            return self.create_cloud_icon()
        # Deszcz
        if code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
            return self.create_rain_icon()
        # Domyślnie
        return self.create_sun_icon()

    def create_sun_icon(self):
        img = Image.new('RGBA', (100, 100), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse((10, 10, 90, 90), fill='yellow', outline='orange', width=5)
        byte_arr = io.BytesIO()
        img.save(byte_arr, format='PNG')
        return byte_arr.getvalue()

    def create_cloud_icon(self):
        img = Image.new('RGBA', (100, 100), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse((10, 40, 60, 90), fill='lightgrey', outline='grey')
        draw.ellipse((30, 20, 80, 70), fill='lightgrey', outline='grey')
        draw.ellipse((50, 40, 100, 90), fill='lightgrey', outline='grey')
        byte_arr = io.BytesIO()
        img.save(byte_arr, format='PNG')
        return byte_arr.getvalue()
        
    def create_rain_icon(self):
        img = self.create_cloud_icon() # Zaczynamy od chmury
        draw = ImageDraw.Draw(img)
        for i in range(3):
            x = 25 + i * 20
            draw.line((x, 80, x+5, 95), fill='blue', width=3)
        byte_arr = io.BytesIO()
        img.save(byte_arr, format='PNG')
        return byte_arr.getvalue()


if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()
