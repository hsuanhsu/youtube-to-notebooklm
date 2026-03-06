---
name: yt-search
description: Search YouTube videos, get video metadata, and download subtitles/transcripts using yt-dlp. Use when the user wants to find videos, search YouTube, look up a YouTube channel, get video info, download captions, grab subtitles, or extract a transcript. Triggers include "找影片", "搜影片", "YouTube 搜尋", "抓字幕", "逐字稿", "search videos", "find videos on YouTube", "get subtitles", "video transcript".
---

# yt-search

用 yt-dlp 搜尋 YouTube 影片、取得元數據、下載字幕。

## 前置條件

- `yt-dlp` 已安裝（`pip install yt-dlp`）

## 能力一覽

### 1. 搜尋影片

```bash
yt-dlp --flat-playlist "ytsearchN:關鍵字" -j
```

- `N` = 搜尋數量（預設 10，最多建議 20）
- 每行輸出一個 JSON 物件，解析需要的欄位：

| 欄位 | 用途 |
|------|------|
| `title` | 影片標題 |
| `channel` | 頻道名 |
| `duration` | 秒數（換算成 mm:ss 顯示） |
| `view_count` | 觀看數 |
| `url` | 影片 URL |
| `id` | 影片 ID |

**呈現格式**（給用戶看）：

```
# | 標題 | 頻道 | 時長 | 觀看數 | URL
1 | How to Make... | FoodBiz | 12:34 | 45K | https://youtube.com/watch?v=xxx
```

### 2. 取得影片元數據

```bash
yt-dlp -j "URL"
```

常用欄位：`title`, `channel`, `upload_date`, `view_count`, `like_count`, `description`, `duration`, `categories`, `tags`

### 3. 下載字幕／逐字稿

下載 VTT 字幕檔（不需要 ffmpeg）：

```bash
yt-dlp --skip-download --write-auto-subs --sub-lang en -o "%(id)s" "URL"
```

- `--skip-download`：不下載影片，只要字幕
- `--write-auto-subs`：包含自動生成字幕
- `--sub-lang zh,en`：優先中文，其次英文（可調整）
- 輸出檔案：`{id}.{lang}.vtt`

VTT 轉純文字（去時間碼、去重複行）：

```python
import re, os
vtt_path = os.path.join(os.environ.get('TEMP', '/tmp'), "VIDEO_ID.en.vtt")
with open(vtt_path, "r", encoding="utf-8") as f:
    content = f.read()
lines = content.split("\n")
seen, text = set(), []
for line in lines:
    line = line.strip()
    if not line or line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:"):
        continue
    if re.match(r"^\d{2}:\d{2}", line) or "-->" in line:
        continue
    clean = re.sub(r"<[^>]+>", "", line)
    if clean and clean not in seen:
        seen.add(clean)
        text.append(clean)
transcript = " ".join(text)
```

### 4. 搜尋 + 篩選工作流

當用戶說「幫我找 XXX 的影片」時：

1. 用 `ytsearch20` 搜尋 20 部
2. 解析 JSON，按觀看數排序
3. 列表呈現，讓用戶挑選
4. 用戶挑選後，可進一步：
   - 取元數據（`yt-dlp -j`）
   - 抓字幕
   - 推送到 NotebookLM（如果有 anything-to-notebooklm skill）

## 注意事項

- Windows 環境下中文輸出可能有編碼問題，加 `PYTHONUTF8=1` 前綴
- `--flat-playlist` 只取元數據不下載，速度快
- 搜尋結果受 YouTube 地區/語言影響，可加 `--geo-bypass`
- 長影片字幕檔可能很大，建議先確認時長再決定是否下載
