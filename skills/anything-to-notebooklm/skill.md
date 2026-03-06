---
name: anything-to-notebooklm
description: 'Upload content from any source to Google NotebookLM and generate podcasts, slide decks, mind maps, quizzes, reports, and more. Supports URLs (web pages, YouTube), local files (PDF, DOCX, PPTX, XLSX, EPUB, Markdown, images, audio, CSV, JSON, ZIP), and search keywords. Use when the user says: "上傳到 NotebookLM", "生成播客", "做成 PPT", "畫思維導圖", "generate podcast", "make slides", "create mind map", "upload to NotebookLM", "做成報告", "出題", "生成 Quiz".'
---

# 多源內容 → NotebookLM 處理器

從多種來源取得內容，上傳到 NotebookLM，根據指令生成播客、PPT、思維導圖等。

## 前置條件

- `notebooklm` CLI 已安裝（`pip install notebooklm-py`）
- `markitdown` 已安裝（`pip install markitdown`）— 用於本地檔案轉換
- 首次使用須執行 `notebooklm login`（開瀏覽器登入 Google 帳號）

## 工作流程

### Step 1: 識別內容源

| 輸入特徵 | 類型 | 處理方式 |
|---------|------|---------|
| `https://youtube.com/...` 或 `https://youtu.be/...` | YouTube | 直接 `source add URL` |
| `https://` 或 `http://` | 網頁 | 直接 `source add URL` |
| 本地 `.pdf/.docx/.pptx/.xlsx/.epub` | Office/電子書 | `markitdown` 轉 Markdown → `source add` |
| 本地 `.md` | Markdown | 直接 `source add` |
| 本地圖片 `.jpg/.png` | 圖片 | `markitdown` OCR → `source add` |
| 本地音訊 `.mp3/.wav` | 音訊 | `markitdown` 轉錄 → `source add` |
| 本地 `.zip` | 壓縮包 | 解壓 → 批量 `markitdown` → `source add` |
| 關鍵詞（無 URL、無路徑） | 搜尋 | WebSearch → 彙總為 TXT → `source add` |

### Step 2: 取得內容並上傳

**URL（網頁/YouTube）**：直接傳給 NotebookLM。

```bash
notebooklm create "筆記本標題"
notebooklm source add "URL" --wait
```

**本地檔案**：先用 markitdown 轉換。

```bash
markitdown "filepath" -o "$TEMP/converted.md"
notebooklm source add "$TEMP/converted.md" --wait
```

**搜尋關鍵詞**：用 WebSearch 搜尋，彙總前 3-5 條結果存為 TXT，再上傳。

**重要**：`source add` 一定要加 `--wait`，等處理完才能生成。

### Step 3: 根據意圖生成內容

| 用戶說的話 | 意圖 | 指令 |
|-----------|------|------|
| 生成播客 / 做成音頻 | audio | `generate audio` → `download audio ./output.wav` |
| 做成 PPT / 生成幻燈片 | slide-deck | `generate slide-deck` → `download slide-deck ./output.pdf` |
| 畫思維導圖 / 生成腦圖 | mind-map | `generate mind-map` → `download mind-map ./map.json` |
| 生成 Quiz / 出題 | quiz | `generate quiz` → `download quiz ./quiz.md --format markdown` |
| 做個視頻 | video | `generate video` → `download video ./output.mp4` |
| 生成報告 / 寫總結 | report | `generate report` → `download report ./report.md` |
| 做信息圖 | infographic | `generate infographic` → `download infographic ./output.png` |
| 做閃卡 / 記憶卡片 | flashcards | `generate flashcards` → `download flashcards ./cards.md --format markdown` |
| 做數據表 | data-table | `generate data-table` → `download data-table ./table.csv` |

**生成流程**：
1. `notebooklm generate <type>` — 發起生成（返回 task）
2. `notebooklm artifact wait` — 等待完成
3. `notebooklm download <type> ./output` — 下載到本地
4. 告知用戶檔案路徑

如果用戶沒指定生成什麼，**只上傳不生成**，等待後續指令。

## 進階用法

**多源合併**：一個 notebook 可加多個 source（最多 50 個），全部加完再生成。

**指定已有 notebook**：用戶說「加到我的 XXX 筆記本」→ `notebooklm list` 找到後 `notebooklm use <id>` → 再 `source add`。

**自訂生成指令**：用戶的額外要求（如「輕鬆幽默風格」）作為 instructions 傳給 generate 指令。

## 注意事項

- 每次請求間隔 > 2 秒，避免被限流
- NotebookLM 生成任務最多 3 個同時進行
- 內容太短（< 100 字）效果差，太長（> 50 萬字）可能超時
- Windows 中文檔名加 `PYTHONUTF8=1` 前綴
- 僅用於個人學習研究，遵守版權規定

## 參考資料

- **使用範例**：見 [references/examples.md](references/examples.md)
- **故障排查**：見 [references/troubleshooting.md](references/troubleshooting.md)
