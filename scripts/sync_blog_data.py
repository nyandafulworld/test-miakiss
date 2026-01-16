#!/usr/bin/env python3
"""
ブログ記事データ同期スクリプト

このスクリプトは以下の処理を自動で行います：
1. blog/ ディレクトリ内のHTMLファイルをスキャン
2. HTMLのメタタグから記事情報を抽出
3. published_articles.json に存在しない新記事を自動追加
4. used_keywords.json も同時に更新
5. published_articles.js を生成

使い方:
    python3 scripts/sync_blog_data.py

これにより、記事HTMLを作成した後にこのスクリプトを実行するだけで、
全てのデータファイルが自動的に更新されます。
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime
import html.parser


class MetaTagParser(html.parser.HTMLParser):
    """HTMLからメタタグを解析するパーサー"""
    
    def __init__(self):
        super().__init__()
        self.title = None
        self.description = None
        self.date_published = None
        self.in_title = False
        self.title_content = []
        self.in_script = False
        self.script_content = []
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        if tag == 'title':
            self.in_title = True
            
        elif tag == 'meta':
            name = attrs_dict.get('name', '')
            content = attrs_dict.get('content', '')
            
            if name == 'description':
                self.description = content
                
        elif tag == 'script':
            script_type = attrs_dict.get('type', '')
            if script_type == 'application/ld+json':
                self.in_script = True
    
    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
            self.title = ''.join(self.title_content).strip()
            # " | 株式会社ミアキス" を除去
            if ' | 株式会社ミアキス' in self.title:
                self.title = self.title.replace(' | 株式会社ミアキス', '')
                
        elif tag == 'script' and self.in_script:
            self.in_script = False
            try:
                script_text = ''.join(self.script_content)
                json_data = json.loads(script_text)
                if json_data.get('@type') == 'Article':
                    self.date_published = json_data.get('datePublished')
            except (json.JSONDecodeError, TypeError):
                pass
            self.script_content = []
    
    def handle_data(self, data):
        if self.in_title:
            self.title_content.append(data)
        elif self.in_script:
            self.script_content.append(data)


def extract_article_info_from_html(html_path):
    """
    HTMLファイルからメタタグを解析して記事情報を抽出
    
    Returns:
        dict: {title, description, date, slug} または None（解析失敗時）
    """
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        parser = MetaTagParser()
        parser.feed(content)
        
        # slugはファイル名から取得（.htmlを除去）
        slug = html_path.stem
        
        if parser.title and parser.date_published:
            return {
                'title': parser.title,
                'description': parser.description or '',
                'date': parser.date_published,
                'slug': slug
            }
        else:
            return None
            
    except Exception as e:
        print(f"⚠️ HTML解析エラー: {html_path} - {e}")
        return None


def find_keyword_info(slug, title, keywords_data):
    """
    スラグとタイトルからキーワード情報を検索
    
    Returns:
        dict: {keyword, keywordId, category} または None
    """
    # まずpublished_articles.jsonに既存のエントリがあるか確認
    # なければkeywords.jsonから検索
    
    keywords = keywords_data.get('keywords', [])
    
    # 完全一致検索
    for kw in keywords:
        theme = kw.get('theme', '')
        # テーマがタイトルに含まれているか確認
        if theme and theme in title:
            return {
                'keyword': kw.get('keyword'),
                'keywordId': kw.get('id'),
                'category': kw.get('category')
            }
    
    # 部分一致検索（キーワードがタイトルに含まれているか）
    for kw in keywords:
        keyword = kw.get('keyword', '')
        if keyword and keyword in title:
            return {
                'keyword': keyword,
                'keywordId': kw.get('id'),
                'category': kw.get('category')
            }
    
    return None


def find_new_articles(blog_dir, published_articles, keywords_data):
    """
    published_articles.jsonに存在しないHTMLファイルを検出
    
    Returns:
        list: 新しい記事情報のリスト
    """
    existing_slugs = set()
    for article in published_articles.get('articles', []):
        existing_slugs.add(article.get('slug'))
    
    new_articles = []
    
    # blog/ディレクトリ内のHTMLファイルをスキャン
    for html_file in blog_dir.glob('*.html'):
        # テンプレートファイルは除外
        if 'template' in html_file.name.lower():
            continue
            
        slug = html_file.stem
        
        # 既存の記事はスキップ
        if slug in existing_slugs:
            continue
        
        # HTMLから情報を抽出
        article_info = extract_article_info_from_html(html_file)
        if article_info:
            # キーワード情報を検索
            kw_info = find_keyword_info(slug, article_info['title'], keywords_data)
            if kw_info:
                article_info['keyword'] = kw_info['keyword']
                article_info['keywordId'] = kw_info['keywordId']
                article_info['category'] = kw_info['category']
            else:
                # キーワード情報が見つからない場合はデフォルト値
                article_info['keyword'] = ''
                article_info['category'] = 'other'
            
            new_articles.append(article_info)
            print(f"✨ 新しい記事を検出: {slug}")
    
    return new_articles


def update_published_articles(published_articles, new_articles):
    """
    published_articles.json に新しい記事を追加
    """
    for article in new_articles:
        entry = {
            'slug': article['slug'],
            'title': article['title'],
            'date': article['date'],
            'category': article.get('category', 'other'),
            'keyword': article.get('keyword', ''),
            'description': article['description']
        }
        
        # keywordIdがある場合は追加
        if article.get('keywordId'):
            entry['keywordId'] = article['keywordId']
        
        published_articles['articles'].append(entry)
    
    # 日付でソート（新しい順）
    published_articles['articles'].sort(key=lambda x: x.get('date', ''), reverse=True)
    
    # 更新日時を設定
    published_articles['lastUpdated'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+09:00')
    
    return published_articles


def update_used_keywords(used_keywords, new_articles):
    """
    used_keywords.json を更新
    """
    for article in new_articles:
        keyword_id = article.get('keywordId')
        keyword = article.get('keyword', '')
        
        if not keyword:
            continue
        
        # used_keyword_ids に追加
        if keyword_id and keyword_id not in used_keywords.get('used_keyword_ids', []):
            used_keywords.setdefault('used_keyword_ids', []).append(keyword_id)
        
        # used_keyword_texts に追加
        if keyword and keyword not in used_keywords.get('used_keyword_texts', []):
            used_keywords.setdefault('used_keyword_texts', []).append(keyword)
        
        # keyword_usage_history に追加
        history_entry = {
            'keywordId': keyword_id,
            'keyword': keyword,
            'date': article['date'],
            'slug': article['slug']
        }
        
        # 重複チェック
        existing_slugs = [h.get('slug') for h in used_keywords.get('keyword_usage_history', [])]
        if article['slug'] not in existing_slugs:
            used_keywords.setdefault('keyword_usage_history', []).append(history_entry)
    
    # 更新日時を設定
    used_keywords['last_updated'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+09:00')
    
    return used_keywords


def generate_js_file(published_articles, js_file):
    """
    published_articles.js を生成
    """
    js_content = f"""// ブログ記事データ（ローカルファイルシステムでも動作するように、JavaScriptファイルとして提供）
