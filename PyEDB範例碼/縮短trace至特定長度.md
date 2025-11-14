縮短trace至特定長度
---

這段程式主要是在處理一條由「直線 + 圓弧」組成的走線中心線（center_line），
讓你可以依指定長度，從前端或後端「只保留一段指定長度」的線路，
並將修剪後的中心線套用到 Ansys EDB（pyedb）中的走線 primitive 上，最後另存為新的 .aedb 專案。

### 功能

* 以兩端點與弧高（sagitta, h）計算圓弧的圓心與半徑。
* 計算圓弧的弧長、起始角度與弧角大小。
* 在圓弧上只保留指定弧長，求出新的端點座標與更新後的弧高。
* 支援一條 center_line 同時包含：

  * 一般直線線段
  * 圓弧線段（以 [h, MAXF] 這種特殊節點表示）
* 提供「由前端保留固定長度」與「由後端保留固定長度」兩種修剪模式。
* 與 pyedb 整合：

  * 建立 stackup 與 Top 層
  * 建立一條依 centerline 描述的 trace
  * 複製 trace、修改其 center_line 為修剪後結果
  * 儲存成新的 .aedb 專案

### 流程架構

1. **幾何計算工具層（圓弧相關）**

   * `dist(a, b)`

     * 計算平面上兩點距離，底層用 `math.hypot` 實作。
   * `arc_center_from_sagitta(p1, p2, h)`

     * 已知兩端點 `p1`、`p2` 與有號弧高 `h`（sagitta），
       先用幾何公式算出圓半徑 `R`，再求圓心 `(cx, cy)`。
     * `h > 0`／`h < 0` 代表弧向量在基準線上方或下方，
       透過右手法向量 `nx, ny` 搭配 `sign` 決定圓心在法線哪一側。
   * `arc_length_and_geometry(p1, p2, h)`

     * 先呼叫 `arc_center_from_sagitta` 得到圓心、半徑。
     * 以 `atan2` 求 `p1`、`p2` 相對圓心的極座標角度 `a1`, `a2`。
     * 調整角度差 `diff`（落在 `(-π, π]` 範圍）避免繞錯方向。
     * 回傳弧長 `L = |diff| * R` 以及幾何資訊 `(cx, cy, R, a1, diff)`。
   * `trim_arc(p1, p2, h, keep_len)`

     * 針對單一弧段，沿著弧從 `p1` 出發，只保留弧長 `keep_len`。
     * 若 `keep_len >= L` → 整段弧保留。
     * 若 `keep_len <= 0` → 退化為點（回到 p1, h=0）。
     * 中間情況：

       * 用比例 `t = keep_len / L` 計算新的角度 `a_new = a1 + diff * t`。
       * 以圓心與半徑算出新端點 `new_p2`。
       * 再依新端點與 `p1` 反推對應的弧高 `h_new`，保持原本弧方向符號。

2. **center_line 修剪邏輯**
   center_line 採用如下資料結構來同時表達直線與圓弧：

   * 直線：

     * 兩個連續點，例如 `[x1, y1]`, `[x2, y2]` 代表一段直線。
   * 圓弧：

     * 使用三個連續元素：`p1`, `[h, MAXF]`, `p2`
     * `[h, MAXF]` 這個節點的第二欄是 `sys.float_info.max`（程式中命名為 `MAXF`）
       → 代表「這是一個弧段，中間這個點不是實體座標，而是弧高 h 的標記」。

   主要的處理流程：

   * `_trim_front(center_line, keep_length)`

     * 從 center_line 的開頭往後掃描，逐段累積長度：

       * 若偵測到 pattern `p1, [h, MAXF], p2` → 當作弧段處理。

         * 先用 `arc_length_and_geometry` 算弧長 `L`。
         * 若 `remaining >= L` → 整段弧保留，直接加入 new_line。
         * 若 `remaining < L` → 呼叫 `trim_arc` 只留前面 `remaining` 長度，
           把新弧段的 `[new_h, MAXF]` 與 `new_p2` 加入 new_line，然後結束。
       * 否則就當作直線：

         * 計算兩點距離 `L`。
         * 若 `remaining >= L` → 整段直線加入 new_line。
         * 若 `remaining < L` → 在此直線段內插值算出「剪斷位置」的座標，
           把該點加入 new_line 後結束。
     * 回傳只保留前端 `keep_length` 長度的新 center_line。

   * `_reverse_center_line(cl)`

     * 將一條 center_line 反向，同時照顧圓弧的方向：

       * 對於弧段 pattern `[..., p1, [h, MAXF], p2]`：

         * 反向時變成 `[..., p2, [-h, MAXF], p1]`。
         * 把弧高 `h` 取負，以維持幾何方向一致。
       * 直線點則單純反向。

   * `trim_center_line(center_line, keep_length, mode="front" | "back")`

     * 封裝對外的 API：

       * `mode="front"`：直接呼叫 `_trim_front`，保留前端。
       * `mode="back"`：

         1. 先 `_reverse_center_line` 反轉
         2. 用 `_trim_front` 在「反向後」的前端修剪
         3. 再 `_reverse_center_line` 反轉回來
       * 這樣就能重用前端修剪邏輯來實作「保留尾端」。

