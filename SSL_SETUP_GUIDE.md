# 🔒 SSL/TLS НАСТРОЙКА ДЛЯ ANSWERS PLATFORM

## 📋 ОБЗОР

Проект поддерживает несколько способов настройки SSL сертификатов:

1. **Let's Encrypt** (Рекомендуется) - бесплатно, автоматическое обновление
2. **Self-signed** - для разработки и тестирования
3. **Существующие сертификаты** - если у вас уже есть сертификаты
4. **Cloudflare Proxy** - через Cloudflare CDN

---

## 🚀 БЫСТРЫЙ СТАРТ С LET'S ENCRYPT

### Шаг 1: Подготовка домена

Убедитесь, что:
- ✅ Домен зарегистрирован на ваше имя
- ✅ DNS A запись указывает на IP вашего сервера
- ✅ Порт 80 открыт (для верификации)

```bash
# Проверка DNS
dig yourdomain.com
ping yourdomain.com
```

### Шаг 2: Запуск скрипта настройки SSL

```bash
cd /path/to/answers-platform
chmod +x setup_ssl.sh
./setup_ssl.sh yourdomain.com admin@yourdomain.com
```

Скрипт автоматически:
1. Остановит сервисы
2. Получит сертификат от Let's Encrypt
3. Настроит автоматическое обновление
4. Скопирует сертификаты в нужную директорию

### Шаг 3: Обновление конфигурации

Отредактируйте `nginx.conf`:
```nginx
server_name yourdomain.com www.yourdomain.com;

# Uncomment Let's Encrypt paths:
ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
```

Обновите `.env`:
```bash
CORS_ORIGINS=https://yourdomain.com
NEXT_PUBLIC_API_URL=https://yourdomain.com/api
```

### Шаг 4: Запуск с SSL

```bash
docker-compose up -d
```

Проверьте: `https://yourdomain.com`

---

## 🔧 ВАРИАНТЫ НАСТРОЙКИ SSL

### Вариант 1: Let's Encrypt (Автоматический) ⭐

**Преимущества:**
- ✅ Полностью бесплатно
- ✅ Автоматическое обновление каждые 90 дней
- ✅ Доверенный CA (браузеры не показывают предупреждений)
- ✅ Поддержка wildcard сертификатов

**Требования:**
- Публичный домен
- Сервер доступен из интернета (порт 80)
- Email для уведомлений

**Настройка:**

```bash
# Метод A: Через setup_ssl.sh (рекомендуется)
./setup_ssl.sh yourdomain.com admin@yourdomain.com

# Метод B: Вручную через docker
docker run --rm \
  -v "./ssl/certs:/etc/letsencrypt" \
  -v "./ssl/www:/var/www/certbot" \
  -p 80:80 \
  certbot/certbot certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  --email admin@yourdomain.com \
  --agree-tos \
  --no-eff-email \
  -d yourdomain.com \
  -d www.yourdomain.com
```

**Автоматическое обновление:**

Certbot контейнер в docker-compose.yml автоматически обновляет сертификаты:
```yaml
certbot:
  image: certbot/certbot:latest
  entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"
```

**Проверка обновления:**
```bash
docker-compose exec certbot certbot renew --dry-run
```

---

### Вариант 2: Self-Signed Certificate (Для разработки)

**Использование:** Только для локальной разработки!

```bash
# Через скрипт
./setup_ssl.sh
# Выберите опцию 2

# Или вручную
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/certs/privkey.pem \
  -out ssl/certs/fullchain.pem \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
```

**В браузере:**
- Chrome: Advanced → Proceed to localhost (unsafe)
- Firefox: Advanced → Accept the Risk and Continue

---

### Вариант 3: Существующие сертификаты

Если у вас уже есть сертификаты от другого CA:

```bash
# Через скрипт
./setup_ssl.sh
# Выберите опцию 3

# Или вручную скопируйте файлы
cp /path/to/your/cert.pem ssl/certs/fullchain.pem
cp /path/to/your/key.pem ssl/certs/privkey.pem

# Установите права
chmod 644 ssl/certs/fullchain.pem
chmod 600 ssl/certs/privkey.pem
```

**Формат файлов:**
- `fullchain.pem` - ваш сертификат + промежуточные сертификаты CA
- `privkey.pem` - приватный ключ (без passphrase)

---

### Вариант 4: Cloudflare SSL (Proxy Mode)

Если используете Cloudflare:

