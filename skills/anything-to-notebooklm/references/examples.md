# anything-to-notebooklm 使用範例

## 範例 1：網頁 → 播客

```
用戶：把這篇文章生成播客 https://example.com/article
```

1. 識別為網頁 URL
2. `notebooklm create "Article Title"`
3. `notebooklm source add https://example.com/article --wait`
4. `notebooklm generate audio`
5. `notebooklm artifact wait`
6. `notebooklm download audio ./output.wav`

## 範例 2：YouTube → 思維導圖

```
用戶：這個視頻幫我畫個思維導圖 https://www.youtube.com/watch?v=abc123
```

1. 識別為 YouTube URL
2. `notebooklm create "Video Title"`
3. `notebooklm source add https://www.youtube.com/watch?v=abc123 --wait`
4. `notebooklm generate mind-map`
5. `notebooklm artifact wait`
6. `notebooklm download mind-map ./mindmap.json`

## 範例 3：本地 PDF → 報告

```
用戶：把這個 PDF 做成報告 ~/Documents/research.pdf
```

1. 識別為本地 PDF
2. `markitdown ~/Documents/research.pdf -o "$TMPDIR/converted.md"`
3. `notebooklm create "Research Report"`
4. `notebooklm source add "$TMPDIR/converted.md" --wait`
5. `notebooklm generate report`
6. `notebooklm artifact wait`
7. `notebooklm download report ./report.md`

## 範例 4：混合多源 → PPT

```
用戶：把這些一起做成 PPT：
- https://example.com/article
- https://youtube.com/watch?v=xyz
- ~/Documents/research.pdf
```

1. `notebooklm create "Multi-Source Slides"`
2. URL 直接加：`notebooklm source add URL --wait`
3. 本地檔案先轉：`markitdown file -o "$TMPDIR/converted.md"` → 再 `source add`
4. 所有 source 加完後：`notebooklm generate slide-deck`
5. `notebooklm artifact wait` → `notebooklm download slide-deck ./slides.pdf`

## 範例 5：搜尋關鍵詞 → 報告

```
用戶：搜索 'NFC juice market trends' 並生成報告
```

1. 用 WebSearch 搜尋關鍵詞
2. 彙總前 3-5 條結果，存為 TXT
3. `notebooklm create "NFC Juice Research"`
4. `notebooklm source add "$TMPDIR/search_results.txt" --wait`
5. `notebooklm generate report`
