EDB 路徑轉換程式
---

EDB當中路徑含有圓弧(archeight)與直線資訊，以下函數可將其轉換為連續可繪製的幾何座標點序列。

## **目的**

此程式的目的是解析一段由直線與圓弧組成的路徑，並根據給定的最大角度限制 (theta_max)，將圓弧離散化為一連串可繪製的點，最終產生一個連續的座標點陣列，方便用於繪圖或路徑規劃。

### 功能

* 解析混合直線與圓弧的路徑資料。
* 根據圓弧高度自動判斷圓弧段。
* 將圓弧以最大角度間距進行切分（細分為小線段）。
* 回傳最終平滑連續的路徑座標點。

### 流程架構

1. **輸入資料格式**：

   * 使用一串座標點 (x, y) 表示路徑。
   * 其中 `y` 值為一個極大值（如 `1e100`）代表這是一個圓弧的高度點（sagitta），用來與前後兩點定義一段圓弧。

2. **資料預處理**：

   * 若開頭或結尾是 arc-height 點，則會補上對應的前後端點，避免處理時出錯。

3. **路徑解析 (_parse_segments)**：

   * 逐點檢查是否為圓弧段或直線段。
   * 若偵測到 arc-height 點，則透過 `_arc_points` 計算離散化的圓弧座標點。
   * 否則直接加入直線點。

4. **圓弧計算 (_arc_points)**：

   * 根據端點 `p0`, `p2` 和 sagitta 高度 `h` 計算圓心與半徑。
   * 判斷方向（順時針或逆時針），以確保路徑通過 sagitta。
   * 使用最大角度 `theta_max` 將整段圓弧切成多個點。
   * 回傳切分後的點陣列。

5. **畫圖展示**：

   * 使用 `matplotlib` 繪製轉換後的路徑座標。

### 補充說明

* **Arc Flag 判斷法**：

  * 使用極大值 `1e100` 作為 `y` 值，來判定該點為 arc-height（弓高點），這是一種特殊的標記技巧。

* **角度計算方式**：

  * 使用 `arctan2` 及模運算將角度保持在 0 到 2π 之間，並透過角度差判斷方向。

* **圓弧細分技巧**：

  * 根據圓心角的大小，決定切分幾段，確保每段角度不超過設定的 `theta_max`。

* **numpy 與向量運算**：

  * 利用 `numpy` 進行向量與座標運算，提高效率與簡潔度。

### 範例程式

```python
import numpy as np

class PathParser:
    ARC_FLAG = 1e100

    def __init__(self, points, theta_max):
        """
        points    : list of (x, y)
        theta_max : max central angle (radian) between adjacent arc points
        """
        self.raw_points = list(points)
        self.theta_max = theta_max

    # ---------- public API ----------

    def parse(self):
        """
        Main entry:
        returns Nx2 numpy array of geometry points
        """
        pts = self._normalize_arc_endpoints(self.raw_points)
        return self._parse_segments(pts)

    # ---------- arc / line detection ----------

    @classmethod
    def _is_arc_height(cls, pt):
        return pt[1] >= cls.ARC_FLAG

    def _normalize_arc_endpoints(self, points):
        """
        If first point is arc-height:
            prepend last point
        If last point is arc-height:
            append first point
        """
        pts = list(points)

        if len(pts) < 2:
            return pts

        if self._is_arc_height(pts[0]):
            pts.insert(0, pts[-1])

        if self._is_arc_height(pts[-1]):
            pts.append(pts[0])

        return pts

    # ---------- core parsing ----------

    def _parse_segments(self, pts):
        result = []
        i = 0

        while i < len(pts) - 1:
            p = pts[i]
            n = pts[i + 1]

            # arc case: real -> arc-height -> real
            if (not self._is_arc_height(p)) and self._is_arc_height(n):
                h = n[0]
                p2 = pts[i + 2]
                arc_pts = self._arc_points(p, p2, h)

                if result:
                    arc_pts = arc_pts[1:]  # avoid duplicate
                result.extend(arc_pts)
                i += 2

            # line case
            else:
                if not result:
                    result.append(np.array(p, float))
                else:
                    result.append(np.array(n, float))
                i += 1

        return np.array(result)

    # ---------- arc geometry ----------

    def _arc_points(self, p0, p2, h):
        """
        Discretize arc defined by p0, p2 and arc-height h
        """
        p0 = np.array(p0, float)
        p2 = np.array(p2, float)

        v = p2 - p0
        L = np.linalg.norm(v)
        if L == 0:
            raise ValueError("Zero-length arc")

        if h == 0:
            return np.vstack([p0, p2])

        M = (p0 + p2) / 2
        n_left = np.array([-v[1], v[0]]) / L

        s = abs(h)
        R = (L**2) / (8*s) + s/2
        d = np.sqrt(max(R**2 - (L/2)**2, 0.0))

        # sagitta point (your rule)
        S = M + h * n_left

        # circle center (opposite side of sagitta)
        C = M - np.sign(h) * d * n_left

        def ang(p):
            return np.mod(np.arctan2(p[1]-C[1], p[0]-C[0]), 2*np.pi)

        th0 = ang(p0)
        th2 = ang(p2)
        ths = ang(S)

        def ccw(a, b):
            return (b - a) % (2*np.pi)

        # choose direction so arc passes through sagitta
        go_ccw = ccw(th0, ths) <= ccw(th0, th2)

        if go_ccw:
            total = ccw(th0, th2)
            sign = +1
        else:
            total = ccw(th2, th0)
            sign = -1

        nseg = max(1, int(np.ceil(total / self.theta_max)))
        dth = total / nseg

        t = th0 + sign * np.arange(nseg + 1) * dth
        return np.c_[C[0] + R*np.cos(t), C[1] + R*np.sin(t)]

import matplotlib.pyplot as plt
coords = [
    (-4, 0),
    (1, 1e100),
    (0, 0),
    (-1, 1e100), 
    (4, 0),
]

parser = PathParser(coords, theta_max=np.deg2rad(10)) 
pts = parser.parse()

plt.plot(pts[:,0], pts[:,1], "-o")
plt.axis("equal")
plt.grid(True)
plt.show()
```

這段程式碼會將原始路徑轉換為順暢的連續座標點，並將其可視化繪製出來。

![](/assets/2025-12-21_21-07-21.png)

![](/assets/Figure%202025-12-21%20205122.png)


```python
import sys
from pyedb import Edb

edb = Edb(version='2024.1')
edb.stackup.add_layer('Top')

infn = sys.float_info.max
pts = [(-4, 0), (1, infn), (0, 0), (-1, infn), (4, 0)]
edb.modeler.create_trace(pts, 'Top', width='0.1')

edb.save_edb_as('d:/demo/test6.aedb')
```