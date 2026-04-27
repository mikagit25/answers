#!/bin/bash
# ============================================
# SSL Certificate Setup Script for Answers Platform
# Supports: Let's Encrypt (automatic) or Manual certificates
# ============================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}SSL Certificate Setup for Answers Platform${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Configuration
DOMAIN="${1:-yourdomain.com}"
EMAIL="${2:-admin@yourdomain.com}"
SSL_DIR="./ssl"
CERTS_DIR="$SSL_DIR/certs"

# Create SSL directories
echo -e "${YELLOW}Creating SSL directories...${NC}"
mkdir -p "$CERTS_DIR"
chmod 755 "$CERTS_DIR"

# Function to check if domain is accessible
check_domain() {
    echo -e "${YELLOW}Checking if domain $DOMAIN is accessible...${NC}"
    if ping -c 1 -W 2 "$DOMAIN" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Domain is reachable${NC}"
        return 0
    else
        echo -e "${RED}✗ Domain is not reachable. Make sure DNS is configured correctly.${NC}"
        return 1
    fi
}

# Option 1: Let's Encrypt (Recommended for production)
setup_letsencrypt() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}Setting up Let's Encrypt SSL Certificate${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    
    # Check if domain is ready
    if ! check_domain; then
        echo -e "${YELLOW}Continuing anyway... (certificate issuance may fail)${NC}"
    fi
    
    # Stop nginx temporarily for certbot standalone mode
    echo -e "${YELLOW}Stopping services for certificate issuance...${NC}"
    docker-compose down || true
    
    # Run certbot in standalone mode
    echo -e "${YELLOW}Requesting certificate from Let's Encrypt...${NC}"
    docker run --rm \
        -v "$CERTS_DIR:/etc/letsencrypt" \
        -v "./ssl/www:/var/www/certbot" \
        -p 80:80 \
        certbot/certbot certonly \
        --standalone \
        --email "$EMAIL" \
        --agree-tos \
        --no-eff-email \
        --force-renewal \
        -d "$DOMAIN" \
        -d "www.$DOMAIN" || {
            echo -e "${RED}Failed to obtain certificate. Please check:${NC}"
            echo -e "  1. Domain DNS is correctly configured"
            echo -e "  2. Port 80 is not blocked by firewall"
            echo -e "  3. Try again in a few minutes"
            exit 1
        }
    
    # Copy certificates to the correct location
    echo -e "${YELLOW}Copying certificates...${NC}"
    cp "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" "$CERTS_DIR/fullchain.pem" 2>/dev/null || \
    cp "$CERTS_DIR/../live/$DOMAIN/fullchain.pem" "$CERTS_DIR/fullchain.pem" || {
        echo -e "${YELLOW}Certificate files not found in expected location.${NC}"
        echo -e "${YELLOW}Please manually copy from /etc/letsencrypt/live/$DOMAIN/${NC}"
    }
    
    cp "/etc/letsencrypt/live/$DOMAIN/privkey.pem" "$CERTS_DIR/privkey.pem" 2>/dev/null || \
    cp "$CERTS_DIR/../live/$DOMAIN/privkey.pem" "$CERTS_DIR/privkey.pem" || {
        echo -e "${YELLOW}Private key not found in expected location.${NC}"
    }
    
    # Set proper permissions
    chmod 644 "$CERTS_DIR/fullchain.pem" 2>/dev/null || true
    chmod 600 "$CERTS_DIR/privkey.pem" 2>/dev/null || true
    
    echo -e "${GREEN}✓ Let's Encrypt certificate setup complete!${NC}"
    echo -e "${YELLOW}Certificate will auto-renew via certbot container${NC}"
}

# Option 2: Self-signed certificate (For development/testing)
setup_selfsigned() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}Generating Self-Signed SSL Certificate${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo -e "${YELLOW}⚠️  WARNING: Self-signed certificates are for development only!${NC}"
    echo -e "${YELLOW}   Browsers will show security warnings.${NC}"
    echo ""
    
    read -p "Continue with self-signed certificate? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Aborted.${NC}"
        exit 0
    fi
    
    echo -e "${YELLOW}Generating self-signed certificate...${NC}"
    
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout "$CERTS_DIR/privkey.pem" \
        -out "$CERTS_DIR/fullchain.pem" \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=$DOMAIN" \
        -addext "subjectAltName=DNS:$DOMAIN,DNS:www.$DOMAIN"
    
    # Set proper permissions
    chmod 644 "$CERTS_DIR/fullchain.pem"
    chmod 600 "$CERTS_DIR/privkey.pem"
    
    echo -e "${GREEN}✓ Self-signed certificate generated!${NC}"
    echo -e "${YELLOW}Certificate valid for 365 days${NC}"
    echo -e "${YELLOW}Location: $CERTS_DIR/${NC}"
}

