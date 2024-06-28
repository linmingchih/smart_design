讀取HFSS ffd檔案並計算Radiated Power
---

這段 Python 程式碼的目的是從一個指定的ffd檔案（HFSS遠場檔案）中提取電場數據，並計算總輻射功率。這裡的處理過程可以分為幾個主要步驟，我將逐一解釋每個步驟的功能和重要性： 
1. **導入模組和文件讀取** ： 
  - 這段程式首先導入了`product`函數用於產生所有角度的組合，`radians`和`sin`函數則用於角度轉換和計算。
 
  - 然後開啟一個名為`exportfields.ffd`的文件並讀取所有行至`text`變量中。
 
2. **讀取角度範圍和間隔** ： 
  - 文件的前兩行包含角度範圍和分割數，分別對應於`theta`（極角）和`phi`（方位角）。
 
  - 程式使用`map`函數將這些數據轉換為整數型態，並計算每個角度的間隔（`dtheta`和`dphi`）。
 
3. **生成角度列表** ： 
  - 利用列表推導式根據間隔生成`theta`和`phi`的完整列表。
 
4. **產生角度組合** ： 
  - 使用`product`函數生成`theta`和`phi`的所有可能組合。
 
5. **提取並轉換數據** ： 
  - 程式遍歷從文件第四行開始的每行數據，將每行分割後的數據轉換為複數形式的電場向量（`etheta`和`ephi`）。
 
6. **計算輻射功率** ：
  - 利用計算公式遍歷之前生成的數據列表，計算每個角度的貢獻，並累加計算總輻射功率。
 
  - 其中`377`是真空中的特性阻抗，`abs`函數用來計算複數的模，`sin`和`radians`用於角度的三角轉換。
 
7. **輸出結果** ： 
  - 最後將計算所得的功率除以`2`得到最終的輻射功率，並輸出。

這段程式碼的應用場景主要是在電磁場模擬和分析中，用於計算從天線或其他輻射源發射的總功率，這對於設計和驗證天線性能是非常重要的。



```python
from itertools import product
from math import radians, sin, pi
with open(r"D:\demo4\exportfields.ffd") as f:
    text = f.readlines()

theta0, theta, ntheta = map(int, text[0].strip().split())
phi0, phi, nphi = map(int, text[1].strip().split())

dtheta = (theta-theta0)/(ntheta-1)
dphi = (phi-phi0)/(nphi-1)

thetas = [i*dtheta + theta0 for i in range(ntheta)]
phis = [i*dphi + phi0 for i in range(nphi)]

angles = list(product(thetas, phis))

data = []
for (theta, phi), line in zip(angles, text[4:]):
    values = [float(v) for v in line.strip().split()]
    etheta = complex(*values[0:2])
    ephi = complex(*values[2:4])
    data.append((theta, phi, etheta, ephi))

power = 0
for theta, phi, etheta, ephi in data:
    power += (abs(etheta)**2 + abs(ephi)**2)/377 * sin(radians(theta))*radians(dtheta)*radians(dphi)

radiated_power = power / 2
print(radiated_power)
```

### 結果比較

比較HFSS結果與腳本輸出結果，誤差1%以內。
![2024-06-28_09-25-17](/assets/2024-06-28_09-25-17.png)