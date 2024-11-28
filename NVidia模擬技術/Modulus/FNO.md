Fourier Neural Operator（FNO）
---
Modulus Fourier Neural Operator（FNO）是一種深度學習技術，屬於神經算子（Neural Operator）家族，用於解決偏微分方程（PDE）問題。這類問題在工程和科學領域非常常見，特別是涉及流體動力學、熱傳遞和電磁場等物理模擬。FNO 的引入有效地降低了解決這些複雜數學問題的計算成本，並且其架構在許多應用場景下都展示出了良好的性能和效率。

### 概念與基本原理 

FNO 利用傅立葉變換來捕捉函數空間的全局特性，從而提高模型的泛化能力和效率。FNO 的基本理念是通過一個網絡來學習函數之間的映射，而不是僅僅局限於點對點的數據對應。這樣的方式使得它在面對不同初始條件和邊界條件時，仍然可以保持良好的預測能力。

具體來說，FNO 的核心步驟可以描述如下：
 
1. **空間傅立葉變換** ：
  - 對輸入數據進行傅立葉變換，將其轉換到頻域。這樣的變換有助於捕捉到整體行為和大範圍的交互信息。
 
2. **頻域上的線性變換** ：
  - 在頻域中，進行一系列線性操作來學習不同頻率下的特徵。這些操作用於捕捉全局的數據模式。
 
3. **逆傅立葉變換** ：
  - 將變換後的結果轉換回原始的空間域，以得到輸出的預測結果。

這些步驟使得 FNO 不再需要像傳統卷積神經網絡（CNN）那樣進行局部感受野操作，而是能夠通過傅立葉變換有效地進行全局信息的學習和傳遞。

### 優勢 
 
1. **高效學習全局信息** ：
FNO 可以捕捉全局的特徵，這意味著它在面對大尺度問題或具有複雜全域行為的 PDE 問題時，能夠比傳統的卷積網絡或 RNN 更具優勢。
 
2. **降低計算成本** ：
傳統數值方法如有限元素法（FEM）在求解 PDE 時的計算量巨大，而 FNO 可以通過神經網絡快速近似出結果，大幅降低計算時間。
 
3. **泛化能力強** ：
FNO 能夠學習函數之間的映射，這使它能夠在多種不同的初始條件下提供有效的解，具有較好的泛化能力。

### 應用 

FNO 在多種物理模擬中都有應用，包括：
 
- **流體動力學** ：例如用於預測不可壓縮流體的速度場。
 
- **結構力學** ：進行應力和應變分析。
 
- **熱傳導問題** ：模擬材料中的熱流分佈。

在 ANSYS Modulus 框架中，FNO 為物理模擬提供了一種高效且可擴展的數學工具，能夠與傳統的模擬工具結合，提供高效的結果預測，特別是在需要多次求解或大量設計空間搜索的情況下。

### 範例
```python
# [imports]
import torch

import modulus
from modulus.datapipes.benchmarks.darcy import Darcy2D
from modulus.metrics.general.mse import mse
from modulus.models.fno.fno import FNO

# [imports]

# [code]
normaliser = {
    "permeability": (1.25, 0.75),
    "darcy": (4.52e-2, 2.79e-2),
}
dataloader = Darcy2D(
    resolution=256, batch_size=32, nr_permeability_freq=5, normaliser=normaliser
)

batch = next(iter(dataloader))

#%%
import matplotlib.pyplot as plt
import torch

# 假設我們有 dataloader 和批次資料
for batch in dataloader:
    darcy_tensor = batch['darcy']  # 取出 'darcy' 的資料
    permeability_tensor = batch['permeability']  # 取出 'permeability' 的資料
    break  # 我們只看第一批資料

# 將張量從 GPU 移動到 CPU，然後轉換為 NumPy 數組
for i in range(32):
    darcy_sample = darcy_tensor[i, 0, :, :].cpu().numpy()
    permeability_sample = permeability_tensor[i, 0, :, :].cpu().numpy()
    
    # 創建並排的子圖
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Darcy 影像顯示
    ax1 = axes[0]
    im1 = ax1.imshow(darcy_sample, cmap='viridis')
    ax1.set_title('Darcy Tensor Visualization')
    ax1.set_xlabel('Width')
    ax1.set_ylabel('Height')
    fig.colorbar(im1, ax=ax1, orientation='vertical')
    
    # Permeability 影像顯示
    ax2 = axes[1]
    im2 = ax2.imshow(permeability_sample, cmap='viridis')
    ax2.set_title('Permeability Tensor Visualization')
    ax2.set_xlabel('Width')
    ax2.set_ylabel('Height')
    fig.colorbar(im2, ax=ax2, orientation='vertical')
    
    # 顯示圖形
    plt.tight_layout()
    plt.show()
```
![2024-11-28_10-54-11](/assets/2024-11-28_10-54-11.png)


