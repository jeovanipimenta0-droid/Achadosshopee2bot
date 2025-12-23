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
    app.run(host='1.0.0.1', port=8080)

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
        # O DISFARCE COMPLETO QUE VOCÊ ENVIOU:
        'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'add_header': [
            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language: pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        ],
        'referer': 'https://shopee.com.br/',
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
    bot.reply_to(message, "✅ Bot de Achados Shopee Ativado!\nEnvie o link do vídeo (TikTok ou Shopee) para baixar.")

@bot.message_handler(func=lambda m: True)
def handle(message):
    url = message.text.strip()
    
    # Reconhece links curtos e longos da Shopee e TikTok
    if any(site in url for site in ["tiktok.com", "shopee.com", "shp.ee"]):
        msg = bot.reply_to(message, "⏳ Link detectado! Tentando burlar bloqueios e baixar o vídeo...")
        
        file_path = download_video(url)
        
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as video:
                    bot.send_video(message.chat.id, video)
                bot.delete_message(message.chat.id, msg.message_id)
                os.remove(file_path) # Limpa o arquivo para o servidor não travar
            except Exception as e:
                bot.reply_to(message, "❌ Erro ao enviar o vídeo para o Telegram.")
        else:
            bot.edit_message_text("⚠️ A Shopee bloqueou o download deste servidor.\n\nIsso acontece porque o IP do Render é público. Tente novamente em alguns minutos ou use o link completo do navegador.", message.chat.id, msg.message_id)
    else:
        bot.reply_to(message, "❌ Por favor, envie um link válido do TikTok ou Shopee Video.")

if __name__ == "__main__":
    keep_alive()
    # Timeout ajustado para evitar o erro 409 de conflito que vimos nos logs
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
