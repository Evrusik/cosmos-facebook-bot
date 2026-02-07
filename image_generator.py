from PIL import Image, ImageDraw, ImageFont, ImageFilter
import requests
from io import BytesIO
import logging
from textwrap import wrap
from typing import Optional
import config

logger = logging.getLogger(__name__)


class ImageGenerator:
    def __init__(self):
        self.width = config.IMAGE_WIDTH
        self.height = config.IMAGE_HEIGHT
        self.background_color = (15, 23, 42)  # Темно-синий космический фон
        self.text_color = (255, 255, 255)  # Белый текст

    def get_space_image(self, title: str, image_url: Optional[str] = None) -> Image.Image:
        """Получить космическое изображение из Unsplash"""
        try:
            # Определяем ключевое слово для поиска
            keyword = self._get_keyword(title)
            
            # Ищем изображение на Unsplash
            if not image_url:
                image_url = self._search_unsplash_image(keyword)
            
            if image_url:
                response = requests.get(image_url, timeout=10)
                img = Image.open(BytesIO(response.content))
                img = img.resize((self.width, self.height), Image.Resampling.LANCZOS)
                return img
                
        except Exception as e:
            logger.error(f"Error fetching image: {e}")
        
        # Если не удалось получить изображение, создаем градиент
        return self._create_gradient_background()

    def _get_keyword(self, title: str) -> str:
        """Выбрать ключевое слово на основе заголовка новости"""
        title_lower = title.lower()
        
        # Проверяем, о какой планете идет речь
        keywords_map = {
            'марс': 'mars landscape',
            'луна': 'moon',
            'юпитер': 'jupiter planet',
            'сатурн': 'saturn rings',
            'венера': 'venus planet',
            'меркурий': 'mercury planet',
            'нептун': 'neptune planet',
            'уран': 'uranus planet',
            'мкс': 'international space station',
            'ракета': 'rocket space',
            'галактика': 'galaxy',
        }
        
        for keyword, search_term in keywords_map.items():
            if keyword in title_lower:
                return search_term
        
        # По умолчанию космос
        return 'space universe'

    def _search_unsplash_image(self, keyword: str) -> Optional[str]:
        """Найти изображение на Unsplash"""
        try:
            url = "https://api.unsplash.com/search/photos"
            params = {
                'query': keyword,
                'per_page': 1,
                'client_id': config.UNSPLASH_API_KEY
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data['results']:
                    return data['results'][0]['urls']['regular']
                    
        except Exception as e:
            logger.error(f"Error searching Unsplash: {e}")
        
        return None

    def _create_gradient_background(self) -> Image.Image:
        """Создать градиентный фон космоса"""
        img = Image.new('RGB', (self.width, self.height), self.background_color)
        
        # Добавляем звезды (точки)
        from random import randint
        draw = ImageDraw.Draw(img)
        
        for _ in range(100):
            x = randint(0, self.width)
            y = randint(0, self.height)
            size = randint(1, 3)
            draw.ellipse(
                [x, y, x + size, y + size],
                fill=(255, 255, 255, 200)
            )
        
        return img

    def add_text_to_image(self, image: Image.Image, title: str, subtitle: str = "") -> Image.Image:
        """Добавить текст к изображению""" 
        # Добавляем полупрозрачный оверлей для читаемости текста
        overlay = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 180))
        
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        image = Image.alpha_composite(image, overlay)
        image = image.convert('RGB')
        
        draw = ImageDraw.Draw(image)
        
        # Пытаемся загрузить шрифт, если не получится - используем дефолтный
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
            subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
        
        # Разбиваем заголовок на строки
        title_lines = wrap(title, width=30)
        
        # Расчитываем позицию Y для центрирования
        y_position = (self.height - len(title_lines) * 60) // 2
        
        # Рисуем заголовок
        for line in title_lines:
            bbox = draw.textbbox((0, 0), line, font=title_font)
            text_width = bbox[2] - bbox[0]
            x_position = (self.width - text_width) // 2
            
            draw.text(
                (x_position, y_position),
                line,
                fill=self.text_color,
                font=title_font
            )
            y_position += 60
        
        # Добавляем источник внизу
        if subtitle:
            bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
            text_width = bbox[2] - bbox[0]
            x_position = (self.width - text_width) // 2
            
            draw.text(
                (x_position, self.height - 80),
                subtitle,
                fill=(200, 200, 200),
                font=subtitle_font
            )
        
        return image

    def generate_post_image(self, title: str, source: str = "Cosmos Bot", image_url: Optional[str] = None) -> Image.Image:
        """Сгенерировать финальное изображение для поста""" 
        # Получаем космическое изображение
        bg_image = self.get_space_image(title, image_url)
        
        # Добавляем текст
        final_image = self.add_text_to_image(bg_image, title, f"📡 {source}")
        
        return final_image

    def save_image(self, image: Image.Image, filename: str = "post_image.jpg") -> str:
        """Сохранить изображение""" 
        try:
            image.save(filename, 'JPEG', quality=95)
            logger.info(f"Image saved: {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error saving image: {e}")
            return None