## 完整訓練
```python
# [imports]
import torch

import modulus
from modulus.datapipes.benchmarks.darcy import Darcy2D
from modulus.metrics.general.mse import mse
from modulus.models.fno.fno import FNO

# [imports]

# [code]
normaliser = {
    "permeability": (1.25, 0.75),
    "darcy": (4.52e-2, 2.79e-2),
}
dataloader = Darcy2D(
    resolution=256, batch_size=32, nr_permeability_freq=5, normaliser=normaliser
)  # 減小批次大小以減少記憶體使用量
model = FNO(
    in_channels=1,
    out_channels=1,
    decoder_layers=1,
    decoder_layer_size=32,
    dimension=2,
    latent_channels=16,  # 減少潛在通道數以減少記憶體使用量
    num_fno_layers=4,
    num_fno_modes=12,
    padding=5,
).to("cuda")

optimizer = torch.optim.Adam(model.parameters(), lr=0.05)
scheduler = torch.optim.lr_scheduler.LambdaLR(
    optimizer, lr_lambda=lambda step: 0.85**step
)

# 執行 100 次迭代
for i in range(100):
    batch = next(iter(dataloader))
    true = batch["darcy"].to("cuda")  # 確保張量被移動到 GPU
    pred = model(batch["permeability"].to("cuda"))
    loss = mse(pred, true)
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()  # 清除梯度以避免累積
    scheduler.step()

    print(f"Iteration: {i}. Loss: {loss.detach().cpu().numpy()}")
# [code]
torch.save(model.state_dict(), "fno_darcy_trained_model.pth")  # 儲存訓練好的模型


#%%
import matplotlib.pyplot as plt
# 載入訓練好的模型進行推論
model.load_state_dict(torch.load("fno_darcy_trained_model.pth"))
model.eval()  # 將模型設定為評估模式

# 獲取一批資料進行推論
batch = next(iter(dataloader))
permeability = batch["permeability"].to("cuda")
true_darcy = batch["darcy"].to("cuda")

# 使用訓練好的模型進行預測
pred_darcy = model(permeability)

# 將張量移動到 CPU 進行繪圖
permeability = permeability.detach().cpu().numpy()[0, 0]
true_darcy = true_darcy.detach().cpu().numpy()[0, 0]
pred_darcy = pred_darcy.detach().cpu().numpy()[0, 0]

# 繪製滲透率、真實 Darcy 場和預測的 Darcy 場
fig, axs = plt.subplots(1, 3, figsize=(18, 6))

axs[0].imshow(permeability, cmap='viridis')
axs[0].set_title('滲透率')
axs[0].axis('off')

axs[1].imshow(true_darcy, cmap='viridis')
axs[1].set_title('真實 Darcy 場')
axs[1].axis('off')

axs[2].imshow(pred_darcy, cmap='viridis')
axs[2].set_title('預測 Darcy 場')
axs[2].axis('off')

plt.show()
# [code]

```

