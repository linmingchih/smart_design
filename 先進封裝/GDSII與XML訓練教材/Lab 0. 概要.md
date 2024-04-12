Lab 0. 概要
---
隨著人工智能技術的飛速發展，高性能計算需求亦急劇增加，這直接推動了CoWoS（Chip on Wafer on Substrate）和Interposer技術的崛起。CoWoS 是一種先進的封裝技術，能夠將多個矽晶片整合到一個中介層上，這種配置不僅提高了芯片之間的連接密度，還顯著改善了信號的傳輸效率和整體性能。

Interposer作為一種關鍵的中介材料，其功能是連接晶片與基板，為高密度的電路提供物理和電氣支持。AI加速器對計算速度和數據傳輸速度的極高要求，使得這些技術成為實現高效能AI處理不可或缺的一部分。因此，半導體業界對Interposer的設計與模擬需求急劇增加，工程師必須能夠掌握電子性能與熱管理準確模擬工具，以確保Interposer設計的可靠性與效能，滿足現代電子產品對空間與性能的雙重要求。

ANSYS作為物理工程模擬的領導者，旗下的AEDT (ANSYS Electronics Desktop) 集成了多物理計算引擎，包括HFSS、Icepak、RaptorX和Mechanical等，已在業界享有盛譽。這些工具提供了從高頻電磁場模擬到熱分析、結構分析以及信號完整性分析的全方位解決方案，極大地增強了設計師在進行集成電路（IC）級電子設計時的分析能力。

![2024-04-12_19-17-46](/assets/2024-04-12_19-17-46.png)


本教材旨在提供從設計導入、建模到模擬設置的全面指導，專注於解釋和展示如何在AEDT當中有效進行電子元件的模擬流程。特別針對Interposer的設計，我們會詳細介紹如何處理和轉換標準的GDS格式文件。GDS格式主要用於記錄2D工藝資訊，例如圖層和幾何圖形，但它不包含材料特性、堆疊結構或端口配置等對於進行電磁分析至關重要的資訊。

為了構建一個完整且可用於HFSS電磁分析的模型，必須將GDS文件與技術文件（tech file）結合使用。技術文件補充了GDS格式中缺少的信息，如材料的電磁特性、組件的三維堆疊資訊以及連接端口的詳細設定。通過這種方式，工程師能夠創建出更精確的三維模型，進而進行有效的模擬分析。

本教材將通過實例來展示這一整合過程，從基本的檔案讀取和處理開始，到進階的模擬技術應用，使學習者能夠掌握從2D平面設計到3D模擬分析的完整轉換過程。這將為處理先進封裝設計提供實用的知識和技能。

### HFSS IC Mode

應對IC與Interposer模擬與分析挑戰，HFSS引入了IC模式，具有以下幾個特點： 
1. **多層平面結構的考量** ：IC通常是多層結構，`IC Mode`是基於3D Layout框架操作環境，這有助於更精確地模擬和分析這種多層結構。 
2. **GDSII支持** ：在IC設計中，元件尺度可以從納米到微米級別(nm-um)，並且設計文件通常是以GDS格式存在的。因此，`IC Mode`支持GDS格式文件的匯入。 
3. **加密製程技術文件支持** ：製造IC需要晶圓廠提供詳細的製程技術文件，這些文件往往包含大量的層堆疊資訊，而且由於涉及到智慧財產權，這些技術文件常常是加密的。因此，`IC Mode`必須支持加密製程技術文件的匯入。
4. **大量端口支持** ：在IC設計中，可能會有數百到數千個端口，`IC Mode`提供了更便捷的設置端口(port)的方式。 
5. **布局簡化** ：由於IC設計中的布局尺度很小，常常使用到via array（通孔陣列）來進行連接。在這種情況下，`IC Mode`提供多種方式來簡化這種複雜的布局。 
6. **複雜Interposer結構加速計算** ：對於那些有複雜Interposer結構的設計，`IC Mode`提供多種加速處理的能力，以便更快完成分析。 
7. **模型抽取靈活性** ：根據不同的需求（如SI、PI或RF分析），`IC Mode`圖供多種求解器以支持不同類型的模型抽取，以滿足各種設計和分析的需求。

