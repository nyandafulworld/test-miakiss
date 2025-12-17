#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ブログ記事をGitHub経由でデプロイするスクリプト

使い方:
    python3 scripts/deploy_article.py <slug> "<commit_message>"
    
例:
    python3 scripts/deploy_article.py "2025-12-17-analytics" "Add new blog article: Googleアナリティクス"

実行内容:
1. 記事関連ファイルをgit add
2. git commit
3. git push（GitHub Actions経由でFTPデプロイ）
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime

# プロジェクトルート
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent


def run_command(cmd, description):
    """
    シェルコマンドを実行
    
    Args:
        cmd: 実行するコマンド（リスト）
        description: コマンドの説明
    
    Returns:
        成功時True、失敗時False
    """
    try:
        print(f"🔄 {description}...")
        result = subprocess.run(
            cmd,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True
        )
        if result.stdout:
            print(result.stdout.strip())
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ エラー: {description}が失敗しました")
        if e.stderr:
            print(e.stderr)
        return False


def deploy_article(slug, commit_message=None):
    """
    記事をデプロイ
    
    Args:
        slug: 記事のスラッグ（例: 2025-12-17-analytics）
        commit_message: コミットメッセージ（オプション）
    
    Returns:
        成功時True、失敗時False
    """
    print(f"\n🚀 記事デプロイを開始: {slug}\n")
    
    # デフォルトのコミットメッセージ
    if not commit_message:
        date = datetime.now().strftime("%Y-%m-%d")
        commit_message = f"Add new blog article ({date})"
    
    # 1. git add（記事関連ファイル）
    files_to_add = [
        f"blog/{slug}.html",
        f"blog/images/{slug}_header.jpg",
        f"blog/images/{slug}_thumbnail.jpg",
        "blog/published_articles.json",
        "blog/used_images.json",
        "sitemap.xml"
    ]
    
    # 存在するファイルのみadd
    existing_files = []
    for file in files_to_add:
        file_path = PROJECT_ROOT / file
        if file_path.exists():
            existing_files.append(file)
        else:
            print(f"⚠️  ファイルが見つかりません（スキップ）: {file}")
    
    if not existing_files:
        print("❌ addするファイルがありません")
        return False
    
    # git add
    if not run_command(
        ["git", "add"] + existing_files,
        "ファイルをステージング"
    ):
        return False
    
    # 2. git commit
    if not run_command(
        ["git", "commit", "-m", commit_message],
        "変更をコミット"
    ):
        # コミットするものがない場合は警告のみ
        print("⚠️  コミットするものがないか、既にコミット済みです")
    
    # 3. git push
    if not run_command(
        ["git", "push", "origin", "master"],
        "GitHubにプッシュ"
    ):
        return False
    
    print("\n" + "="*60)
    print("✅ デプロイ完了！")
    print("="*60)
    print("\n📦 GitHub Actionsが自動的に起動し、FTPデプロイが開始されます")
    print("⏱️  1-2分後にサイトに反映されます")
    print(f"🔗 URL: https://www.miakiss.co.jp/blog/{slug}.html")
    print("\n" + "="*60)
    
    return True


def main():
    """メイン処理"""
    if len(sys.argv) < 2:
        print("使用方法: python3 scripts/deploy_article.py <slug> [<commit_message>]")
        print('例: python3 scripts/deploy_article.py "2025-12-17-analytics" "Add analytics article"')
        sys.exit(1)
    
    slug = sys.argv[1]
    commit_message = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = deploy_article(slug, commit_message)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

