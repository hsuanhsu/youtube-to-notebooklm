---
name: whisper-transcribe
description: 'Transcribe audio/video to accurate subtitles using Whisper AI, with optional translation and delivery. Supports YouTube URLs and local audio/video files. Use when: (1) a YouTube video has no subtitles, (2) auto-generated captions are inaccurate, (3) the user wants high-quality transcription, (4) the user needs translated subtitles, (5) the user wants transcripts sent to email or cloud storage. Triggers: "轉錄", "語音轉文字", "Whisper", "沒有字幕", "字幕不準", "transcribe", "speech to text", "no subtitles", "bad captions", "翻譯字幕", "translate subtitles", "寄到信箱", "上傳到雲端". Make sure to use this skill whenever the user needs transcription beyond what YouTube auto-captions provide, or when yt-search reports no subtitles available.'
---

# whisper-transcribe

用 Whisper AI 將音頻/影片轉錄為高準確度字幕（SRT），可選翻譯和投遞。

## 何時使用

- yt-search 回報影片**沒有字幕**
- YouTube 自動字幕**品質差**（用戶抱怨不準）
- 用戶需要**非 YouTube 來源**的轉錄（本地音頻、會議錄音等）
- 用戶要求**翻譯字幕**
- 用戶想把字幕**寄到信箱或上傳雲端**

## 前置條件

- `yt-dlp` + `ffmpeg`（下載音頻）
- **本地模式**：`pip install faster-whisper`（需 GPU 或可用 CPU）
- **雲端模式**：`pip install groq` + `GROQ_API_KEY`

詳細安裝見 [references/setup.md](references/setup.md)。

## 核心流程：轉錄

### 從 YouTube URL

```bash
python <skill-path>/scripts/transcribe.py "https://youtube.com/watch?v=xxx" \
  -o "$TEMP/transcripts" \
  --model large-v3 \
  --device cuda
```

### 從本地檔案

```bash
python <skill-path>/scripts/transcribe.py ./recording.mp3 \
  -o "$TEMP/transcripts" \
  --model large-v3
```

### 使用 Groq 雲端（無 GPU）

```bash
python <skill-path>/scripts/transcribe.py "URL_or_FILE" \
  -o "$TEMP/transcripts" \
  --backend groq
```

輸出：`{video_id}.srt`（帶時間碼）+ `{video_id}.txt`（純文字）。

### 參數選擇指引

| 情境 | 建議參數 |
|------|---------|
| 一般英文影片 | `--model large-v3`（預設） |
| 中文/日文內容 | `--model large-v3 --language zh` 或 `ja` |
| 快速預覽 | `--model small --device cpu` |
| 無 GPU | `--backend groq` |
| 長影片（> 2 小時） | 本地模式，避免 API 超時 |

不指定 `--language` 時會自動偵測。但已知語言時指定會提高準確度。

## 可選：翻譯字幕

轉錄完成後，用戶想翻譯：

```bash
python <skill-path>/scripts/translate_srt.py "$TEMP/transcripts/VIDEO_ID.srt" \
  --target zh-tw \
  --engine deepl \
  -o "$TEMP/transcripts/VIDEO_ID_zh.srt"
```

**翻譯引擎選擇**：

| 引擎 | 品質 | 速度 | 成本 | 設定 |
|------|------|------|------|------|
| `deepl` | 最佳 | 快 | 免費 50 萬字/月 | `DEEPL_API_KEY` |
| `openai` | 很好（上下文感知） | 中 | 按量計費 | `OPENAI_API_KEY` |

也可以讓 Agent 直接讀取 TXT 檔後在對話中翻譯，不需要額外 API — 適合短內容或用戶想邊看邊討論。

## 可選：投遞

### 寄到 Gmail

Agent 使用可用的 email 工具（Claude Code 有 Gmail MCP）：

1. 讀取轉錄/翻譯後的檔案
2. 建立草稿或直接發送，附上 SRT/TXT 檔案
3. 主旨建議：`[Transcript] {影片標題}`

### 上傳到 Google Drive

```bash
rclone copy "$TEMP/transcripts/VIDEO_ID.srt" gdrive:/Transcripts/
rclone copy "$TEMP/transcripts/VIDEO_ID.txt" gdrive:/Transcripts/
```

需要先設定 rclone（見 [references/setup.md](references/setup.md)）。

如果用戶沒有 rclone，也可以用 Google Drive API 或手動告知檔案路徑讓用戶自己上傳。

## 與其他 Skill 的串接

### ← 從 yt-search 接手

yt-search 用 `--list-subs` 發現沒有字幕，或用戶表示自動字幕不準時：

1. 告知用戶：「這部影片沒有（好的）字幕，要用 Whisper 轉錄嗎？」
2. 用戶同意後，用影片 URL 執行轉錄
3. 輸出 SRT + TXT

### → 推送到 anything-to-notebooklm

轉錄完成後，用戶想推進 NotebookLM：

1. 用 TXT 檔做 `notebooklm source add "$TEMP/transcripts/VIDEO_ID.txt" --wait`
2. 或直接用影片 URL（NotebookLM 原生支援 YouTube）

TXT 檔的優勢：經過 Whisper 轉錄，品質遠高於 NotebookLM 自己抓的 YouTube 自動字幕。

## 完整工作流範例

```
用戶：「幫我找 AI agent 的教學影片」
  → yt-search 搜尋，列出 20 部

用戶：「第 3 部看起來不錯，幫我抓字幕」
  → yt-search 回報：這部影片沒有字幕

用戶：「那用 Whisper 轉錄」
  → whisper-transcribe 下載音頻 + 轉錄
  → 產出 SRT + TXT

用戶：「翻譯成繁中，然後寄到我信箱」
  → translate_srt.py 翻譯
  → Gmail 寄出

用戶：「也幫我推到 NotebookLM 生成播客」
  → anything-to-notebooklm source add TXT
  → generate audio
```

## 清理暫存

```bash
rm -rf "$TEMP/transcripts/"
```

## 注意事項

- 首次使用會下載模型（large-v3 約 3GB），之後從快取載入
- GPU 記憶體不足時自動降級：先試 `large-v3`，不行換 `medium` 或 `small`
- Windows 加 `PYTHONUTF8=1` 前綴
- 長音頻（> 3 小時）建議用本地模式，雲端 API 可能超時或超額
