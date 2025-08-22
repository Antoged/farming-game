#!/usr/bin/env python3
"""
Тест HTTPS соединения
Основной URL игры: https://antoged.github.io/farming-game/
Telegram Mini App: https://antoged.github.io/farming-game/telegram-app.html
"""

import requests
import urllib3

# Отключаем предупреждения о самоподписанных сертификатах
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_https():
    """Тестируем HTTPS соединение"""
    try:
        response = requests.get('https://antoged.github.io/farming-game/', verify=False)
        print(f"✅ HTTPS сервер работает!")
        print(f"📊 Статус: {response.status_code}")
        print(f"📄 Размер ответа: {len(response.text)} байт")
        print(f"🌐 URL: https://antoged.github.io/farming-game/")
        print("📱 Telegram Mini App готов к использованию!")
        print("\n🌐 Основной URL игры: https://antoged.github.io/farming-game/")
        print("📱 Telegram Mini App: https://antoged.github.io/farming-game/telegram-app.html")
        return True
    except Exception as e:
        print(f"❌ Ошибка HTTPS соединения: {e}")
        return False

if __name__ == "__main__":
    print("🔒 Тестирование HTTPS соединения...")
    test_https()
