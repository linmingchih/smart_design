利用 Shapely 與 PyEDB 自動清除與訊號線過遠的空洞與元件以加速HFSS電磁模擬
---


**阿傑:** 歡迎收聽「EDA 新攻略」，我是主持人阿傑。今天我們非常榮幸邀請到一位在 EDA 自動化領域的專家，同時也是我們今天要介紹的這個實用 Python 腳本的開發者——鳴志哥！鳴志哥，您好！

**鳴志哥:** 阿傑好，各位聽眾大家好。很高興有這個機會來分享一下我寫的這個小工具。

**阿傑:** 鳴志哥，我們知道您在訊號完整性 (SI) 模擬方面有很多經驗。您開發這個腳本，最初的動機是什麼呢？

**鳴志哥:** 是的，在做 SI 模擬的時候，我們常常會遇到一個情況。大家都知道，SI 模擬關注的是傳輸線以及它周圍迴路路徑的均勻性和連續性。但是在很多實際的 PCB 設計中，會存在一些對 SI 分析結果影響非常小的結構。

**阿傑:** 您指的是哪些結構呢？

**鳴志哥:** 比如說，在一些大的電源層或接地層上，有些銅箔的空洞 (voids) 可能離我們關注的主要訊號線非常遠。或者，板子上有些零件的佔位區，它們本身並不是這次 SI 分析的重點。這些結構，雖然對訊號的電磁特性影響不大，但在進行全波電磁模擬的時候，求解器還是會試圖去精確地剖分它們的網格 (meshing)。

**阿傑:** 我想我明白了。這意味著，這些「不太重要」的結構，反而會佔用大量的電腦記憶體來生成網格，並且拖慢整個模擬的計算時間，對吧？

**鳴志哥:** 完全正確！有時候，尤其是面對複雜或大型的板子，光是等待這些細枝末節的部分完成網格剖分，可能就要花掉好幾個小時，但它們對最終我們關心的 SI 指標，比如 S 參數或 TDR 阻抗，貢獻卻微乎其微。所以我才想，能不能寫一個腳本，自動化地去識別並移除這些「低貢獻、高成本」的結構，來優化我們的模擬流程。

**阿傑:** 這聽起來非常實用！那這個腳本是怎麼運作的呢？可以請鳴志哥您親自為我們導覽一下嗎？

**鳴志哥:** 當然。首先，腳本需要載入我們要處理的 Ansys EDB 檔案。

```python
# %% 參數設定
path = "D:/demo/test.aedb"
edb = Edb(path, edbversion="2024.1")
```
這一步就是透過 PyAEDT 的 `Edb` 類別，建立一個與 EDB 檔案的連接。這個 `edb` 物件就是我們後續所有操作的基礎。

**阿傑:** 這是 PyAEDT 使用的標準起手式。

**鳴志哥:** 沒錯。接下來，為了判斷哪些結構是「遠離」的，我們首先需要知道所有「重要」的訊號線在哪裡。所以我會遍歷 EDB 中所有的訊號網路 (`signal_nets`)，提取它們的中心線。

```python
# %% 擷取所有線段並建立 STRtree
lines = []
for net in edb.nets.signal_nets.values():
    for prim in net.primitives:
        lines.append(LineString(prim.center_line))

line_tree = STRtree(lines)
```
這裡我用了 Shapely 這個幾何函式庫，把每一段線轉換成 `LineString` 物件。然後，一個關鍵步驟是，我把所有這些線段建成了一個 `STRtree`。

**阿傑:** STRtree？這聽起來有點專業，它有什麼特別的作用嗎？

**鳴志哥:** STRtree 是一種空間索引。你可以把它想像成我預先幫所有的訊號線畫好了一張精密的地圖，並且做了索引。這樣，當我之後想查詢某個特定區域附近有哪些訊號線時，STRtree 可以非常快速地給我答案，而不需要我把設計中的每一條線都拿來比對一次。這對提升腳本的執行效率非常重要。

**阿傑:** 原來是為了加速搜尋。那有了訊號線的地圖之後呢？

**鳴志哥:** 接下來，我就去收集那些我們可能想要清理掉的「候選」結構。這主要包括兩類：

