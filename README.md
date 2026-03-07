# youtube-to-notebooklm

Search YouTube, grab transcripts, push to NotebookLM, and generate podcasts, mind maps, quizzes — all from your terminal with natural language.

[Overview](#overview) • [Getting started](#getting-started) • [Usage](#usage) • [Built with](#built-with)

[![中文版 README](https://img.shields.io/badge/中文版-README-blue)](README.zh-TW.md)

```
You:   "Find me videos about cold pressed juice"
            ↓  yt-search
Agent: Lists 20 videos (title, channel, duration, views)
            ↓  You pick one
You:   "Upload #3 to NotebookLM and generate a podcast"
            ↓  anything-to-notebooklm
Agent: Downloads 34 MB podcast to your machine
```

![Demo: mind map, summary with footnotes, and podcast generation in terminal](demo.png)

## Overview

Three [AI Agent Skills](https://docs.anthropic.com/en/docs/claude-code/skills) that work together inside your terminal. You talk; the agent figures out which skill to call.

| Skill | What it does | Powered by |
|-------|-------------|------------|
| **yt-search** | Search YouTube, get metadata, download subtitles | [yt-dlp](https://github.com/yt-dlp/yt-dlp) |
| **anything-to-notebooklm** | Upload any content to NotebookLM and generate outputs | [notebooklm-py](https://github.com/teng-lin/notebooklm-py) |
| **whisper-transcribe** | Transcribe audio/video, translate subtitles, deliver via email/cloud | [faster-whisper](https://github.com/SYSTRAN/faster-whisper) |

```
User ──natural language──▶ AI Agent
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
     yt-search      anything-to-notebooklm  whisper-transcribe
     (yt-dlp)         (notebooklm-py)       (faster-whisper)
          │                   │                   │
          ▼                   ▼                   ▼
   Search results      Podcasts, slides,    SRT/TXT transcripts
   Subtitles           mind maps, quizzes   Translated subtitles
```

## Getting started

### Prerequisites

- **Python 3.10+**
- **Google account** — NotebookLM is free
- **AI Agent with Skills support** — [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [Cursor](https://www.cursor.com/), [Windsurf](https://windsurf.com/), or any agent that reads `~/.claude/skills/`

### Installation

**macOS / Linux / Git Bash:**

```bash
git clone https://github.com/azuma520/youtube-to-notebooklm.git
cd youtube-to-notebooklm
bash install.sh
```

**Windows (PowerShell):**

```powershell
git clone https://github.com/azuma520/youtube-to-notebooklm.git
cd youtube-to-notebooklm
.\install.ps1
```

The installer does three things:

1. Installs pip packages (`yt-dlp`, `notebooklm-py`, `markitdown`)
2. Copies skills to your agent's skill directory (auto-detects Claude Code, Cursor, Windsurf)
3. Opens a browser to log in to NotebookLM (one-time)

> [!IMPORTANT]
> After installation, **restart your AI agent** to load the new skills.

<details>
<summary>Manual installation</summary>

```bash
pip install yt-dlp notebooklm-py markitdown

cp -r skills/yt-search ~/.claude/skills/
cp -r skills/anything-to-notebooklm ~/.claude/skills/
cp -r skills/whisper-transcribe ~/.claude/skills/

notebooklm login
```

</details>

## Usage

Talk to your agent in natural language. Skills trigger automatically.

### Search YouTube

```
"search YouTube for videos about trade show booth setup"
"find me some tutorials on NFC juice processing"
```

### Get transcripts

```
"get the transcript of this video https://youtu.be/..."
"download the English subtitles from this video"
```

### Transcribe with Whisper

When YouTube has no subtitles or auto-captions are inaccurate:

```
"this video has no subtitles, transcribe it with Whisper"
"transcribe this and translate to Chinese, then send to my email"
```

> [!NOTE]
> `whisper-transcribe` requires additional setup (GPU recommended). See the skill's [setup guide](skills/whisper-transcribe/references/setup.md) for details.

### Push to NotebookLM

```
"upload this video to NotebookLM and generate a podcast"
"turn this webpage into a mind map https://example.com/article"
"make slides from this PDF ~/Documents/research.pdf"
```

### Supported outputs

| Say | Get |
|-----|-----|
| generate podcast | WAV audio (deep-dive, brief, critique, debate) |
| make slides | PDF slides or editable PPTX |
| mind map | JSON mind map |
| generate quiz | Markdown quiz |
| write report | Markdown report |
| flashcards | Markdown cards |

NotebookLM also supports video, infographic, and data-table outputs.

### Multi-source

A single notebook can hold up to 50 sources. Add everything first, then generate:

```
"Upload these and make a report:
 - https://example.com/article
 - https://youtube.com/watch?v=xyz
 - ~/Documents/research.pdf"
```

### End-to-end workflow

```
You:   "Search YouTube for AI agent tutorials"
Agent: Lists 20 videos with metadata
You:   "Get the transcript of #3"
Agent: No subtitles available for this video
You:   "Transcribe it with Whisper"
Agent: Downloads audio, transcribes → SRT + TXT
You:   "Translate to Chinese and upload to NotebookLM as a podcast"
Agent: Translates subtitles, uploads, generates podcast → WAV file
```

## Built with

| Tool | Role | Cost |
|------|------|------|
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | YouTube search, metadata, subtitles | Free |
| [notebooklm-py](https://github.com/teng-lin/notebooklm-py) | NotebookLM CLI bridge | Free |
| [markitdown](https://github.com/microsoft/markitdown) | Convert PDF/DOCX/PPTX to Markdown | Free |
| [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | High-accuracy speech-to-text | Free (local) |

> [!TIP]
> **Windows users**: prefix CLI commands with `PYTHONUTF8=1` if you see garbled output with non-ASCII characters.
> ```bash
> PYTHONUTF8=1 notebooklm create "my notebook"
> ```
