import telebot
import yt_dlp
import os
from flask import Flask
from threading import Thread

# Seu Token
CHAVE_API = '8207994174:AAGQyQgc0CwsJaDz4O6KKhJgKznbQVTqP4s' 

bot = telebot.TeleBot(CHAVE_API)
app = Flask('')

@app.route('/')
def home():
    return "Bot Multi-Plataforma Online"

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
        'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'add_header': [
            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language: pt-BR,pt;q=0.9',
        ],
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)
    except Exception as e:
        print(f"Erro: {e}")
        return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🤖 Bot de Download Ativado!\n\nEnvie links de:\n✅ YouTube\n✅ TikTok / Kwai\n✅ Pinterest / Instagram\n✅ Shopee / Mercado Livre")

@bot.message_handler(func=lambda m: True)
def handle(message):
    url = message.text.strip()
    # Adicionado YouTube e YouTu.be à lista
    sites_aceitos = ["youtube.com", "youtu.be", "tiktok", "shopee", "shp.ee", "kwai", "pinterest", "pin.it", "instagram", "mercadolivre"]
    
    if any(site in url.lower() for site in sites_aceitos):
        msg = bot.reply_to(message, "⏳ Processando seu vídeo... aguarde um momento.")
        
        file_path = download_video(url)
        
        if file_path and os.path.exists(file_path):
            try:
                # Nota: O Telegram tem limite de 50MB para bots enviarem arquivos no plano normal
                with open(file_path, 'rb') as video:
                    bot.send_video(message.chat.id, video)
                bot.delete_message(message.chat.id, msg.message_id)
                os.remove(file_path)
            except Exception as e:
                bot.edit_message_text(f"❌ Erro ao enviar. O vídeo pode ser muito grande para o Telegram.", message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("⚠️ Não consegui baixar este vídeo.", message.chat.id, msg.message_id)
    else:
        bot.reply_to(message, "❌ Link não suportado. Tente YouTube, TikTok, Shopee, etc.")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling(timeout=20)
