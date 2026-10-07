import os
import threading
from flask import Flask
import telebot
from telebot import types

BOT_TOKEN = "8905355459:AAHrZqJMqWiBnt5h--VuAiJsOW1yHirxG7I"
CHANNEL_ID = "@xyyjeآیدی_کانال_خودت"  # آیدی کانالت را اینجا بنویس
WEBAPP_URL = "https://mohamadhmadizzzzz16-code.github.io/hokm/"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# سرور وب برای روشن ماندن در Render
@app.route('/')
def home():
    return "Bot is running!"

# تابع چک کردن عضویت
def is_user_member(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        # وضعیت‌هایی که یعنی کاربر عضو است
        return member.status in ['creator', 'administrator', 'member']
    except:
        return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if is_user_member(user_id):
        # اگر عضو بود، دکمه شروع بازی را نشان بده
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🃏 شروع بازی حکم", web_app=types.WebAppInfo(url=WEBAPP_URL)))
        bot.send_message(message.chat.id, "خوش آمدی! بازی آماده است.", reply_markup=markup)
    else:
        # اگر عضو نبود، لینک کانال را بده
        bot.send_message(message.chat.id, f"برای بازی ابتدا باید در کانال ما عضو شوی:\n{CHANNEL_ID}")

if __name__ == "__main__":
    threading.Thread(target=bot.infinity_polling).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