總之，HFSS的IC模式是針對現代高速、高頻電子設計的需求而設計的，提供了一系列功能來滿足這些設計中的特定挑戰。

#### IC Mode
在HFSS 3D Layout中，預設「General」模式是指通用或者標準的操作模式，適合大多數的PCB及封裝設計模擬；而「IC」模式則是針對集成電路（Integrated Circuit）設計的特殊操作模式，提供了更為專業的工具集或參數設置。處理IC設計模型抽取時，要切換到`IC Mode`。

![2024-03-21_04-58-34](/assets/2024-03-21_04-58-34.png)

`IC Mode`的求解器與`General mode`的有所不同，如下圖所示：

![2024-04-08_14-54-02](/assets/2024-04-08_14-54-02_770ebtbuz.png)

### 範例檔案

> :link: **範例檔案下載**
[example.gds](/assets/example.gds)
[example.xml](/assets/example.xml)

生成example.gds的python程式碼：

```python
import gdspy

# 定義單元大小和實例之間的間距
unit_size = 0.05  # 方塊的大小
spacing = 10   # 實例之間的間距

# 創建一個新的庫（或GDSII文件）
lib = gdspy.GdsLibrary()

# 為方塊陣列創建一個cell
cell = lib.new_cell('SQUARE_ARRAY')

# 向cell中添加方塊
for i in range(10):
    for j in range(10):
        square = gdspy.Rectangle((0.1*i, 0.1*j), 
                                 (0.1*i+unit_size, 0.1*j+unit_size),
                                 layer=100, 
                                 datatype=0)
        cell.add(square)

# 創建主cell以放置陣列的實例
main_cell = lib.new_cell('MAIN')

# 創建兩個間隔一定距離的方塊陣列cell的實例
instance1 = gdspy.CellReference(cell, (0, 0))
instance2 = gdspy.CellReference(cell, (unit_size + spacing, 0))

# 將實例添加到主cell
main_cell.add(instance1)
main_cell.add(instance2)

# 添加外框以顯示實例的位置和邊界
rectangle = gdspy.Rectangle((-0.05, -0.05), (1, 1), layer=200, datatype=0)
main_cell.add(rectangle)
rectangle = gdspy.Rectangle((10, -0.05), (11.05, 1), layer=200, datatype=0)
main_cell.add(rectangle)

# 添加更大的外框以顯示整個設計的邊界
rectangle = gdspy.Rectangle((-0.1, -0.1), (11.1, 1.05), layer=300, datatype=0)
main_cell.add(rectangle)

# 將標籤添加到 cell
label = gdspy.Label('s0', (0.5, 0.5), layer=200, texttype=20)
main_cell.add(label)

# 將設計保存到GDSII文件
gds_filename = 'd:/demo/lab2.gds'
lib.write_gds(gds_filename)
```

![2024-04-12_04-19-57](/assets/2024-04-12_04-19-57.png)


### 輔助工具

KLayout 是一款功能強大的微電子版圖設計軟件，主要用於設計和檢視集成電路（IC）的版圖。它支援多種版圖格式，如GDSII、OASIS 等，並且能夠處理非常大的數據集。KLayout 不僅提供基本的版圖編輯功能，還包括複雜的版圖檢查和自動化處理功能，使其成為專業的半導體設計工程師和學術研究人員廣泛使用的工具。

這款軟件具有以下特點： 
1. **跨平台支持** ：KLayout 可以在多種作業系統上運行，包括Windows、Linux 和 macOS。 
2. **用戶界面** ：它有一個直觀的用戶界面，支援圖形和文字兩種操作方式，方便各種用戶習慣。 
3. **自動化與腳本** ：KLayout 允許使用Ruby或Python腳本進行自動化處理，這使得它可以輕鬆地集成到更大的設計流程中。 
4. **高效的數據處理** ：即使是非常大的版圖檔案，KLayout 也能夠高效地進行渲染和編輯。

KLayout 不僅用於商業環境，也因其開源和免費的特性，在學術界和研究領域得到了廣泛應用。它支持擴展和客製化，這使得用戶可以根據自己的需求修改和擴充軟件功能。

> :link: **連結**
[KLayout官方網站](https://www.klayout.de/)