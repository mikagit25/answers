# SSL Certificates Directory

## ⚠️ IMPORTANT SECURITY NOTICE

**NEVER commit SSL certificates or private keys to version control!**

This directory is excluded from git via `.gitignore` for security reasons.

---

## 📁 Directory Structure

```
ssl/
├── certs/
│   ├── fullchain.pem      # Your SSL certificate + intermediate CA certs
│   ├── privkey.pem        # Your private key (KEEP SECRET!)
│   └── .gitkeep           # Keeps directory in git (empty file)
├── www/                   # Let's Encrypt webroot validation
└── README.md              # This file
```

---

## 🚀 How to Setup SSL

### Option 1: Let's Encrypt (Recommended)

```bash
# Run the automated setup script
chmod +x ../setup_ssl.sh
../setup_ssl.sh yourdomain.com admin@yourdomain.com
```

This will:
1. Obtain certificate from Let's Encrypt
2. Place files in `ssl/certs/`
3. Configure automatic renewal

### Option 2: Self-Signed (Development Only)

```bash
# Generate self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/certs/privkey.pem \
  -out ssl/certs/fullchain.pem \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
```

⚠️ Browsers will show security warnings!

### Option 3: Existing Certificates

Copy your certificate files:
```bash
cp /path/to/your/fullchain.pem ssl/certs/fullchain.pem
cp /path/to/your/privkey.pem ssl/certs/privkey.pem

# Set proper permissions
chmod 644 ssl/certs/fullchain.pem
chmod 600 ssl/certs/privkey.pem
```

---

## 🔒 File Permissions

Correct permissions are critical for security:

```bash
# Certificate (public)
chmod 644 ssl/certs/fullchain.pem  # rw-r--r--

# Private key (secret!)
chmod 600 ssl/certs/privkey.pem    # rw-------

# Directory
chmod 755 ssl/certs/               # rwxr-xr-x
```

---

## 📋 Required Files

For SSL to work, you need:

1. **fullchain.pem** (or cert.pem)
   - Your domain certificate
   - Plus any intermediate CA certificates
   - Can be public

2. **privkey.pem** (or key.pem)
   - Your private key
   - **MUST BE KEPT SECRET**
   - Never share, never commit to git

---

## 🔄 Certificate Renewal

### Let's Encrypt (Automatic)

The certbot container in docker-compose.yml automatically renews certificates every 90 days.

Check renewal status:
```bash
docker-compose logs certbot
docker-compose exec certbot certbot certificates
```

Force renewal:
```bash
docker-compose exec certbot certbot renew --force-renewal
```

### Manual Certificates

You must manually replace expired certificates:

1. Obtain new certificate from your CA
2. Replace files in `ssl/certs/`
3. Restart nginx:
   ```bash
   docker-compose restart frontend
   ```

---

## ✅ Verification

After placing certificates, verify:

```bash
# Check certificate details
openssl x509 -in ssl/certs/fullchain.pem -text -noout

# Check expiry date
openssl x509 -enddate -noout -in ssl/certs/fullchain.pem

# Verify private key matches certificate
openssl x509 -noout -modulus -in ssl/certs/fullchain.pem | md5sum
openssl rsa -noout -modulus -in ssl/certs/privkey.pem | md5sum
# Both should produce the same hash
```

---

## 🐛 Troubleshooting

### Problem: Permission denied

```bash
# Fix permissions
chmod 600 ssl/certs/privkey.pem
chmod 644 ssl/certs/fullchain.pem
chown -R 101:101 ssl/certs/  # nginx user
```

### Problem: Certificate not found

Ensure files are in correct location:
```bash
ls -la ssl/certs/
# Should show:
# fullchain.pem
# privkey.pem
```

### Problem: Invalid certificate format

Convert if needed:
```bash
# From .crt and .key to .pem
cat cert.crt intermediate.crt > fullchain.pem
cp key.key privkey.pem

# From PFX/PKCS12
openssl pkcs12 -in certificate.pfx -out fullchain.pem -nodes
```

---

## 📚 Additional Resources

- [SSL Setup Guide](../SSL_SETUP_GUIDE.md)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Nginx SSL Configuration](https://nginx.org/en/docs/http/configuring_https_servers.html)

---

**Remember:** Keep your private key secure and never commit it to version control! 🔒
