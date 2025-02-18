# Meta Tags Checker

A Python-based tool that generates visual previews of how your website appears on different social media platforms and search engines.

## Features

🔍 **Visual Previews For:**
- Google Search Results
- Facebook/Meta Link Preview
- Twitter Cards
- LinkedIn Posts
- Pinterest Pins
- Slack Link Unfurling

🛠️ **Technical Checks:**
- Meta tag validation
- Image dimension verification
- Social media meta tags compliance
- Canonical URL verification

## Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Configure your settings:
```bash
cp .env.example .env
```

## Configuration

Edit `.env` file:
```bash
# List of URLs to check (comma-separated)
URLS_TO_CHECK=https://example.com,https://example.org

# Browser settings (chrome/firefox)
BROWSER=chrome

# Output directories
REPORT_PATH=reports
SCREENSHOT_PATH=screenshots
```

## Usage

1. Basic check:
```bash
python main.py
```

2. Check multiple URLs:
```bash
# In .env file
URLS_TO_CHECK=https://site1.com,https://site2.com,https://site3.com
```

## Generated Report

The HTML report includes:

1. **Search Engine Preview**
   - Google search result appearance

2. **Social Media Previews**
   - Facebook/Meta link preview
   - Twitter Card (summary/summary_large_image)
   - LinkedIn post preview
   - Pinterest pin preview
   - Slack unfurled link

3. **Technical Details**
   - Image dimensions for og:image and twitter:image
   - Canonical URL if present

## Image Requirements

For optimal display across platforms:

- **Facebook/Meta**: 1200x630 pixels
- **Twitter**: 
  - Summary Card: 120x120 pixels minimum
  - Summary Card with Large Image: 280x150 pixels minimum
- **LinkedIn**: 1200x627 pixels
- **Pinterest**: 1000x1500 pixels (2:3 ratio)

## Common Issues

The tool helps identify:
- Missing meta tags
- Incorrect image dimensions
- Missing social media tags
- Invalid canonical URLs

## Output Example

Reports are saved as: `reports/meta_report_YYYYMMDD_HHMMSS.html`
Screenshots: `screenshots/domain_com.png`

## Dependencies

- Selenium: Web automation
- Python-dotenv: Environment configuration
- Jinja2: HTML report generation
- Pillow: Image processing
- Requests: HTTP client