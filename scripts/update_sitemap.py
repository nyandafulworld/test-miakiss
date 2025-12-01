#!/usr/bin/env python3
"""
sitemap.xml を自動更新するスクリプト
blog/published_articles.json から記事URLを追加
"""

import json
import os
from datetime import datetime
import xml.etree.ElementTree as ET

def load_published_articles():
    """published_articles.json を読み込む"""
    json_path = os.path.join(os.path.dirname(__file__), '..', 'blog', 'published_articles.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('articles', [])

def update_sitemap():
    """sitemap.xml を更新"""
    sitemap_path = os.path.join(os.path.dirname(__file__), '..', 'sitemap.xml')
    base_url = 'https://www.miakiss.co.jp'
    
    # 既存のsitemap.xmlを読み込む
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    
    # 名前空間を処理
    ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    
    # 既存のURLを取得
    existing_urls = set()
    for url in root.findall('sm:url', ns):
        loc = url.find('sm:loc', ns)
        if loc is not None:
            existing_urls.add(loc.text)
    
    # 記事を読み込む
    articles = load_published_articles()
    added_count = 0
    
    for article in articles:
        slug = article.get('slug', '')
        date = article.get('date', datetime.now().strftime('%Y-%m-%d'))
        article_url = f'{base_url}/blog/{slug}.html'
        
        if article_url not in existing_urls:
            # 新しいURL要素を作成
            url_elem = ET.SubElement(root, 'url')
            loc = ET.SubElement(url_elem, 'loc')
            loc.text = article_url
            lastmod = ET.SubElement(url_elem, 'lastmod')
            lastmod.text = date
            changefreq = ET.SubElement(url_elem, 'changefreq')
            changefreq.text = 'monthly'
            priority = ET.SubElement(url_elem, 'priority')
            priority.text = '0.6'
            added_count += 1
    
    # 書き込む
    tree.write(sitemap_path, encoding='UTF-8', xml_declaration=True)
    
    # XMLを整形（改行を追加）
    with open(sitemap_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 整形
    content = content.replace('><', '>\n<')
    content = content.replace('<?xml version=\'1.0\' encoding=\'UTF-8\'?>', '<?xml version="1.0" encoding="UTF-8"?>')
    
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated sitemap.xml: {added_count} new URLs added")

if __name__ == '__main__':
    update_sitemap()
