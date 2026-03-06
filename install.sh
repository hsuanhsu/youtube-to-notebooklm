#!/bin/bash
# YouTube → NotebookLM 研究工作流 安裝腳本
# 適用於任何支援 Skills 的 AI Agent（Claude Code、Cursor、Windsurf 等）

set -e

echo "=== YouTube → NotebookLM 研究工作流 ==="
echo ""

# 1. 安裝 Python 依賴
echo "[1/3] 安裝 Python 依賴..."
pip install yt-dlp
pip install notebooklm-py
pip install markitdown
echo "  ✓ yt-dlp, notebooklm-py, markitdown 安裝完成"
echo ""

# 2. 複製 Skills
SKILL_DIR="${HOME}/.claude/skills"
echo "[2/3] 複製 Skills 到 ${SKILL_DIR}..."

mkdir -p "${SKILL_DIR}/yt-search"
mkdir -p "${SKILL_DIR}/anything-to-notebooklm/references"

cp skills/yt-search/skill.md "${SKILL_DIR}/yt-search/skill.md"
cp skills/anything-to-notebooklm/skill.md "${SKILL_DIR}/anything-to-notebooklm/skill.md"
cp skills/anything-to-notebooklm/references/examples.md "${SKILL_DIR}/anything-to-notebooklm/references/examples.md"
cp skills/anything-to-notebooklm/references/troubleshooting.md "${SKILL_DIR}/anything-to-notebooklm/references/troubleshooting.md"
echo "  ✓ yt-search + anything-to-notebooklm Skills 已安裝"
echo ""

# 3. NotebookLM 登入
echo "[3/3] NotebookLM 登入..."
echo "  執行 notebooklm login 開啟瀏覽器登入 Google 帳號"
echo "  （登入一次即可，之後不用再登）"
echo ""
notebooklm login
echo ""

# 驗證
echo "=== 驗證安裝 ==="
echo -n "  yt-dlp: "; yt-dlp --version
echo -n "  notebooklm: "; notebooklm --version 2>/dev/null || echo "(installed)"
echo -n "  markitdown: "; markitdown --version 2>/dev/null || echo "(installed)"
echo ""
echo "✓ 安裝完成！重啟你的 AI Agent 即可使用。"
echo ""
echo "試試看："
echo "  「幫我搜 YouTube 上關於 cold pressed juice 的影片」"
echo "  「把這個影片上傳到 NotebookLM 生成播客 https://youtube.com/watch?v=...」"
