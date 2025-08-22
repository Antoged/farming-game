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
    """Веб-приложение доступно только через GitHub Pages"""
    print("🌐 Веб-приложение доступно по адресу:")
    print("   https://antoged.github.io/farming-game/")
    print("❌ Локальный сервер отключен")
    return

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
    print("🌾 Фермерская игра")
    print()
    
    # Показать информацию о веб-приложении
    run_webapp()
    print()
    
    # Проверка зависимостей
    try:
        import telegram  # noqa: F401
        print("✅ Зависимости установлены")
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("📦 Установите зависимости: pip install -r requirements.txt")
        return
    
    print("🤖 Запуск Telegram бота...")
    
    # Запуск только бота
    try:
        run_bot()
    except KeyboardInterrupt:
        print("\n🛑 Остановка бота...")
    finally:
        print("👋 Бот остановлен")

if __name__ == "__main__":
    main()
