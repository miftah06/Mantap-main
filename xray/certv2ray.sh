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
echo start
sleep 0.5
source /var/lib/crot/ipvps.conf
domain=$(cat /etc/xray/domain)
sudo lsof -t -i tcp:80 -s tcp:listen | sudo xargs kill
cd /root/
curl https://get.acme.sh | sh
bash acme.sh --install
rm acme.sh
cd .acme.sh
echo "starting...., Port 80 Akan di Hentikan Saat Proses install Cert"
#!/bin/bash

# Install acme.sh if not already installed
curl https://get.acme.sh | sh

# Initialize acme.sh in the current session
source ~/.bashrc

# Prompt user for email and domain
read -p "Enter your email address for registration: " email
read -p "Enter your domain name: " domain

# Register account with ZeroSSL
acme.sh --register-account --server https://acme.zerossl.com/v2/DV90 --email $email

# Issue certificate for your domain
acme.sh --issue --standalone -d $domain

# Install certificate
bash acme.sh --installcert -d $domain --fullchainpath /etc/xray/xray.crt --keypath /etc/xray/xray.key
echo "Certificate installation completed for $domain."
