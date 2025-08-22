# 🚀 Руководство по развертыванию

Подробные инструкции по развертыванию Фермерской игры на различных платформах.

## 📋 Предварительные требования

- Python 3.8+
- Git
- Telegram Bot Token
- Веб-сервер или хостинг-платформа

## 🏠 Локальная разработка

### 1. Клонирование и настройка

```bash
# Клонируйте репозиторий
git clone https://github.com/your-username/farming-game.git
cd farming-game

# Создайте виртуальное окружение
python -m venv venv

# Активируйте виртуальное окружение
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt
```

### 2. Настройка переменных окружения

```bash
# Скопируйте пример конфигурации
cp env_example.txt .env

# Отредактируйте .env файл
nano .env
```

Содержимое `.env`:
```env
BOT_TOKEN=your_telegram_bot_token_here
WEBAPP_URL=https://your-domain.com
```

### 3. Запуск для разработки

```bash
# Запуск всех компонентов
python run.py

# Или запуск отдельных компонентов
python webapp.py  # Веб-приложение
python bot.py     # Telegram бот
```

## 🌐 Развертывание на VPS

### 1. Подготовка сервера

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка необходимых пакетов
sudo apt install python3 python3-pip python3-venv nginx git -y

# Создание пользователя для приложения
sudo adduser farming
sudo usermod -aG sudo farming
```

### 2. Клонирование и настройка приложения

```bash
# Переключение на пользователя
sudo su - farming

# Клонирование репозитория
git clone https://github.com/your-username/farming-game.git
cd farming-game

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Настройка переменных окружения
cp env_example.txt .env
nano .env
```

### 3. Настройка Nginx

```bash
# Создание конфигурации Nginx
sudo nano /etc/nginx/sites-available/farming-game
```

Содержимое конфигурации:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/farming/farming-game/static;
        expires 30d;
    }
}
```

```bash
# Активация сайта
sudo ln -s /etc/nginx/sites-available/farming-game /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 4. Настройка systemd

```bash
# Создание сервиса для бота
sudo nano /etc/systemd/system/farming-bot.service
```

Содержимое сервиса:
```ini
[Unit]
Description=Farming Game Bot
After=network.target

[Service]
Type=simple
User=farming
WorkingDirectory=/home/farming/farming-game
Environment=PATH=/home/farming/farming-game/venv/bin
ExecStart=/home/farming/farming-game/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Создание сервиса для веб-приложения
sudo nano /etc/systemd/system/farming-web.service
```

Содержимое сервиса:
```ini
[Unit]
Description=Farming Game Web App
After=network.target

[Service]
Type=simple
User=farming
WorkingDirectory=/home/farming/farming-game
Environment=PATH=/home/farming/farming-game/venv/bin
ExecStart=/home/farming/farming-game/venv/bin/python webapp.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 5. Запуск сервисов

```bash
# Включение и запуск сервисов
sudo systemctl enable farming-bot
sudo systemctl enable farming-web
sudo systemctl start farming-bot
sudo systemctl start farming-web

# Проверка статуса
sudo systemctl status farming-bot
sudo systemctl status farming-web
```

### 6. Настройка SSL (Let's Encrypt)

```bash
# Установка Certbot
sudo apt install certbot python3-certbot-nginx -y

# Получение SSL сертификата
sudo certbot --nginx -d your-domain.com

# Настройка автоматического обновления
sudo crontab -e
# Добавьте строку:
# 0 12 * * * /usr/bin/certbot renew --quiet
```

## ☁️ Развертывание на Heroku

### 1. Подготовка

```bash
# Установка Heroku CLI
# Скачайте с https://devcenter.heroku.com/articles/heroku-cli

# Вход в Heroku
heroku login
```

### 2. Создание приложения

```bash
# Создание приложения на Heroku
heroku create your-farming-game

# Добавление переменных окружения
heroku config:set BOT_TOKEN=your_bot_token
heroku config:set WEBAPP_URL=https://your-farming-game.herokuapp.com
```

