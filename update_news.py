"""Refresh the short Fasecolda news list for this static site."""
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

url = 'https://www.fasecolda.com/category/noticias/feed/'
request = urllib.request.Request(url, headers={'User-Agent': 'PrascaSegurosNews/1.0 (+https://www.fasecolda.com/category/noticias/)'})
with urllib.request.urlopen(request, timeout=25) as response:
    root = ET.fromstring(response.read())
items = []
for item in root.findall('./channel/item'):
    link = (item.findtext('link') or '').strip()
    title = (item.findtext('title') or '').strip()
    if not link.startswith('https://www.fasecolda.com/') or not title:
        continue
    date = (item.findtext('pubDate') or '').strip()
    try:
        from email.utils import parsedate_to_datetime
        date = parsedate_to_datetime(date).strftime('%Y-%m-%d')
    except (ValueError, TypeError):
        date = ''
    items.append({'title': title, 'url': link, 'date': date})
    if len(items) == 4:
        break
if not items:
    raise RuntimeError('The Fasecolda feed did not contain news items')
Path('news.json').write_text(json.dumps({'updated': datetime.now(timezone.utc).isoformat(), 'items': items}, ensure_ascii=False, indent=2) + '\n')