3. **與 pyedb / Edb 的整合流程**

   * 建立 Edb 物件與層：

     * `edb = Edb(version='2024.1')`
     * `edb.stackup.add_layer('Top')` 新增一個 Top 導體層。
   * 建立一條原始 centerline：

     * 範例中的 `centerline` 使用字串單位（例如 `'2mm'`、`'4mm'`），
       並插入 `[h, sys.float_info.max]` 當作圓弧高度標記：

       * `(0, 0)` → 起點
       * `('2mm', 0)` → 直線到 x=2mm
       * `('0.5mm', MAXF)` → 以 0.5mm 弧高定義接下來與前一點的弧段
       * `('4mm', '1mm')` → 弧段終點
       * `('5mm', '6mm')` → 直線
       * `('-0.5mm', MAXF)` + `('10mm', '3mm')` → 另一段反方向弧
   * 用 centerline 建立 trace：

     * `trace = edb.modeler.create_trace(centerline, 'Top', width='0.1mm')`
     * pyedb 會負責把這條含直線與弧段的中心線轉成 Edb primitive。
   * 複製 trace 並只保留尾端一小段：

     * `x = trace.clone()` 建立複本。
     * 從 `edb.modeler.primitives` 中找到剛剛 clone 出來的 primitive（用 id 比對）。
     * `cloned.center_line = trim_center_line(trace.center_line, 0.013, mode='back')`

       * 取得原 trace 的數值 center_line（通常已轉成 Edb 使用的座標單位）。
       * 呼叫 `trim_center_line`，以 `keep_length=0.013`，`mode='back'` 表示只保留尾端 0.013（對應單位的）長度。
       * 將修剪後的 center_line 指派給複製的 primitive，得到一條只保留尾端短段的走線。
   * 存檔：

     * `edb.save_edb_as('d:/demo/test.aedb')` 把專案存到指定路徑。

### 補充說明

* **弧高（sagitta, h）概念**

  * 若以 `p1`、`p2` 兩點作為 chord（弦），弧高是 chord 中點到圓弧上對應點的垂直距離。
  * 此程式用 `h` 的正負號來代表弧在 chord 的哪一側（上方或下方）。

* **MAXF 作為圓弧標記**

  * `MAXF = sys.float_info.max` 是 Python 可表示的最大浮點數，幾乎不可能在正常座標中出現。
  * 利用 `點[1] == MAXF` 這個條件作為「這一個節點是弧高資訊，而不是實際座標」的旗標。

* **center_line 的資料型別**

  * 在 pyedb 建立 trace 時，centerline 允許使用字串單位（例如 `'2mm'`）。
  * 但在幾何計算（`trim_center_line` 一側）會操作 `trace.center_line`，
    實務上會是 Edb 已經轉換好的數值座標（例如公尺）。
  * 若要直接把自訂的 center_line 丟給 `trim_center_line` 做幾何計算，
    需先自行做單位轉換成純數值（float）。

* **反向弧段時弧高取負號的原因**

  * 反向 center_line 代表「走線方向反轉」，弧的前後端點互換。
  * 為了讓弧在幾何上仍然向同一側偏折，需要同時把弧高 `h` 取負，
    這樣在 `arc_center_from_sagitta` 裡面計算圓心時，會落到相同物理位置。

* **Python 語法小提醒**

  * `center_line[0][:]`：複製第一個點的 list 內容（避免直接引用同一個物件）。
  * list comprehension：`[i for i in edb.modeler.primitives if i.id == x.GetId()]` 是一種簡潔寫法，用來從集合中篩選出符合條件的元素。
  * `math.atan2(y, x)`：回傳對應向量 `(x, y)` 的極座標角度，可處理完整象限，適合做圓弧角度計算。

### 範例程式

