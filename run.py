#!/usr/bin/env python3
"""
Главный скрипт для запуска Фермерской игры
Запускает веб-приложение и бота одновременно
"""

import subprocess
import sys
import time
import signal
import os
from threading import Thread

def run_webapp():
    """Запуск веб-приложения"""
    try:
        subprocess.run([sys.executable, "webapp.py"], check=True)
    except KeyboardInterrupt:
        print("Веб-приложение остановлено")
    except Exception as e:
        print(f"Ошибка запуска веб-приложения: {e}")

def run_bot():
    """Запуск Telegram бота"""
    try:
        subprocess.run([sys.executable, "bot.py"], check=True)
    except KeyboardInterrupt:
        print("Бот остановлен")
    except Exception as e:
        print(f"Ошибка запуска бота: {e}")

def main():
    """Главная функция"""
    print("🌾 Запуск Фермерской игры...")
    
    # Проверка наличия .env файла
    if not os.path.exists('.env'):
        print("⚠️  Файл .env не найден!")
        print("📝 Создайте файл .env на основе env_example.txt")
        print("🔧 Укажите BOT_TOKEN и WEBAPP_URL")
        return
    
    # Проверка зависимостей
    try:
        import flask  # noqa: F401
        import telegram  # noqa: F401
        print("✅ Зависимости установлены")
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("📦 Установите зависимости: pip install -r requirements.txt")
        return
    
    print("🚀 Запуск компонентов...")
    
    # Запуск веб-приложения в отдельном потоке
    webapp_thread = Thread(target=run_webapp, daemon=True)
    webapp_thread.start()
    
    # Небольшая задержка для запуска веб-приложения
    time.sleep(2)
    
    # Запуск бота в основном потоке
    try:
        run_bot()
    except KeyboardInterrupt:
        print("\n🛑 Остановка приложения...")
    finally:
        print("👋 Фермерская игра остановлена")

if __name__ == "__main__":
    main()
