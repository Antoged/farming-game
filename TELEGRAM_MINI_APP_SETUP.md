# 📱 Настройка Telegram Mini App

Пошаговое руководство по настройке фермерской игры как Telegram Mini App.

## 🎯 Что такое Telegram Mini App?

Telegram Mini App - это веб-приложение, которое работает внутри Telegram и предоставляет пользователям доступ к играм и сервисам прямо в мессенджере. Ваша фермерская игра теперь доступна как Mini App!

## 🚀 Быстрый старт

### 1. Создание бота
1. Откройте Telegram и найдите @BotFather
2. Отправьте команду `/newbot`
3. Следуйте инструкциям:
   - Укажите название бота (например: "Фермерская игра")
   - Укажите username (например: "farming_game_bot")
4. Сохраните полученный токен бота

### 2. Настройка Mini App
1. Отправьте @BotFather команду `/newapp`
2. Выберите созданного бота
3. Укажите название Mini App: "Фермерская игра"
4. Укажите описание: "Игра-ферма с посадкой и сбором урожая"
5. **Важно:** Укажите URL: `https://antoged.github.io/farming-game/`

### 3. Проверка настройки
```bash
# Тест Mini App (замените <BOT_TOKEN> на ваш токен)
curl "https://api.telegram.org/bot<BOT_TOKEN>/getWebAppInfo"
```

## 🔧 Детальная настройка

### Настройка команд бота
Отправьте @BotFather команду `/setcommands` и выберите вашего бота:

```
start - 🎮 Начать игру
farm - 🌱 Управление фермой
shop - 🛒 Магазин семян
inventory - 📦 Инвентарь
stats - 📊 Статистика
help - ❓ Помощь
```

### Настройка меню бота
Отправьте @BotFather команду `/setmenubutton`:

```
Выберите бота: @farming_game_bot
Текст кнопки: 🎮 Играть
URL: https://antoged.github.io/farming-game/
```

### Настройка описания бота
Отправьте @BotFather команду `/setdescription`:

```
Выберите бота: @farming_game_bot
Описание:
🌾 Фермерская игра - выращивайте культуры, собирайте урожай и развивайте свою ферму!

🎮 Играйте прямо в Telegram
🌱 6 участков для посадки
🛒 Магазин семян
📦 Система инвентаря
💰 Экономика и торговля
```

### Настройка информации о боте
Отправьте @BotFather команду `/setabouttext`:

```
Выберите бота: @farming_game_bot
О боте:
🌾 Фермерская игра - увлекательная игра-ферма!

🎯 Цель: Вырастить самую успешную ферму
🌱 Посадите семена на участках
⏰ Дождитесь созревания урожая
🌾 Соберите готовые культуры
💰 Продайте урожай за монеты
🛒 Покупайте новые семена
📈 Повышайте уровень и опыт

🎮 Играйте бесплатно прямо в Telegram!
```

## 📱 Интеграция с игрой

### Поддержка Telegram Web App API
Игра автоматически определяет, запущена ли она в Telegram:

```javascript
// Проверка запуска в Telegram
if (window.Telegram && window.Telegram.WebApp) {
    const tg = window.Telegram.WebApp;
    
    // Инициализация
    tg.ready();
    tg.expand();
    
    // Получение данных пользователя
    if (tg.initDataUnsafe && tg.initDataUnsafe.user) {
        const user = tg.initDataUnsafe.user;
        console.log('Пользователь Telegram:', user);
    }
}
```

### Адаптация под тему Telegram
Игра автоматически подстраивается под тему Telegram:

```javascript
// Применение темы Telegram
if (tg.themeParams) {
    document.documentElement.style.setProperty(
        '--tg-theme-bg-color', 
        tg.themeParams.bg_color || '#ffffff'
    );
    document.documentElement.style.setProperty(
        '--tg-theme-text-color', 
        tg.themeParams.text_color || '#000000'
    );
    // ... другие цвета
}
```

## 🎮 Тестирование Mini App

### 1. Тест в Telegram
1. Найдите вашего бота @farming_game_bot
2. Отправьте команду `/start`
3. Нажмите на кнопку "🎮 Играть" или "Menu"
4. Игра должна открыться в Telegram