### 3. Настройка Procfile

Создайте файл `Procfile`:
```
web: python webapp.py
worker: python bot.py
```

### 4. Развертывание

```bash
# Отправка кода на Heroku
git push heroku main

# Запуск воркера для бота
heroku ps:scale worker=1
```

## 🐳 Развертывание с Docker

### 1. Создание Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "run.py"]
```

### 2. Создание docker-compose.yml

```yaml
version: '3.8'

services:
  farming-game:
    build: .
    ports:
      - "5000:5000"
    environment:
      - BOT_TOKEN=${BOT_TOKEN}
      - WEBAPP_URL=${WEBAPP_URL}
    volumes:
      - ./farm_game.db:/app/farm_game.db
    restart: unless-stopped
```

### 3. Запуск с Docker

```bash
# Сборка и запуск
docker-compose up -d

# Просмотр логов
docker-compose logs -f
```

## 🔧 Настройка мониторинга

### 1. Логирование

```bash
# Создание папки для логов
mkdir -p logs

# Настройка ротации логов
sudo nano /etc/logrotate.d/farming-game
```

Содержимое:
```
/home/farming/farming-game/logs/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 farming farming
}
```

### 2. Мониторинг с помощью systemd

```bash
# Просмотр логов сервисов
sudo journalctl -u farming-bot -f
sudo journalctl -u farming-web -f

# Проверка статуса
sudo systemctl status farming-bot
sudo systemctl status farming-web
```

## 🔒 Безопасность

### 1. Настройка файрвола

```bash
# Установка UFW
sudo apt install ufw

# Настройка правил
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### 2. Обновления безопасности

```bash
# Автоматические обновления безопасности
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

## 📊 Резервное копирование

### 1. Автоматическое резервное копирование

```bash
# Создание скрипта резервного копирования
nano backup.sh
```

Содержимое:
```bash
#!/bin/bash
BACKUP_DIR="/home/farming/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
cp /home/farming/farming-game/farm_game.db $BACKUP_DIR/farm_game_$DATE.db
cp /home/farming/farming-game/.env $BACKUP_DIR/env_$DATE.backup

# Удаление старых резервных копий (старше 30 дней)
find $BACKUP_DIR -name "*.db" -mtime +30 -delete
find $BACKUP_DIR -name "*.backup" -mtime +30 -delete
```

```bash
# Делаем скрипт исполняемым
chmod +x backup.sh

# Добавляем в cron (ежедневно в 2:00)
crontab -e
# Добавьте строку:
# 0 2 * * * /home/farming/farming-game/backup.sh
```

## 🚨 Устранение неполадок

### Частые проблемы

1. **Бот не отвечает**
   - Проверьте токен в `.env`
   - Убедитесь, что бот запущен: `sudo systemctl status farming-bot`

2. **Веб-приложение недоступно**
   - Проверьте статус: `sudo systemctl status farming-web`
   - Проверьте логи: `sudo journalctl -u farming-web -f`

3. **Проблемы с базой данных**
   - Проверьте права доступа к файлу БД
   - Создайте резервную копию перед изменениями

4. **Проблемы с SSL**
   - Проверьте конфигурацию Nginx
   - Обновите сертификат: `sudo certbot renew`

### Полезные команды

```bash
# Перезапуск всех сервисов
sudo systemctl restart farming-bot farming-web nginx

# Просмотр логов в реальном времени
sudo journalctl -u farming-bot -f
sudo journalctl -u farming-web -f

# Проверка портов
sudo netstat -tlnp | grep :5000

# Проверка конфигурации Nginx
sudo nginx -t
```

## 📞 Поддержка

Если у вас возникли проблемы:

1. Проверьте логи сервисов
2. Убедитесь, что все зависимости установлены
3. Проверьте конфигурацию переменных окружения
4. Создайте Issue в репозитории с подробным описанием проблемы

---

**Удачного развертывания! 🚀**
