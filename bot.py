import os
from threading import Thread
from flask import Flask
import telebot

# توکن شما
TOKEN = '8613666293:AAEICgMQtjjS2uVerhOr71kRh-tvGNGRQr0'
bot = telebot.TeleBot(TOKEN)

# سرور وب کوچک برای فعال نگه داشتن ربات در رندر
app = Flask('')


@app.route('/')
def home():
  return 'Bot is active and running!'


def run_web():
  port = int(os.environ.get('PORT', 10000))
  app.run(host='0.0.0.0', port=port)


# دستورات ربات شما
@bot.message_handler(commands=['start'])
def send_welcome(message):
  bot.reply_to(message, 'سلام! ربات با موفقیت روشن شد.')


# اجرای همزمان سرور وب و ربات تلگرام
if __name__ == '__main__':
  t = Thread(target=run_web)
  t.start()
  bot.infinity_polling()
