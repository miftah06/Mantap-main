#!/bin/bash
# ==========================================
# Color
RED='\033[0;31m'
NC='\033[0m'
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
LIGHT='\033[0;37m'
# ==========================================
# Getting
clear
echo -e "${GREEN}Starting...${NC}"
sleep 0.5

# Load the domain from the configuration file
source /var/lib/crot/ipvps.conf
domain=$(cat /etc/xray/domain)

# Stop any process listening on port 80
echo -e "${ORANGE}Stopping any services using port 80...${NC}"
if sudo lsof -t -i tcp:80 -s tcp:listen; then
    sudo kill $(sudo lsof -t -i tcp:80 -s tcp:listen)
else
    echo -e "${LIGHT}No services are using port 80.${NC}"
fi

# Install acme.sh if not already installed
if ! command -v acme.sh &> /dev/null; then
    echo -e "${ORANGE}Installing acme.sh...${NC}"
    curl https://get.acme.sh | sh
    sudo mv ~/.acme.sh/acme.sh /usr/bin/acme.sh
    sudo chmod +x /usr/bin/acme.sh
else
    echo -e "${GREEN}acme.sh is already installed.${NC}"
fi

# Initialize acme.sh in the current session
source ~/.bashrc

# Prompt user for email and domain
read -p "Enter your email address for registration: " email

# Check for existing certificate
if acme.sh --list | grep -q "$domain"; then
    echo -e "${BLUE}An existing certificate for $domain was found. No need to issue a new one.${NC}"
else
    # Register account with ZeroSSL
    acme.sh --register-account --server https://acme.zerossl.com/v2/DV90 --email $email

    # Issue certificate for your domain
    acme.sh --issue --standalone -d $domain --force
fi

# Install certificate
acme.sh --installcert -d $domain --fullchainpath /etc/xray/xray.crt --keypath /etc/xray/xray.key
echo -e "${GREEN}Certificate installation completed for $domain.${NC}"
