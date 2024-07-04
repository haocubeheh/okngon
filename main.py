import telebot
import subprocess
import sys
from requests import post, Session
import time
import datetime
import random
import string
import os
import io
import zipfile
import json
import requests
import sqlite3
import psutil
import pytz
from io import BytesIO
from datetime import timedelta
from telebot import types
from time import strftime
from keep_alive import keep_alive
admin_diggory = "DevNDHhi" # ví dụ : để user name admin là @diggory347 bỏ dấu @ đi là đc
name_bot = "Ꮶꭺꭱꮖꮪ • 𝘽𝙊𝙏"
zalo = "https://zalo.me/g/daubuoi"
web = "https://beacons.ai/concac"
facebook = "https://t.me/cc"
allowed_group_id = -1002167325764
bot=telebot.TeleBot("6777690636:AAHwlFqsNmMI7KrWHxinN5DMtPvgjnBNFx8") #token botinfogithub
check_ip_api_url = 'https://api.sumiproject.net/checkdomain?domain='  # Thay đổi URL API thật
check_key_api_url = 'https://api.rosieteam.net/bypass/fluxus/?hwid='
API_URL = "https://nguyenmanh.name.vn/api/fbInfo"
API_URL2 = "https://nguyenmanh.name.vn/api/shortlink"
API_KEY = 'KoWyVINz'
API_KEYFB = 'apikeysumi'
WEATHER_API_URL = 'https://nguyenmanh.name.vn/api/thoitiet'
print("Bot đã được khởi động thành công")
users_keys = {}
key = ""
auto_spam_active = False
last_sms_time = {}
allowed_users = []
processes = []
ADMIN_ID =  6253407525 # id admin
connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()
last_command_time = {}


def check_command_cooldown(user_id, command, cooldown):
    current_time = time.time()
    
    if user_id in last_command_time and current_time - last_command_time[user_id].get(command, 0) < cooldown:
        remaining_time = int(cooldown - (current_time - last_command_time[user_id].get(command, 0)))
        return remaining_time
    else:
        last_command_time.setdefault(user_id, {})[command] = current_time
        return None

# Create the users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        expiration_time TEXT
    )
