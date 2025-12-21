# Calches記事の画像追加手順

## 完了したこと ✅

- ✅ Calches記事を新デザインテンプレートで更新
- ✅ 目次・関連記事機能を追加
- ✅ 画像表示エリアを追加（フォールバック対応済み）

## 次のステップ：画像の追加

添付画像（旅行アイテムの写真）をブログに追加する手順です。

---

## 手順1: 添付画像をダウンロード

チャットに添付されている画像（パスポート・スマホ・変換プラグの写真）を以下の場所に保存してください：

```
/Users/game_gct/Miakiss_Web/blog/images/calches-original.jpg
```

### 方法（Cursor AIから画像をダウンロード）:

1. チャット内の画像を右クリック
2. 「画像を保存」を選択
3. ファイル名を `calches-original.jpg` にして保存
4. 保存先: `/Users/game_gct/Miakiss_Web/blog/images/`

---

## 手順2: 画像をリサイズ

ターミナルで以下のコマンドを実行：

```bash
cd /Users/game_gct/Miakiss_Web

# 画像をリサイズ（サムネイル800px + ヘッダー1200px）
python3 scripts/resize_and_save_image.py \
  blog/images/calches-original.jpg \
  calches-travel-adapter-story
```

### 生成されるファイル:

```
blog/images/calches-travel-adapter-story_thumbnail.jpg  # 800px（一覧ページ用）
blog/images/calches-travel-adapter-story_header.jpg     # 1200px（記事ヘッダー用）
```

---

## 手順3: 表示確認

ローカルサーバーで確認：

```bash
cd /Users/game_gct/Miakiss_Web
python3 test_server.py
```

ブラウザで開く：
- http://localhost:8000/blog/calches-travel-adapter-story.html

### 確認ポイント:
- [ ] ヘッダー画像が表示されているか
- [ ] デザインが新テンプレート（左揃えタイトル、蛍光ペン強調）になっているか
- [ ] 目次が自動生成されているか
- [ ] 関連記事が表示されているか

---

## 代替方法：手動でリサイズ

Pythonスクリプトが使えない場合、画像編集ソフトで手動リサイズ：

### サムネイル画像:
- 幅: 800px
- 形式: JPEG
- 品質: 85%
- ファイル名: `calches-travel-adapter-story_thumbnail.jpg`
- 保存先: `blog/images/`

### ヘッダー画像:
- 幅: 1200px
- 形式: JPEG
- 品質: 85%
- ファイル名: `calches-travel-adapter-story_header.jpg`
- 保存先: `blog/images/`

---

## トラブルシューティング

### 画像が表示されない

1. ファイル名が正しいか確認：
   ```bash
   ls -la blog/images/ | grep calches
   ```

2. ファイルが存在すれば以下が表示されるはず：
   ```
   calches-travel-adapter-story_thumbnail.jpg
   calches-travel-adapter-story_header.jpg
   ```

3. 画像がない場合でもエラーにならない（フォールバック機能）

---

## まとめ

### 更新内容

**デザイン改善（完了）:**
- ✅ タイトルを左揃えに変更
- ✅ 強調色を蛍光ペン風ハイライトに変更  
- ✅ h2見出しをモダンデザインに
- ✅ 目次の自動生成
- ✅ 関連記事3件表示

**画像（次のステップ）:**
- ⏳ 添付画像をダウンロード
- ⏳ リサイズスクリプトを実行
- ⏳ 表示確認

---

添付画像を保存してリサイズすれば、Calches記事も他の記事と同じく美しいデザインで表示されます！ 🎉

























