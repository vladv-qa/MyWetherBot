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


@bot.message_handler(commands=['start'])
def start_message(message):
    user_name = message.chat.first_name
    bot.send_message(message.chat.id, f"Hello {user_name}! I'm happy that you choose Me!")
    bot.send_message(message.chat.id, "To get started I need your location. Please send location",  reply_markup=markup_location)

@bot.message_handler(content_types=['location'])
def get_user_location(message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    weather_url = f"api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}"

    return print(weather_url)

bot.polling()