''')
connection.commit()

def TimeStamp():
  now = str(datetime.date.today())
  return now


def load_users_from_database():
  cursor.execute('SELECT user_id, expiration_time FROM users')
  rows = cursor.fetchall()
  for row in rows:
    user_id = row[0]
    expiration_time = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
    if expiration_time > datetime.datetime.now():
      allowed_users.append(user_id)

def check_group(message):
    if message.chat.id != allowed_group_id:
        bot.send_message(message.chat.id, "Vui lòng sử dụng bot trong group @karispowerchat")
        return False
    return True

def save_user_to_database(connection, user_id, expiration_time):
  cursor = connection.cursor()
  cursor.execute(
    '''
        INSERT OR REPLACE INTO users (user_id, expiration_time)
        VALUES (?, ?)
    ''', (user_id, expiration_time.strftime('%Y-%m-%d %H:%M:%S')))
  connection.commit()

start_time = time.time()

def get_elapsed_time():
    elapsed_time = time.time() - start_time
    return str(timedelta(seconds=int(elapsed_time)))

def get_banner_image(elapsed_time):
    random_number = random.randint(1, 45)
    url = f"https://nguyenmanh.name.vn/api/avtWibu6?id={random_number}&tenchinh=TIME%20BOT&tenphu={elapsed_time}&mxh=Nguyen%20Hao%20YT&apikey=QEXSJd62"
    response = requests.get(url)
    return BytesIO(response.content)

def get_weather(location: str) -> dict:
    params = {
        'type': 'text',
        'query': location,
        'apikey': API_KEY
    }
    response = requests.get(WEATHER_API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"status": response.status_code, "result": None}

help_message = """
╭─────「𝕄𝔼ℕ𝕌」──────۰۪۪۫۫●۪۫۰
│◈/help: menu bot
│◈/admin: info admin
│◈/start: start bot
│◈/bot: info server bot
│◈/resetstart: reset bot
│◈/off: off bot
├───《Social network 》───⭔
│◈/spamngl: spam link NGL FB
│◈/uid: get id posts và uid
│◈/fb: info Facebook
│◈/tiktokuser: get info tiktok
│◈/weather: thời tiết 7day sau
│◈/short: short url
│◈/fbdow: download video
│◈/yt: download Youtube 
│◈/github: info github
│◈/capcut: download video
│◈/check: in website
│◈/cap: lấy ảnh website
│◈/fluxs: lấy key fluxs
│◈/code: lấy index.html
│◈/tiktok: download video
│◈/view: buff view vd tiktok
│◈/time: check time bot
├─────《ATTACK》─────⭔
│◈/svip: spam sms free
│◈/attack: dos website
╰─────────────⭓
"""

# URL của ảnh GIF
gif_url = 'https://files.catbox.moe/ijb25a.gif'

def get_dependency_count():
    try:
        with open('package.json', 'r') as file:
            package_json = json.load(file)
            return len(package_json.get('dependencies', {}))
    except Exception as error:
        print(f'❎ Cannot read package.json file: {error}')
        return -1

def get_status_by_ping(ping):
    if ping < 200:
        return 'smooth'
    elif ping < 800:
        return 'average'
    else:
        return 'lag'

def convert_to_gb(bytes):
    return f'{bytes / (1024 ** 3):.2f}GB' if bytes else 'N/A'

def get_facebook_info(uid):
    url = f"https://api.sumiproject.net/facebook/getinfo?uid={uid}&apikey=apikeysumi"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_tiktok_user_info(username):
    url = f'https://api.sumiproject.net/tiktok?info={username}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def send_ngl_spam(username, message, amount):
    url = f'https://api.sumiproject.net/ngl?username={username}&message={message}&amount={amount}'
    response = requests.get(url)
    return response.status_code == 200

def get_youtube_video_info(url):
    api_url = f'https://api-locdev.vercel.app/api/ytmp4?url={url}'
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    return None

def get_gpt_response(question):
    url = f'https://api.sumiproject.net/gpt4?q={question}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_facebook_uid(link):
    url = f'https://sumiproject.io.vn/facebook/uid?link={link}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Lệnh /uid
@bot.message_handler(commands=['uid'])
def get_uid(message):
 if check_group(message):
    try:
        # Tách và kiểm tra dữ liệu đầu vào
        parts = message.text.split(' ', 1)
        if len(parts) != 2:
            bot.reply_to(message, "Sai cú pháp. Vui lòng sử dụng: /uid (link bài viết hoặc link Facebook người dùng)")
            return

        link = parts[1].strip()
        data = get_facebook_uid(link)

        if data and data['success'] == 200:
            uid = data['id']
            bot.reply_to(message, f"UID của liên kết là: {uid}")
        else:
            bot.reply_to(message, "Không thể lấy UID hoặc có lỗi xảy ra.")
    except IndexError:
        bot.reply_to(message, "Vui lòng nhập link bài viết hoặc link Facebook người dùng. Ví dụ: /uid https://www.facebook.com/zuck")
    except Exception as e:
        bot.reply_to(message, f"Đã xảy ra lỗi: {e}")

# Lệnh /gpt
@bot.message_handler(commands=['gpt'])
def chat_gpt(message):
 if check_group(message):
    try:
        # Tách và kiểm tra dữ liệu đầu vào
        parts = message.text.split(' ', 1)
        if len(parts) != 2:
            bot.reply_to(message, "Sai cú pháp. Vui lòng sử dụng: /gpt (câu hỏi cho ChatGPT)")
            return

        question = parts[1].strip()
        data = get_gpt_response(question)

        if data and 'data' in data:
            response_message = data['data']
            bot.reply_to(message, response_message)
        else:
            bot.reply_to(message, "Không thể lấy phản hồi từ ChatGPT hoặc có lỗi xảy ra.")
    except IndexError:
        bot.reply_to(message, "Vui lòng nhập câu hỏi cho ChatGPT. Ví dụ: /gpt What is the weather today?")
    except Exception as e:
        bot.reply_to(message, f"Đã xảy ra lỗi: {e}")

# Lệnh /yt
@bot.message_handler(commands=['yt'])
def download_youtube_video(message):
 if check_group(message):
    try:
        # Tách và kiểm tra dữ liệu đầu vào
        parts = message.text.split()
        if len(parts) != 2:
            bot.reply_to(message, "Sai cú pháp. Vui lòng sử dụng: /yt (link video Youtube)")
            return

        youtube_url = parts[1].strip()
        data = get_youtube_video_info(youtube_url)
        
        if data and data['status'] == 200:
            video_info = data['result']

            # Tạo thông điệp trả về
            response_message = f"""
Download video successfully
Request by: @{message.from_user.username}
---------------------------------------
Channel: {video_info['channel']}
View: {video_info['views']}
Date Submitted: {video_info['published']}
"""
            video_url = video_info['url']

            # Gửi tin nhắn kèm video
            bot.send_video(message.chat.id, video_url, caption=response_message)
        else:
            bot.reply_to(message, "Không thể tải thông tin video hoặc có lỗi xảy ra.")
    except IndexError:
        bot.reply_to(message, "Vui lòng nhập link video Youtube. Ví dụ: /yt https://www.youtube.com/watch?v=???")
    except Exception as e:
        bot.reply_to(message, f"Đã xảy ra lỗi: {e}")

# Lệnh /spamngl
@bot.message_handler(commands=['spamngl'])
def spam_ngl(message):
 if check_group(message):
    try:
        # Tách và kiểm tra dữ liệu đầu vào
        parts = message.text.split('|')
        if len(parts) != 4:
            bot.reply_to(message, "Sai cú pháp. Vui lòng sử dụng: /spamngl | (user ngl) | (message) | (số lần spam không được quá 30)")
            return
        
        user_ngl = parts[1].strip()
        user_message = parts[2].strip()
        spam_amount = int(parts[3].strip())

        if spam_amount > 30:
            bot.reply_to(message, "Số lần spam không được quá 30.")
            return
        
        # Gửi dữ liệu đến API
        if send_ngl_spam(user_ngl, user_message, spam_amount):
            confirmation_message = f"""
Start spamming NGL
Người dùng: @{message.from_user.username}
Tin nhắn: {user_message}
Số lần spam: {spam_amount}
"""
            gif_url = 'https://files.catbox.moe/yhmbg3.gif'
            bot.send_animation(message.chat.id, gif_url, caption=confirmation_message)
        else:
            bot.reply_to(message, "Gửi dữ liệu đến API thất bại. Vui lòng thử lại sau.")
    except ValueError:
        bot.reply_to(message, "Số lần spam phải là một số nguyên.")
    except Exception as e:
        bot.reply_to(message, f"Đã xảy ra lỗi: {e}")

# Lệnh /tiktokuser
@bot.message_handler(commands=['tiktokuser'])
def send_tiktok_user_info(message):
 if check_group(message):
    try:
        username = message.text.split()[1]
        data = get_tiktok_user_info(username)
        
        if data and data['code'] == 0:
            user_info = data['data']['user']
            stats = data['data']['stats']

            # Tạo thông điệp trả về
            response_message = f"""
[📡]➜User ID: {user_info['id']}
[💤]➜Username: {user_info['uniqueId']}
[🏷️]➜Nickname: {user_info['nickname']}
[✅]➜Verified: {user_info['verified']}
[👀]➜Following: {stats['followingCount']}
[👁️‍🗨️]➜Follower: {stats['followerCount']}
[♥️]➜Tim: {stats['heartCount']}
[🎥]➜Video: {stats['videoCount']}
"""

            avatar_url = user_info['avatarLarger']

            # Gửi tin nhắn kèm ảnh đại diện
            bot.send_photo(message.chat.id, avatar_url, caption=response_message)
        else:
            bot.reply_to(message, "Không tìm thấy thông tin người dùng hoặc có lỗi xảy ra.")
    except IndexError:
        bot.reply_to(message, "Vui lòng nhập username của TikTok. Ví dụ: /tiktokuser nguyen.hao20")
    except Exception as e:
        bot.reply_to(message, f"Đã xảy ra lỗi: {e}")

@bot.message_handler(commands=['fb'])
def handle_fb_command(message):
 if check_group(message):
    try:
        uid = message.text.split()[1]
        info = get_facebook_info(uid)
        if info:
            response_message = (
                f"‏‏\n┌───〘 𝕚𝕟𝕗𝕠 • 🅨🅞🅤 〙───۰۪۪۫۫●۪۫۰\n├➣𝙽𝚊𝚖𝚎: {info.get('name', 'N/A')}\n"
                f"├➣𝙻𝚒𝚗𝚔: {info.get('link_profile', 'N/A')}\n"
                f"├➣𝚄𝙸𝙳: {info.get('uid', 'N/A')}\n"
                f"├➣𝚞𝚜𝚎𝚛𝚗𝚊𝚖𝚎: {info.get('username', 'N/A')}\n"
                f"├➣𝙲𝚛𝚎𝚊𝚝𝚎𝚍-𝚃𝚒𝚖𝚎: {info.get('created_time', 'N/A')}\n"
                f"├➣𝚆𝚎𝚋𝚜𝚒𝚝𝚎: {info.get('web', 'N/A')}\n"
                f"├➣𝙶𝚎𝚗𝚍𝚎𝚛: {info.get('gender', 'N/A')}\n"
                f"├➣𝚁𝚎𝚕𝚊𝚝𝚒𝚘𝚗𝚜𝚑𝚒𝚙-𝚂𝚝𝚊𝚝𝚞𝚜: {info.get('relationship_status', 'N/A')}\n"
                f"├➣𝙻𝚘𝚟𝚎: {info.get('love', {}).get('name', 'N/A') if isinstance(info.get('love'), dict) else 'N/A'}\n"
                f"├➣𝙱𝚒𝚛𝚝𝚑𝚍𝚊𝚢: {info.get('birthday', 'N/A')}\n"
                f"├➣𝙵𝚘𝚕𝚕𝚘𝚠𝚎𝚛𝚜: {info.get('follower', 'N/A')}\n"
                f"├➣𝚅𝚎𝚛𝚒𝚏𝚒𝚎𝚍: {'Yes' if info.get('tichxanh') else 'No'}\n"
                f"├➣𝙰𝚋𝚘𝚞𝚝: {info.get('about', 'N/A')}\n"
                f"├➣𝙻𝚘𝚌𝚊𝚕𝚎: {info.get('locale', 'N/A')}\n"
                f"├➣𝙻𝚘𝚌𝚊𝚝𝚒𝚘𝚗: {info.get('location', 'N/A')}\n"
                f"├➣𝙷𝚘𝚖𝚎𝚝𝚘𝚠𝚗: {info.get('hometown', 'N/A')}\n"
                f"├➣𝚀𝚞𝚘𝚝𝚎𝚜: {info.get('quotes', 'N/A')}\n"
            )

            work_info = info.get('work', [])
            if work_info:
                response_message += "└────《 𝙬𝙤𝙧𝙠 》──────✆\n"
                for work in work_info:
                    response_message += (
                        f"   |\n   |➽𝙴𝚖𝚙𝚕𝚘𝚢𝚎𝚛: {work.get('employer', {}).get('name', 'N/A')}\n"
                        f"   |➽𝙿𝚘𝚜𝚒𝚝𝚒𝚘𝚗: {work.get('position', {}).get('name', 'N/A')}\n"
                        f"   |➽𝚂𝚝𝚊𝚛𝚝-𝙳𝚊𝚝𝚎: {work.get('start_date', 'N/A')}\n"
                        f"   |➽𝙳𝚎𝚜𝚌𝚛𝚒𝚙𝚝𝚒𝚘𝚗: {work.get('description', 'N/A')}\n"
                        f"   |➽𝙱𝚒𝚘: {work.get('description', 'N/A')}\n  └─────────────────☻\n"
                    )
            avatar_url = info.get('avatar', None)
            if avatar_url:
                avatar_response = requests.get(avatar_url)
                if avatar_response.status_code == 200:
                    avatar_image = BytesIO(avatar_response.content)
                    bot.send_photo(message.chat.id, avatar_image, caption=response_message)
                else:
                    bot.reply_to(message, "Không thể tải ảnh đại diện.")
            else:
                bot.reply_to(message, response_message)
        else:
            bot.reply_to(message, "Không tìm thấy thông tin hoặc lỗi API.")
    except IndexError:
        bot.reply_to(message, "Vui lòng nhập UID của người dùng Facebook. Ví dụ: /fb 1234567890")
    except Exception as e:
        bot.reply_to(message, f"Đã xảy ra lỗi: {e}")

@bot.message_handler(commands=['bot'])
def handle_bot_command(message):
 if check_group(message):
    start_ping = time.time()

    total_memory = psutil.virtual_memory().total
    free_memory = psutil.virtual_memory().available
    used_memory = psutil.Process(os.getpid()).memory_info().rss

    name = message.from_user.full_name
    dependency_count = get_dependency_count()
    bot_status = get_status_by_ping((time.time() - start_ping) * 1000)

    try:
        # Get disk usage for a specific partition
        partitions = psutil.disk_partitions()
        usage = psutil.disk_usage(partitions[0].mountpoint)  # Get usage for the first partition
        disk_usage = f"{partitions[0].device} - {convert_to_gb(usage.total)} Total, {convert_to_gb(usage.free)} Free"

        ping_real = (time.time() - start_ping) * 1000

        reply_msg = (
            "♨️ Bot status: {}\n"
            "🛢️ Free RAM: {}\n"
            "🔍 Used RAM: {:.2f}MB\n"
            "💾 Disk Usage:\n{}\n"
            "📊 Total packages: {}\n"
            "🛜 Ping: {:.0f}ms\n"
            "👤 Requested by: {}"
        ).format(
            bot_status,
            convert_to_gb(free_memory),
            used_memory / (1024 ** 2),
            disk_usage,
            dependency_count if dependency_count >= 0 else 'Unknown',
            ping_real,
            name
        )

        bot.reply_to(message, reply_msg)
    except Exception as error:
        print(f'❎ Error getting bot information: {error}')
        bot.reply_to(message, '❎ Error getting bot information.')

# Lệnh /help
@bot.message_handler(commands=['help'])
def send_help(message):
 if check_group(message):
    chat_id = message.chat.id
    bot.send_animation(chat_id, gif_url, caption=help_message)

@bot.message_handler(commands=['weather'])
def send_weather(message):
 if check_group(message):
    location = message.text[len('/weather '):].strip()
    if not location:
        bot.reply_to(message, 'Please provide a location. Usage: /weather <location>')
        return

    weather_data = get_weather(location)
    if weather_data['status'] == 200:
        result = weather_data['result']['result']
        image_url = weather_data['result']['image']

        # Download the image
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            image_path = 'weather_image.bin'
            with open(image_path, 'wb') as image_file:
                image_file.write(image_response.content)
            
            # Send the image first
            with open(image_path, 'rb') as image_file:
                bot.send_photo(message.chat.id, image_file, caption="Weather 7 ngày tiếp theo")
            
            # Remove the image file after sending
            os.remove(image_path)
        else:
            bot.reply_to(message, 'Could not retrieve weather image.')
            return
        
        # Send the weather result message
        bot.send_message(message.chat.id, result)
    else:
        bot.reply_to(message, f'Could not retrieve weather data for {location}. Please try again.')

@bot.message_handler(commands=['time'])
def send_time(message):
 if check_group(message):
    elapsed_time = get_elapsed_time()
    banner_image = get_banner_image(elapsed_time)
    
    bot.send_photo(
        message.chat.id,
        banner_image,
        caption=f"[❄️]======>TIME<======[❄️]\nBot đã hoạt động được\n[{elapsed_time}]"
    )

@bot.message_handler(commands=['add', 'adduser'])
def add_user(message):
 if check_group(message):
   
  admin_id = message.from_user.id
  if admin_id != ADMIN_ID:
    bot.reply_to(message, 'BẠN KHÔNG CÓ QUYỀN SỬ DỤNG LỆNH NÀY')
    return

  if len(message.text.split()) == 1:
    bot.reply_to(message, 'VUI LÒNG NHẬP ID NGƯỜI DÙNG')
    return

  user_id = int(message.text.split()[1])
  allowed_users.append(user_id)
  expiration_time = datetime.datetime.now() + datetime.timedelta(days=30)
  connection = sqlite3.connect('user_data.db')
  save_user_to_database(connection, user_id, expiration_time)
  connection.close()

  bot.reply_to(
    message,
    f'NGƯỜI DÙNG CÓ ID {user_id} ĐÃ ĐƯỢC THÊM VÀO DANH SÁCH ĐƯỢC PHÉP SỬ DỤNG LỆNH /spamvipspamvip'
  )


load_users_from_database()






def is_key_approved(chat_id, key):
    if chat_id in users_keys:
        user_key, timestamp = users_keys[chat_id]
        if user_key == key:
            current_time = datetime.datetime.now()
            if current_time - timestamp <= datetime.timedelta(hours=2):
                return True
            else:
                del users_keys[chat_id]
    return False

@bot.message_handler(commands=['svip'])
def lqm_sms(message):
 if check_group(message):
    user_id = message.from_user.id
    if len(message.text.split()) == 1:
        bot.reply_to(message, '/svip (sđt)')
        return

    phone_number = message.text.split()[1]
    if not phone_number.isnumeric():
        bot.reply_to(message, 'hãy nhập đúng')
        return

    if phone_number in ['113','911','114','115','+84346452531','0949404151','0355366216']:
        # Số điện thoại nằm trong danh sách cấm
        bot.reply_to(message,"Không Được Spam Số Này💢")
        return

    file_path = os.path.join(os.getcwd(), "sms1.py")
    file_path2 = os.path.join(os.getcwd(), "sms2.py")
    file_path3 = os.path.join(os.getcwd(), "sms4.py")
    file_path4 = os.path.join(os.getcwd(), "sms3.py")
    file_path5 = os.path.join(os.getcwd(), "sms5.py")
    process = subprocess.Popen(["python", file_path, phone_number, "300"])    
    process = subprocess.Popen(["python", file_path2, phone_number, "200"])
    process = subprocess.Popen(["python", file_path3, phone_number, "300"])
    process = subprocess.Popen(["python", file_path4, phone_number, "300"])
    process = subprocess.Popen(["python", file_path5, phone_number, "300"])
    processes.append(process)
    bot.reply_to(message, f'┏━━━━━━━━━━━━━━━━┓\n┣➤ 🚀 Gửi Yêu Cầu Tấn Công Thành Công 🚀 \n┣➤ Created By Nguyen Hao\n┣➤ Số Tấn Công 📱:[ {phone_number} ]\nThời gian 🕐: 100s ✅\nBạn Đang Sử Dụng Spamvip\nhttps://files.catbox.moe/36gpm3.mp4')

is_bot_active = True


@bot.message_handler(commands=['view'])
def lqm_sms(message):
 if check_group(message):
    user_id = message.from_user.id
    if len(message.text.split()) == 1:
        bot.reply_to(message, '/view (link video tiktok)')
        return

    if phone_number in ['113','911','114','115','+84346452531','0949404151','0355366216']:
        # Số điện thoại nằm trong danh sách cấm
        bot.reply_to(message,"...?")
        return

    file_path = os.path.join(os.getcwd(), "view.py")
    file_path2 = os.path.join(os.getcwd(), "view.py")
    file_path3 = os.path.join(os.getcwd(), "view.py")
    file_path4 = os.path.join(os.getcwd(), "view.py")
    file_path5 = os.path.join(os.getcwd(), "view.py")
    process = subprocess.Popen(["python", file_path, phone_number, "100"])    
    process = subprocess.Popen(["python", file_path2, phone_number, "100"])
    process = subprocess.Popen(["python", file_path3, phone_number, "100"])
    process = subprocess.Popen(["python", file_path4, phone_number, "100"])
    process = subprocess.Popen(["python", file_path5, phone_number, "100"])
    processes.append(process)
    bot.reply_to(message, f'┏━━━━━━━━━━━━━━━━┓\n┣➤ 🚀 Gửi Yêu Cầu Buff View Ok 〽️\n┣➤ View Mặc Định 500\n┣➤ Video 🎥:[ {phone_number} ]\nView👀: 500✅\nBạn Đang Sử Dụng Spamvip\nhttps://files.catbox.moe/36gpm3.mp4')

is_bot_active = True

@bot.message_handler(commands=['code'])
def code(message):
 if check_group(message):
    user_id = message.from_user.id
    if len(message.text.split()) != 2:
        bot.reply_to(message, 'Vui lòng nhập đúng cú pháp.\nVí dụ: /code + [link website]')
        return

    url = message.text.split()[1]

    try:
        response = requests.get(url)
        if response.status_code != 200:
            bot.reply_to(message, 'Không thể lấy mã nguồn từ trang web này. Vui lòng kiểm tra lại URL.')
            return

        content_type = response.headers.get('content-type', '').split(';')[0]
        if content_type not in ['text/html', 'application/x-php', 'text/plain']:
            bot.reply_to(message, 'Trang web không phải là HTML hoặc PHP. Vui lòng thử với URL trang web chứa file HTML hoặc PHP.')
            return

        source_code = response.text

        zip_file = io.BytesIO()
        with zipfile.ZipFile(zip_file, 'w') as zipf:
            zipf.writestr("source_code.txt", source_code)

        zip_file.seek(0)
        bot.send_chat_action(message.chat.id, 'upload_document')
        bot.send_document(message.chat.id, zip_file)

    except Exception as e:
        bot.reply_to(message, f'Có lỗi xảy ra: {str(e)}')

@bot.message_handler(commands=['admin'])
def diggory(message):
 if check_group(message):
     
    username = message.from_user.username
    diggory_chat = f'''
