import requests
from bs4 import BeautifulSoup
import telebot
from datetime import datetime
import time
import schedule

# конфиг
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHANNEL_ID = "@your_channel_name"  # или ID канала 
RSS_FEED_URL = "https://example.com/rss"  # или API новстей


bot = telebot.TeleBot(TELEGRAM_TOKEN)

def parse_articles():
    try:
        response = requests.get(RSS_FEED_URL)
        soup = BeautifulSoup(response.text, "xml") 
        articles = soup.find_all("item")[:5]  
        
        for article in articles:
            title = article.title.text
            link = article.link.text
            description = article.description.text[:200] + "..."  

            post = f"📢 <b>{title}</b>\n\n{description}\n\n🔗 <a href='{link}'>Читать далее</a>"
            
            bot.send_message(
                CHANNEL_ID, 
                post, 
                parse_mode="HTML", 
                disable_web_page_preview=False
            )
            time.sleep(5)  # чтоб не спамить
            
    except Exception as e:
        print(f"Ошибка: {e}")

schedule.every().day.at("12:00").do(parse_articles)

if __name__ == "__main__":
    print("Бот запущен! Ожидание публикаций...")
    while True:
        schedule.run_pending()
        time.sleep(60)