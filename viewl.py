import os
import subprocess
import telebot
import time

API_TOKEN = '6777690636:AAHwlFqsNmMI7KrWHxinN5DMtPvgjnBNFx8'
bot = telebot.TeleBot(API_TOKEN)

user_last_used = {}

@bot.message_handler(commands=['view'])
def send_welcome(message):
    user_id = message.from_user.id
    current_time = time.time()
    
    if user_id in user_last_used:
        elapsed_time = current_time - user_last_used[user_id]
        if elapsed_time < 360:  # 6 minutes in seconds
            bot.reply_to(message, "Bạn cần chờ khoảng 6 phút trước khi sử dụng lại lệnh này.")
            return

    if len(message.text.split()) != 2:
        bot.reply_to(message, "Vui lòng nhập đúng định dạng: view (link video tiktok)")
        return
    
    tiktok_link = message.text.split()[1]

    if not tiktok_link.startswith("https://vt.tiktok.com/"):
        bot.reply_to(message, "Vui lòng nhập đúng định dạng link TikTok.")
        return

    # Chạy 5 file view.py với link TikTok
    file_path = os.path.join(os.getcwd(), "view.py")
    for _ in range(5):
        subprocess.Popen(["python", file_path, tiktok_link, "100"])
    
    # Cập nhật thời gian sử dụng lệnh
    user_last_used[user_id] = current_time

    # Gửi tin nhắn xác nhận
    response_message = (
        "┏━━━━━━━━━━━━━━━━┓\n"
        "┣➤ 🚀 Gửi Yêu Cầu Buff View Ok 〽️\n"
        "┣➤ View Mặc Định 500\n"
        f"┣➤ Video 🎥:[ {tiktok_link} ]\n"
        "View👀: 500✅\n"
        "Bạn Đang Sử Dụng Spamvip\n"
        "https://files.catbox.moe/36gpm3.mp4"
    )
    bot.reply_to(message, response_message)

# Start polling
bot.polling()