===🌸ADMIN🌸===
━━━━━━━━━━━━━━━━━━
[🙈] 𝐓𝐞̂𝐧: Nguyễn Đình Hạo
[💮] 𝐁𝐢𝐞̣̂𝐭 𝐃𝐚𝐧𝐡: Karis
[🛸] 𝐓𝐮𝐨̂̉𝐢: 14+
[👤] 𝐆𝐢𝐨̛́𝐢 𝐓𝐢́𝐧𝐡: Nam
[💘] 𝐌𝐨̂́𝐢 𝐐𝐮𝐚𝐧 𝐇𝐞̣̂: Docthan
[🌎] 𝐐𝐮𝐞̂ 𝐐𝐮𝐚́𝐧: Lạng Sơn
[👫] 𝐆𝐮: Biết nấu cớm:))
[🌸] 𝐓𝐢́𝐧𝐡 𝐂𝐚́𝐜𝐡: Hót boi,Cool ngầu,Lạnh Lùng,Máu Lạnh😏
[🌀] 𝐒𝐨̛̉ 𝐓𝐡𝐢́𝐜𝐡: Ngịch 🐦
━━━━━━━━━━━━━━━━━━
💻𝐂𝐨𝐧𝐭𝐚𝐜𝐭💻
☎ 𝐙𝐚𝐥𝐨: 0969549113
🌐 𝐅𝐛: https://www.facebook.com/haodz.duma.210
✉️ 𝐄𝐦𝐚𝐢𝐥: nguyenhaodb210@hotmail.com
------Bot UwU 🚬------
🛸𝐃𝐨𝐧𝐚𝐭𝐞:
💳momo: chưa update
    '''
    bot.send_message(message.chat.id, diggory_chat)

@bot.message_handler(commands=['restart'])
def restart(message):
 if check_group(message):
     
    if str(message.from_user.username) != admin_diggory:
        bot.reply_to(message, '🚀 Bạn không có quyền sử dụng lệnh này. 🚀')
        return

    bot.reply_to(message, '🚀 Bot sẽ được khởi động lại trong giây lát... 🚀')
    time.sleep(10)
    python = sys.executable
    os.execl(python, python, *sys.argv)

@bot.message_handler(commands=['off'])
def stop(message):
 if check_group(message):
     
    if str(message.from_user.username) != admin_diggory:
        bot.reply_to(message, '🚀 Bạn không có quyền sử dụng lệnh này. 🚀')
        return

    bot.reply_to(message, '🚀 Bot sẽ dừng lại trong giây lát... 🚀')
    time.sleep(1)
    bot.stop_polling()

@bot.message_handler(commands=['attack'])
def supersms(message):
 if check_group(message):
    user_id = message.from_user.id
    if len(message.text.split()) == 1:
        bot.send_message(chat_id=message.chat.id, text="/attack url")
        return

    phone_number = message.text.split()[1]

    username = message.from_user.username
    diggory_chat4 = f'''
