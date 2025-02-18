import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    URLS = os.getenv('URLS_TO_CHECK', '').split(',')
    BROWSER = os.getenv('BROWSER', 'chrome')
    REPORT_PATH = os.getenv('REPORT_PATH', 'reports')
    SCREENSHOT_PATH = os.getenv('SCREENSHOT_PATH', 'screenshots')
