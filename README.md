# youtube-to-notebooklm

Search YouTube, grab transcripts, push to NotebookLM, and generate podcasts, mind maps, quizzes — all from your terminal with natural language.

搜 YouTube 影片、抓逐字稿、推進 NotebookLM，生成播客、思維導圖、測驗 — 全程在終端用自然語言完成。

```
You:   "Find me videos about cold pressed juice"
       「幫我找 cold pressed juice 的教學影片」
            ↓  yt-search skill
Agent: Lists 20 videos (title, channel, duration, views)
            ↓  You pick one
You:   "Upload #3 to NotebookLM and generate a podcast"
       「把第 3 部上傳到 NotebookLM 生成播客」
            ↓  anything-to-notebooklm skill
Agent: Downloads 34 MB podcast to your machine
```

![Demo: mind map, summary with footnotes, and podcast generation in terminal](demo.png)

## How It Works / 運作方式

Two [AI Agent Skills](https://docs.anthropic.com/en/docs/claude-code/skills) that work together:

| Skill | What it does |
|-------|-------------|
| **yt-search** | Search YouTube, get metadata, download subtitles via [yt-dlp](https://github.com/yt-dlp/yt-dlp) |
| **anything-to-notebooklm** | Upload any content to [NotebookLM](https://notebooklm.google.com/) and generate outputs via [notebooklm-py](https://github.com/nicholasgcoles/notebooklm-py) |

Your AI agent reads these skills and knows when to call which tool — you just talk to it.

## Prerequisites / 前置條件

- **Python 3.10+**
- **Google account** (NotebookLM is free / NotebookLM 免費)
- **AI Agent with Skills support** — Claude Code, Cursor, Windsurf, or any agent that reads `~/.claude/skills/`

## Getting Started / 安裝

```bash
git clone https://github.com/azuma520/youtube-to-notebooklm.git
cd youtube-to-notebooklm
bash install.sh
```

The script installs three pip packages, copies the skills to `~/.claude/skills/`, and opens a browser to log in to NotebookLM (one-time).

安裝腳本會裝三個 pip 套件、複製 Skills、開瀏覽器登入 NotebookLM（只需一次）。

> [!IMPORTANT]
> After installation, **restart your AI agent** to load the new skills.
> 安裝完請**重啟 AI Agent** 讓它載入新 Skills。

<details>
<summary>Manual installation / 手動安裝</summary>

```bash
pip install yt-dlp notebooklm-py markitdown

cp -r skills/yt-search ~/.claude/skills/
cp -r skills/anything-to-notebooklm ~/.claude/skills/

notebooklm login
```

</details>

## Usage / 用法

Talk to your agent in natural language. Skills trigger automatically.

安裝完直接用自然語言對 AI Agent 說話，Skills 會自動觸發。

### Search YouTube / 搜影片

```
"search YouTube for videos about trade show booth setup"
「搜影片 台灣水果外銷」
「幫我搜 NFC juice market 的 YouTube 影片」
```

### Get Transcripts / 抓字幕

```
"get the transcript of this video https://youtu.be/..."
「幫我抓這部影片的字幕 https://youtube.com/watch?v=...」
```

### Push to NotebookLM / 推進 NotebookLM

```
"upload this video to NotebookLM https://youtube.com/watch?v=..."
"turn this webpage into a podcast https://example.com/article"
「把這個 PDF 生成思維導圖 ~/Documents/research.pdf」
```

### Supported Outputs / 可以生成什麼

| Say / 說 | Get / 得到 |
|----------|-----------|
| generate podcast / 生成播客 | WAV audio file |
| make slides / 做成 PPT | PDF slides |
| mind map / 畫思維導圖 | JSON mind map |
| generate quiz / 出題 | Markdown quiz |
| write report / 生成報告 | Markdown report |
| flashcards / 做閃卡 | Markdown cards |

NotebookLM also supports video, infographic, and data-table outputs.

### Multi-Source / 多源合併

A single notebook can hold up to 50 sources. Add everything first, then generate:

```
"Upload these and make a report:
 - https://example.com/article
 - https://youtube.com/watch?v=xyz
 - ~/Documents/research.pdf"
```

## Built With / 背後工具

| Tool | Role | Cost |
|------|------|------|
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | YouTube search, metadata, subtitles | Free |
| [notebooklm-py](https://github.com/nicholasgcoles/notebooklm-py) | NotebookLM CLI bridge | Free |
| [markitdown](https://github.com/microsoft/markitdown) | Convert PDF/DOCX/PPTX to Markdown | Free |

> [!TIP]
> **Windows users**: Prefix CLI commands with `PYTHONUTF8=1` if you see garbled Chinese output.
> **Windows 用戶**：中文亂碼時在指令前加 `PYTHONUTF8=1`。
> ```bash
> PYTHONUTF8=1 notebooklm create "筆記本名稱"
> ```