┌───⭓ {name_bot}
│» Thông Báo Tới : @{username}
│» Port: 443
│» Thead:350
│» Time : [120]
│» Methods : Thập Cẩm
│» Website:{phone_number}
└─────────────∅
    '''
    bot.send_message(message.chat.id, diggory_chat4)
    file_path = os.path.join(os.getcwd(), "HYBRID.py")
    process = subprocess.Popen(["python", file_path, phone_number, "550", "GET"])
    file_path2 = os.path.join(os.getcwd(), "MURD_OPT.py")
    process = subprocess.Popen(["python", file_path2, phone_number, "550", "GET"])
    processes.append(process)


@bot.message_handler(commands=['cap'])
def capture_website(message):
    try:
        # Lấy link website từ tin nhắn của người dùng
        link = message.text.split()[1]
        api_url = f'https://image.thum.io/get/width/1920/crop/400/fullpage/noanimate/{link}'
        
        # Gửi yêu cầu tới API để lấy ảnh chụp màn hình
        response = requests.get(api_url, stream=True)
        
        if response.status_code == 200:
            # Lưu ảnh vào file tạm thời
            with open('screenshot.png', 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            
            # Gửi ảnh chụp màn hình tới người dùng
            with open('screenshot.png', 'rb') as file:
                bot.send_photo(message.chat.id, file, caption='Success')
        else:
            bot.reply_to(message, 'Không thể chụp ảnh website. Vui lòng kiểm tra lại đường dẫn.')
    
    except IndexError:
        bot.reply_to(message, 'Vui lòng cung cấp link website. Ví dụ: /cap https://www.example.com')
    except Exception as e:
        bot.reply_to(message, f'Đã xảy ra lỗi: {str(e)}')

@bot.message_handler(commands=['tiktok']) 
def download_tiktok(message): 
 if check_group(message):
    if len(message.text.split()) < 2: 
        bot.reply_to(message, "Vui lòng thêm url video tiktok.") 
        return 
 
    url = message.text.split()[1] 
    api_url = f"https://api.sumiproject.net/tiktok?video={url}" 
 
    try: 
        response = requests.get(api_url) 
        if response.status_code == 200: 
            data = response.json() 
            if 'data' in data and 'play' in data['data']: 
                video_play = data['data']['play'] 
                video = requests.get(video_play) 
                if video.status_code == 200: 
                    with open("video.mp4", 'wb') as file: 
                        file.write(video.content)
                    caption = "┌───⭓ DOWNLOAD TIKTOK\n│» Status : Success🌩️\n│» để sử dụng các lệnh khác\n│» sử dụng /help\n└───────────⧕" 
                    video_file = open('video.mp4', 'rb')  # Open the video file 
                    bot.send_video(message.chat.id, video_file, caption=caption)
                    video_file.close()
                else: 
                    bot.reply_to(message, "Không thể lấy ảnh từ API.") 
            else: 
                bot.reply_to(message, "Dữ liệu trả về từ API không hợp lệ.") 
        else: 
            bot.reply_to(message, "Không thể kết nối đến API.") 
    except Exception as e: 
        bot.reply_to(message, "Đã xảy ra lỗi khi xử lý yêu cầu.") 

@bot.message_handler(commands=['check']) 
def check_ip_info(message): 
 if check_group(message):
    command_parts = message.text.split(' ') 
    if len(command_parts) < 2: 
        bot.send_message(message.chat.id, "vui lòng thêm website bạn muốn check") 
        return 
 
    ip_address = command_parts[1]  # Extract the IP address from the command 
    api_response = requests.get(check_ip_api_url + ip_address)  # Send a GET request to the API 
 
    if api_response.status_code == 200: 
        response_data = api_response.json() 
        if response_data.get('status') == 'success': 
            country = response_data.get('country') 
            city = response_data.get('city') 
            isp = response_data.get('isp') 
            org = response_data.get('org') 
            query = response_data.get('query') 
            reverse = response_data.get('reverse') 
            hosting = response_data.get('hosting') 
            message_text = f"IP Address: {ip_address}\nCountry: {country}\nCity: {city}\nISP: {isp}\nOrganization: {org}\nquery: {query}\nhosting: {hosting}\nreverse: {reverse}" 
            bot.send_message(message.chat.id, message_text) 
        else: 
            bot.send_message(message.chat.id, "vui lòng bỏ https:// ra để bắt đầu lấy info") 
    else: 
        bot.send_message(message.chat.id, "Failed to get IP information from the API") 
 

@bot.message_handler(commands=['fluxs']) 
def get_fluxs(message): 
 if check_group(message):
    command_parts = message.text.split(' ') 
    if len(command_parts) < 2: 
        bot.send_message(message.chat.id, "thêm id getkey fluxs") 
        return 
 
    devuot = command_parts[1]  # Extract the IP address from the command 
    api_response = requests.get(check_key_api_url + devuot)  # Send a GET request to the API 
 
    if api_response.status_code == 200: 
        response_data = api_response.json() 
        if response_data.get('Status') == 'success': 
            key = response_data.get('key') 
            message_text = f"┌───⭓ GET KEY FLUXS🍀\n│» Status : Success🌩️\n│» Key:`{key}`\n│» Giờ Bạn Có Thể Chơi GAME\n└───────────⧕" 
            bot.send_message(message.chat.id, message_text)
            bot.delete_message(message.chat.id, message.message_id) 
        else: 
            bot.send_message(message.chat.id, "lỗi") 
    else: 
        bot.send_message(message.chat.id, "Failed to get IP information from the API")

@bot.message_handler(commands=['github']) 
def handle_infogithub(message): 
 if check_group(message):
    try: 
        username = message.text.split()[1]  # Lấy username từ lệnh infogithub 
        api_url = f"https://api.sumiproject.net/github/info?username={username}" 
        response = requests.get(api_url) 
        data = response.json() 
 
        if response.status_code == 200: 
            info_text = "┌─────⭓ INFO GITHUB\n│» user: {}\n".format(username) 
            info_text += "│» ID: {}\n".format(data.get('id', 'Không có'))
            info_text += "│» Tên: {}\n".format(data.get('name', 'Không có')) 
            info_text += "│» Bio: {}\n".format(data.get('bio', 'Không có'))
            info_text += "│» Số repositories: {}\n".format(data.get('public_repos', 0)) 
            info_text += "│» Số người theo dõi: {}\n".format(data.get('followers', 0)) 
            info_text += "│» Số người đang theo dõi: {}\n".format(data.get('following', 0)) 
            info_text += "│» Ngày tạo: {}\n".format(data.get('ngay_tao', 'Không có')) 
            info_text += "│» Giờ Tạo: {}\n".format(data.get('gio_tao', 'Không có'))
            info_text += "│» location: {}\n".format(data.get('location', 'Không rõ'))
            info_text += "│» Link: {}\n".format(data.get('html_url', 'Không có'))
            info_text += "│» Avatar: {}\n".format(data.get('avatar_url', 'Không có'))
 
            bot.reply_to(message, info_text) 
        else: 
            bot.reply_to(message, "Không thể lấy thông tin Github của người dùng. Vui lòng thử lại sau.") 
 
    except IndexError: 
        bot.reply_to(message, "Vui lòng cung cấp username sau lệnh infogithub.") 

@bot.message_handler(commands=['capcut']) 
def handle_capcut(message): 
 if check_group(message):
    try: 
        url = message.text.split()[1]  # Lấy URL từ lệnh capcut 
        api_url = f"https://api.sumiproject.net/capcutdowload?url={url}" 
        response = requests.get(api_url) 
 
        if response.status_code == 200: 
            data = response.json() 
            title = data.get("title", "N/A") 
            description = data.get("description", "N/A") 
            usage = data.get("usage", "N/A") 
            video_url = data.get("video") 
 
            if video_url: 
                bot.send_message(message.chat.id, f"Mô Tả: {title}\nDescription: {description}\nLượt dùng: {usage}") 
                bot.send_video(message.chat.id, video_url) 
            else: 
                bot.reply_to(message, "Không tìm thấy URL video trong dữ liệu API.") 
        else: 
            bot.reply_to(message, "Không thể kết nối đến API. Vui lòng thử lại sau.") 
 
    except IndexError: 
        bot.reply_to(message, "Vui lòng cung cấp URL sau lệnh capcut.") 

@bot.message_handler(commands=['fbdow'])  
def handle_fbdow(message):  
 if check_group(message):
    try:  
        url = message.text.split()[1]  # Lấy URL từ lệnh fbdow  
        api_url = f"https://api.sumiproject.net/facebook/video?url={url}"  
        response = requests.get(api_url)  
  
        if response.status_code == 200:  
            data = response.json()  
            video_url = data.get("sd")  
            thumbnail_url = data.get("thumbnail")  
  
            if video_url:  
                bot.send_video(message.chat.id, video_url, caption="Video từ link Facebook")  
                bot.send_photo(message.chat.id, thumbnail_url, caption="Ảnh Bìa Video")  
  
            else:  
                bot.reply_to(message, "Không tìm thấy URL video trong dữ liệu API.")  
        else:  
            bot.reply_to(message, "Không thể kết nối đến API. Vui lòng thử lại sau.")  
  
    except IndexError:  
        bot.reply_to(message, "Vui lòng cung cấp URL sau lệnh fbdow.")

@bot.message_handler(commands=['short']) 
def handle_infogithub(message): 
 if check_group(message):
    try: 
        username = message.text.split()[1]  # Lấy username từ lệnh infogithub 
        api_url = f"https://nguyenmanh.name.vn/api/shortlink?url={username}&apikey=KoWyVINz" 
        response = requests.get(api_url) 
        data = response.json() 
 
        if response.status_code == 200: 
            info_text = "┌─────⭓ SHORT URL\n".format(username) 
            info_text += "│» LINK: {}".format(data.get('result', 'Không có'))
 
            bot.reply_to(message, info_text) 
        else: 
            bot.reply_to(message, "error") 
 
    except IndexError: 
        bot.reply_to(message, "Vui lòng cung cấp website bạn muốn rút gọn")

@bot.message_handler(commands=['pinter'])
def get_pinterest_images(message):
 if check_group(message):
    try:
        # Tách tên tìm kiếm và số lượng ảnh từ thông báo người dùng
        parts = message.text.split()
        if len(parts) != 3:
            bot.reply_to(message, "Usage: /pinter <search_term> <number_of_images>")
            return
        
        search_term = parts[1]
        try:
            number_of_images = int(parts[2])
        except ValueError:
            bot.reply_to(message, "Please provide a valid number for the number of images.")
            return

        # URL API để tìm kiếm ảnh trên Pinterest, thay API_URL bằng URL của bạn
        api_url = f'https://api.sumiproject.net/pinterest?search={search_term}'

        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            print(data)  # Debug: In ra dữ liệu phản hồi để kiểm tra

            image_urls = data.get('data', [])[:number_of_images]  # Sử dụng .get() để tránh KeyError
            if image_urls:
                media_group = [InputMediaPhoto(media=url) for url in image_urls]  # Đảm bảo sử dụng đúng tham số 'media'
                bot.send_media_group(message.chat.id, media_group)
                bot.send_message(message.chat.id, f"Successfully sent {len(image_urls)} images for '{search_term}'.")
            else:
                bot.reply_to(message, "No images found.")
        else:
            bot.reply_to(message, f"Could not fetch images. Status code: {response.status_code}")
    
    except IndexError:
        bot.reply_to(message, "Usage: /pinter <search_term> <number_of_images>")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")
keep_alive()
bot.polling()
