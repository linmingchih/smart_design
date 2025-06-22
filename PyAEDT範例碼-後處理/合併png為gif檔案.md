合併png為gif檔案
---

想要將多個不同時間，不同頻率的場型PNG檔案合併成GIF檔案，可以使用PIL庫來實現這個功能。下面是一個使用 Pillow （Python 影像處理函式庫）將同一資料夾內多張 PNG 圖片合併成 GIF 動畫的範例程式。請先用 `pip install pillow` 安裝 pillow。

```python
from PIL import Image
import os

def pngs_to_gif(input_folder, output_path, duration=500, loop=0):
    """
    將指定資料夾內的所有 PNG 檔案依檔名排序後輸出成 GIF。

    參數：
    - input_folder: 圖片所在資料夾路徑
    - output_path : 輸出的 GIF 檔案路徑（含 .gif 延伸名）
    - duration    : 每幀顯示時間（毫秒）
    - loop        : 迴圈次數，0 表示永久循環

    範例：
    pngs_to_gif("frames", "animation.gif", duration=200, loop=0)
    """
    # 取得所有 .png，並依檔名排序
    filenames = sorted([
        fn for fn in os.listdir(input_folder)
        if fn.lower().endswith(".png")
    ])
    if not filenames:
        raise ValueError(f"{input_folder} 中找不到任何 PNG 檔案")

    # 讀取成 Image 物件列表
    images = []
    for fn in filenames:
        path = os.path.join(input_folder, fn)
        img = Image.open(path)
        # 若影像不是 RGBA，轉成 RGBA 以保留透明度
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGBA")
        images.append(img)

    # 第一張為基底，其餘附加為後續幀
    base_image, *frames = images

    # 儲存為 GIF
    base_image.save(
        output_path,
        save_all=True,
        append_images=frames,
        format="GIF",
        duration=duration,
        loop=loop
    )
    print(f"已輸出 {output_path}，共 {len(images)} 幀，duration={duration}ms，loop={loop}")

if __name__ == "__main__":
    # 範例：將當前資料夾 ./frames 內的 png 合成 animation.gif
    pngs_to_gif(input_folder="./frames",
                output_path="animation.gif",
                duration=200,
                loop=0)
```


### 使用說明

1. **安裝套件**

   ```bash
   pip install pillow
   ```
2. **準備圖片**
   將所有要合成的 PNG 檔案放到同一資料夾（範例程式中為 `./frames`），並用有序檔名（例如 `frame001.png`、`frame002.png`…）以決定動畫順序。
3. **執行程式**

   ```bash
   python pngs_to_gif.py
   ```

設定好 `input_folder`、`output_path`、`duration`（每幀毫秒）、`loop`（迴圈次數；`0` 表示無限循環）即可。

這樣就能快速將多張 PNG 串成一個可重複播放的 GIF 動畫。若有其他需求（如調整尺寸、調整透明度…），也可在讀圖時用 `img.resize()`、`img.putalpha()` 等方法進一步處理。
