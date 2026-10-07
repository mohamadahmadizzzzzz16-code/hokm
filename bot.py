import telebot
from telebot import types

# ----------------- تنظیمات -----------------
BOT_TOKEN = "8905355459:AAHrZqJMqWiBnt5h--VuAiJsOW1yHirxG7I"  # توکن ربات از BotFather
CHANNEL_ID = "@xyyje"    # آیدی کانال شما (با @)
CHANNEL_LINK = "https://t.me/xyyje"  # لینک عضویت کانال

# آدرس صفحه بازی شما روی گیت‌هاب:
WEBAPP_URL = "https://mohamadhmadizzzzz16-code.github.io/hokm/"
# -------------------------------------------

bot = telebot.TeleBot(BOT_TOKEN)

def is_user_member(user_id):
    """بررسی عضویت کاربر در کانال"""
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ['creator', 'administrator', 'member']:
            return True
        return False
    except Exception as e:
        print(f"Error checking membership: {e}")
        return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name

    if is_user_member(user_id):
        # اگر کاربر عضو کانال بود: نمایش دکمه ورود به بازی
        markup = types.InlineKeyboardMarkup()
        game_button = types.InlineKeyboardButton(
            text="🃏 شروع بازی حکم (سه‌بعدی)",
            web_app=types.WebAppInfo(url=WEBAPP_URL)
        )
        markup.add(game_button)
        
        bot.send_message(
            message.chat.id,
            f"سلام {first_name} عزیز! خوش آمدید.\nبرای شروع بازی روی دکمه زیر کلیک کنید:",
            reply_markup=markup
        )
    else:
        # اگر عضو نبود: قفل کانال و درخواست عضویت
        markup = types.InlineKeyboardMarkup(row_width=1)
        join_btn = types.InlineKeyboardButton("📢 عضویت در کانال", url=CHANNEL_LINK)
        check_btn = types.InlineKeyboardButton("✅ عضو شدم (بررسی مجدد)", callback_data="check_join")
        markup.add(join_btn, check_btn)

        bot.send_message(
            message.chat.id,
            f"سلام {first_name} عزیز!\n\n⚠️ برای استفاده از بازی، لطفاً ابتدا در کانال ما عضو شوید و سپس دکمه «عضو شدم» را بزنید:",
            reply_markup=markup
        )

@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def check_join_callback(call):
    user_id = call.from_user.id
    
    if is_user_member(user_id):
        # پیام قبلی را حذف یا ویرایش می‌کند
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        # نمایش دکمه بازی
        markup = types.InlineKeyboardMarkup()
        game_button = types.InlineKeyboardButton(
            text="🃏 شروع بازی حکم (سه‌بعدی)",
            web_app=types.WebAppInfo(url=WEBAPP_URL)
        )
        markup.add(game_button)
        
        bot.send_message(
            call.message.chat.id,
            "✅ عضویت شما تایید شد! حالا می‌توانید بازی کنید:",
            reply_markup=markup
        )
    else:
        bot.answer_callback_query(
            call.id,
            "❌ هنوز در کانال عضو نشده‌اید! لطفاً ابتدا عضو شوید.",
            show_alert=True
        )

# روشن نگه‌داشتن همیشگی ربات
bot.infinity_polling()
