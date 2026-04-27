# 🚀 БЫСТРАЯ НАСТРОЙКА SSL - 5 МИНУТ

## ⚡ САМЫЙ БЫСТРЫЙ СПОСОБ (Let's Encrypt)

### Шаг 1: Подготовьте домен

```bash
# Убедитесь что домен указывает на ваш сервер
ping yourdomain.com
```

### Шаг 2: Запустите скрипт

```bash
chmod +x setup_ssl.sh
./setup_ssl.sh yourdomain.com admin@yourdomain.com
```

Следуйте инструкциям на экране.

### Шаг 3: Обновите nginx.conf

Откройте `nginx.conf` и замените:
```nginx
server_name yourdomain.com www.yourdomain.com;  # Ваш домен
```

### Шаг 4: Запустите проект

```bash
docker-compose up -d
```

### Шаг 5: Проверьте

Откройте в браузере: **https://yourdomain.com**

✅ Должен быть зеленый замок!

---

## 🔧 АЛЬТЕРНАТИВНЫЕ ВАРИАНТЫ

### Для локальной разработки (Self-Signed)

```bash
./setup_ssl.sh
# Выберите опцию 2: Self-signed certificate

# Запустите
docker-compose up -d

# В браузере нажмите Advanced → Proceed
```

⚠️ Браузер покажет предупреждение безопасности (это нормально для localhost)

---

### Если уже есть сертификаты

```bash
./setup_ssl.sh
# Выберите опцию 3: Use existing certificates

# Укажите пути к вашим файлам:
# - fullchain.pem (или cert.pem)
# - privkey.pem (или key.pem)
```

---

## 📋 ПРОВЕРКА РАБОТЫ

```bash
# Проверьте что HTTPS работает
curl -I https://yourdomain.com

# Проверьте сертификат
openssl x509 -enddate -noout -in ssl/certs/fullchain.pem

# Проверьте редирект HTTP → HTTPS
curl -I http://yourdomain.com
# Должен вернуть: 301 Moved Permanently → https://
```

---

## 🐛 ЕСЛИ ЧТО-ТО НЕ РАБОТАЕТ

### Проблема: Порт 80 занят

```bash
# Найдите процесс
sudo lsof -i :80

# Остановите его
sudo systemctl stop apache2  # или другой сервис
```

### Проблема: DNS не настроен

```bash
# Проверьте DNS
dig yourdomain.com A

# Должен вернуть IP вашего сервера
```

### Проблема: Firewall блокирует

```bash
# Откройте порты
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw reload
```

### Проблема: Certificate issuance failed

```bash
# Попробуйте standalone mode
docker run --rm -p 80:80 certbot/certbot certonly \
  --standalone \
  -d yourdomain.com
```

---

## 💡 ПОЛЕЗНЫЕ КОМАНДЫ

```bash
# Посмотреть логи
docker-compose logs frontend
docker-compose logs certbot

# Перезапустить nginx
docker-compose restart frontend

# Проверить конфигурацию
docker-compose config

# Обновить сертификат вручную
docker-compose exec certbot certbot renew

# Посмотреть информацию о сертификате
openssl x509 -in ssl/certs/fullchain.pem -text -noout
```

---

## ✅ CHECKLIST

После настройки проверьте:

- [ ] https://yourdomain.com открывается
- [ ] Зеленый замок в браузере
- [ ] HTTP автоматически редиректит на HTTPS
- [ ] Нет warnings о mixed content
- [ ] API запросы работают по HTTPS
- [ ] Сертификат действителен (проверьте expiry date)

---

## 📚 ПОЛНАЯ ДОКУМЕНТАЦИЯ

Подробное руководство: [SSL_SETUP_GUIDE.md](SSL_SETUP_GUIDE.md)

---

**Готово!** 🎉 Ваш сайт теперь работает по HTTPS!