```python
# %% 擷取所有 void polygon
polygons = {}  # { primitive_obj: raw_point_data }
# 第一類：電源網路中的空洞 (voids)
for net in edb.nets.power_nets.values():
    for prim in net.primitives:
        if prim.is_void: # 如果這個圖元是空洞
            polygons[prim] = prim.points() # 就記錄下它和它的點位資料

# 第二類：板子上的零件佔位區 (components)
for _, comp in edb.components.components.items():
    x1, y1, x2, y2 = comp.bounding_box # 取得零件的邊界框
    # 把邊界框的四個角點也當作一個多邊形的點位資料存起來
    polygons[comp] = ([x1, x2, x2, x1], [y1, y1, y2, y2])
```
我把這些空洞和零件的邊界框都當作多邊形 (Polygons) 來處理，存在一個叫做 `polygons` 的字典裡。字典的鍵 (key) 是原始的 EDB 物件，值 (value) 是它的幾何點位資料。

**阿傑:** 所以現在我們有了訊號線的集合，也有了潛在要被清理的空洞和零件集合。接下來就是判斷它們之間的距離了嗎？

**鳴志哥:** 正是如此。這也是腳本最核心的部分：

```python
# %% 計算每個 polygon 與最近線段的最短距離
poly_distances = {} # 用來存放每個多邊形到最近訊號線的距離
for prim, raw_pts in polygons.items(): # 遍歷每一個候選多邊形
    # 1. 首先，把原始的點位資料 raw_pts 整理成 Shapely 能接受的標準格式
    if isinstance(raw_pts, tuple) and len(raw_pts) == 2:
        xs, ys = raw_pts
        coords = list(zip(xs, ys))
    elif isinstance(raw_pts, list) and raw_pts and len(raw_pts[0]) == 2:
        coords = raw_pts
    else:
        continue # 格式不對就跳過

    # 2. 試著用這些點位建立一個 Shapely 的 Polygon 物件
    try:
        poly = Polygon(coords)
    except Exception:
        continue # 建立失敗也跳過

    # 3. 為了加速查詢，我先定義一個「搜尋緩衝區」
    minx, miny, maxx, maxy = poly.bounds # 取得多邊形的邊界
    # 建立一個比多邊形本身大一點的搜尋框 (這裡我設了擴大 10mm，也就是 0.01 公尺)
    search_box = box(minx - 0.01, miny - 0.01, maxx + 0.01, maxy + 0.01)

    # 4. 利用前面建好的 STRtree，快速找出所有在這個搜尋框範圍內的訊號線
    idxs = line_tree.query(search_box)

    # 5. 計算這個多邊形到這些「候選訊號線」的最短距離
    if len(idxs) > 0: # 如果搜尋框內有訊號線
        candidate_lines = [lines[i] for i in idxs] # 取出這些候選線
        # 計算並找到最短的那個距離
        min_dist = min(poly.distance(line) for line in candidate_lines)
    else: # 如果搜尋框內一條訊號線都沒有
        min_dist = float("inf") # 那就表示它離所有訊號線都非常遠，距離設為無限大

    poly_distances[prim] = min_dist # 把算出來的最小距離記錄下來
```
這段的邏輯是，對於每一個空洞或零件，我先在它周圍畫一個小小的「搜尋緩衝區」。然後，我只在這個緩衝區內，透過 STRtree 快速找到可能相關的訊號線。最後，我才計算這個空洞/零件到這些「鄰近」訊號線的實際最短距離。這樣就避免了大量的無效計算。

**阿傑:** 非常聰明的做法！利用 STRtree 和搜尋緩衝區來大幅縮小計算範圍。那算出了最短距離之後，如何決定哪些要刪除呢？

**鳴志哥:** 這就需要設定一個「距離門檻」了。

```python
# %% 找出距離過遠(1mm)的元件與空洞 (實際程式碼中使用 5mm)
# 我目前設定的門檻是 0.005 公尺，也就是 5 毫米
# 如果一個結構，它離最近的訊號線的距離都還大於 5 毫米，我就認為它可以被移除
to_delete = [prim for prim, dist in poly_distances.items() if dist > 0.005]
```
這個 5 毫米的門檻值，使用者當然可以根據自己的設計特性和模擬需求來調整。例如，對於更高頻的訊號，或者更精密的結構，這個門檻可能就要設得更小一些。

