#!/bin/bash

# ==========================================
# Color Definitions for Output
RED='\033[0;31m'
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m'
# ==========================================

# Arguments: Username, Password, Expiration (Days)
Login="$1"
Pass="$2"
masaaktif="$3"

# Check Arguments
if [[ -z "$Login" || -z "$Pass" || -z "$masaaktif" ]]; then
    echo -e "${ORANGE}Usage: $0 <username> <password> <expiration_days>${NC}"
    exit 1
fi

# Load Domain and Port Information
domain=$(cat /etc/xray/domain)
sldomain=$(cat /root/nsdomain)
cdndomain=$(cat /root/awscdndomain)
slkey=$(cat /etc/slowdns/server.pub)
IP=$(wget -qO- ipinfo.io/ip)
ws=$(grep -w "Websocket TLS" ~/log-install.txt | cut -d: -f2 | sed 's/ //g')
ws2=$(grep -w "Websocket None TLS" ~/log-install.txt | cut -d: -f2 | sed 's/ //g')
ssl=$(grep -w "Stunnel5" ~/log-install.txt | cut -d: -f2)
sqd=$(grep -w "Squid" ~/log-install.txt | cut -d: -f2)
ovpn=$(netstat -nlpt | grep -i openvpn | grep -i 0.0.0.0 | awk '{print $4}' | cut -d: -f2)
ovpn2=$(netstat -nlpu | grep -i openvpn | grep -i 0.0.0.0 | awk '{print $4}' | cut -d: -f2)

# Restart Necessary Services
services=("client-sldns" "server-sldns" "ws-tls" "ws-nontls" "ssh-ohp" "dropbear-ohp" "openvpn-ohp")
for service in "${services[@]}"; do
    systemctl restart "$service"
done

# Add New User with Expiration
useradd -e "$(date -d "$masaaktif days" +"%Y-%m-%d")" -s /bin/false -M "$Login"
echo -e "$Pass\n$Pass" | passwd "$Login" &> /dev/null

# Date Variables
hariini=$(date +"%Y-%m-%d")
expi=$(date -d "$masaaktif days" +"%Y-%m-%d")

# Display Account Information
clear
echo -e "${CYAN}====== SSH & OpenVPN Account Information ======${NC}"
echo -e "Username           : $Login"
echo -e "Password           : $Pass"
echo -e "Created            : $hariini"
echo -e "Expired            : $expi"
echo -e "IP/Host            : $IP"
echo -e "Domain SSH         : $domain"
echo -e "Domain Cloudflare  : $domain"
echo -e "Domain CloudFront  : $cdndomain"
echo -e "========== SLOWDNS Configuration ==========="
echo -e "DNS                : 8.8.8.8"
echo -e "Name Server (NS)   : $sldomain"
echo -e "DNS PUBLIC KEY     : $slkey"
echo -e "Domain SlowDNS     : $sldomain"
echo -e "=========== Service Ports ==================="
echo -e "SlowDNS            : 443, 22, 109, 143"
echo -e "OpenSSH            : 22"
echo -e "Dropbear           : 443, 109, 143"
echo -e "SSL/TLS            : 443, 4443, 445, 447, 222"
echo -e "SSH Websocket TLS  : $ws"
echo -e "SSH Websocket HTTP : 8880"
echo -e "BadVPN UDPGW       : 7100, 7200, 7300"
echo -e "OHP SSH            : 8181"
echo -e "OHP Dropbear       : 8282"
echo -e "OHP OpenVPN        : 8383"
echo -e "OVPN Websocket     : 2086"
echo -e "OVPN TCP           : http://$IP:89/tcp.ovpn"
echo -e "OVPN UDP           : http://$IP:89/udp.ovpn"
echo -e "OVPN SSL           : http://$IP:89/ssl.ovpn"
echo -e "============================================="
echo -e "SNI/Server Spoof   : Use with any bug"
echo -e "Payload Websocket TLS:"
echo -e "GET wss://bug.com/ HTTP/1.1[crlf]Host: [host][crlf]Upgrade: websocket[crlf][crlf]"
echo -e "Payload Websocket HTTP:"
echo -e "GET / HTTP/1.1[crlf]Host: [host][crlf]Upgrade: websocket[crlf][crlf]"
echo -e "============================================="
echo -e "Script Mod By SL"