**Шаг 1: Настройка Cloudflare**

1. Войдите в Cloudflare Dashboard
2. Перейдите в SSL/TLS → Overview
3. Выберите режим:
   - **Flexible** - Cloudflare → HTTP на сервер (можно self-signed)
   - **Full** - Cloudflare → HTTPS на сервер (любой сертификат)
   - **Full (strict)** - Cloudflare → HTTPS с валидным сертификатом (Let's Encrypt)

**Шаг 2: Настройка Origin Rules**

```
Proxy status: Proxied (orange cloud)
SSL/TLS encryption mode: Full (strict)
```

**Шаг 3: Генерация сертификата**

```bash
# Для Full (strict) используйте Let's Encrypt
./setup_ssl.sh yourdomain.com admin@yourdomain.com

# Или для Flexible можно использовать self-signed
./setup_ssl.sh
# Опция 2
```

**Преимущества Cloudflare:**
- ✅ Бесплатный SSL на edge
- ✅ DDoS protection
- ✅ CDN глобальная доставка
- ✅ Не нужно открывать порт 80 на сервере (в Full mode)

---

## 🛡️ БЕЗОПАСНОСТЬ SSL КОНФИГУРАЦИИ

### TLS Версии и Cipher Suites

Наша конфигурация использует современные стандарты:

```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:...';
ssl_prefer_server_ciphers off;
```

**Проверка безопасности:**
```bash
# Online тест
https://www.ssllabs.com/ssltest/analyze.html?d=yourdomain.com

# Локальная проверка
nmap --script ssl-enum-ciphers -p 443 yourdomain.com
```

### Security Headers

Добавлены в nginx.conf:
```nginx
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Content-Security-Policy "..." always;
```

### HSTS (HTTP Strict Transport Security)

Принудительно использует HTTPS:
```nginx
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
```

**Важно:** После включения HSTS сайт будет доступен ТОЛЬКО по HTTPS в течение 2 лет!

---

## 🔍 МОНИТОРИНГ И ОБНОВЛЕНИЕ

### Проверка срока действия сертификата

```bash
# Через OpenSSL
openssl x509 -enddate -noout -in ssl/certs/fullchain.pem

# Через curl
curl -vI https://yourdomain.com 2>&1 | grep expire

# Автоматическая проверка (добавить в crontab)
0 0 * * * openssl x509 -checkend 864000 -noout -in /path/to/ssl/certs/fullchain.pem && echo "OK" || echo "EXPIRING SOON"
```

### Ручное обновление Let's Encrypt

```bash
# Принудительное обновление
docker-compose exec certbot certbot renew --force-renewal

# Проверка статуса
docker-compose exec certbot certbot certificates
```

### Логи Certbot

```bash
docker-compose logs certbot
docker-compose exec certbot cat /var/log/letsencrypt/letsencrypt.log
```

---

## 🐛 УСТРАНЕНИЕ НЕПОЛАДОК

### Проблема: Certificate issuance failed

**Причины:**
1. DNS не настроен правильно
2. Порт 80 заблокирован firewall
3. Domain validation не прошла

**Решение:**
```bash
# Проверьте DNS
dig yourdomain.com A

# Проверьте firewall
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Попробуйте standalone mode вместо webroot
docker run --rm -p 80:80 certbot/certbot certonly --standalone -d yourdomain.com
```

### Проблема: SSL certificate error в браузере

**Причины:**
1. Self-signed сертификат (ожидаемо)
2. Сертификат истек
3. Несоответствие домена

**Решение:**
```bash
# Проверьте сертификат
openssl x509 -in ssl/certs/fullchain.pem -text -noout | grep "Subject:"

# Обновите если истек
./setup_ssl.sh yourdomain.com admin@yourdomain.com
```

### Проблема: Mixed Content warnings

**Причина:** Некоторые ресурсы загружаются по HTTP

**Решение:**
1. Обновите все URL в коде на HTTPS
2. Используйте protocol-relative URLs (`//example.com/resource`)
3. Добавьте Content-Security-Policy header

### Проблема: ERR_TOO_MANY_REDIRECTS

**Причина:** Циклическая переадресация HTTP → HTTPS

**Решение:**
```nginx
# В nginx.conf убедитесь что только один server блок делает redirect
server {
    listen 80;
    return 301 https://$host$request_uri;
}
```

---

## 📊 ТЕСТирование SSL КОНФИГУРАЦИИ

### Онлайн инструменты

1. **SSL Labs Test** (наиболее полный)
   ```
   https://www.ssllabs.com/ssltest/analyze.html?d=yourdomain.com
   ```
   Цель: Рейтинг A или A+

2. **Security Headers**
   ```
   https://securityheaders.com/?q=yourdomain.com
   ```

3. **Mozilla Observatory**
   ```
   https://observatory.mozilla.org/analyze/yourdomain.com
   ```

### Локальные тесты

```bash
# Проверка TLS версии
openssl s_client -connect yourdomain.com:443 -tls1_2

# Проверка cipher suites
nmap --script ssl-enum-ciphers -p 443 yourdomain.com

# Проверка сертификата
openssl s_client -showcerts -connect yourdomain.com:443 </dev/null

# Проверка HSTS
curl -I https://yourdomain.com | grep Strict-Transport-Security
```

---

## 🔄 MIGRATION С HTTP НА HTTPS

### Шаг 1: Получите SSL сертификат

```bash
./setup_ssl.sh yourdomain.com admin@yourdomain.com
```

### Шаг 2: Обновите конфигурацию

**nginx.conf:**
```nginx
# Измените server_name
server_name yourdomain.com www.yourdomain.com;

# Раскомментируйте SSL пути
ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
```

**.env:**
```bash
CORS_ORIGINS=https://yourdomain.com
NEXT_PUBLIC_API_URL=https://yourdomain.com/api
```

### Шаг 3: Обновите frontend код

**frontend/lib/api.ts:**
```typescript
// Было:
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// Стало:
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'https://yourdomain.com/api'
```

### Шаг 4: Перезапустите

```bash
docker-compose down
docker-compose up -d
```

### Шаг 5: Проверьте

- [ ] https://yourdomain.com загружается
- [ ] Зеленый замок в браузере
- [ ] API запросы работают
- [ ] Нет mixed content warnings
- [ ] Redirect HTTP → HTTPS работает

---

## 💰 СТОИМОСТЬ SSL

| Тип сертификата | Стоимость | Обновление |
|----------------|-----------|------------|
| **Let's Encrypt** | **Бесплатно** | Автоматически (90 дней) |
| Self-signed | Бесплатно | Вручную |
| Comodo/Sectigo | $5-50/год | Вручную |
| DigiCert | $100-500/год | Вручную |
| Wildcard Let's Encrypt | Бесплатно | Автоматически |

**Рекомендация:** Используйте Let's Encrypt для production!

---

## 🎯 BEST PRACTICES

### ✅ DO:
- Используйте Let's Encrypt для production
- Включите HSTS после тестирования
- Настройте автоматическое обновление
- Регулярно проверяйте expiry date
- Используйте strong cipher suites
- Включите OCSP stapling (опционально)
- Мониторьте SSL Labs рейтинг

### ❌ DON'T:
- Не используйте self-signed в production
- Не отключайте TLS 1.2 (пока нужен для совместимости)
- Не храните private key в git
- Не используйте weak ciphers (RC4, DES, MD5)
- Не забывайте про renewal
- Не игнорируйте security headers

---

## 📚 ДОПОЛНИТЕЛЬНЫЕ РЕСУРСЫ

**Документация:**
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Nginx SSL Configuration](https://nginx.org/en/docs/http/configuring_https_servers.html)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [OWASP TLS Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html)

**Инструменты:**
- [SSL Labs Test](https://www.ssllabs.com/ssltest/)
- [Certbot Documentation](https://certbot.eff.org/docs/)
- [Security Headers Scanner](https://securityheaders.com/)

---

## 🚀 QUICK REFERENCE COMMANDS

```bash
# Setup SSL
./setup_ssl.sh yourdomain.com admin@yourdomain.com

# Check certificate expiry
openssl x509 -enddate -noout -in ssl/certs/fullchain.pem

# Force renewal
docker-compose exec certbot certbot renew --force-renewal

# View certificates
docker-compose exec certbot certbot certificates

# Test SSL configuration
docker-compose config

# Restart with new certificates
docker-compose restart frontend

# Check logs
docker-compose logs frontend
docker-compose logs certbot

# Backup certificates
tar czf ssl-backup-$(date +%Y%m%d).tar.gz ssl/certs/
```

---

**Дата создания:** 26 апреля 2026  
**Версия:** 1.0  
**Статус:** ✅ Полная SSL поддержка добавлена в проект
