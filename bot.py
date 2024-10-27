import telebot
import json
import csv
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import telebot
import json
import csv
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import telebot
import pandas as pd
import os
import subprocess
import smtplib
import json

# Inisialisasi bot dengan token
TOKEN = 'ambil di https://t.me/BotFather'  # Gantilah dengan token bot Anda
bot = telebot.TeleBot(TOKEN)

link_jualan = "https://wa.me/+6285656777382"  # Ganti dengan link QRIS Anda

import telebot
import json
import csv
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import telebot
import json
import csv
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import telebot
import pandas as pd
import os
import subprocess
import smtplib
import json

# Load users from JSON file
def load_usernya_from_json():
    global user_ids, group_ids
    try:
        with open('admin.json', 'r') as file:
            data = json.load(file)
            users = data.get('users', [])
            user_ids = [user['chat_id'] for user in users if user['chat_id'] > 0]  # Positive chat IDs
            group_ids = [user['chat_id'] for user in users if user['chat_id'] < 0]  # Negative chat IDs
            return users
    except (IOError, json.JSONDecodeError) as e:
        logging.error(f"Error reading JSON file: {e}")
        return []
        

def is_whitelisted(user_id):
    admins = load_admins()  # Memuat admin dari file
    return str(user_id) in admins.keys()  # Cek jika user_id ada dalam kunci JSON admin
    
