# anything-to-notebooklm 故障排查

## NotebookLM 認證失敗

先用內建診斷確認問題：

```bash
notebooklm auth check --test    # 完整網路驗證
```

如果失敗，重新登入：

```bash
notebooklm login    # 開瀏覽器重新認證
notebooklm list     # 驗證成功
```

## markitdown 轉換失敗

```bash
pip install markitdown    # 確認已安裝
markitdown --help         # 確認可用
```

常見原因：
- 檔案路徑有空格 → 用雙引號包
- PDF 是掃描件 → markitdown 會嘗試 OCR，需要額外依賴

注意：PDF、DOCX、Markdown、CSV、TXT、圖片、音訊可直接用 `notebooklm source add` 上傳，不一定需要 markitdown 轉換。markitdown 主要用於 PPTX、XLSX、EPUB 等 NotebookLM 不直接支援的格式。

## Source 上傳後生成失敗

- 內容太短（< 100 字）→ 生成效果差
- 內容太長（> 50 萬字）→ 可能超時
- 忘記 `--wait` → source 還沒處理完就開始生成

**關鍵**：`source add` 一定要加 `--wait`。

## 生成任務卡住

```bash
notebooklm artifact list    # 查看所有成品狀態
notebooklm artifact poll <task_id>    # 查看特定任務
```

如果 pending 超過 10 分鐘，到 NotebookLM 網頁端手動操作。

遇到速率限制時，用 `--retry 3` 自動重試（指數退避）。

## 生成失敗

成品狀態為 FAILED 時：
1. 確認來源內容足夠（> 100 字）
2. 確認來源已處理完成（不在 PREPARING 狀態）
3. 嘗試 `--retry 3` 重新生成
4. 檢查是否達到每日生成上限

## 跨平台暫存目錄

Skill 中的 `$TEMP` 在不同平台對應：

| 平台 | 變數 | 典型路徑 |
|------|------|---------|
| Windows (PowerShell) | `$env:TEMP` | `C:\Users\<user>\AppData\Local\Temp` |
| Windows (Git Bash) | `$TEMP` | `/tmp` 或 Windows temp |
| macOS / Linux | `$TMPDIR` 或 `/tmp` | `/tmp` |

Agent 會自動處理，但如果手動執行指令，用對應平台的變數。

## Windows 中文編碼

中文檔名或中文輸出亂碼時，在指令前加 `PYTHONUTF8=1`：

```bash
PYTHONUTF8=1 notebooklm create "筆記本名稱"
PYTHONUTF8=1 markitdown "中文檔名.pdf" -o "$TEMP/converted.md"
```

## 除錯模式

遇到難以診斷的問題，啟用詳細日誌：

```bash
NOTEBOOKLM_LOG_LEVEL=DEBUG notebooklm <command>
```
