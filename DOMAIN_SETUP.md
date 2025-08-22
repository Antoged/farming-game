# 🌐 Настройка именного домена для GitHub Pages

## 📋 Что нужно сделать

### 1. Настройка GitHub Pages

1. **Перейдите в настройки репозитория:**
   - Откройте [https://github.com/Antoged/farming-game](https://github.com/Antoged/farming-game)
   - Нажмите на вкладку **Settings**
   - В левом меню найдите **Pages**

2. **Настройте GitHub Pages:**
   - В разделе **Source** выберите **Deploy from a branch**
   - В **Branch** выберите **main** и папку **/docs**
   - Нажмите **Save**

### 2. Настройка именного домена

#### Вариант A: Домен на GitHub (рекомендуется)

1. **В том же разделе Pages:**
   - В поле **Custom domain** введите ваш домен (например: `farming.antoged.com`)
   - Поставьте галочку **Enforce HTTPS**
   - Нажмите **Save**

2. **GitHub автоматически создаст файл CNAME**

#### Вариант B: Ручная настройка

1. **Обновите файл CNAME:**
   ```bash
   # Замените your-domain.com на ваш реальный домен
   echo "your-domain.com" > CNAME
   ```

2. **Сделайте коммит и пуш:**
   ```bash
   git add CNAME
   git commit -m "Update custom domain"
   git push origin main
   ```

### 3. Настройка DNS провайдера

#### Для домена на Cloudflare:

1. **Добавьте CNAME запись:**
   - Тип: `CNAME`
   - Имя: `@` (или поддомен, например `farming`)
   - Значение: `antoged.github.io`
   - Проксирование: включено (оранжевое облачко)

2. **Добавьте A запись (альтернатива):**
   - Тип: `A`
   - Имя: `@`
   - Значение: `185.199.108.153`
   - Проксирование: включено

#### Для других провайдеров:

1. **CNAME запись:**
   ```
   farming.yourdomain.com CNAME antoged.github.io
   ```

2. **Или A записи:**
   ```
   farming.yourdomain.com A 185.199.108.153
   farming.yourdomain.com A 185.199.109.153
   farming.yourdomain.com A 185.199.110.153
   farming.yourdomain.com A 185.199.111.153
   ```

### 4. Проверка настройки

1. **Подождите 5-15 минут** для распространения DNS
2. **Проверьте доступность:**
   - Откройте ваш домен в браузере
   - Должна загрузиться страница Фермерской Игры

### 5. SSL сертификат

- GitHub автоматически предоставляет SSL сертификат
- Убедитесь, что галочка **Enforce HTTPS** включена
- При необходимости обновите ссылки в коде на HTTPS

## 🔧 Примеры конфигурации

### Для домена `farming.antoged.com`:

**CNAME файл:**
```
farming.antoged.com
```

**DNS записи:**
```
farming.antoged.com CNAME antoged.github.io
```

### Для корневого домена `antoged.com`:

**CNAME файл:**
```
antoged.com
```

**DNS записи:**
```
antoged.com CNAME antoged.github.io
```

## 🚨 Важные моменты

1. **DNS провайдер:** Убедитесь, что ваш DNS провайдер поддерживает CNAME записи
2. **Время распространения:** DNS изменения могут занять до 24 часов
3. **HTTPS:** GitHub автоматически предоставляет SSL сертификат
4. **Обновления:** При изменении домена обновите файл CNAME и сделайте коммит

## 📱 Проверка работы

После настройки:

1. **Откройте ваш домен** в браузере
2. **Проверьте HTTPS** - должен работать без ошибок
3. **Проверьте мобильную версию** - сайт должен быть адаптивным
4. **Проверьте скорость загрузки** - GitHub Pages оптимизированы

## 🆘 Если что-то не работает

1. **Проверьте DNS записи** через [whatsmydns.net](https://whatsmydns.net)
2. **Проверьте настройки GitHub Pages** в репозитории
3. **Убедитесь, что файл CNAME** находится в корне репозитория
4. **Подождите больше времени** для распространения DNS

## 📞 Поддержка

Если нужна помощь:
- 📧 Email: anton.gedziun@gmail.com
- 🐛 GitHub Issues: [https://github.com/Antoged/farming-game/issues](https://github.com/Antoged/farming-game/issues)