# Fungsi untuk memuat data langganan dari file JSON
def load_subscriptions():
    try:
        with open('subscriptions.json', mode='r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"subscriptions": []}  # Mengembalikan list kosong jika file tidak ada

# Fungsi untuk menyimpan data langganan ke dalam file JSON
def save_subscriptions(subscriptions):
    with open('subscriptions.json', mode='w') as file:
        json.dump(subscriptions, file, indent=4)

# Fungsi untuk membaca data pelanggan dari file JSON
def load_pelanggan():
    try:
        with open('pelanggan.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Fungsi untuk membaca data admin dari file JSON
def load_admin():
    try:
        with open('admin.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

import csv

def read_barang():
    items = []
    with open('items.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            items.append(row)
    return items


# Fungsi untuk menyimpan barang ke file CSV
def save_barang(barang_list):
    if barang_list:  # Cek jika daftar tidak kosong
        with open('items.csv', mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=barang_list[0].keys())
            writer.writeheader()
            writer.writerows(barang_list)

# Command '/siaran' untuk pelanggan
@bot.message_handler(commands=['siaran'])
def siaran_pelanggan(message):
    try:
        data = message.text.split(" ", 1)
        tunneling_address = data[1] if len(data) > 1 else None
        
        if tunneling_address:
            bot.reply_to(message, f"Pesan siaran akan dikirim ke alamat tunneling: {tunneling_address}.")
            # Di sini, tambahkan logika untuk mengirim notifikasi ke pengguna yang terdaftar.
        else:
            bot.reply_to(message, "Silakan masukkan alamat tunneling setelah perintah.")
    except IndexError:
        bot.reply_to(message, "Format salah. Gunakan: /siaran <alamat tunneling> query")

# Command '/notifikasi' untuk admin
@bot.message_handler(commands=['notifikasi'])
def notifikasi_admin(message):
    admins = load_admins()
    if str(message.chat.id) not in admins:
        bot.reply_to(message, "Anda tidak memiliki akses admin.")
        return

    # Mengambil pesan dari admin
    try:
        data = message.text.split(" ", 1)
        notification_message = data[1] if len(data) > 1 else None
        
        if notification_message:
            subscriptions = load_subscriptions()
            for subscription in subscriptions['subscriptions']:
                bot.send_message(subscription['user_id'], notification_message)
            bot.reply_to(message, "Notifikasi berhasil dikirim ke semua pengguna.")
        else:
            bot.reply_to(message, "Silakan masukkan pesan setelah perintah.")
    except IndexError:
        bot.reply_to(message, "Format salah. Gunakan: /notifikasi <pesan> query")

# Command '/daftar' untuk mendaftar akun baru
@bot.message_handler(commands=['daftar'])
def daftar_user(message):
    try:
        data = message.text.split(" ")
        email, password = data[1], data[2]
        pelanggan = load_pelanggan()
        
        # Memeriksa apakah pengguna sudah terdaftar
        if str(message.chat.id) in pelanggan:
            bot.reply_to(message, "Akun sudah terdaftar.")
            return
        
        # Mendapatkan tanggal kedaluwarsa langganan
        subscription_date = datetime.now().strftime("%Y-%m-%d")
        expiration_date = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
        
        # Menyimpan data langganan
        subscriptions = load_subscriptions()
        new_subscription = {
            "user_id": str(message.chat.id),
            "email": email,
            "status": "active",
            "subscription_date": subscription_date,
            "expiration_date": expiration_date,
            "transactions": []
        }
        subscriptions['subscriptions'].append(new_subscription)
        save_subscriptions(subscriptions)
        
        # Menyimpan data pelanggan
        pelanggan[str(message.chat.id)] = {'email': email, 'password': password, 'saldo': 100}
        with open('pelanggan.json', 'w') as f:
            json.dump(pelanggan, f)
        
        bot.reply_to(message, "Pendaftaran berhasil.")
    except IndexError:
        bot.reply_to(message, "Format salah. Gunakan: /daftar email password")

# Command '/login' untuk login
@bot.message_handler(commands=['login'])
def login_user(message):
    try:
        data = message.text.split(" ")
        email, password = data[1], data[2]
        pelanggan = load_pelanggan()
        
        # Memeriksa apakah email dan password cocok
        if str(message.chat.id) in pelanggan and pelanggan[str(message.chat.id)]['email'] == email and pelanggan[str(message.chat.id)]['password'] == password:
            bot.reply_to(message, "Login berhasil.")
        else:
            bot.reply_to(message, "Login gagal, akun tidak ditemukan atau password salah.")
    except IndexError:
        bot.reply_to(message, "Format salah. Gunakan: /login email password")

# Membaca data barang dari CSV
def load_items():
    if os.path.exists('items.csv'):
        return pd.read_csv('items.csv')
    return pd.DataFrame(columns=['item_id', 'price', 'command', 'tunnel', 'user_id', 'saldo', 'konten'])

# Command '/pesan' untuk admin mengonfirmasi pesan kepada pengguna
@bot.message_handler(commands=['pesan'])
def pesan_to_user(message):
    admins = load_admins()
    if str(message.chat.id) not in admins:
        bot.reply_to(message, "Anda tidak memiliki akses admin.")
        return

    # Mengambil data dari perintah
    try:
        # Memisahkan input dari pesan yang diterima
        data = message.text.split(" ", 2)  # Memisahkan menjadi 3 bagian
        
        # Mengambil user_id dan query
        user_id = data[1] if len(data) > 1 else None
        user_message = data[2] if len(data) > 2 else "Pesanan Anda telah dikonfirmasi. Terima kasih! silahkan menunggu!"
        
        if user_id is None:
            bot.reply_to(message, "Format salah. Gunakan: /pesan {user_id} {query}")
            return

        # Mengambil detail pelanggan
        pelanggan = load_pelanggan()
        if user_id not in pelanggan:
            bot.reply_to(message, f"User ID {user_id} tidak ditemukan.")
            return

        # Mengirim notifikasi ke pengguna
        bot.send_message(user_id, user_message)
        bot.reply_to(message, f"Pesan telah dikirim kepada pengguna {user_id}.")
    
    except IndexError:
        bot.reply_to(message, "Format salah. Gunakan: /pesan {user_id} {query}")
        
        
# Fungsi untuk mengirim email notifikasi ke admin
def notify_email(message):
    admin_email = 'admin@example.com'  # Ganti dengan email admin
    subject = 'Notifikasi Transaksi'
    body = message

    # Membangun pesan email
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = admin_email
    msg['To'] = admin_email

    # Mengirim email
    try:
        with smtplib.SMTP('smtp.example.com', 587) as server:  # Ganti dengan server SMTP Anda
            server.starttls()  # Mulai TLS untuk keamanan
            server.login('your_email@example.com', 'your_password')  # Ganti dengan kredensial email Anda
            server.sendmail(admin_email, [admin_email], msg.as_string())
        print("Notifikasi email terkirim.")
    except Exception as e:
        print(f"Error mengirim email: {e}")

# Fungsi untuk mengirim notifikasi ke admin
def notify_admin(message):
    admins = load_admins()
    for admin_id in admins.keys():
        bot.send_message(admin_id, message)

# Fungsi untuk memproduksi tautan QRIS untuk pembelian
def generate_qris_link(amount):
    return f"{link_jualan}" #?amount={amount}"  # Konten link QRIS dengan jumlah
    
import requests

def notify_bot(username, password):
    # Menggunakan bot Telegram untuk mengirim informasi akun
    telegram_token = '7041898397:AAFahnEv3xgUbcid77ph62pqH0DxEnMV0Co'  # Ganti dengan token bot Anda
    chat_id = load_admins  # Ganti dengan ID chat yang sesuai

    message = f"Akun VPN baru dibuat!\nUsername: {username}\nPassword: {password}"
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'  # Menggunakan HTML untuk pemformatan
    }

    response = requests.post(url, json=payload)
    return response.json()

# Dalam fungsi pembuat akun, setelah akun berhasil dibuat, panggil notify_bot
def create_vpn_account(vpn_type, username, password, limit_ip, duration):
    """
    Kode sebelumnya untuk membuat akun VPN...
    """

    # Panggil notify_bot di sini
    notify_bot(username, password)

# Fungsi untuk memuat data langganan dari file JSON
def load_subscriptions():
    try:
        with open('subscriptions.json', mode='r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"subscriptions": []}  # Mengembalikan list kosong jika file tidak ada

# Fungsi untuk menyimpan data langganan ke dalam file JSON
def save_subscriptions(subscriptions):
    with open('subscriptions.json', mode='w') as file:
        json.dump(subscriptions, file, indent=4)

# Fungsi untuk membaca data pelanggan dari file JSON
def load_pelanggan():
    try:
        with open('pelanggan.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Fungsi untuk membaca data admin dari file JSON
def load_admins():
    try:
        with open('adminnya.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Fungsi untuk membaca data barang dari CSV
def read_barang():
    items = []
    with open('items.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            items.append(row)
    return items

# Fungsi untuk menyimpan barang ke file CSV
def save_barang(barang_list):
    if barang_list:  # Cek jika daftar tidak kosong
        with open('items.csv', mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=barang_list[0].keys())
            writer.writeheader()
            writer.writerows(barang_list)

def save_pelanggan(pelanggan):
    with open('pelanggan.json', 'w') as f:
        json.dump(pelanggan, f, indent=4)
        
# Fungsi untuk mengurangi saldo pengguna
def reduce_user_balance(user_id, amount):
    pelanggan = load_pelanggan()
    if user_id in pelanggan:
        current_balance = pelanggan[user_id].get('saldo', 0)
        if current_balance >= amount:
            pelanggan[user_id]['saldo'] -= amount
            save_pelanggan(pelanggan)
            notify_admin(f"Saldo pengguna {user_id} dikurangi sebesar {amount}.")
            return True
    return False

# Fungsi untuk menyimpan transaksi
def save_transaction(user_id, item_id, price):
    transaction_data = {
        "user_id": user_id,
        "item_id": item_id,
        "price": price,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    if os.path.exists('transactions.json'):
        with open('transactions.json', 'r') as f:
            transactions = json.load(f)
    else:
        transactions = []
    
    transactions.append(transaction_data)

    with open('transactions.json', 'w') as f:
        json.dump(transactions, f, indent=4)
    
    notify_admin(f"Transaksi: User {user_id} membeli item {item_id} seharga {price}. segera cek saldo rekening/dana lalu konfirmasi akun jualan dengan \n\n /pesan {user_id} informasi_akun")

# Fungsi untuk menambah saldo pengguna (Top-Up)
def top_up_balance(user_id, amount):
    users = load_pelanggan()

    if user_id in users:
        users[user_id]['saldo'] += amount
        with open('pelanggan.json', 'w') as f:
            json.dump(users, f, indent=4)
        return True
    return False

# Fungsi untuk menghasilkan QRIS
def generate_qris(amount):
    qris_data = f"{link_jualan}" #?amount={amountMengatur data untuk QRIS
    qr = qrcode.make(qris_data)
    qr_filename = f"qris_{amount}.png"
    qr.save(qr_filename)
    return qr_filename

@bot.message_handler(commands=['topup'])
def topup_command(message):
    if not is_whitelisted(message.from_user.id):
        bot.reply_to(message, "Hanya admin yang dapat melakukan top-up.")
        return

    try:
        data = message.text.split(" ")
        if len(data) != 3:
            bot.reply_to(message, "Format salah. Gunakan: /topup user_id amount.")
            return
        
        user_id = data[1]
        amount = float(data[2])

        if top_up_balance(user_id, amount):
            bot.reply_to(message, f"Top-up sebesar {amount} berhasil untuk pengguna {user_id}.")
        else:
            bot.reply_to(message, "Pengguna tidak ditemukan!")

    except ValueError:
        bot.reply_to(message, "Jumlah harus berupa angka.")
    except Exception as e:
        bot.reply_to(message, f"Terjadi kesalahan: {str(e)}")
        
# Command '/start' untuk memulai bot
@bot.message_handler(commands=['VPN'])
def start_command(message):
    welcome_message = (
        "Selamat datang di Bot VPN Akun Manajer!\n"
        "Gunakan perintah berikut untuk berinteraksi:\n"
        "/daftar email password - Daftar akun baru\n"
        "/login email password - Masuk ke akun Anda\n"
        "/ssh - Beli ssh\n"
        "/vmess - Beli vmess\n"
        "/vless - Beli vless\n"
        "/trojan - Beli trojan\n"
        "/trial1 - trial ssh\n"
        "/trial2 - trial vmess\n"
        "/harga SSH nilai - ubah info harga (hanya admin)\n"
        "/notifikasi pesan - untuk menyampaikan broadcast (hanya admin)\n"
        "/siaran pesan - pesan siaran ke pengguna tunnel\n"
        "/topup user_id amount - Top-up saldo pengguna (hanya admin)\n"
        "/info - Tampilkan informasi akun\n"
    )
    bot.reply_to(message, welcome_message)

# Fungsi untuk menjalankan perintah tunnel di VPS
def run_tunnel_command(tunnel_id):
    command = f"sudo {tunnel_id}"  # Ganti dengan perintah yang sesuai
    try:
        # Menjalankan perintah dan menangkap output
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        output = result.stdout.strip()  # Hapus whitespace tambahan
        error = result.stderr.strip()    # Hapus whitespace tambahan untuk error
        if output:
            print(f"Perintah dijalankan: {output}")  # Menampilkan output ke console
        if error:
            print(f"Error: {error}")  # Menampilkan error ke console
        return output, error  # Mengembalikan output dan error
    except subprocess.CalledProcessError as e:
        print(f"Error menjalankan perintah: {e.output}, {e.stderr}")  # Tampilkan error
        return None, e.stderr  # Mengembalikan None dan sub error
        

        
# Command for SSH item purchases
@bot.message_handler(commands=['ssh'])
def purchase_ssh(message):
    item_id = "ssh"
    return handle_purchase(message, item_id)

# Command for VMess item purchases
@bot.message_handler(commands=['vmess'])
def purchase_vmess(message):
    item_id = "vmess"
    return handle_purchase(message, item_id)

# Command for VLess item purchases
@bot.message_handler(commands=['vless'])
def purchase_vless(message):
    item_id = "vless"
    return handle_purchase(message, item_id)

# Command for XRay item purchases
@bot.message_handler(commands=['trojan'])
def purchase_xray(message):
    item_id = "trojan"
    return handle_purchase(message, item_id)

def handle_purchase(message, item_id):
    try:
        # Memuat daftar barang dari CSV
        items = read_barang()
        
        # Mencari barang berdasarkan item_id
        item = next((x for x in items if x['item_id'] == item_id), None)

        if not item:
            bot.reply_to(message, f"Barang dengan ID '{item_id}' tidak ditemukan!")
            return
        
        # Mengambil harga dan command barang
        price = float(item['price'])
        command_to_run = item['command']  # Ambil command dari item
        user_id = str(message.chat.id)
        
        # Membuat QRIS link untuk pembayaran
        qris_link = generate_qris_link(price)

        # Mengurangi saldo pengguna
        if not reduce_user_balance(user_id, price):
            bot.reply_to(message, "Saldo Anda tidak cukup untuk melakukan pembelian.")
            return

        # Menyimpan transaksi
        save_transaction(user_id, item['item_id'], price)

        # Menjalankan perintah tunnel dengan command dari item
        tunnel_output, tunnel_error = run_tunnel_command(command_to_run)  # Jalankan command dari item
        if tunnel_output:
            bot.reply_to(message, f"Perintah tunnel berhasil dijalankan: {tunnel_output}")
        if tunnel_error:
            bot.reply_to(message, f"Terdapat kesalahan saat menjalankan perintah: {tunnel_error}")

        # Kirim link QRIS kepada pengguna
        bot.reply_to(message, f"Silakan lakukan pembayaran ke link berikut: {qris_link}")

        # Notifikasi kepada admin bahwa pengguna telah melakukan pemesanan
        notify_admin(f"User ID {user_id} telah melakukan pembelian '{item['konten']}' seharga {price}. Silakan cek saldo rekening Anda.")
        
        # Notifikasi kepada pelanggan untuk menunggu persetujuan
        bot.send_message(user_id, "Mohon bersabar dan menunggu persetujuan dari admin setelah melakukan pembayaran.")

    except Exception as e:
        bot.reply_to(message, f"Terjadi kesalahan: {str(e)}")

# Command '/harga' to change the price of items
@bot.message_handler(commands=['harga'])
def update_price(message):
    try:
        data = message.text.split(" ")
        
        if len(data) != 3:
            bot.reply_to(message, "Format salah. Gunakan: /harga [item_id] [harga_baru]")
            return
        
        item_id = data[1]
        new_price = float(data[2])

        # Load items and update the specified item's price
        items = read_barang()
        item_found = False
        for item in items:
            if item['item_id'] == item_id:
                item['price'] = new_price
                item_found = True
                break
        
        if item_found:
            save_barang(items)
            bot.reply_to(message, f"Harga barang dengan ID '{item_id}' berhasil diupdate menjadi {new_price}.")
        else:
            bot.reply_to(message, f"Barang dengan ID '{item_id}' tidak ditemukan.")
    
    except ValueError:
        bot.reply_to(message, "Harga harus berupa angka.")
    except Exception as e:
        bot.reply_to(message, f"Terjadi kesalahan: {str(e)}")

# Update on other necessary functions: `read_barang`, `reduce_user_balance`, etc.

# Dictionary to store user trial status
user_trials = {}

@bot.message_handler(commands=['trial1'])
def beli_trial1(message):
    try:
        user_id = message.from_user.id

        # Check if user has already used this command
        if user_trials.get(user_id, {}).get('trial1'):
            bot.reply_to(message, "Anda sudah menggunakan trial SSH sekali. Tidak dapat menggunakannya lagi.")
            return
        # Mark this trial as used
        user_trials.setdefault(user_id, {})['trial1'] = True

        # Hand off to handle_purchase for processing
        return handle_purchase(message, 'trial-ssh')

    except Exception as e:
        bot.reply_to(message, f"Terjadi kesalahan: {str(e)}")

@bot.message_handler(commands=['trial2'])
def beli_trial2(message):
    try:
        user_id = message.from_user.id

        # Check if user has already used this command
        if user_trials.get(user_id, {}).get('trial2'):
            bot.reply_to(message, "Anda sudah menggunakan trial V2Ray sekali. Tidak dapat menggunakannya lagi.")
            return

        # Mark this trial as used
        user_trials.setdefault(user_id, {})['trial2'] = True

        # Hand off to handle_purchase for processing
        return handle_purchase(message, 'trial-v2ray')

    except Exception as e:
        bot.reply_to(message, f"Terjadi kesalahan: {str(e)}")



# Command '/info' untuk menampilkan informasi langganan pengguna
@bot.message_handler(commands=['info'])
def info_user(message):
    subscriptions = load_subscriptions()
    user_id = str(message.chat.id)
    pelanggan = load_pelanggan()
    if user_id in pelanggan:
        email = pelanggan[user_id]['email']
        saldo = pelanggan[user_id]['saldo']
        bot.reply_to(message, f"Info Pengguna:\nEmail: {email}\nSaldo: {saldo}")
    else:
        bot.reply_to(message, "Anda belum terdaftar sebagai pengguna.")
        
    for subscription in subscriptions['subscriptions']:
        if subscription['user_id'] == user_id:
            bot.reply_to(message, f"Info Langganan:\n"
                                   f"Email: {subscription['email']}\n"
                                   f"Status: {subscription['status']}\n")
            return
    
    bot.reply_to(message, "Anda belum terdaftar dalam langganan.")

    
# Start polling the bot
def start_bot():
    bot.polling()

if __name__ == "__main__":
    start_bot()