# Option 3: Use existing certificates
use_existing() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}Using Existing SSL Certificates${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    
    echo -e "${YELLOW}Please provide paths to your certificate files:${NC}"
    read -p "Full chain certificate (fullchain.pem or cert.pem): " CERT_PATH
    read -p "Private key (privkey.pem or key.pem): " KEY_PATH
    
    if [ ! -f "$CERT_PATH" ]; then
        echo -e "${RED}Error: Certificate file not found: $CERT_PATH${NC}"
        exit 1
    fi
    
    if [ ! -f "$KEY_PATH" ]; then
        echo -e "${RED}Error: Private key file not found: $KEY_PATH${NC}"
        exit 1
    fi
    
    echo -e "${YELLOW}Copying certificates...${NC}"
    cp "$CERT_PATH" "$CERTS_DIR/fullchain.pem"
    cp "$KEY_PATH" "$CERTS_DIR/privkey.pem"
    
    # Set proper permissions
    chmod 644 "$CERTS_DIR/fullchain.pem"
    chmod 600 "$CERTS_DIR/privkey.pem"
    
    echo -e "${GREEN}✓ Certificates copied successfully!${NC}"
}

# Option 4: Cloudflare SSL (Proxy mode)
setup_cloudflare_info() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}Cloudflare SSL Configuration${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo -e "${GREEN}If you're using Cloudflare:${NC}"
    echo -e "  1. Enable 'Flexible' or 'Full' SSL in Cloudflare dashboard"
    echo -e "  2. Cloudflare will handle SSL termination"
    echo -e "  3. You can use self-signed certs on the server"
    echo -e "  4. Or use Let's Encrypt for 'Full (strict)' mode"
    echo ""
    echo -e "${YELLOW}Would you like to generate self-signed certs for Cloudflare? (y/N): ${NC}"
    read -p "" -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        setup_selfsigned
    fi
}

# Main menu
echo -e "${GREEN}Choose SSL certificate option:${NC}"
echo -e "  1) Let's Encrypt (Free, automatic renewal) - ${BLUE}Recommended${NC}"
echo -e "  2) Self-signed certificate (Development only)"
echo -e "  3) Use existing certificates"
echo -e "  4) Cloudflare proxy information"
echo ""
read -p "Enter choice [1-4]: " choice

case $choice in
    1)
        setup_letsencrypt
        ;;
    2)
        setup_selfsigned
        ;;
    3)
        use_existing
        ;;
    4)
        setup_cloudflare_info
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

# Verify certificates
echo ""
echo -e "${BLUE}Verifying SSL certificates...${NC}"
if [ -f "$CERTS_DIR/fullchain.pem" ] && [ -f "$CERTS_DIR/privkey.pem" ]; then
    echo -e "${GREEN}✓ Certificate files found${NC}"
    
    # Check certificate expiry
    if command -v openssl &> /dev/null; then
        EXPIRY=$(openssl x509 -enddate -noout -in "$CERTS_DIR/fullchain.pem" 2>/dev/null | cut -d= -f2)
        if [ ! -z "$EXPIRY" ]; then
            echo -e "${GREEN}✓ Certificate expires: $EXPIRY${NC}"
        fi
    fi
    
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}SSL Setup Complete!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo -e "  1. Update nginx.conf with your domain name"
    echo -e "  2. Update .env file with CORS_ORIGINS=https://$DOMAIN"
    echo -e "  3. Run: docker-compose up -d"
    echo -e "  4. Test: https://$DOMAIN"
    echo ""
else
    echo -e "${RED}✗ Certificate files not found!${NC}"
    echo -e "${RED}Please run this script again or manually place certificates in: $CERTS_DIR/${NC}"
    exit 1
fi
