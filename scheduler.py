from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
from news_fetcher import NewsFetcher
from image_generator import ImageGenerator
from facebook_poster import FacebookPoster
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BotScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.news_fetcher = NewsFetcher()
        self.image_generator = ImageGenerator()
        self.facebook_poster = FacebookPoster()

    def post_news(self):
        """Основная функция для постинга новостей"""
        logger.info("Starting news posting cycle...")
        
        try:
            # Получаем последнюю новость
            news_list = self.news_fetcher.get_latest_news(limit=1)
            
            if not news_list:
                logger.warning("No news found!")
                return
            
            news = news_list[0]
            
            logger.info(f"Processing news: {news['title']}")
            
            # Генерируем изображение
            image = self.image_generator.generate_post_image(
                title=news['title'],
                source=news.get('source', 'Cosmos Bot'),
                image_url=news.get('image_url')
            )
            
            # Сохраняем изображение
            image_path = self.image_generator.save_image(image, "temp_post.jpg")
            
            # Готовим сообщение для Facebook
            message = f"""🚀 {news['title']}\n\n{news['description'][:300]}...\n\n📖 Подробнее: {news['link']}\n\n#Космос #NASA #Роскосмос #SpaceNews"""
            
            # Постим в Facebook
            success = self.facebook_poster.post_to_group(message, image_path)
            
            if success:
                logger.info("News posted successfully!")
            else:
                logger.error("Failed to post news")
                
        except Exception as e:
            logger.error(f"Error in post_news: {e}")

    def start(self):
        """Запустить планировщик"""
        self.scheduler.add_job(
            self.post_news,
            trigger=IntervalTrigger(hours=config.POST_INTERVAL_HOURS),
            id='post_news_job',
            name='Post space news to Facebook'
        )
        
        self.scheduler.start()
        logger.info(f"Scheduler started! Posts every {config.POST_INTERVAL_HOURS} hours")

    def stop(self):
        """Остановить планировщик"""
        self.scheduler.shutdown()
        logger.info("Scheduler stopped")
