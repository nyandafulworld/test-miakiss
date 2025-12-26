#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
既存記事を新しいテンプレートに更新するスクリプト
"""

import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup

# プロジェクトルート
PROJECT_ROOT = Path(__file__).parent.parent
BLOG_DIR = PROJECT_ROOT / "blog"
TEMPLATE_FILE = BLOG_DIR / "article_template.html"


def extract_article_content(html_content):
    """
    既存記事HTMLから必要な情報を抽出
    
    Returns:
        dict: {title, date, date_display, slug, description, content}
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # タイトル
    title_tag = soup.find('h1', class_='article-title')
    title = title_tag.get_text(strip=True) if title_tag else ""
    
    # 日付
    date_tag = soup.find('time', class_='article-date')
    date = date_tag.get('datetime', '') if date_tag else ""
    date_display = date_tag.get_text(strip=True) if date_tag else ""
    
    # メタ description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    description = meta_desc.get('content', '') if meta_desc else ""
    
    # 本文コンテンツ
    content_div = soup.find('div', class_='article-content')
    if content_div:
        # 本文のHTMLを取得（タグごと）
        content = str(content_div)
        # 外側の<div class="article-content">タグを削除
        content = re.sub(r'<div[^>]*class="article-content"[^>]*>', '', content, count=1)
        content = re.sub(r'</div>\s*$', '', content, count=1)
        content = content.strip()
    else:
        content = ""
    
    # slug（URLから抽出）
    canonical = soup.find('link', attrs={'rel': 'canonical'})
    slug = ""
    if canonical:
        href = canonical.get('href', '')
        # https://www.miakiss.co.jp/blog/SLUG.html から SLUG を抽出
        match = re.search(r'/blog/([^/]+)\.html', href)
        if match:
            slug = match.group(1)
    
    return {
        'title': title,
        'date': date,
        'date_display': date_display,
        'slug': slug,
        'description': description,
        'content': content
    }


def update_article_with_template(article_file, template_file):
    """
    記事ファイルを新しいテンプレートで更新
    """
    # 既存記事を読み込み
    with open(article_file, 'r', encoding='utf-8') as f:
        article_html = f.read()
    
    # コンテンツを抽出
    data = extract_article_content(article_html)
    
    print(f"\n📄 記事: {data['title']}")
    print(f"   Slug: {data['slug']}")
    print(f"   日付: {data['date']}")
    
    # テンプレートを読み込み
    with open(template_file, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # プレースホルダーを置換
    new_html = template
    new_html = new_html.replace('{{TITLE}}', data['title'])
    new_html = new_html.replace('{{DATE}}', data['date'])
    new_html = new_html.replace('{{DATE_DISPLAY}}', data['date_display'])
    new_html = new_html.replace('{{SLUG}}', data['slug'])
    new_html = new_html.replace('{{DESCRIPTION}}', data['description'])
    new_html = new_html.replace('{{CONTENT}}', data['content'])
    
    # ファイルを上書き保存
    with open(article_file, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f"   ✅ 更新完了")


def main():
    """
    メイン処理
    """
    if len(sys.argv) < 2:
        print("使用方法: python update_article_template.py <記事ファイル名>")
        print("例: python update_article_template.py 2025-12-01-website-maintenance-contract-necessity.html")
        sys.exit(1)
    
    article_filename = sys.argv[1]
    article_file = BLOG_DIR / article_filename
    
    if not article_file.exists():
        print(f"❌ エラー: ファイルが見つかりません: {article_file}")
        sys.exit(1)
    
    if not TEMPLATE_FILE.exists():
        print(f"❌ エラー: テンプレートファイルが見つかりません: {TEMPLATE_FILE}")
        sys.exit(1)
    
    # 記事を更新
    update_article_with_template(article_file, TEMPLATE_FILE)
    print("\n✅ 処理完了")


if __name__ == "__main__":
    main()
































