from jinja2 import Environment, FileSystemLoader
import os
from datetime import datetime
from .config import Config
from urllib.parse import urlparse

def get_domain(url):
    return urlparse(url).netloc

class ReportGenerator:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader('templates'))
        # Add custom filter
        self.env.filters['urlparse'] = get_domain
        self.template = self.env.get_template('report_template.html')

    def generate_report(self, results):
        report_data = {
            'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'results': results
        }
        
        report_path = os.path.join(Config.REPORT_PATH, f'meta_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html')
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(self.template.render(report_data))
        
        return report_path
