# 🚀 Деплой фермерской игры

Инструкции по развертыванию игры на различных платформах.

## 🌐 GitHub Pages (Основной способ)

### Автоматический деплой
1. **Настройте GitHub Pages:**
   - Перейдите в Settings → Pages
   - Source: Deploy from a branch
   - Branch: main
   - Folder: /docs

2. **Структура файлов:**
   ```
   docs/
   ├── index.html          # Основная игра
   ├── telegram-app.html   # Telegram Mini App
   └── CNAME              # Домен antoged.github.io
   ```

3. **Деплой:**
   ```bash
   git add .
   git commit -m "Обновление игры"
   git push origin main
   ```
   Игра автоматически обновится через несколько минут.

### Ручной деплой
```bash
# Обновите файлы в папке docs/
cp templates/index.html docs/index.html
cp templates/telegram-app.html docs/telegram-app.html

# Запушьте изменения
git add docs/
git commit -m "Обновление GitHub Pages"
git push origin main
```

## 🐳 Docker

### Создание образа
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "webapp.py"]
```

### Запуск
```bash
# Сборка
docker build -t farming-game .

# Запуск
docker run -p 5000:5000 farming-game
```

## ☁️ Heroku

### 1. Создайте приложение
```bash
heroku create your-farming-game
```

### 2. Настройте переменные окружения
```bash
heroku config:set BOT_TOKEN=your_telegram_bot_token
heroku config:set WEBAPP_URL=https://your-app.herokuapp.com
```

### 3. Деплой
```bash
git push heroku main
```

### 4. Откройте приложение
```bash
heroku open
```

## 🐧 VPS/Сервер

### 1. Установите зависимости
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx

# CentOS/RHEL
sudo yum install python3 python3-pip nginx
```

### 2. Настройте Python окружение
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Настройте systemd сервис
```ini
# /etc/systemd/system/farming-game.service
[Unit]
Description=Farming Game
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/farming-game
Environment=PATH=/var/www/farming-game/venv/bin
ExecStart=/var/www/farming-game/venv/bin/python webapp.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### 4. Настройте Nginx
```nginx
# /etc/nginx/sites-available/farming-game
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass https://antoged.github.io/farming-game/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 5. Запустите сервисы
```bash
sudo systemctl enable farming-game
sudo systemctl start farming-game
sudo systemctl enable nginx
sudo systemctl start nginx
```

## 🔒 HTTPS с Let's Encrypt

### 1. Установите Certbot
```bash
sudo apt install certbot python3-certbot-nginx
```

### 2. Получите сертификат
```bash
sudo certbot --nginx -d your-domain.com
```

### 3. Автообновление
```bash
sudo crontab -e
# Добавьте строку:
0 12 * * * /usr/bin/certbot renew --quiet
```

## 📱 Telegram Mini App

### 1. Настройте бота через @BotFather
```
/newapp
Выберите бота
Укажите название: Фермерская игра
Укажите описание: Игра-ферма с посадкой и сбором урожая
Укажите URL: https://antoged.github.io/farming-game/
```

### 2. Проверьте настройки
```bash
# Тест Mini App
curl "https://api.telegram.org/bot<BOT_TOKEN>/getWebAppInfo"
```

## 🔧 Переменные окружения

### Основные настройки
```bash
# .env файл
BOT_TOKEN=your_telegram_bot_token
WEBAPP_URL=https://your-domain.com
SECRET_KEY=your_secret_key
DEBUG=False
```

### Настройки базы данных
```bash
DATABASE_URL=sqlite:///farm_game.db
# или для PostgreSQL:
DATABASE_URL=postgresql://user:password@your-database-host/farming_game
```

## 📊 Мониторинг

### Логи
```bash
# Systemd
sudo journalctl -u farming-game -f

# Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Статус сервисов
```bash
sudo systemctl status farming-game
sudo systemctl status nginx
```

## 🚨 Устранение неполадок

### Проблемы с портами
```bash
# Проверьте занятые порты
sudo netstat -tlnp | grep :5000

# Убейте процесс если нужно
sudo kill -9 <PID>
```

### Проблемы с правами
```bash
# Исправьте права на файлы
sudo chown -R www-data:www-data /var/www/farming-game
sudo chmod -R 755 /var/www/farming-game
```

### Проблемы с базой данных
```bash
# Проверьте подключение
python3 -c "from database import Database; db = Database(); print('OK')"

# Создайте резервную копию
cp farm_game.db farm_game.db.backup
```

## 🔄 Обновления

### Автоматические обновления
```bash
# Создайте скрипт обновления
#!/bin/bash
cd /var/www/farming-game
git pull origin main
sudo systemctl restart farming-game
```

### Откат изменений
```bash
git log --oneline
git reset --hard <commit_hash>
sudo systemctl restart farming-game
```

## 📈 Масштабирование

### Горизонтальное масштабирование
- Используйте балансировщик нагрузки
- Настройте несколько экземпляров приложения
- Используйте Redis для сессий

### Вертикальное масштабирование
- Увеличьте ресурсы сервера
- Оптимизируйте код и базу данных
- Используйте кэширование

---

**🎮 Удачного деплоя!** 🚀
