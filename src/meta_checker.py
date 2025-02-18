from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os
import json
from datetime import datetime
from .config import Config
import requests
from PIL import Image
from io import BytesIO

class MetaChecker:
    def __init__(self):
        self.setup_driver()
        self.results = []

    def setup_driver(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def check_meta_tags(self, url):
        self.driver.get(url)
        
        # Get social media images
        og_image = self._get_og_meta().get('og:image')
        twitter_image = self._get_twitter_meta().get('twitter:image')
        
        # Get image dimensions
        image_info = {
            'og_image_dimensions': self._get_image_dimensions(og_image) if og_image else "No image",
            'twitter_image_dimensions': self._get_image_dimensions(twitter_image) if twitter_image else "No image"
        }

        result = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'meta_tags': self._get_meta_tags(),
            'social_previews': self._get_social_previews(),
            'screenshots': self._take_screenshots(url),
            'image_info': image_info
        }
        self.results.append(result)
        return result

    def _get_meta_tags(self):
        meta_tags = {}
        # Get title
        title = self.driver.title
        meta_tags['title'] = title

        # Get all meta tags
        tags = self.driver.find_elements(By.TAG_NAME, 'meta')
        for tag in tags:
            name = tag.get_attribute('name') or tag.get_attribute('property')
            content = tag.get_attribute('content')
            if name and content:
                meta_tags[name] = content

        # Get Pinterest-specific meta
        pinterest_tags = self.driver.find_elements(By.CSS_SELECTOR, 'meta[data-pin-name]')
        for tag in pinterest_tags:
            name = f"pinterest:{tag.get_attribute('data-pin-name')}"
            content = tag.get_attribute('content')
            if content:
                meta_tags[name] = content

        # Get canonical URL
        canonical = self.driver.find_elements(By.CSS_SELECTOR, 'link[rel="canonical"]')
        if canonical:
            meta_tags['canonical'] = canonical[0].get_attribute('href')

        return meta_tags

    def _get_social_previews(self):
        og_meta = self._get_og_meta()
        twitter_meta = self._get_twitter_meta()
        
        return {
            'og': og_meta,
            'twitter': twitter_meta,
            'schema': self._get_schema_meta(),
            'pinterest': self._get_pinterest_meta(),
            'card_types': {
                'facebook': self._determine_fb_card_type(og_meta),
                'twitter': twitter_meta.get('twitter:card', 'summary_large_image')
            }
        }

    def _get_og_meta(self):
        og_tags = {}
        # Get Facebook-specific meta tags
        for tag in self.driver.find_elements(By.CSS_SELECTOR, 'meta[property^="og:"], meta[property^="fb:"]'):
            property_name = tag.get_attribute('property')
            content = tag.get_attribute('content')
            if property_name and content:
                og_tags[property_name] = content
        
        # Get additional Facebook meta
        fb_app_id = self.driver.find_elements(By.CSS_SELECTOR, 'meta[property="fb:app_id"]')
        if fb_app_id:
            og_tags['fb:app_id'] = fb_app_id[0].get_attribute('content')
        
        return og_tags

    def _get_twitter_meta(self):
        twitter_tags = {}
        # Get Twitter card type
        card = self.driver.find_elements(By.CSS_SELECTOR, 'meta[name="twitter:card"]')
        if card:
            twitter_tags['twitter:card'] = card[0].get_attribute('content')
        
        # Get all Twitter meta tags
        for tag in self.driver.find_elements(By.CSS_SELECTOR, 'meta[name^="twitter:"]'):
            name = tag.get_attribute('name')
            content = tag.get_attribute('content')
            if name and content:
                twitter_tags[name] = content
        
        # Fallback to OG tags if Twitter tags are missing
        if 'twitter:title' not in twitter_tags:
            og_title = self._get_og_meta().get('og:title')
            if og_title:
                twitter_tags['twitter:title'] = og_title
        
        if 'twitter:description' not in twitter_tags:
            og_desc = self._get_og_meta().get('og:description')
            if og_desc:
                twitter_tags['twitter:description'] = og_desc
        
        if 'twitter:image' not in twitter_tags:
            og_image = self._get_og_meta().get('og:image')
            if og_image:
                twitter_tags['twitter:image'] = og_image
                
        # Set default card type if missing
        if 'twitter:card' not in twitter_tags:
            twitter_tags['twitter:card'] = 'summary_large_image'
        
        return twitter_tags

    def _determine_fb_card_type(self, og_meta):
        """Determine Facebook card type based on OG meta tags"""
        if 'og:video' in og_meta:
            return 'video'
        elif 'og:image' in og_meta:
            if 'og:image:width' in og_meta and 'og:image:height' in og_meta:
                width = int(og_meta['og:image:width'])
                height = int(og_meta['og:image:height'])
                if width >= 600 and height >= 314:
                    return 'large_image'
            return 'standard_image'
        return 'website'

    def _get_schema_meta(self):
        schema_tags = []
        for tag in self.driver.find_elements(By.CSS_SELECTOR, 'script[type="application/ld+json"]'):
            try:
                schema_tags.append(json.loads(tag.get_attribute('innerHTML')))
            except json.JSONDecodeError:
                continue
        return schema_tags

    def _get_pinterest_meta(self):
        pinterest_tags = {}
        selectors = [
            'meta[name^="pinterest:"]',
            'meta[data-pin-name]',
            'meta[data-pin-description]',
            'meta[data-pin-id]'
        ]
        
        for selector in selectors:
            for tag in self.driver.find_elements(By.CSS_SELECTOR, selector):
                name = (tag.get_attribute('name') or 
                       f"pinterest:{tag.get_attribute('data-pin-name')}" or
                       f"pinterest:{tag.get_attribute('data-pin-description')}")
                content = tag.get_attribute('content')
                if name and content:
                    pinterest_tags[name] = content
        
        return pinterest_tags

    def _take_screenshots(self, url):
        screenshot_path = os.path.join(Config.SCREENSHOT_PATH, f"{url.replace('://', '_').replace('/', '_')}.png")
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        self.driver.save_screenshot(screenshot_path)
        return screenshot_path

    def _get_image_dimensions(self, image_url):
        try:
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))
            return f"{img.width}x{img.height}px"
        except:
            return "Unable to fetch dimensions"

    def close(self):
        self.driver.quit()
