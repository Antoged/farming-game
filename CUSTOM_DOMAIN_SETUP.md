# 🌐 Настройка кастомного домена для GitHub Pages

Полная инструкция по настройке собственного домена для вашего проекта.

## 📋 Варианты доменов

### Вариант 1: Бесплатные поддомены
- **Freenom** (tk, ml, ga, cf) - бесплатно на 1 год
- **GitHub Pages** (username.github.io/repo-name) - всегда бесплатно
- **Netlify** (app-name.netlify.app) - бесплатно

### Вариант 2: Платные домены
- **Namecheap** - от $1-15/год
- **GoDaddy** - от $2-20/год  
- **Cloudflare** - от $1/год

## 🚀 Быстрая настройка с бесплатным доменом

### Вариант A: Использовать стандартный GitHub Pages

1. **Определите ваш username на GitHub**
   - Ваш домен будет: `https://YOUR_USERNAME.github.io/farming-game/`

2. **Обновите файл .env:**
   ```env
   WEBAPP_URL=https://YOUR_USERNAME.github.io/farming-game/
   ```

3. **Обновите конфигурацию в GitHub:**
   - Перейдите в Settings → Pages
   - Source: Deploy from a branch
   - Branch: gh-pages
   - Folder: / (root)

### Вариант B: Использовать Netlify (рекомендуется)

1. **Зарегистрируйтесь на [Netlify](https://netlify.com)**

2. **Подключите GitHub репозиторий:**
   - New site from Git
   - Выберите ваш репозиторий
   - Build command: оставьте пустым
   - Publish directory: `docs`

3. **Получите домен:**
   - Netlify автоматически создаст домен типа `app-name.netlify.app`
   - Можете изменить имя в Site settings → Domain management

4. **Обновите конфигурацию:**
   ```env
   WEBAPP_URL=https://your-app-name.netlify.app
   ```

## 💰 Настройка платного домена

### Шаг 1: Купите домен

#### На Namecheap:
1. Перейдите на [Namecheap](https://namecheap.com)
2. Найдите доступный домен
3. Добавьте в корзину и оплатите
4. Подтвердите email

#### На Cloudflare:
1. Перейдите на [Cloudflare Registrar](https://dash.cloudflare.com/)
2. Зарегистрируйтесь и найдите домен
3. Купите домен (часто дешевле других)

### Шаг 2: Настройте DNS записи

После покупки домена настройте DNS:

#### Для GitHub Pages:
```
A записи:
185.199.108.153
185.199.109.153  
185.199.110.153
185.199.111.153

CNAME запись:
www -> YOUR_USERNAME.github.io
```

#### Для Netlify:
```
CNAME запись:
@ -> your-app-name.netlify.app
www -> your-app-name.netlify.app
```

### Шаг 3: Настройте домен в GitHub/Netlify

#### В GitHub Pages:
1. Перейдите в Settings → Pages
2. Custom domain: введите ваш домен
3. ✅ Enforce HTTPS
4. Подождите несколько минут для активации SSL

#### В Netlify:
1. Site settings → Domain management
2. Add custom domain
3. Введите ваш домен
4. SSL автоматически настроится

## 🔧 Обновление конфигурации проекта

После настройки домена обновите файлы:

### 1. Обновите .env файл:
```env
BOT_TOKEN=your_bot_token_here
WEBAPP_URL=https://your-domain.com
DATABASE_PATH=farm_game.db
```

### 2. Обновите GitHub репозиторий:
```bash
git add .
git commit -m "feat: update domain configuration"
git push origin main
```

### 3. Создайте CNAME файл (только для GitHub Pages):
```bash
echo "your-domain.com" > docs/CNAME
git add docs/CNAME
git commit -m "feat: add CNAME for custom domain"
git push origin main
```

## 🤖 Настройка Telegram бота

После настройки домена:

1. **Обновите Menu Button в @BotFather:**
   - `/mybots` → выберите бота
   - Bot Settings → Menu Button  
   - URL: `https://your-domain.com`

2. **Протестируйте бота:**
   - Запустите: `python run.py`
   - Откройте бота в Telegram
   - Нажмите "🌾 Играть в ферму"

## 📊 Мониторинг и аналитика

### Google Analytics (опционально):
1. Создайте аккаунт на [Google Analytics](https://analytics.google.com)
2. Добавьте код отслеживания в `docs/index.html`
3. Отслеживайте посетителей сайта

### Cloudflare Analytics:
- Если используете Cloudflare, получите бесплатную аналитику
- Защита от DDoS атак
- Ускорение сайта через CDN

## ⚡ Рекомендации

### Для тестирования:
- Используйте стандартный GitHub Pages домен
- Или бесплатный Netlify домен

### Для продакшена:
- Купите короткий запоминающийся домен
- Используйте Cloudflare для защиты и ускорения
- Настройте мониторинг работоспособности

## 🚨 Устранение неполадок

### Домен не работает:
1. Проверьте DNS записи (может занять до 48 часов)
2. Убедитесь, что CNAME файл создан правильно
3. Проверьте настройки в GitHub Pages/Netlify

### SSL сертификат не работает:
1. Подождите несколько минут
2. Проверьте, что домен правильно указан
3. Попробуйте пересоздать сертификат

### Бот не открывает веб-приложение:
1. Проверьте URL в @BotFather
2. Убедитесь, что HTTPS работает
3. Проверьте консоль браузера на ошибки

## 💡 Примеры доменов

```
Хорошие примеры:
- farmgame.site
- myfarming.app  
- cropgame.io
- farm-bot.com

Плохие примеры:
- my-super-long-farming-game-2024.com
- farm123456.tk
- игра-ферма.рф (кириллица может не работать)
```

## 📞 Поддержка

Если возникли проблемы:
1. Проверьте DNS записи на [DNS Checker](https://dnschecker.org/)
2. Протестируйте SSL на [SSL Labs](https://www.ssllabs.com/ssltest/)
3. Создайте Issue в репозитории

---

**Удачной настройки домена! 🌐**
