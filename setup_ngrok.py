#!/usr/bin/env python3
"""
Скрипт для настройки ngrok и обновления .env файла
"""

import subprocess
import time
import requests
import json
import os

def get_ngrok_url():
    """Получить URL от ngrok"""
    try:
        response = requests.get('http://localhost:4040/api/tunnels')
        if response.status_code == 200:
            tunnels = response.json()['tunnels']
            for tunnel in tunnels:
                if tunnel['proto'] == 'https':
                    return tunnel['public_url']
    except:
        pass
    return None

def update_env_file(ngrok_url):
    """Обновить .env файл с новым URL"""
    env_content = f"""# Telegram Bot Token (получите у @BotFather)
BOT_TOKEN=your_bot_token_here

# URL вашего веб-приложения (после деплоя)
WEBAPP_URL={ngrok_url}

# Настройки базы данных (опционально)
DATABASE_PATH=farm_game.db
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print(f"✅ Обновлен .env файл с URL: {ngrok_url}")

def main():
    print("🚀 Настройка ngrok для Telegram Mini App...")
    
    # Запускаем ngrok
    print("📡 Запуск ngrok...")
    ngrok_process = subprocess.Popen(['ngrok', 'http', '5000'], 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE)
    
    # Ждем запуска ngrok
    time.sleep(3)
    
    # Получаем URL
    ngrok_url = get_ngrok_url()
    
    if ngrok_url:
        print(f"✅ Ngrok запущен: {ngrok_url}")
        update_env_file(ngrok_url)
        
        print("\n🔧 Теперь:")
        print("1. Отредактируйте .env файл и укажите ваш BOT_TOKEN")
        print("2. Запустите бота: python bot.py")
        print("3. Запустите веб-приложение: python webapp.py")
        print(f"4. Ваш Mini App будет доступен по адресу: {ngrok_url}")
        
        # Держим ngrok запущенным
        try:
            ngrok_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Остановка ngrok...")
            ngrok_process.terminate()
    else:
        print("❌ Не удалось получить URL от ngrok")
        print("💡 Убедитесь, что ngrok установлен и доступен")

if __name__ == "__main__":
    main()