### 2. Тест через URL
1. Откройте браузер
2. Перейдите по адресу: `https://antoged.github.io/farming-game/`
3. Игра должна работать как обычное веб-приложение

### 3. Тест на мобильных устройствах
1. Откройте Telegram на телефоне
2. Найдите вашего бота
3. Запустите игру через меню
4. Проверьте адаптивность интерфейса

## 🔍 Отладка и диагностика

### Проверка настроек бота
```bash
# Получить информацию о боте
curl "https://api.telegram.org/bot<BOT_TOKEN>/getMe"

# Получить информацию о Mini App
curl "https://api.telegram.org/bot<BOT_TOKEN>/getWebAppInfo"

# Получить команды бота
curl "https://api.telegram.org/bot<BOT_TOKEN>/getMyCommands"
```

### Логи в браузере
Откройте Developer Tools (F12) и проверьте консоль:

```javascript
// Проверка загрузки Telegram Web App
console.log('Telegram WebApp:', window.Telegram?.WebApp);

// Проверка данных пользователя
if (window.Telegram?.WebApp?.initDataUnsafe?.user) {
    console.log('Пользователь:', window.Telegram.WebApp.initDataUnsafe.user);
}
```

### Проверка в Telegram
1. Отправьте боту команду `/start`
2. Проверьте, что появилось меню с кнопкой игры
3. Нажмите на кнопку и проверьте открытие игры

## 🚨 Решение проблем

### Проблема: Mini App не открывается
**Возможные причины:**
- Неправильный URL в настройках
- Ошибки в коде игры
- Проблемы с GitHub Pages

**Решение:**
1. Проверьте URL в настройках BotFather
2. Убедитесь, что игра работает в браузере
3. Проверьте консоль браузера на ошибки

### Проблема: Игра не загружается в Telegram
**Возможные причины:**
- Проблемы с HTTPS
- Блокировка со стороны Telegram
- Ошибки в JavaScript коде

**Решение:**
1. Убедитесь, что используется HTTPS
2. Проверьте, что домен не заблокирован
3. Протестируйте игру в разных браузерах

### Проблема: Не работает авторизация
**Возможные причины:**
- Не настроен Telegram Web App API
- Ошибки в получении user_id
- Проблемы с инициализацией пользователя

**Решение:**
1. Проверьте интеграцию с Telegram Web App
2. Убедитесь, что user_id корректно передается
3. Проверьте инициализацию Telegram Web App

## 📊 Аналитика и метрики

### Отслеживание использования
```javascript
// Отправка статистики в Telegram
if (window.Telegram?.WebApp) {
    const tg = window.Telegram.WebApp;
    
    // Отправка события
    tg.sendData(JSON.stringify({
        action: 'game_started',
        timestamp: Date.now(),
        user_id: tg.initDataUnsafe?.user?.id
    }));
}
```

### Метрики для анализа
- Количество запусков игры
- Время сессии
- Популярные действия
- Конверсия (запуск → игра)

## 🔄 Обновления и поддержка

### Обновление Mini App
1. Внесите изменения в код игры
2. Запушьте изменения в GitHub
3. GitHub Pages автоматически обновится
4. Mini App в Telegram обновится автоматически

### Поддержка пользователей
1. Создайте команду `/help` с инструкциями
2. Добавьте команду `/support` для связи
3. Регулярно обновляйте FAQ

## 📚 Полезные ресурсы

### Документация Telegram
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Telegram Web App](https://core.telegram.org/bots/webapps)
- [Mini Apps Platform](https://core.telegram.org/bots/webapps)

### Инструменты разработки
- [BotFather](https://t.me/BotFather) - создание и настройка ботов
- [@WebAppBot](https://t.me/WebAppBot) - тестирование Mini Apps
- [Telegram Web App Validator](https://validator.telegram.org/)

### Сообщество
- [Telegram Developers](https://t.me/TelegramDevelopers)
- [Bot Support](https://t.me/BotSupport)
- [Web App Developers](https://t.me/WebAppDev)

---

**🎮 Удачной настройки Mini App!** 📱✨