```python
import math
import sys

MAXF = sys.float_info.max

def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def arc_center_from_sagitta(p1, p2, h):
    """由兩端點 + 有號弧高 h 求圓心與半徑"""
    H = abs(h)
    d = dist(p1, p2)
    if d == 0:
        raise ValueError("Arc endpoints must not be identical.")

    R = d*d/(8.0*H) + H/2.0

    dx = (p2[0] - p1[0]) / d
    dy = (p2[1] - p1[1]) / d

    nx, ny = dy, -dx       # 右手法向量
    sign = 1.0 if h >= 0 else -1.0

    mx = (p1[0] + p2[0]) / 2.0
    my = (p1[1] + p2[1]) / 2.0

    cx = mx + sign * (R - H) * nx
    cy = my + sign * (R - H) * ny

    return cx, cy, R


def arc_length_and_geometry(p1, p2, h):
    """回傳 (弧長 L, 圓心 cx,cy, 半徑 R, 起始角 a1, 弧角 diff)"""
    cx, cy, R = arc_center_from_sagitta(p1, p2, h)

    a1 = math.atan2(p1[1] - cy, p1[0] - cx)
    a2 = math.atan2(p2[1] - cy, p2[0] - cx)

    diff = a2 - a1
    if diff <= -math.pi:
        diff += 2.0 * math.pi
    elif diff > math.pi:
        diff -= 2.0 * math.pi

    L = abs(diff) * R
    return L, (cx, cy, R, a1, diff)


def trim_arc(p1, p2, h, keep_len):
    """從 p1 沿弧保留 keep_len，回傳 new_p2, new_h"""
    L, (cx, cy, R, a1, diff) = arc_length_and_geometry(p1, p2, h)

    if keep_len >= L:
        return p2, h

    if keep_len <= 0:
        return p1, 0.0

    t = keep_len / L
    a_new = a1 + diff * t

    x_new = cx + R * math.cos(a_new)
    y_new = cy + R * math.sin(a_new)
    new_p2 = (x_new, y_new)

    d_new = dist(p1, new_p2)
    inside = max(R*R - (d_new/2.0)**2, 0.0)
    H_new = R - math.sqrt(inside)

    sign = 1.0 if h >= 0 else -1.0
    h_new = sign * H_new

    return new_p2, h_new


def _trim_front(center_line, keep_length):
    """前端保留的實作"""
    new_line = [center_line[0][:]]
    remaining = keep_length
    i = 0

    while i < len(center_line) - 1 and remaining > 0:

        # arc segment
        if i + 2 < len(center_line) and center_line[i+1][1] == MAXF:
            p1 = center_line[i]
            h  = center_line[i+1][0]
            p2 = center_line[i+2]

            L, _ = arc_length_and_geometry(p1, p2, h)

            if remaining >= L:
                new_line.append([h, MAXF])
                new_line.append(list(p2))
                remaining -= L
                i += 2
            else:
                new_p2, new_h = trim_arc(p1, p2, h, remaining)
                new_line.append([new_h, MAXF])
                new_line.append([new_p2[0], new_p2[1]])
                return new_line

        else:
            # straight line
            p1 = center_line[i]
            p2 = center_line[i+1]
            L = dist(p1, p2)

            if remaining >= L:
                new_line.append(list(p2))
                remaining -= L
                i += 1
            else:
                t = remaining / L
                x = p1[0] + (p2[0] - p1[0]) * t
                y = p1[1] + (p2[1] - p1[1]) * t
                new_line.append([x, y])
                return new_line

    return new_line


def _reverse_center_line(cl):
    """將 center_line 反向（含 arc）"""
    out = []
    i = len(cl) - 1
    while i >= 0:
        if i - 2 >= 0 and cl[i-1][1] == MAXF:
            # arc: [..., p1, [h, MAXF], p2]
            p2 = cl[i]
            h  = cl[i-1][0]
            p1 = cl[i-2]

            out.append([p2[0], p2[1]])
            out.append([-h, MAXF])        # 方向反轉 → arc_height 取負
            out.append([p1[0], p1[1]])

            i -= 3
        else:
            out.append([cl[i][0], cl[i][1]])
            i -= 1
    return out


def trim_center_line(center_line, keep_length, mode="front"):
    """
    mode = "front" → 保留前端
    mode = "back"  → 保留後端（尾端）
    """

    if mode == "front":
        return _trim_front(center_line, keep_length)

    elif mode == "back":
        # step 1: reverse
        rev = _reverse_center_line(center_line)
        # step 2: trim front
        trimmed = _trim_front(rev, keep_length)
        # step 3: reverse back
        return _reverse_center_line(trimmed)

    else:
        raise ValueError("mode must be 'front' or 'back'")

from pyedb import  Edb
import sys
edb = Edb( version='2024.1')

edb.stackup.add_layer('Top')
centerline = [(0,0), 
              ('2mm', 0), 
              ('0.5mm', sys.float_info.max),  
              ('4mm','1mm'),
              ('5mm', '6mm'),
              ('-0.5mm', sys.float_info.max),              
              ('10mm','3mm')]

trace = edb.modeler.create_trace(centerline, 'Top', width='0.1mm')
x = trace.clone()

cloned = [i for i in edb.modeler.primitives if i.id == x.GetId()][0] 
cloned.center_line = trim_center_line(trace.center_line, 0.013, mode='back')

edb.save_edb_as('d:/demo/test.aedb',)
```

![](/assets/2025-11-14_17-23-40.png)