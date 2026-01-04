# MP4 -> WAV 轉換器

這個小工具使用系統上的 `ffmpeg` 將 MP4（或其他包含音訊的多媒體檔）轉成 WAV。

安裝與使用：

- 1) 安裝 ffmpeg 並將其加入系統 PATH（Windows 範例）：
  - 下載 https://ffmpeg.org/ ，或使用包管理工具安裝
  - 確認在 PowerShell 中可執行 `ffmpeg`（`ffmpeg -version`）

- 2) 進入資料夾並執行（假設 Python 已安裝）：

```powershell
cd class14\changetowav
python changetowav.py input.mp4
```

- 也可以指定輸出檔與取樣率/聲道：

```powershell
python changetowav.py input.mp4 -o output.wav --rate 16000 --channels 1
```

備註：此工具呼叫系統的 `ffmpeg`，不額外依賴 Python 第三方套件。
