---
name: yt-search
description: Search YouTube videos, get video metadata, and download subtitles/transcripts using yt-dlp. Use when the user wants to find videos, search YouTube, look up a YouTube channel, get video info, download captions, grab subtitles, or extract a transcript. Triggers include "找影片", "搜影片", "YouTube 搜尋", "抓字幕", "逐字稿", "search videos", "find videos on YouTube", "get subtitles", "video transcript", "youtube tutorial", "watch video about", "影片推薦", "有沒有影片", "教學影片". Make sure to use this skill whenever the user mentions YouTube, video search, subtitles, or transcripts — even if they don't explicitly say "yt-search".
---

# yt-search

YouTube 影片搜尋、元數據查詢、字幕下載。依賴 `yt-dlp`（`pip install yt-dlp`）。

## 搜尋影片

```bash
yt-dlp --flat-playlist "ytsearchN:關鍵字" -j
```

`N` = 結果數（預設 10，建議最多 20）。每行一個 JSON，取 `title`、`channel`、`duration_string`、`view_count`、`url`、`id`。

呈現為表格讓用戶挑選（按觀看數排序）：

```
# | 標題 | 頻道 | 時長 | 觀看數 | URL
1 | How to Make... | FoodBiz | 12:34 | 45K | https://youtube.com/watch?v=xxx
```

**按上傳日期搜尋**（找最新內容）：用 `ytsearchdateN:` 取代 `ytsearchN:`。

**過濾搜尋結果**：用 `--match-filters` 在搜尋層直接篩選，比下載後再過濾高效：

```bash
# 排除短影片（< 1 分鐘）和直播
yt-dlp --flat-playlist "ytsearch20:關鍵字" -j --match-filters "duration>60 & !is_live"

# 只要高人氣影片
yt-dlp --flat-playlist "ytsearch20:關鍵字" -j --match-filters "view_count>?1000"
```

用戶挑選後可進一步：取元數據、抓字幕、或推送到 NotebookLM（搭配 anything-to-notebooklm skill）。

## 取得影片元數據

```bash
yt-dlp -j "URL"
```

除基本欄位外，`channel_follower_count` 可評估頻道規模，`like_count` / `comment_count` 可評估內容互動度。

## 下載字幕

**先確認可用字幕**（避免下載失敗）：

```bash
yt-dlp --list-subs "URL" 2>&1 | head -30
```

確認有字幕後再下載。`--sub-langs` 支援正則，可抓所有語言變體：

```bash
# 抓中文（含 zh-TW, zh-Hans 等）和英文（含 en-US 等）
yt-dlp --skip-download --write-auto-subs --sub-langs "zh.*,en.*" --sub-format vtt -o "$TEMP/%(id)s" "URL"
```

也可同時抓手動字幕（品質更好）和自動字幕：

```bash
yt-dlp --skip-download --write-subs --write-auto-subs --sub-langs "zh.*,en.*" --sub-format vtt -o "$TEMP/%(id)s" "URL"
```

手動字幕（`--write-subs`）品質優於自動字幕（`--write-auto-subs`），有手動的優先用。

輸出 VTT 檔，用內建腳本轉純文字：

```bash
python <skill-path>/scripts/parse_vtt.py "$TEMP/VIDEO_ID.en.vtt" -o "$TEMP/transcript.txt"
```

如果 `--list-subs` 顯示無字幕，告知用戶該影片沒有可用字幕。

## 年齡限制 / 會員內容

遇到年齡限制或需要登入才能觀看的影片，可從瀏覽器提取 Cookie：

```bash
yt-dlp --cookies-from-browser chrome -j "URL"
```

支援 chrome、firefox、edge、brave 等瀏覽器。先詢問用戶慣用的瀏覽器。

## 與 anything-to-notebooklm 的銜接

用戶常見流程：搜影片 → 選一部 → 推 NotebookLM。選定影片後，記住 URL，直接傳給 anything-to-notebooklm skill 使用（YouTube URL 可直接 `source add`，不需要先抓字幕）。

如果用戶想看逐字稿再決定是否推送，先抓字幕讓用戶確認內容。

## 注意事項

- Windows 中文輸出亂碼 → 指令前加 `PYTHONUTF8=1`
- 搜尋結果受地區影響 → 可加 `--geo-bypass`
- 長影片字幕檔很大 → 先確認 `duration` 再決定是否下載
- 批量操作加 `--sleep-requests 1` 避免被 YouTube 限流
- 用完字幕後清理暫存：`rm "$TEMP"/VIDEO_ID.*.vtt`
