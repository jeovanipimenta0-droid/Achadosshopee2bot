import telebot, yt_dlp, os, time
from flask import Flask
from threading import Thread

CHAVE_API = '8207994174:AAGQyQgc0CwsJaDz4O6KKhJgKznbQVTqP4s'
bot = telebot.TeleBot(CHAVE_API)
app = Flask('')

@app.route('/')
def home(): return "Bot Online"

def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(id)s.%(ext)s',
        'quiet': True,
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'referer': 'https://shopee.com.br/',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)
    except: return None

@bot.message_handler(func=lambda m: True)
def handle(message):
    url = message.text.strip()
    if any(x in url for x in ["tiktok.com", "shopee.com", "shp.ee"]):
        msg = bot.reply_to(message, "⏳ Processando vídeo da Shopee...")
        arquivo = download_video(url)
        if arquivo:
            with open(arquivo, 'rb') as v:
                bot.send_video(message.chat.id, v)
            os.remove(arquivo)
            bot.delete_message(message.chat.id, msg.message_id)
        else:
            bot.reply_to(message, "⚠️ A Shopee bloqueou o download neste servidor. Tente novamente em instantes.")

def run(): app.run(host='0.0.0.0', port=8080)
if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

