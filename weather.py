import requests # type: ignore
from datetime import datetime

# c помощью  API получаем координаты необходимого города
def get_coords(city: str):
      url_for_coord = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
      coord = requests.get(url_for_coord)
      if coord.status_code == 200:
            coord = coord.json()
            if coord['results']:
                  latitude = coord['results'][0]['latitude']
                  longitude = coord['results'][0]['longitude']
                  return latitude, longitude
            else: 
                  return None
      elif coord.status_code == 400:
            return 400
      elif coord.status_code == 500:
            return 500
      else:
            return -1
# -------------------------------------

# подставляем координаты в API и получаем необходимые параметры
def get_weather(latitude, longitude):
      url_for_weather = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,wind_speed_10m&timezone=auto&forecast_days=1"
      weather = requests.get(url_for_weather)
      if weather.status_code == 200:
            weather = weather.json()
            time = weather['current']['time'] 
            time = datetime.fromisoformat(time) # создаём объект datetime и форматируем время в более удобном варианте
            time_formatted = time.strftime("%d.%m.%Y %H:%M")
            temperature = weather['current']['temperature_2m']
            humidity = weather['current']['relative_humidity_2m']
            wind_speed = weather['current']['wind_speed_10m']

            return time_formatted, temperature, humidity, wind_speed
      elif weather.status_code == 400:
            return 400
      elif weather.status_code == 500:
            return 500
      else:
            return -1

city = input("Введите город: ")
coords = get_coords(city)

if coords == 400:
      print("Неправильный запрос!")
elif coords == 500:
      print("Ошибка сервера!")
elif coords == -1:
      print("Не удалось получить данные!")
elif coords is None:
      print("Город не найден!")
else:
      weather = get_weather(coords[0], coords[1])
      if weather == 400:
            print("Неправильный запрос!")
      elif weather == 500:
            print("Ошибка сервера!")
      elif weather == -1:
            print("Не удалось получить данные!")
      
      else:
            print(f"""
                  Город: {city}
                  ----------
                  
                  Текущее время: {weather[0]}
                  Температура: {weather[1]} °C
                  Влажность: {weather[2]} %
                  Скорость ветра: {weather[3]} км/ч
                  """)