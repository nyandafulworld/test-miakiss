#!/usr/bin/env python3
"""
index.html のブログセクションを自動更新するスクリプト
blog/published_articles.json から最新5件を取得して表示
"""

import json
import os
import re
from datetime import datetime

def load_published_articles():
    """published_articles.json を読み込む"""
    json_path = os.path.join(os.path.dirname(__file__), '..', 'blog', 'published_articles.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('articles', [])

def format_date(date_str):
    """YYYY-MM-DD を YYYY.MM.DD 形式に変換"""
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return dt.strftime('%Y.%m.%d')
    except:
        return date_str

def generate_blog_html(articles, max_items=5):
    """ブログ記事のHTMLを生成"""
    # 日付で降順ソート
    sorted_articles = sorted(articles, key=lambda x: x.get('date', ''), reverse=True)
    latest = sorted_articles[:max_items]
    
    html_items = []
    for article in latest:
        slug = article.get('slug', '')
        title = article.get('title', '')
        date = article.get('date', '')
        description = article.get('description', '')
        
        # 画像はデフォルトでogp.pngを使用（将来的に記事ごとに設定可能）
        image = 'image/ogp.png'
        
        html_item = f'''                    <article class="blog-item">
                        <a href="blog/{slug}.html">
                            <div class="blog-image">
                                <img src="{image}" alt="{title}">
                            </div>
                            <div class="blog-content">
                                <time class="blog-date" datetime="{date}">{format_date(date)}</time>
                                <h3 class="blog-title">{title}</h3>
                                <p class="blog-excerpt">{description}</p>
                            </div>
                        </a>
                    </article>'''
        html_items.append(html_item)
    
    return '\n'.join(html_items)

def update_index_html():
    """index.html のブログセクションを更新"""
    index_path = os.path.join(os.path.dirname(__file__), '..', 'index.html')
    
    # index.html を読み込む
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 記事を読み込む
    articles = load_published_articles()
    if not articles:
        print("No articles found")
        return
    
    # 新しいブログHTMLを生成
    new_blog_html = generate_blog_html(articles)
    
    # blog-grid の中身を置換
    pattern = r'(<div class="blog-grid">)\s*.*?\s*(</div>\s*</div>\s*</section>\s*<section id="company")'
    replacement = f'\\1\n{new_blog_html}\n                \\2'
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # 書き込む
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Updated index.html with {len(articles)} articles (showing latest 5)")

if __name__ == '__main__':
    update_index_html()