// このファイルは published_articles.json と同じ内容を保持します
// ⚠️ このファイルは自動生成されます。手動で編集しないでください。
// 更新する場合は published_articles.json を編集し、scripts/sync_blog_data.py を実行してください。
window.BLOG_ARTICLES_DATA = {json.dumps(published_articles, ensure_ascii=False, indent=2)};
"""
    
    with open(js_file, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    return True


def sync_blog_data():
    """
    メインの同期処理
    """
    # スクリプトのディレクトリからプロジェクトルートを取得
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    blog_dir = project_root / 'blog'
    
    # ファイルパス
    published_json = blog_dir / 'published_articles.json'
    published_js = blog_dir / 'published_articles.js'
    used_keywords_json = blog_dir / 'used_keywords.json'
    keywords_json = blog_dir / 'keywords.json'
    
    # published_articles.json を読み込む
    try:
        with open(published_json, 'r', encoding='utf-8') as f:
            published_articles = json.load(f)
    except FileNotFoundError:
        print(f"⚠️ {published_json} が見つかりません。新規作成します。")
        published_articles = {'articles': [], 'lastUpdated': ''}
    except json.JSONDecodeError as e:
        print(f"❌ JSONデコードエラー: {e}")
        return False
    
    # used_keywords.json を読み込む
    try:
        with open(used_keywords_json, 'r', encoding='utf-8') as f:
            used_keywords = json.load(f)
    except FileNotFoundError:
        print(f"⚠️ {used_keywords_json} が見つかりません。新規作成します。")
        used_keywords = {
            'used_keyword_ids': [],
            'used_keyword_texts': [],
            'keyword_usage_history': []
        }
    except json.JSONDecodeError as e:
        print(f"❌ used_keywords.json JSONデコードエラー: {e}")
        return False
    
    # keywords.json を読み込む（キーワード情報検索用）
    try:
        with open(keywords_json, 'r', encoding='utf-8') as f:
            keywords_data = json.load(f)
    except FileNotFoundError:
        print(f"⚠️ {keywords_json} が見つかりません")
        keywords_data = {'keywords': []}
    except json.JSONDecodeError as e:
        print(f"⚠️ keywords.json JSONデコードエラー: {e}")
        keywords_data = {'keywords': []}
    
    # 新しい記事を検出
    new_articles = find_new_articles(blog_dir, published_articles, keywords_data)
    
    if new_articles:
        print(f"\n📝 {len(new_articles)}件の新しい記事を追加します")
        
        # published_articles.json を更新
        published_articles = update_published_articles(published_articles, new_articles)
        
        with open(published_json, 'w', encoding='utf-8') as f:
            json.dump(published_articles, f, ensure_ascii=False, indent=2)
        print(f"✅ {published_json} を更新しました")
        
        # used_keywords.json を更新
        used_keywords = update_used_keywords(used_keywords, new_articles)
        
        with open(used_keywords_json, 'w', encoding='utf-8') as f:
            json.dump(used_keywords, f, ensure_ascii=False, indent=2)
        print(f"✅ {used_keywords_json} を更新しました")
    else:
        print("📋 新しい記事はありません")
    
    # published_articles.js を生成
    try:
        generate_js_file(published_articles, published_js)
        print(f"✅ {published_js} を更新しました")
        print(f"📊 記事数: {len(published_articles.get('articles', []))}件")
        return True
    except Exception as e:
        print(f"❌ JSファイル書き込みエラー: {e}")
        return False


if __name__ == '__main__':
    print("=" * 50)
    print("ブログデータ同期スクリプト")
    print("=" * 50)
    print("\n🔄 ブログデータを同期しています...\n")
    
    success = sync_blog_data()
    
    print()
    if success:
        print("=" * 50)
        print("✅ 同期完了")
        print("=" * 50)
    else:
        print("=" * 50)
        print("❌ 同期失敗")
        print("=" * 50)
        exit(1)
