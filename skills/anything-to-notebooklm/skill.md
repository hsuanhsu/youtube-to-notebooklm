---
name: anything-to-notebooklm
description: 'Upload content from any source to Google NotebookLM and generate podcasts, slide decks, mind maps, quizzes, reports, and more. Supports URLs (web pages, YouTube), local files (PDF, DOCX, PPTX, XLSX, EPUB, Markdown, images, audio, CSV, JSON, ZIP), AI research search, and Google Drive files. Use when the user says: "上傳到 NotebookLM", "生成播客", "做成 PPT", "畫思維導圖", "generate podcast", "make slides", "create mind map", "upload to NotebookLM", "做成報告", "出題", "生成 Quiz", "turn this into a podcast", "summarize this as slides", "把這個做成播客", "幫我整理成報告", "ask NotebookLM", "問筆記本". Make sure to use this skill whenever the user wants to push any content to NotebookLM, generate audio/visual outputs from documents, ask questions about uploaded content, or convert content into study materials — even if they don''t explicitly mention NotebookLM.'
---

# 多源內容 → NotebookLM 處理器

從多種來源取得內容，上傳到 NotebookLM，生成播客、PPT、思維導圖等。

依賴：`notebooklm-py`（CLI）、`markitdown`（本地檔案轉換）。首次使用須 `notebooklm login`。

## Step 1: 識別內容源

| 輸入特徵 | 處理方式 |
|---------|---------|
| YouTube URL | 直接 `source add URL --wait` |
| 網頁 URL | 直接 `source add URL --wait` |
| Google Drive 文件 | `source add-drive <file_id> "title"` |
| 本地 `.pdf/.docx/.md/.csv/.txt` | 直接 `source add "filepath" --wait` |
| 本地 `.pptx/.xlsx/.epub` | `markitdown "file" -o "$TEMP/converted.md"` → `source add` |
| 本地圖片/音訊 | 直接 `source add "filepath" --wait`（自動 OCR/轉錄）|
| 純關鍵詞（無 URL 無路徑） | `source add-research "query"`（見下方） |

## Step 2: 上傳

```bash
notebooklm create "筆記本標題"
notebooklm source add "來源" --wait    # --wait 必加
```

多源合併：一個 notebook 最多 50 個 source，全部 `source add --wait` 完再生成。

**上傳前確認**：推送到 NotebookLM 會建立新 notebook，操作前告知用戶即將建立的 notebook 名稱，確認後再執行。

## Step 3: 生成

所有生成指令都支援 `--wait`（等待完成）、`--retry N`（自動重試）、`-s <source_id>`（僅用指定來源）。

| 用戶意圖 | 指令 | 下載 |
|---------|------|------|
| 播客/音頻 | `generate audio --wait` | `download audio ./output.wav` |
| PPT/幻燈片 | `generate slide-deck --wait` | `download slide-deck ./output.pdf` |
| 思維導圖 | `generate mind-map` | `download mind-map ./map.json` |
| Quiz/出題 | `generate quiz --wait` | `download quiz ./quiz.md --format markdown` |
| 報告/總結 | `generate report --wait` | `download report ./report.md` |
| 視頻 | `generate video --wait` | `download video ./output.mp4` |
| 信息圖 | `generate infographic --wait` | `download infographic ./output.png` |
| 閃卡 | `generate flashcards --wait` | `download flashcards ./cards.md --format markdown` |
| 數據表 | `generate data-table "description" --wait` | `download data-table ./table.csv` |

用戶沒指定生成什麼 → 只上傳不生成，等後續指令。

### 生成格式選項

用戶有風格偏好時，用這些參數：

**Audio 播客：**
- `--format deep-dive`（預設深度對談）/ `brief`（簡短摘要）/ `critique`（批評分析）/ `debate`（辯論）
- `--length short` / `default` / `long`

**Video 影片：**
- `--format explainer`（解說）/ `brief`（簡短）
- `--style auto` / `classic` / `whiteboard` / `kawaii` / `anime` / `watercolor` / `retro` / `heritage` / `paper-craft`

**Slide Deck 簡報：**
- `--format detailed` / `presenter`
- 下載可選 `--format pdf`（預設）或 `--format pptx`（可編輯的 PowerPoint）

**Report 報告：**
- `--format briefing-doc` / `study-guide` / `blog-post` / `custom`
- `--append "額外指示"` 附加自訂要求

**Quiz / Flashcards：**
- `--difficulty easy` / `medium` / `hard`
- `--quantity fewer` / `standard` / `more`
- 下載可選 `--format json`（預設）/ `markdown` / `html`

**Infographic 信息圖：**
- `--orientation landscape` / `portrait` / `square`
- `--detail concise` / `standard` / `detailed`

用戶的額外要求（如「輕鬆幽默風格」「用繁體中文」）作為 description 傳給 generate 指令。

### 修改單一投影片

生成簡報後用戶要修改某一頁：

```bash
notebooklm generate revise-slide "修改要求" --artifact <id> --slide 3 --wait
```

## AI 研究搜尋

用戶給的是純關鍵詞（不是 URL 也不是檔案），用 NotebookLM 內建的研究功能，不需要手動 WebSearch：

```bash
notebooklm source add-research "query" --mode deep --from web --import-all
```

- `--mode fast`（快速）/ `deep`（深度，較慢但更全面）
- `--from web`（網路搜尋）/ `drive`（Google Drive）
- `--import-all` 自動匯入找到的所有來源
- `--no-wait` 背景執行（用 `research status` 查進度，`research wait` 等待）

## 對來源提問

上傳完來源後，用戶可以直接提問：

```bash
notebooklm ask "問題內容"
notebooklm ask "問題" -s <source_id>        # 僅針對特定來源
notebooklm ask "問題" --save-as-note         # 答案存為筆記
```

## 語言設定

生成非英文內容前，設定 NotebookLM 語言：

```bash
notebooklm language set zh_Hant    # 繁體中文
notebooklm language set ja         # 日文
```

也可在個別指令加 `--language zh_Hant`。

## 與 yt-search 的銜接

用戶搜影片後選定一部，想推送到 NotebookLM 時：直接用影片 URL 做 `source add`，NotebookLM 原生支援 YouTube URL。

如果用戶已經用 yt-search 抓了字幕並存為文字檔，也可以直接 `source add` 該文字檔。

## 進階用法

- **指定已有 notebook**：`notebooklm list` → `notebooklm use <id>` → `source add`
- **重新命名**：`notebooklm rename "新名稱"`
- **分享**：`notebooklm share public --enable` 或 `notebooklm share add user@email.com`
- **來源全文**：`notebooklm source fulltext <id>` 取得完整索引文本
- **來源摘要**：`notebooklm source guide <id>` 取得 AI 摘要
- **認證問題**：`notebooklm auth check --test` 診斷

## 暫存檔清理

生成完成、用戶確認收到輸出後，清理暫存檔：

```bash
rm -f "$TEMP"/converted.md
```

## 注意事項

- 每次請求間隔 > 2 秒，避免被限流
- 生成任務最多 3 個同時進行
- 內容太短（< 100 字）效果差，太長（> 50 萬字）可能超時
- Windows 中文檔名 → 指令前加 `PYTHONUTF8=1`

## 參考資料

- **使用範例**：見 [references/examples.md](references/examples.md)
- **故障排查**：見 [references/troubleshooting.md](references/troubleshooting.md)
