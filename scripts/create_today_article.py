#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
今日のブログ記事を自動生成するスクリプト

使い方:
    python3 scripts/create_today_article.py

実行内容:
1. keywords.jsonから配分比率に基づいてランダム選択
2. 未使用キーワードから選択（厳密な重複チェック付き）
3. 選択したキーワード情報を出力
4. AIに記事生成を依頼（このスクリプトは情報提供のみ）

重複防止機能:
- keywordIdベースの厳密な重複チェック
- keywordテキストベースの重複チェック（古い記事対応）
- used_keywords.jsonで使用済みキーワードを管理
"""

import json
import random
import sys
from pathlib import Path
from datetime import datetime

# プロジェクトルート
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
BLOG_DIR = PROJECT_ROOT / "blog"
USED_KEYWORDS_FILE = BLOG_DIR / "used_keywords.json"

# カテゴリ別の配分比率
CATEGORY_WEIGHTS = {
    "A": 25,  # 新規制作案件向け
    "B": 25,  # 保守・サブスク案件向け
    "C": 20,  # 課題解決型
    "D": 15,  # 用語解説
    "E": 15   # 補助金情報
}


def load_keywords():
    """keywords.jsonを読み込む"""
    keywords_file = BLOG_DIR / "keywords.json"
    with open(keywords_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data["categories"], data["keywords"]


def load_published_articles():
    """published_articles.jsonを読み込む"""
    articles_file = BLOG_DIR / "published_articles.json"
    with open(articles_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get("articles", [])


def load_used_keywords():
    """used_keywords.jsonを読み込む"""
    if not USED_KEYWORDS_FILE.exists():
        return {"used_keyword_ids": [], "used_keyword_texts": [], "last_updated": None}
    
    try:
        with open(USED_KEYWORDS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, Exception) as e:
        print(f"⚠️  used_keywords.json の読み込みエラー: {e}")
        return {"used_keyword_ids": [], "used_keyword_texts": [], "last_updated": None}


def save_used_keywords(data):
    """used_keywords.jsonを保存する"""
    data["last_updated"] = datetime.now().isoformat()
    
    with open(USED_KEYWORDS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ used_keywords.json を更新しました")


def build_used_keywords_from_articles():
    """
    published_articles.jsonから使用済みキーワード情報を構築
    （初回実行時やデータ修復時に使用）
    """
    articles = load_published_articles()
    
    used_keyword_ids = set()
    used_keyword_texts = set()
    
    for article in articles:
        # keywordIdがある場合
        if "keywordId" in article:
            used_keyword_ids.add(article["keywordId"])
        
        # keywordテキストがある場合
        if "keyword" in article:
            used_keyword_texts.add(article["keyword"])
    
    return {
        "used_keyword_ids": sorted(list(used_keyword_ids)),
        "used_keyword_texts": sorted(list(used_keyword_texts)),
        "last_updated": datetime.now().isoformat()
    }


def get_used_keyword_data():
    """
    使用済みキーワードのデータを取得
    used_keywords.jsonとpublished_articles.jsonの両方をマージ
    """
    # used_keywords.jsonを読み込み
    used_keywords = load_used_keywords()
    
    # published_articles.jsonからも取得してマージ
    articles = load_published_articles()
    
    used_ids = set(used_keywords.get("used_keyword_ids", []))
    used_texts = set(used_keywords.get("used_keyword_texts", []))
    
    for article in articles:
        if "keywordId" in article:
            used_ids.add(article["keywordId"])
        if "keyword" in article:
            used_texts.add(article["keyword"])
    
    return used_ids, used_texts


def is_keyword_used(keyword, used_ids, used_texts):
    """
    キーワードが既に使用済みかどうかをチェック
    
    Args:
        keyword: チェック対象のキーワード辞書
        used_ids: 使用済みkeywordIdのセット
        used_texts: 使用済みkeywordテキストのセット
    
    Returns:
        (is_used, reason) - 使用済みの場合True、理由の説明文
    """
    keyword_id = keyword.get("id")
    keyword_text = keyword.get("keyword", "")
    
    # 1. keywordIdでチェック（最優先）
    if keyword_id in used_ids:
        return True, f"keywordId {keyword_id} は既に使用されています"
    
    # 2. keywordテキストでチェック
    if keyword_text in used_texts:
        return True, f"キーワード '{keyword_text}' は既に使用されています"
    
    return False, ""


def register_used_keyword(keyword):
    """
    使用したキーワードを登録
    
    Args:
        keyword: 使用するキーワード辞書
    """
    used_keywords = load_used_keywords()
    
    keyword_id = keyword.get("id")
    keyword_text = keyword.get("keyword", "")
    
    # IDを追加
    if keyword_id and keyword_id not in used_keywords.get("used_keyword_ids", []):
        if "used_keyword_ids" not in used_keywords:
            used_keywords["used_keyword_ids"] = []
        used_keywords["used_keyword_ids"].append(keyword_id)
    
    # テキストを追加
    if keyword_text and keyword_text not in used_keywords.get("used_keyword_texts", []):
        if "used_keyword_texts" not in used_keywords:
            used_keywords["used_keyword_texts"] = []
        used_keywords["used_keyword_texts"].append(keyword_text)
    
    save_used_keywords(used_keywords)


def select_keyword_by_weight(categories, keywords, used_ids, used_texts):
    """
    配分比率に基づいてキーワードを選択（厳密な重複チェック付き）
    
    Args:
        categories: カテゴリ辞書
        keywords: キーワードリスト
        used_ids: 使用済みkeywordIdのセット
        used_texts: 使用済みkeywordテキストのセット
    
    Returns:
        選択されたキーワード辞書、またはNone
    """
    # 未使用キーワードをカテゴリ別に分類
    available_by_category = {cat: [] for cat in CATEGORY_WEIGHTS.keys()}
    
    for kw in keywords:
        is_used, _ = is_keyword_used(kw, used_ids, used_texts)
        if not is_used:
            category = kw["category"]
            if category in available_by_category:
                available_by_category[category].append(kw)
    
    # 各カテゴリの未使用キーワード数を表示
    print("\n📊 カテゴリ別未使用キーワード数:")
    total_available = 0
    for cat, kw_list in available_by_category.items():
        cat_name = categories.get(cat, cat)
        print(f"  {cat} ({cat_name}): {len(kw_list)}個")
        total_available += len(kw_list)
    
    print(f"\n📊 合計未使用キーワード: {total_available}個")
    print(f"📊 使用済みキーワードID数: {len(used_ids)}個")
    print(f"📊 使用済みキーワードテキスト数: {len(used_texts)}個")
    
    # 利用可能なキーワードがない場合
    if total_available == 0:
        print("\n❌ 利用可能な未使用キーワードがありません")
        return None
    
    # 重み付けリストを作成
    weighted_pool = []
    for category, weight in CATEGORY_WEIGHTS.items():
        category_keywords = available_by_category.get(category, [])
        if category_keywords:
            for kw in category_keywords:
                weighted_pool.extend([kw] * weight)
    
    if not weighted_pool:
        print("\n❌ 選択可能なキーワードがありません")
        return None
    
    # ランダムに選択
    selected_kw = random.choice(weighted_pool)
    
    return selected_kw


def generate_slug(keyword, date_str):
    """
    スラッグを生成
    
    Args:
        keyword: キーワード辞書
        date_str: 日付文字列（YYYY-MM-DD）
    
    Returns:
        スラッグ文字列
    """
    keyword_text = keyword["keyword"].lower()
    
    # 簡易的な変換マッピング
    slug_map = {
        "ホームページ": "website",
        "制作": "creation",
        "保守": "maintenance",
        "運用": "operation",
        "費用": "cost",
        "相場": "price",
        "埼玉": "saitama",
        "戸田市": "toda",
        "中小企業": "sme",
        "補助金": "subsidy",
        "申請": "application",
        "活用": "utilization",
        ".htaccess": "htaccess",
        "ssl": "ssl",
        "証明書": "certificate",
        "wordpress": "wordpress",
        "seo": "seo",
        "対策": "strategy",
        "とは": "what-is",
        "初心者": "beginner",
        "使い方": "how-to-use",
        "解説": "explanation",
        "わかりやすく": "explained",
        "it導入補助金": "it-subsidy",
        "小規模事業者": "small-business",
        "持続化補助金": "sustainability-subsidy",
        "ものづくり": "manufacturing",
        "事業再構築": "business-restructuring",
        "デジタル化": "digitalization",
        "dx": "dx",
        "推進": "promotion",
        "サーチコンソール": "search-console",
        "アナリティクス": "analytics",
        "ドメイン": "domain",
        "サーバー": "server",
        "レスポンシブ": "responsive",
        "デザイン": "design",
        "cms": "cms",
        "プラグイン": "plugin",
        "キャッシュ": "cache",
        "リダイレクト": "redirect",
        "バックアップ": "backup",
        "meo": "meo",
        "google": "google",
        "ビジネス": "business",
        "プロフィール": "profile",
        "sns": "sns",
        "連携": "integration",
        "コンテンツ": "content",
        "マーケティング": "marketing",
        "問い合わせ": "inquiry",
        "増やす": "increase",
        "リニューアル": "renewal",
        "納期": "deadline",
        "見積もり": "estimate",
        "選び方": "selection",
        "格安": "budget",
        "採用": "recruitment",
        "店舗": "store",
        "士業": "professional",
        "医療": "medical",
        "クリニック": "clinic",
        "飲食店": "restaurant",
        "美容室": "salon",
        "不動産": "realestate",
        "btob": "btob",
        "トレンド": "trend",
        "素材": "material",
        "準備": "preparation",
        "フリーランス": "freelance",
        "丸投げ": "outsource",
        "月額": "monthly",
        "セキュリティ": "security",
        "更新": "update",
        "バックアップ": "backup",
        "サイト": "site",
        "改善": "improvement",
        "pdca": "pdca",
        "コスト": "cost",
        "削減": "reduction",
        "契約": "contract",
        "引き継ぎ": "handover",
        "トラブル": "trouble",
        "緊急": "emergency",
        "監視": "monitoring",
        "放置": "neglect",
        "リスク": "risk",
        "ハッキング": "hacking",
        "改ざん": "tampering",
        "復旧": "recovery",
        "古い": "old",
        "スマホ": "mobile",
        "非対応": "incompatible",
        "検索": "search",
        "集客": "marketing",
        "離脱率": "bounce-rate",
        "直帰率": "exit-rate",
        "効果測定": "analytics",
        "競合": "competitor",
    }
    
    slug_parts = []
    for jp, en in slug_map.items():
        if jp in keyword_text:
            if en not in slug_parts:  # 重複を避ける
                slug_parts.append(en)
    
    # スラッグが生成できなかった場合はデフォルト
    if not slug_parts:
        slug_parts = ["article"]
    
    slug = "-".join(slug_parts[:4])  # 最大4単語
    return f"{date_str}-{slug}"


def display_selected_keyword(keyword, categories):
    """選択されたキーワード情報を表示"""
    category_name = categories.get(keyword["category"], keyword["category"])
    
    print("\n" + "="*60)
    print("🎯 本日の記事キーワードが選択されました")
    print("="*60)
    print(f"\n📌 キーワードID: {keyword['id']}")
    print(f"📁 カテゴリ: {keyword['category']} ({category_name})")
    print(f"🔑 キーワード: {keyword['keyword']}")
    print(f"📝 テーマ: {keyword['theme']}")
    print(f"\n📅 日付: {datetime.now().strftime('%Y年%m月%d日')}")
    
    # スラッグを生成
    date_str = datetime.now().strftime('%Y-%m-%d')
    slug = generate_slug(keyword, date_str)
    print(f"🔗 スラッグ: {slug}")
    
    print("\n" + "="*60)
    print("📋 記事生成のための情報")
    print("="*60)
    
    # カテゴリ別のガイドライン
    guidelines = {
        "A": "費用、選び方、事例を中心に",
        "B": "必要性、リスク、月額メリットを強調",
        "C": "問題提起と具体的な解決策を提示",
        "D": "技術用語の分かりやすい解説、実務での使い方を説明",
        "E": "申請方法、活用事例、注意点を具体的に"
    }
    
    print(f"\n💡 カテゴリ別ガイドライン: {guidelines.get(keyword['category'], '')}")
    print("\n✅ 記事作成の必須要件:")
    print("  - 文字数: 2500-3500字")
    print("  - h2見出し: 3-5個")
    print("  - 内部リンク: /#service, /#pricing, /#contact")
    print("  - ミアキス代表の経験談や自社事例を含める")
    print("  - 埼玉県・戸田市の地域文脈を入れる")
    print("  - 具体的な数字や独自見解を含める")
    print("  - Q&A形式や会話調で自然な語り口")
    print("\n" + "="*60)
    
    return {
        "id": keyword["id"],
        "category": keyword["category"],
        "category_name": category_name,
        "keyword": keyword["keyword"],
        "theme": keyword["theme"],
        "slug": slug,
        "date": date_str
    }


def sync_used_keywords():
    """
    used_keywords.jsonをpublished_articles.jsonから再構築
    （データ修復用）
    """
    print("🔄 used_keywords.json を再構築中...")
    data = build_used_keywords_from_articles()
    save_used_keywords(data)
    print(f"✅ 再構築完了: {len(data['used_keyword_ids'])}個のID、{len(data['used_keyword_texts'])}個のテキスト")
    return data


def main():
    """メイン処理"""
    print("\n🚀 ブログ記事自動生成ワークフローを開始します\n")
    
    # キーワードを読み込み
    print("📂 keywords.jsonを読み込み中...")
    categories, keywords = load_keywords()
    print(f"✅ {len(keywords)}個のキーワードを読み込みました")
    
    # 記事を読み込み
    print("📂 published_articles.jsonを読み込み中...")
    articles = load_published_articles()
    print(f"✅ {len(articles)}個の公開済み記事を確認しました")
    
    # used_keywords.jsonが存在しない場合は再構築
    if not USED_KEYWORDS_FILE.exists():
        print("\n⚠️  used_keywords.json が見つかりません。再構築します...")
        sync_used_keywords()
    
    # 使用済みキーワードデータを取得
    used_ids, used_texts = get_used_keyword_data()
    
    # キーワードを選択（厳密な重複チェック付き）
    print("\n🎲 配分比率に基づいてキーワードを選択中（厳密な重複チェック付き）...")
    print(f"   配分: A={CATEGORY_WEIGHTS['A']}%, B={CATEGORY_WEIGHTS['B']}%, "
          f"C={CATEGORY_WEIGHTS['C']}%, D={CATEGORY_WEIGHTS['D']}%, E={CATEGORY_WEIGHTS['E']}%")
    
    selected = select_keyword_by_weight(categories, keywords, used_ids, used_texts)
    
    if not selected:
        print("\n❌ キーワードの選択に失敗しました")
        sys.exit(1)
    
    # 選択されたキーワード情報を表示
    info = display_selected_keyword(selected, categories)
    
    # JSON形式で情報を出力（AIが読み取りやすいように）
    print("\n📤 記事情報（JSON形式）:")
    print(json.dumps(info, ensure_ascii=False, indent=2))
    
    print("\n✅ キーワード選択完了")
    print("\n💬 次のステップ:")
    print("  1. 上記のキーワード・テーマで記事HTMLを生成してください")
    print("  2. 画像を取得します（自動）")
    print("  3. published_articles.jsonを更新します（自動）")
    print("  4. used_keywords.jsonを更新します（自動）")
    print("  5. デプロイします（自動）")
    print("\n" + "="*60)
    
    return info


if __name__ == "__main__":
    # コマンドライン引数で同期モードを指定可能
    if len(sys.argv) > 1 and sys.argv[1] == "--sync":
        sync_used_keywords()
        sys.exit(0)
    
    try:
        info = main()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
