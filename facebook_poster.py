import requests
import logging
from typing import Optional
import config

logger = logging.getLogger(__name__)


class FacebookPoster:
    def __init__(self):
        self.access_token = config.FACEBOOK_ACCESS_TOKEN
        self.group_id = config.FACEBOOK_GROUP_ID
        self.api_version = "v18.0"
        self.base_url = f"https://graph.facebook.com/{self.api_version}"

    def post_to_group(self, message: str, image_path: Optional[str] = None) -> bool:
        """Постить сообщение и изображение в Facebook группу"""
        try:
            if image_path:
                return self._post_with_image(message, image_path)
            else:
                return self._post_text_only(message)
                
        except Exception as e:
            logger.error(f"Error posting to Facebook: {e}")
            return False

    def _post_text_only(self, message: str) -> bool:
        """Постить только текст"""
        url = f"{self.base_url}/{self.group_id}/feed"
        
        params = {
            'message': message,
            'access_token': self.access_token
        }
        
        response = requests.post(url, data=params)
        
        if response.status_code == 200:
            logger.info("Successfully posted text to Facebook")
            return True
        else:
            logger.error(f"Facebook API error: {response.text}")
            return False

    def _post_with_image(self, message: str, image_path: str) -> bool:
        """Постить с изображением"""
        url = f"{self.base_url}/{self.group_id}/photos"
        
        try:
            with open(image_path, 'rb') as img_file:
                files = {
                    'source': img_file,
                }
                
                data = {
                    'message': message,
                    'access_token': self.access_token
                }
                
                response = requests.post(url, files=files, data=data)
                
                if response.status_code == 200:
                    logger.info("Successfully posted image to Facebook")
                    return True
                else:
                    logger.error(f"Facebook API error: {response.text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error uploading image: {e}")
            return False

    def get_group_info(self) -> dict:
        """Получить информацию о группе"""
        try:
            url = f"{self.base_url}/{self.group_id}"
            params = {'access_token': self.access_token}
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error getting group info: {response.text}")
                return {}
                
        except Exception as e:
            logger.error(f"Error: {e}")
            return {}