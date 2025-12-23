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
    return "Bot Profissional Online"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

def download_video(url):
    # DADOS DO SEU PROXY EXTRAÍDOS DA IMAGEM
    proxy_url = "http://14aa05e12f829:afbfc370cc@185.123.144.222:12323"
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'proxy': proxy_url, # Seu túnel particular para evitar bloqueios
        'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'add_header': [
            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language: pt-BR,pt;q=0.9',
        ],
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
    bot.reply_to(message, "🚀 Bot de Achados Pro Ativado!\n\nEnvie links de: Shopee, TikTok, Kwai, Pinterest, Instagram ou Mercado Livre.")

@bot.message_handler(func=lambda m: True)
def handle(message):
    url = message.text.strip()
    sites_aceitos = ["tiktok", "shopee", "shp.ee", "kwai", "pinterest", "pin.it", "instagram", "mercadolivre"]
    
    if any(site in url.lower() for site in sites_aceitos):
        status = bot.reply_to(message, "⏳ Utilizando Proxy para baixar seu vídeo... aguarde.")
        
        file_path = download_video(url)
        
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as video:
                    bot.send_video(message.chat.id, video)
                bot.delete_message(message.chat.id, status.message_id)
                os.remove(file_path)
            except:
                bot.edit_message_text("❌ Erro ao enviar o arquivo.", message.chat.id, status.message_id)
        else:
            bot.edit_message_text("⚠️ Mesmo com Proxy, o vídeo não pôde ser baixado.\nVerifique se o link é público ou tente novamente.", message.chat.id, status.message_id)
    else:
        bot.reply_to(message, "❌ Link não reconhecido.")

if __name__ == "__main__":
    keep_alive()
    # Timeout longo para o proxy ter tempo de responder
    bot.infinity_polling(timeout=30, long_polling_timeout=15)