這段迴圈會運行 20 次，每次訓練模型一步。讓我們逐步解釋每一行的作用：
 
1. **`for i in range(20):`** ： 
  - 這是一個 `for` 迴圈，用來進行 20 次迭代訓練。
 
  - 變數 `i` 是一個迴圈計數器，從 0 開始到 19，總共 20 次迴圈。
 
2. **`batch = next(iter(dataloader))`** ：
  - 這行代碼從 dataloader 中獲取下一個批次的資料。
 
  - `dataloader` 是一個生成器物件，它會生成一個包含多個樣本的批次。
 
  - `iter(dataloader)` 創建一個迭代器，`next()` 從這個迭代器中獲取下一批資料。

  - 這個批次資料包含了兩個主要部分：'permeability'（滲透率）和 'darcy'（達西的結果）。
 
3. **`true = batch["darcy"]`** ： 
  - 從批次資料中取出 `'darcy'` 的資料，作為模型的 "真實值"（ground truth）。
 
  - `true` 是我們用來比較模型輸出的正確答案，在這裡它代表了達西定律的數值解。
 
4. **`pred = model(batch["permeability"])`** ： 
  - 使用模型 `model` 來對 `batch['permeability']` 進行預測。
 
  - `model` 是一個 Fourier Neural Operator（FNO），可以輸入滲透率資料並預測相應的達西數據。
 
  - 這行代碼中，`pred` 就是模型根據輸入的滲透率資料給出的預測達西結果。
 
5. **`loss = mse(pred, true)`** ： 
  - 計算預測值 `pred` 和真實值 `true` 之間的誤差，這裡使用均方誤差（Mean Squared Error，MSE）作為損失函數。
 
  - `loss` 反映了模型預測值與真實值之間的差距，值越小表示模型預測的效果越好。
 
6. **`loss.backward()`** ：
  - 計算損失相對於模型參數的梯度。

  - 這些梯度用來更新模型參數，使得模型能夠更好地學習並縮小預測和真實值之間的誤差。

  - 這是反向傳播過程的一部分，用於優化模型的參數。
 
7. **`optimizer.step()`** ： 
  - 使用計算出的梯度來更新模型的參數，這裡的 `optimizer` 是 Adam 優化器。
 
  - `optimizer.step()` 根據參數的梯度以及學習率來進行參數的更新，這是模型訓練的核心過程之一。
 
8. **`scheduler.step()`** ： 
  - `scheduler` 用來調整學習率，這裡採用的是 LambdaLR 調度器。
 
  - 每次迭代後，`scheduler.step()` 會根據預先定義的規則來更新學習率。這裡的規則是每次迭代將學習率乘以 0.85。

  - 這樣的調整方式有助於在訓練過程中逐步減少學習率，以更精細地調整模型。
 
9. **`print(f"Iteration: {i}. Loss: {loss.detach().cpu().numpy()}")`** ：
  - 這行代碼用來在每次迭代後輸出當前的迭代次數和損失值，幫助我們追蹤模型訓練的過程。
 
  - `loss.detach().cpu().numpy()` 將張量轉換為 NumPy 格式，並確保從 GPU 中移到 CPU，這樣可以便於顯示和儲存。
 
  - `f"Iteration: {i}. Loss: {loss.detach().cpu().numpy()}"` 使用了 Python 的 f-string 格式，可以方便地插入變數的值來生成輸出訊息。

這個 `for` 迴圈的主要目的是訓練模型，使得模型在 20 次迭代之後逐步學習如何根據滲透率預測達西數據。每一步都包括資料擷取、模型預測、損失計算、梯度反向傳播、參數更新和學習率調整等過程。透過這樣的反覆訓練，模型的預測能力將會逐步提高，並且損失值應隨著迭代次數的增加而減少。

![2024-11-28_16-11-47.png](/assets/2024-11-28_16-11-47.png)


