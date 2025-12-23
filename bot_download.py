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
        # Disfarce universal para mobile
        'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'add_header': [
            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language: pt-BR,pt;q=0.9',
        ],
    }
    
    # Ajuste de referer baseado na rede social
    if "pinterest" in url: ydl_opts['referer'] = 'https://www.pinterest.com/'
    elif "instagram" in url: ydl_opts['referer'] = 'https://www.instagram.com/'
    elif "mercadolivre" in url: ydl_opts['referer'] = 'https://www.mercadolivre.com.br/'
    elif "kwai" in url: ydl_opts['referer'] = 'https://www.kwai.com/'
    else: ydl_opts['referer'] = 'https://www.google.com/'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)
    except Exception as e:
        print(f"Erro: {e}")
        return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🤖 Bot de Download Ativado!\n\nEnvie links de:\n✅ Shopee / Mercado Livre\n✅ TikTok / Kwai\n✅ Instagram / Pinterest")

@bot.message_handler(func=lambda m: True)
def handle(message):
    url = message.text.strip()
    sites_aceitos = ["tiktok", "shopee", "shp.ee", "kwai", "pinterest", "pin.it", "instagram", "mercadolivre", "mercadolibre"]
    
    if any(site in url.lower() for site in sites_aceitos):
        msg = bot.reply_to(message, "⏳ Processando seu link... isso pode levar alguns segundos.")
        
        file_path = download_video(url)
        
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as video:
                    bot.send_video(message.chat.id, video)
                bot.delete_message(message.chat.id, msg.message_id)
                os.remove(file_path)
            except:
                bot.reply_to(message, "❌ Erro ao enviar o vídeo.")
        else:
            bot.edit_message_text("⚠️ Não consegui baixar este vídeo.\n\nMotivo: O site bloqueou o acesso do servidor ou o link é privado.", message.chat.id, msg.message_id)
    else:
        bot.reply_to(message, "❌ Link não suportado. Envie um link válido.")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
