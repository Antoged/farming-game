#!/usr/bin/env python3
"""
HTTPS сервер для Telegram Mini App
"""

import ssl
import os
import ipaddress
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import json
from game_logic import GameLogic
from config import SEEDS, WEATHER_EFFECTS

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)

game = GameLogic()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/init', methods=['POST'])
def init_user():
    """Инициализация пользователя"""
    data = request.get_json()
    user_id = data.get('user_id')
    username = data.get('username')
    
    if not user_id:
        return jsonify({'error': 'user_id required'}), 400
    
    player = game.db.get_or_create_player(user_id, username)
    return jsonify({'success': True, 'player': player})

@app.route('/api/farm', methods=['GET'])
def get_farm():
    """Получить статус фермы"""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id required'}), 400
    
    farm_status = game.get_farm_status(int(user_id))
    weather_info = game.get_current_weather_info()
    
    return jsonify({
        'farm': farm_status,
        'weather': weather_info
    })

@app.route('/api/plant', methods=['POST'])
def plant_seed():
    """Посадить семечко"""
    data = request.get_json()
    user_id = data.get('user_id')
    plot_id = data.get('plot_id')
    seed_type = data.get('seed_type')
    
    if not all([user_id, plot_id, seed_type]):
        return jsonify({'error': 'Missing required parameters'}), 400
    
    success, message = game.plant_seed(int(user_id), int(plot_id), seed_type)
    return jsonify({'success': success, 'message': message})

@app.route('/api/harvest', methods=['POST'])
def harvest_plot():
    """Собрать урожай"""
    data = request.get_json()
    user_id = data.get('user_id')
    plot_id = data.get('plot_id')
    
    if not all([user_id, plot_id]):
        return jsonify({'error': 'Missing required parameters'}), 400
    
    success, message = game.harvest_plot(int(user_id), int(plot_id))
    return jsonify({'success': success, 'message': message})

@app.route('/api/shop', methods=['GET'])
def get_shop():
    """Получить товары магазина"""
    shop_items = game.get_shop_items_with_names()
    return jsonify({'items': shop_items})

@app.route('/api/buy', methods=['POST'])
def buy_seed():
    """Купить семечко"""
    data = request.get_json()
    user_id = data.get('user_id')
    seed_type = data.get('seed_type')
    
    if not all([user_id, seed_type]):
        return jsonify({'error': 'Missing required parameters'}), 400
    
    success, message = game.buy_seed(int(user_id), seed_type)
    return jsonify({'success': success, 'message': message})

@app.route('/api/inventory', methods=['GET'])
def get_inventory():
    """Получить инвентарь"""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id required'}), 400
    
    inventory = game.db.get_inventory(int(user_id))
    return jsonify({'items': inventory})

@app.route('/api/sell', methods=['POST'])
def sell_item():
    """Продать предмет"""
    data = request.get_json()
    user_id = data.get('user_id')
    item_id = data.get('item_id')
    
    if not all([user_id, item_id]):
        return jsonify({'error': 'Missing required parameters'}), 400
    
    success, message = game.sell_item(int(user_id), int(item_id))
    return jsonify({'success': success, 'message': message})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Получить статистику игрока"""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id required'}), 400
    
    stats = game.get_player_stats(int(user_id))
    return jsonify(stats)

@app.route('/api/weather', methods=['GET'])
def get_weather():
    """Получить информацию о погоде"""
    weather_info = game.get_current_weather_info()
    return jsonify(weather_info)

def create_self_signed_cert():
    """Создать самоподписанный сертификат"""
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from datetime import datetime, timedelta, timezone
    
    # Генерируем приватный ключ
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    
    # Создаем сертификат
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "RU"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Moscow"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Moscow"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Farming Game"),
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.now(timezone.utc)
    ).not_valid_after(
        datetime.now(timezone.utc) + timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName("localhost"),
            x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
        ]),
        critical=False,
    ).sign(private_key, hashes.SHA256())
    
    # Сохраняем сертификат и ключ
    with open("cert.pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    with open("key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    print("✅ Самоподписанный сертификат создан")

if __name__ == '__main__':
    # Создаем сертификат если его нет
    if not os.path.exists('cert.pem') or not os.path.exists('key.pem'):
        try:
            create_self_signed_cert()
        except ImportError:
            print("❌ Для создания HTTPS сертификата нужен модуль cryptography")
            print("💡 Установите: pip install cryptography")
            print("🌐 Запускаем HTTP сервер...")
            app.run(debug=True, host='0.0.0.0', port=5000)
            exit()
    
    # Создаем SSL контекст
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('cert.pem', 'key.pem')
    
    print("🔒 Запуск HTTPS сервера на https://localhost:5000")
    print("⚠️  Используется самоподписанный сертификат")
    print("📱 Для Telegram Mini App используйте этот URL в .env файле")
    
    app.run(debug=True, host='0.0.0.0', port=5000, ssl_context=context)