**阿傑:** 了解，這個門檻是可調的。最後，就是執行刪除操作了。

**鳴志哥:** 對。腳本會遍歷這個 `to_delete` 列表，把裡面的每一個 EDB 物件 (空洞或零件) 呼叫它的 `delete()` 方法從 EDB 資料中移除。

```python
# %% 刪除這些 primitive 並儲存新的 EDB
for prim in to_delete:
    prim.delete()

# 最後，把修改後的 EDB 存成一個新的檔案，避免覆蓋原始檔
edb.save_edb_as("d:/demo/simp7.aedb")
```
我強烈建議大家總是儲存到一個新的檔案，這樣原始的設計檔案才能得到保留。

**阿傑:** 鳴志哥，聽您這樣詳細解說下來，這個腳本的思路非常清晰，而且確實解決了 SI 模擬中一個很實際的痛點。它可以幫助工程師在開始耗時的模擬之前，先對模型做一次有效的「瘦身」。

**鳴志哥:** 是的，這就是我的主要目的。透過移除這些對 SI 結果影響不大，卻會大量消耗計算資源的遠離結構，我們可以期望獲得更快的網格剖分速度和模擬時間，同時又盡可能地保持了 SI 分析的準確性。當然，這終究是一個輔助工具，使用者還是需要根據自己的專業判斷來設定合理的距離門檻，並且在執行後稍微檢查一下結果，確保沒有誤刪任何關鍵的設計部分。

**阿傑:** 非常感謝鳴志哥今天帶來這麼精彩的分享，不僅讓我們了解了這個實用腳本的來龍去脈，也學習到了許多 EDA 自動化開發的巧思。相信對我們的聽眾來說，這一定非常有啟發。

**鳴志哥:** 不客氣，也很高興能有這個機會跟大家交流。希望這個小工具能對大家在 SI 模擬工作上有所幫助。

**阿傑:** 再次感謝鳴志哥。也謝謝各位聽眾的收聽，我們下次「EDA 新攻略」再會！

### 範例程式

```python
from shapely.geometry import LineString, Polygon, box
from shapely.strtree import STRtree
from ansys.aedt.core import Edb

# 載入 AEDB 檔案
path = r"d:/demo/test.aedb"
edb = Edb(path, edbversion="2024.1")

# 擷取信號線段並建立 STRtree
lines = []
for net in edb.nets.signal_nets.values():
    for prim in net.primitives:
        lines.append(LineString(prim.center_line))
line_tree = STRtree(lines)

# 擷取所有 void polygon 與元件框線
polygons = {}
for net in edb.nets.power_nets.values():
    for prim in net.primitives:
        if prim.is_void:
            polygons[prim] = prim.points()

for _, comp in edb.components.components.items():
    x1, y1, x2, y2 = comp.bounding_box
    polygons[comp] = ([x1, x2, x2, x1], [y1, y1, y2, y2])

# 計算每個 polygon 與最近線段距離
poly_distances = {}
for prim, raw_pts in polygons.items():
    if isinstance(raw_pts, tuple) and len(raw_pts) == 2:
        coords = list(zip(*raw_pts))
    elif isinstance(raw_pts, list) and raw_pts and len(raw_pts[0]) == 2:
        coords = raw_pts
    else:
        continue

    try:
        poly = Polygon(coords)
    except Exception:
        continue

    minx, miny, maxx, maxy = poly.bounds
    search_box = box(minx - 0.01, miny - 0.01, maxx + 0.01, maxy + 0.01)
    idxs = line_tree.query(search_box)

    if len(idxs) > 0:
        candidate_lines = [lines[i] for i in idxs]
        min_dist = min(poly.distance(line) for line in candidate_lines)
    else:
        min_dist = float("inf")

    poly_distances[prim] = min_dist

# 刪除距離過遠的 primitive
to_delete = [prim for prim, dist in poly_distances.items() if dist > 0.001]
for prim in to_delete:
    prim.delete()

# 儲存新的 AEDB 檔案
edb.save_edb_as("d:/demo/simp6.aedb")
```

![2025-05-26_14-24-52](/assets/2025-05-26_14-24-52.png)