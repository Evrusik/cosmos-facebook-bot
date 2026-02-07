import feedparser
import requests
from datetime import datetime
import logging
from typing import List, Dict
from google.cloud import translate_v2
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsFetcher:
    def __init__(self):
        self.translate_client = translate_v2.Client()
        self.fetched_news = []

    def fetch_from_rss(self) -> List[Dict]:
        """Получить новости из RSS фидов"""
        all_news = []
        
        for rss_url in config.RSS_SOURCES:
            try:
                logger.info(f"Fetching from RSS: {rss_url}")
                feed = feedparser.parse(rss_url)
                
                for entry in feed.entries[:3]:  # Берем последние 3 новости с каждого источника
                    news_item = {
                        'title': entry.get('title', 'No title'),
                        'description': entry.get('summary', entry.get('description', '')),
                        'link': entry.get('link', ''),
                        'published': entry.get('published', ''),
                        'source': rss_url,
                    }
                    all_news.append(news_item)
                    
            except Exception as e:
                logger.error(f"Error fetching RSS from {rss_url}: {e}")
                
        return all_news

    def fetch_from_space_api(self) -> List[Dict]:
        """Получить новости из Space Flight News API"""
        try:
            logger.info("Fetching from Space Flight News API")
            url = "https://api.spaceflightnewsapi.net/v4/articles/?limit=5"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                news = []
                
                for article in data.get('results', []):
                    # Переводим на русский
                    translated_title = self.translate_text(article.get('title', ''))
                    translated_summary = self.translate_text(article.get('summary', ''))
                    
                    news_item = {
                        'title': translated_title,
                        'description': translated_summary,
                        'link': article.get('url', ''),
                        'published': article.get('published_at', ''),
                        'source': 'Space Flight News API',
                        'image_url': article.get('image_url', ''),
                    }
                    news.append(news_item)
                    
                return news
                
        except Exception as e:
            logger.error(f"Error fetching from Space API: {e}")
            
        return []

    def translate_text(self, text: str) -> str:
        """Переводит текст на русский язык"""
        try:
            if not text:
                return text
                
            result = self.translate_client.translate_text(
                text,
                target_language='ru'
            )
            return result['translatedText']
            
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return text

    def get_all_news(self) -> List[Dict]:
        """Получить все новости из всех источников"""
        all_news = []
        
        # Получаем из RSS
        rss_news = self.fetch_from_rss()
        all_news.extend(rss_news)
        
        # Получаем из Space API
        api_news = self.fetch_from_space_api()
        all_news.extend(api_news)
        
        # Удаляем дубликаты
        seen = set()
        unique_news = []
        for news in all_news:
            title = news['title'].lower()
            if title not in seen:
                seen.add(title)
                unique_news.append(news)
        
        logger.info(f"Fetched {len(unique_news)} unique news items")
        return unique_news

    def get_latest_news(self, limit: int = 1) -> List[Dict]:
        """Получить последние новости"""
        all_news = self.get_all_news()
        return all_news[:limit]