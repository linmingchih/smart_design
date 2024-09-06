Maxwell_PCB_Litz_Wire
---

《Design and Optimization with Litz Wire Version of PCB in Solid-State Transformer》，由Zheqing Li、Feng Jin、Xin Lou、Yi-Hsun Hsieh、Qiang Li以及Fred C. Lee合著，發表於IEEE相關會議。本研究團隊來自Virginia Polytechnic and State University的Center for Power Electronic Systems。

研究焦點在於提出一種新的PCB（印刷電路板）繞線設計，使用Litz線的結構來優化固態變壓器的效能。Litz線因其特殊的絞合和交織結構，適合於高頻電流的應用，有效減少高功率應用中的繞組損耗。本文中，研究人員將Litz線結構應用於PCB繞線中，並詳細說明了其設計過程與優化方法。

以下PyAEDT腳本用來在Maxwell當中生成類似論文當中的結構。

```python
from math import cos, sin, pi
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
from math import sqrt, atan2, degrees
# 1, 5, 7, 11, 13, 17, 19, 23, 25, 29, 31, 35, 37, 41, 43, 47, 49, 53, 55, 59, 61, 65, 67, 71

n = 13
d = 4
gap = 1
w = 0.4
r0 = 12
r1 = 22

pts0 = [(r0*cos(i*pi/36+pi/72), r0*sin(i*pi/36+pi/72)) for i in range(72)]
pts1 = [(r1*cos(i*pi/36), r1*sin(i*pi/36)) for i in range(72)]


def find_offset_center(x0, y0, x1, y1, d):
    # 計算中心點
    xm = (x0 + x1) / 2
    ym = (y0 + y1) / 2
    
    # 從 (x0, y0) 到 (x1, y1) 的向量
    dx = x1 - x0
    dy = y1 - y0
    
    # 向量的長度
    L = sqrt(dx**2 + dy**2)
    
    # 計算垂直向量並乘以偏移距離 d
    dx_prime = d * dy / L
    dy_prime = -d * dx / L
    
    # 計算最終的偏移座標
    xc = xm + dx_prime
    yc = ym + dy_prime
    
    return xc, yc


k = 0
top = []
bot = []
for i in range(72):
    x0, y0 = pts0[k]
    k = (k + n) % 72
    x1, y1 = pts1[k]
    xc, yc = find_offset_center(x0, y0, x1, y1, d)
    plt.plot((x0, xc, x1), (y0, yc, y1), c='r')
    top.append(((x0, y0), (xc, yc), (x1, y1)))
    k = (k + n-1) % 72
    x0, y0 = pts0[k]
    xc, yc = find_offset_center(x1, y1, x0, y0, d)
    plt.plot((x1, xc, x0), (y1, yc, y0), c='b')
    bot.append(((x1, y1), (xc, yc), (x0, y0)))

from pyaedt import Maxwell3d
maxwell = Maxwell3d(version='2024.2')

for pts in top:
    x0, y0 = pts[0]
    maxwell.modeler.create_cylinder('XY', [x0, y0, -0.01], w/2, gap+0.02, material='copper')
    maxwell.modeler.create_polyline(points=[(x, y, 0) for x, y in pts],
                                 segment_type="Arc",
                                 xsection_type='Rectangle',
                                 xsection_width=w,
                                 xsection_height=0.02,
                                 xsection_bend_type=0.2,
                                 material='copper')

for pts in bot:
    x0, y0 = pts[0]
    maxwell.modeler.create_cylinder('XY', [x0, y0, -0.01], w/2, gap+0.02, material='copper')
    maxwell.modeler.create_polyline(points=[(x, y, gap) for x, y in pts],
                                 segment_type="Arc",
                                 xsection_type='Rectangle',
                                 xsection_width=w,
                                 xsection_height=0.02,
                                 xsection_bend_type=0.2,
                                 material='copper')


```

![2024-09-06_13-34-35](/assets/2024-09-06_13-34-35.png)