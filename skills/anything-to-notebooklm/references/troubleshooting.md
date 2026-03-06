# anything-to-notebooklm 故障排查

## NotebookLM 認證失敗

```bash
notebooklm login    # 重新登入（會開瀏覽器）
notebooklm list     # 驗證認證成功
```

## markitdown 轉換失敗

```bash
pip install markitdown    # 確認已安裝
markitdown --help         # 確認可用
```

常見原因：
- 檔案路徑有空格 → 用雙引號包
- PDF 是掃描件 → markitdown 會嘗試 OCR，需要額外依賴

## Source 上傳後生成失敗

- 內容太短（< 100 字）→ 生成效果差
- 內容太長（> 50 萬字）→ 可能超時
- 忘記 `--wait` → source 還沒處理完就開始生成

**關鍵**：`notebooklm source add ... --wait` 一定要加 `--wait`。

## 生成任務卡住

```bash
notebooklm artifact list    # 查看任務狀態
```

如果 pending 超過 10 分鐘，到 NotebookLM 網頁端手動操作。

## 跨平台注意

- Windows 中文檔名需要 `PYTHONUTF8=1` 前綴
- 暫存目錄：macOS/Linux 用 `$TMPDIR` 或 `/tmp`，Windows 用 `$TEMP`
- 路徑分隔符：Skill 中用 `$TEMP` 通用寫法，Agent 會自動處理
