import constants
import telebot
import requests
from telebot.types import Message
from telebot import types

message = Message
bot = telebot.TeleBot(constants.API_TOKEN)
markup_location = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
user_location = telebot.types.KeyboardButton('Send Location', request_location=True)
markup_location.add(user_location)

weather_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
current_day_weather = types.KeyboardButton('What the weather?')
weather_markup.add(current_day_weather)


@bot.message_handler(commands=['start'])
def start_message(message):
    user_name = message.chat.first_name
    bot.send_message(message.chat.id, f"Hello {user_name}! I'm happy that you choose Me!")
    bot.send_message(message.chat.id, "To get started I need your location. Please send location",
                     reply_markup=markup_location)


@bot.message_handler(content_types=['location'])
def get_the_weather(message):
    user_name = message.chat.first_name
    latitude = message.location.latitude
    longitude = message.location.longitude
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?appid=84ab65202ce25088f419b99eb4d7c1e2&lat={latitude}&lon={longitude}&units=metric"
    res = requests.get(weather_url)
    data = res.json()
    temperature = data['main']['temp']  # температура
    description = data['weather'][0]['description']  # опис
    humidity = data['main']['humidity']  # вологість
    wind_speed = data['wind']['speed']  # швидкість вітру
    location = data['name']  # місце знаходження
    if location == '':
        location = "Somewhere"
    bot.send_message(message.chat.id, f"""
    {user_name}, the forecast in {location} is:

        Temperature: {temperature} C°
        Description: {description}.
        Humidity: {humidity} %.
        Wind speed: {wind_speed} m/s.""", reply_markup=markup_location)


bot.polling()
