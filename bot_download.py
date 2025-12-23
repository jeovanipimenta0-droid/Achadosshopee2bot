import telebot
import yt_dlp
import os
from flask import Flask
from threading import Thread

# Seu Token configurado
CHAVE_API = '8207994174:AAGQyQgc0CwsJaDz4O6KKhJgKznbQVTqP4s' 

bot = telebot.TeleBot(CHAVE_API)
app = Flask('')

@app.route('/')
def home():
    return "Bot Online"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True, 
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)
    except Exception as e:
        print(f"Erro no download: {e}")
        return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Olá! Mande o link da Shopee ou TikTok.")

@bot.message_handler(func=lambda m: True)
def handle(message):
    url = message.text.strip()
    if any(site in url for site in ["tiktok.com", "shopee.com", "shp.ee"]):
        msg = bot.reply_to(message, "⏳ Link detectado! Baixando vídeo...")
        file = download_video(url)
        if file:
            try:
                with open(file, 'rb') as v:
                    bot.send_video(message.chat.id, v)
                bot.delete_message(message.chat.id, msg.message_id)
                os.remove(file)
            except:
                bot.reply_to(message, "Erro ao enviar o vídeo.")
        else:
            bot.reply_to(message, "Não consegui baixar. A Shopee Video às vezes bloqueia servidores, tentando novamente...")
    else:
        bot.reply_to(message, "Por favor, envie um link válido.")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
