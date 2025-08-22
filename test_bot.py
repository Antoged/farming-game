#!/usr/bin/env python3
"""
Тестовый бот без Mini App для проверки работы
Основной URL игры: https://antoged.github.io/farming-game/
Telegram Mini App: https://antoged.github.io/farming-game/telegram-app.html
"""

import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    
    welcome_text = f"""
🌾 Добро пожаловать в Фермерскую игру, {user.first_name}!

🎮 Это тестовая версия бота без Mini App.
📱 Для полной версии нужен HTTPS URL.

🔧 Статус: Тестовый режим
"""
    
    keyboard = [
        [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
        [InlineKeyboardButton("🏪 Магазин", callback_data="shop")],
        [InlineKeyboardButton("🌤️ Погода", callback_data="weather")],
        [InlineKeyboardButton("❓ Помощь", callback_data="help")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик кнопок"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "stats":
        keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("📊 Статистика:\n💰 Деньги: 100\n🌱 Уровень: 1\n📦 Инвентарь: 0", reply_markup=reply_markup)
    elif query.data == "shop":
        keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🏪 Магазин:\n🥕 Морковь: 10 монет\n🍅 Помидор: 20 монет\n🥔 Картофель: 15 монет", reply_markup=reply_markup)
    elif query.data == "weather":
        keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🌤️ Погода:\n☀️ Ясно\n📈 Множитель цены: 1.0x", reply_markup=reply_markup)
    elif query.data == "help":
        keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("❓ Помощь:\n/start - Главное меню\n/stats - Статистика\n/shop - Магазин\n/weather - Погода", reply_markup=reply_markup)
    elif query.data == "back_to_main":
        # Возвращаемся к главному меню
        welcome_text = f"""
🌾 Добро пожаловать в Фермерскую игру!

🎮 Это тестовая версия бота без Mini App.
📱 Для полной версии нужен HTTPS URL.

🔧 Статус: Тестовый режим
"""
        keyboard = [
            [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
            [InlineKeyboardButton("🏪 Магазин", callback_data="shop")],
            [InlineKeyboardButton("🌤️ Погода", callback_data="weather")],
            [InlineKeyboardButton("❓ Помощь", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(welcome_text, reply_markup=reply_markup)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда статистики"""
    keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📊 Ваша статистика:\n💰 Деньги: 100\n🌱 Уровень: 1\n📦 Инвентарь: 0", reply_markup=reply_markup)

async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда магазина"""
    keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🏪 Товары в магазине:\n🥕 Морковь: 10 монет\n🍅 Помидор: 20 монет\n🥔 Картофель: 15 монет", reply_markup=reply_markup)

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда погоды"""
    keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🌤️ Текущая погода:\n☀️ Ясно\n📈 Множитель цены: 1.0x", reply_markup=reply_markup)

def main():
    """Главная функция"""
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN не найден в .env файле!")
        return
    
    print("🤖 Запуск тестового бота...")
    
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("shop", shop))
    application.add_handler(CommandHandler("weather", weather))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("✅ Бот запущен!")
    print("📱 Найдите бота в Telegram и отправьте /start")
    print("\n🌐 Основной URL игры: https://antoged.github.io/farming-game/")
    print("📱 Telegram Mini App: https://antoged.github.io/farming-game/telegram-app.html")
    
    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()
