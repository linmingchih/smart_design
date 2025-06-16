自動化建立 RLC 元件 Edge Port 的 AEDT 腳本
---

本腳本設計的目的是協助使用者在 ANSYS Electronics Desktop（AEDT）環境中，自動為具有兩個 pins 的 RLC 元件建立對應的 Edge Port，以利後續 HFSS 模擬使用。腳本執行前，**使用者需先手動於版圖中選取欲建立 Port 的 RLC 元件**，腳本會依據這些選取的元件逐一進行處理。

首先，腳本會擷取每個元件的 padstack 定義，從中判斷其形狀是否為矩形（Rct）或方形（Sq），並換算實際幾何尺寸。接著，透過 Stackup 結構取得元件所在的放置層與其對應 Layer ID。為避免模擬時 RLC 元件與 Port 衝突，腳本會自動停用元件原有的模型資訊（Disable Model Info）。

接下來，根據元件本身的擺放角度與 pin 的相對位置，計算其實際方向，並依照 padstack 尺寸與方向差（theta）自動建立一組 Edge Port。該 Port 會由兩條對稱邊界構成，並以 `port_元件名稱` 命名，方便辨識與後處理。

整體而言，本腳本可大幅減少手動建立 Port 的操作時間，並確保建立的幾何與方向正確一致，是進行 batch 模擬或多元件分析時的高效輔助工具。

[腳本下載](/assets/createEdgePorts.py)

![2025-06-16_08-58-59](/assets/2025-06-16_08-58-59.png)