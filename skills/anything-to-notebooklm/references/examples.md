# anything-to-notebooklm 使用範例

## 範例 1：網頁 → 播客（辯論風格）

```
用戶：把這篇文章生成播客，用辯論方式 https://example.com/article
```

1. `notebooklm create "Article Discussion"`
2. `notebooklm source add https://example.com/article --wait`
3. `notebooklm generate audio --format debate --wait`
4. `notebooklm download audio ./output.wav`

## 範例 2：YouTube → 思維導圖

```
用戶：這個視頻幫我畫個思維導圖 https://www.youtube.com/watch?v=abc123
```

1. `notebooklm create "Video Mind Map"`
2. `notebooklm source add https://www.youtube.com/watch?v=abc123 --wait`
3. `notebooklm generate mind-map`
4. `notebooklm download mind-map ./mindmap.json`

## 範例 3：本地 PDF → 可編輯 PPT

```
用戶：把這個 PDF 做成可以編輯的 PPT ~/Documents/research.pdf
```

1. `notebooklm create "Research Slides"`
2. `notebooklm source add ~/Documents/research.pdf --wait`
3. `notebooklm generate slide-deck --format detailed --wait`
4. `notebooklm download slide-deck ./slides.pptx --format pptx`

## 範例 4：混合多源 → 報告（學習指南格式）

```
用戶：把這些一起做成學習指南：
- https://example.com/article
- https://youtube.com/watch?v=xyz
- ~/Documents/research.pdf
```

1. `notebooklm create "Study Guide"`
2. `notebooklm source add https://example.com/article --wait`
3. `notebooklm source add https://youtube.com/watch?v=xyz --wait`
4. `notebooklm source add ~/Documents/research.pdf --wait`
5. `notebooklm generate report --format study-guide --wait`
6. `notebooklm download report ./guide.md`

## 範例 5：關鍵詞 AI 研究 → 報告

```
用戶：搜索 'NFC juice market trends' 並生成報告
```

1. `notebooklm create "NFC Juice Research"`
2. `notebooklm source add-research "NFC juice market trends 2026" --mode deep --from web --import-all`
3. `notebooklm research wait`
4. `notebooklm generate report --format briefing-doc --wait`
5. `notebooklm download report ./report.md`

## 範例 6：生成高難度 Quiz

```
用戶：用這篇文章出一些難的題目 https://example.com/ml-paper
```

1. `notebooklm create "ML Quiz"`
2. `notebooklm source add https://example.com/ml-paper --wait`
3. `notebooklm generate quiz --difficulty hard --quantity more --wait`
4. `notebooklm download quiz ./quiz.md --format markdown`

## 範例 7：對來源提問 + 存筆記

```
用戶：上傳完之後幫我問一下這篇論文的核心論點是什麼
```

1. （接續上傳步驟後）
2. `notebooklm ask "What are the core arguments in this paper?" --save-as-note --note-title "Core Arguments"`

## 範例 8：生成 anime 風格影片

```
用戶：把這篇文章做成 anime 風格的短影片 https://example.com/article
```

1. `notebooklm create "Anime Explainer"`
2. `notebooklm source add https://example.com/article --wait`
3. `notebooklm generate video --format explainer --style anime --wait`
4. `notebooklm download video ./video.mp4`

## 範例 9：繁體中文播客

```
用戶：用繁體中文生成播客
```

1. `notebooklm language set zh_Hant`
2. `notebooklm generate audio --wait`
3. `notebooklm download audio ./podcast.wav`
