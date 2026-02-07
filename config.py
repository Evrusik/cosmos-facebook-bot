import os
from dotenv import load_dotenv

load_dotenv()

# Facebook
FACEBOOK_ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN')
FACEBOOK_GROUP_ID = os.getenv('FACEBOOK_GROUP_ID')

# API Keys
UNSPLASH_API_KEY = os.getenv('UNSPLASH_API_KEY')
GOOGLE_TRANSLATE_API_KEY = os.getenv('GOOGLE_TRANSLATE_API_KEY')
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')

# Bot Settings
POST_INTERVAL_HOURS = 6  # Постить каждые 6 часов
IMAGE_WIDTH = 1200
IMAGE_HEIGHT = 630
FONT_SIZE = 40

# News Sources (RSS фиды на русском)
RSS_SOURCES = [
    'https://www.roscosmos.ru/rss/',
    'https://novosti-kosmonavtiki.ru/feed/',
    'https://universemagazine.com/ru/feed/',
]

# Тематика космоса для поиска изображений
SPACE_KEYWORDS = {
    'mars': ['марс', 'красная планета'],
    'moon': ['луна', 'спутник земли'],
    'jupiter': ['юпитер', 'газовый гигант'],
    'saturn': ['сатурн', 'кольца'],
    'nasa': ['нейса', 'космос'],
    'iss': ['мкс', 'станция'],
    'rocket': ['ракета', 'запуск'],
    'galaxy': ['галактика', 'млечный путь'],
    'space': ['космос', 'космическое пространство'],
}