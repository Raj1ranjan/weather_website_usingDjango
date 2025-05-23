from django.shortcuts import render
import requests
from datetime import datetime
import os


def home(request):
    weather = {}
    forecast = []
    background_class = "default"

    if request.method == "POST":
        city = request.POST.get("city").strip()
        api_key = os.environ.get("OPENWEATHERMAP_API_KEY")


        print("== DEBUG START ==")
        print("City received:", city)
        print("API Key from env:", api_key)

        # Debug: Check if API key is being read correctly
        print("API Key from env:", api_key)

        if not api_key:
            weather = {'error': "API key is missing. Check environment settings."}
        else:
            current_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            r1 = requests.get(current_url)
            
            print("Weather API response:", r1.text)


            # Debug: Check the actual API response from OpenWeatherMap
            print("Weather API response:", r1.text)

            if r1.status_code == 200:
                data = r1.json()

                weather = {
                    'city': data['name'],
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon'],
                }

                main_weather = data['weather'][0]['main'].lower()

                if 'clear' in main_weather:
                    background_class = 'sunny'
                elif 'clouds' in main_weather:
                    background_class = 'cloudy'
                elif 'rain' in main_weather or 'drizzle' in main_weather:
                    background_class = 'rainy'
                elif 'thunderstorm' in main_weather:
                    background_class = 'stormy'
                elif 'snow' in main_weather:
                    background_class = 'snowy'
                elif 'mist' in main_weather or 'fog' in main_weather:
                    background_class = 'foggy'

                # Get 5-day forecast
                forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
                r2 = requests.get(forecast_url)

                if r2.status_code == 200:
                    data2 = r2.json()
                    seen_dates = set()

                    for item in data2['list']:
                        dt_txt = item['dt_txt']
                        date = dt_txt.split()[0]
                        time = dt_txt.split()[1]

                        if time == "12:00:00" and date not in seen_dates:
                            seen_dates.add(date)
                            forecast.append({
                                'date': datetime.strptime(date, "%Y-%m-%d").strftime("%a %d %b"),
                                'temp': item['main']['temp'],
                                'desc': item['weather'][0]['description'],
                                'icon': item['weather'][0]['icon']
                            })
            else:
                weather = {'error': "City not found. Please try again."}

    return render(request, 'home.html', {
        'weather': weather,
        'forecast': forecast,
        'background_class': background_class
    })
print("API key:", repr('OPENWEATHERMAP_API_KEY'))  # Shows even if it's empty or has spaces
