# YouTube → NotebookLM 研究工作流

用自然語言搜 YouTube 影片、推進 NotebookLM、生成播客/摘要/思維導圖等產出。全程在終端完成，不用切視窗。

## 它做什麼

```
「幫我找 cold pressed juice 的教學影片」
    ↓ AI Agent 觸發 yt-search skill
列出 20 部影片（標題、頻道、時長、觀看數）
    ↓ 你挑選
「把第 3 部上傳到 NotebookLM 生成播客」
    ↓ AI Agent 觸發 anything-to-notebooklm skill
NotebookLM 處理 → 播客音檔下載到本機
```

## 需要什麼

- **Python 3.10+**
- **支援 Skills 的 AI Agent**（Claude Code、Cursor、Windsurf、或任何支援 `~/.claude/skills/` 的 Agent）
- **Google 帳號**（NotebookLM 免費使用）

## 安裝

```bash
git clone https://github.com/你的帳號/youtube-to-notebooklm.git
cd youtube-to-notebooklm
bash install.sh
```

安裝腳本會：
1. `pip install` 三個工具（yt-dlp、notebooklm-py、markitdown）
2. 複製兩個 Skills 到 `~/.claude/skills/`
3. 開瀏覽器登入 NotebookLM（只需一次）

裝完重啟你的 AI Agent 即可。

### 手動安裝

如果你不想用腳本：

```bash
# 裝工具
pip install yt-dlp notebooklm-py markitdown

# 複製 skills（改成你的 Agent 的 skills 路徑）
cp -r skills/yt-search ~/.claude/skills/
cp -r skills/anything-to-notebooklm ~/.claude/skills/

# 登入 NotebookLM
notebooklm login
```

## 用法

安裝完後，直接用自然語言對 AI Agent 說話：

### 搜 YouTube

- 「幫我搜 NFC juice market 的 YouTube 影片」
- 「search YouTube for videos about trade show booth setup」
- 「找影片 台灣水果外銷」

### 抓字幕 / 逐字稿

- 「幫我抓這部影片的字幕 https://youtube.com/watch?v=...」
- 「get the transcript of this video」

### 推進 NotebookLM

- 「把這個影片上傳到 NotebookLM https://youtube.com/watch?v=...」
- 「把這個網頁做成播客 https://example.com/article」
- 「把這個 PDF 生成思維導圖 ~/Documents/research.pdf」

### 可以生成什麼

| 說 | 得到 |
|----|------|
| 生成播客 / generate podcast | WAV 音檔 |
| 做成 PPT / make slides | PDF 幻燈片 |
| 畫思維導圖 / mind map | JSON 腦圖 |
| 出題 / generate quiz | Markdown 測驗 |
| 生成報告 / write report | Markdown 報告 |
| 做閃卡 / flashcards | Markdown 卡片 |

## 背後三個工具

| 工具 | 用途 | 成本 |
|------|------|------|
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | 搜 YouTube、抓元數據、下載字幕 | 免費 |
| [notebooklm-py](https://github.com/nicholasgcoles/notebooklm-py) | NotebookLM CLI 橋接 | 免費 |
| [markitdown](https://github.com/microsoft/markitdown) | PDF/DOCX/PPTX 轉 Markdown | 免費 |

## 檔案結構

```
youtube-to-notebooklm/
├── skills/
│   ├── yt-search/
│   │   └── skill.md              # YouTube 搜尋 + 字幕 Skill
│   └── anything-to-notebooklm/
│       ├── skill.md              # NotebookLM 上傳 + 生成 Skill
│       └── references/
│           ├── examples.md       # 使用範例
│           └── troubleshooting.md # 故障排查
├── evals/
│   └── yt-search-trigger-eval.json  # Skill 觸發測試集
├── install.sh                    # 一鍵安裝腳本
└── README.md
```

## Windows 注意

Windows 上中文輸出可能亂碼，CLI 指令前加 `PYTHONUTF8=1`：

```bash
PYTHONUTF8=1 notebooklm create "筆記本名稱"
```

## 授權

MIT
