from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import json
import os
from game_logic import GameLogic
try:
    from config_local import SEEDS, WEATHER_EFFECTS
except ImportError:
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
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        username = data.get('username')
        
        if not user_id:
            return jsonify({'error': 'user_id required'}), 400
        
        player = game.db.get_or_create_player(user_id, username)
        return jsonify({'success': True, 'player': player})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/farm', methods=['GET'])
def get_farm():
    """Получить статус фермы"""
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'user_id required'}), 400
        
        farm_status = game.get_farm_status(int(user_id))
        weather_info = game.get_current_weather_info()
        
        return jsonify({
            'farm': farm_status,
            'weather': weather_info
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/plant', methods=['POST'])
def plant_seed():
    """Посадить семечко"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        plot_id = data.get('plot_id')
        seed_type = data.get('seed_type')
        
        if not all([user_id, plot_id, seed_type]):
            return jsonify({'error': 'Missing required parameters'}), 400
        
        success, message = game.plant_seed(int(user_id), int(plot_id), seed_type)
        return jsonify({'success': success, 'message': message})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/harvest', methods=['POST'])
def harvest_plot():
    """Собрать урожай"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        plot_id = data.get('plot_id')
        
        if not all([user_id, plot_id]):
            return jsonify({'error': 'Missing required parameters'}), 400
        
        success, message = game.harvest_plot(int(user_id), int(plot_id))
        return jsonify({'success': success, 'message': message})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/shop', methods=['GET'])
def get_shop():
    """Получить товары магазина"""
    try:
        shop_items = game.get_shop_items()
        return jsonify({'items': shop_items})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/buy', methods=['POST'])
def buy_seed():
    """Купить семечко"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        seed_type = data.get('seed_type')
        
        if not all([user_id, seed_type]):
            return jsonify({'error': 'Missing required parameters'}), 400
        
        success, message = game.buy_seed(int(user_id), seed_type)
        return jsonify({'success': success, 'message': message})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/inventory', methods=['GET'])
def get_inventory():
    """Получить инвентарь"""
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'user_id required'}), 400
        
        inventory = game.db.get_inventory(int(user_id))
        return jsonify({'items': inventory})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sell', methods=['POST'])
def sell_item():
    """Продать предмет"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        item_id = data.get('item_id')
        
        if not all([user_id, item_id]):
            return jsonify({'error': 'Missing required parameters'}), 400
        
        success, message = game.sell_item(int(user_id), int(item_id))
        return jsonify({'success': success, 'message': message})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Получить статистику игрока"""
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'user_id required'}), 400
        
        stats = game.get_player_stats(int(user_id))
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/weather', methods=['GET'])
def get_weather():
    """Получить информацию о погоде"""
    try:
        weather_info = game.get_current_weather_info()
        return jsonify(weather_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/player', methods=['GET'])
def get_player():
    """Получить информацию об игроке"""
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'user_id required'}), 400
        
        player = game.db.get_or_create_player(int(user_id), None)
        return jsonify(player)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Веб-приложение работает только через GitHub Pages
# Используйте: https://antoged.github.io/farming-game/
if __name__ == '__main__':
    print("⚠️  Веб-приложение доступно только через GitHub Pages:")
    print("🌐 https://antoged.github.io/farming-game/")
    print("❌ Локальный сервер отключен для безопасности")
