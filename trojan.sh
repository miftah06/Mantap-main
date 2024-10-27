#!/bin/bash
# SL
# ==========================================
# Color Definitions
RED='\033[0;31m'
NC='\033[0m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
# ==========================================

# Arguments: Username and Expiration (Days)
user="$1"
masaaktif="$2"

# Check Arguments
if [[ -z "$user" || -z "$masaaktif" ]]; then
    echo -e "${CYAN}Usage: $0 <username> <expiration_days>${NC}"
    exit 1
fi

# Permission Check
MYIP=$(wget -qO- ipinfo.io/ip)
echo "Checking VPS"
IZIN=$(curl -s ipinfo.io/ip | grep "$MYIP")
if [[ "$MYIP" == "$MYIP" ]]; then
    echo -e "${GREEN}Permission Accepted...${NC}"
else
    echo -e "${RED}Permission Denied!${NC}"
    exit 1
fi

# Load Configuration
source /var/lib/crot/ipvps.conf
domain=${IP:-$(cat /etc/xray/domain)}
tr=$(grep -w "Trojan" ~/log-install.txt | cut -d: -f2 | sed 's/ //g')

# Check if Username Exists
user_EXISTS=$(grep -w "$user" /etc/xray/config.json | wc -l)
if [[ "$user_EXISTS" -gt 0 ]]; then
    echo -e "${RED}Error: Username ${user} already exists on VPS. Please choose another.${NC}"
    exit 1
fi

# Generate Expiry Dates
hariini=$(date +"%Y-%m-%d")
exp=$(date -d "$masaaktif days" +"%Y-%m-%d")

# Add User to Configuration
sed -i '/#xray-trojan$/a\### '"$user $exp"'\
},{"password": "'""$user""'","email": "'""$user""'"' /etc/xray/config.json

# Restart Service
systemctl restart xray.service
service cron restart

# Generate Trojan Link
trojanlink="trojan://${user}@${domain}:${tr}"

# Display Account Information
clear
echo -e "${CYAN}====== XRAYS/TROJAN Account Information ======${NC}"
echo -e "Remarks      : ${user}"
echo -e "IP/Host      : ${MYIP}"
echo -e "Domain       : ${domain}"
echo -e "Port         : ${tr}"
echo -e "Key          : ${user}"
echo -e "Created      : ${hariini}"
echo -e "Expired      : ${exp}"
echo -e "============================================"
echo -e "Link Trojan  : ${trojanlink}"
echo -e "============================================"
