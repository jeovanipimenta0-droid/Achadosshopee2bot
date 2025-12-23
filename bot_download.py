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
    bot.reply_to(message, "Olá! Cole o link do TikTok ou Shopee Video aqui para eu baixar.")

@bot.message_handler(func=lambda m: True)
def handle(message):
    url = message.text.strip()
    if "tiktok.com" in url or "shopee.com.br/universal-link/video" in url:
        msg = bot.reply_to(message, "⏳ Processando seu vídeo... aguarde.")
        file = download_video(url)
        if file:
            try:
                with open(file, 'rb') as v:
                    bot.send_video(message.chat.id, v)
                bot.delete_message(message.chat.id, msg.message_id)
                os.remove(file)
            except:
                bot.reply_to(message, "Erro ao enviar o arquivo.")
        else:
            bot.reply_to(message, "Não consegui baixar. Verifique se o link é público.")
    else:
        bot.reply_to(message, "Por favor, envie um link válido do TikTok ou Shopee Video.")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()

