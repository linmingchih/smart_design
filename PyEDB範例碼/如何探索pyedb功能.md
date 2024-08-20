如何探索pyedb功能
---
### Q. 何謂EDB？
Ansys EDB（Electronics Database，電子數據庫）是一種專為電子設計自動化（EDA）領域設計的數據格式，它存儲有關電子元件和電路板設計的詳細信息。Ansys EDB 文件通常被用於在多種設計和仿真工具之間進行數據交換，特別是在 Ansys 的電子設計套件中，例如 Ansys HFSS 3D Layout、Ansys SIwave 等。主要以.aedb目錄儲存。

### Q. aedb目錄的組成？
從圖片中可以看到，.aedb目錄包括以下兩個主要文件或文件夾： 
1. **stride 文件夾**  - 這個文件夾包含與特定設計的步進數據或版本有關的信息。通常這樣的文件夾會用於組織和存儲過程中的臨時數據或具有不同設計階段的數據。
 
2. **edb.def 文件**  - 包含定義電子數據庫中特定部分的設定信息。這類文件一般用於保存設計的定義參數，使得用戶能夠按照既定的規範重用或修改設計。
![2024-08-20_09-23-59](/assets/2024-08-20_09-23-59.png)

### Q. 何為PyEDB？

`pyedb` 是一個用於訪問和操作 Ansys Electronics Desktop (AEDT) 中的 Electronics DataBase (EDB) 的 Python 接口。EDB 是一個專為存儲和管理電子組件和電路設計數據的數據庫格式，廣泛用於高頻和電磁仿真應用中。以下是 `pyedb` 的一些主要功能： 
1. **數據訪問和管理** ：`pyedb` 提供了一種直接從 Python 腳本訪問和操作 EDB 數據的方法。用戶可以讀取、修改、新增或刪除電路設計中的元件和層次結構，而無需打開圖形用戶界面。
 
2. **自動化和整合** ：通過 `pyedb`，開發者和設計師可以在 Python 環境中自動化常見的設計和分析任務，如參數修改、設計優化、數據擷取等，並且可以將其與其他工具和流程融合。
 
3. **擴展功能** ：利用 Python 的強大功能和豐富的庫，`pyedb` 使得用戶可以擴展電子設計的分析能力，實現複雜的數據處理、統計分析和機器學習整合。
 
4. **用戶自定義腳本** ：用戶可以撰寫自定義的 Python 腳本來直接操作 EDB 中的數據，提高設計和分析的靈活性和效率。

### Q. 如何從其他檔案格式如.brd, .gdsII, .odb++等轉換成.aedb？
要從其他文件格式如 `.brd`（電路板設計文件），`.gdsII`（積體電路設計），或 `.odb++`（PCB 和封裝設計的數據交換格式）轉換成 `.aedb`（Ansys Electronics DataBase），您可以通過以下幾種方法： 

1. **使用 Ansys Electronics Desktop (AEDT)** ： 
Ansys 提供了導入工具來直接將這些文件類型導入到 AEDT 中，然後可以將導入的設計保存為 `.aedb` 格式。在 AEDT 中打開應用程序，選擇相應的導入選項，載入您的 `.brd` 或 `.odb++` 文件，並按照提示進行操作來完成導入和保存過程。

 
2. **使用PyEDB** ： 
PyEDB 是一款強大的工具，允許用戶直接從 Python 環境中訪問和操作 Ansys Electronics Database（EDB）。它不僅提供了操作 EDB 的接口，還支援將多種常見的電子設計文件格式轉換為 `.aedb` 格式。這些格式包括 PCB 設計文件的 `BRD`、用於 PCB 和組件製造的 `IPC2581 XML`、積體電路設計的 `GDSII`，以及 CAD 繪圖的 `DXF` 文件。

```python
edb = Edb("D:/demo/Galileo_G87173_204.brd", edbversion='2024.1')
```

### Q. PyEDB如何連結資料庫？
```python
edb = Edb('d:/demo4/Galileo_G87173_204162.aedb', edbversion='2024.1')
```
這行代碼建立了一個 `Edb` 物件的實例，指向一個位於 `d:/demo4/` 目錄下的 `.aedb` 文件。`edbversion='2024.1'` 指定了文件的版本，這是必須與你的文件兼容的版本。一旦數據庫文件被載入，你就可以使用 `edb` 物件來進行各種操作，如查詢、更新或處理數據。具體的操作會依賴於 `Edb` 類提供哪些方法和功能。

### Q. 資料庫當中包含哪些資料？
這個資料庫通常用於電子設計自動化（EDA）軟件，專門存儲關於印刷電路板（PCB）或集成電路（IC）設計的各種數據。根據你提供的資訊，這裡有一個基本的解釋關於EDB資料庫可能包含的一些主要資料類型：

#### 1. 材料（Materials） 

存儲有關用於製造電路板的各種材料的資訊，例如導電材料、絕緣材料等，這些特性對於分析電路板的電氣特性至關重要。

#### 2. 堆疊結構（Stackup） 

描述PCB的層疊結構，包括各層的材料、厚度和其他物理特性。這對於理解電路板的整體設計和性能非常重要。

#### 3. 網絡（Nets） 

表示電路板上的電氣連接。一個網絡包括連接一組電子元件的導體，這些元件共享電氣特性。

#### 4. 層（Layers） 

PCB中的各個層次，每一層可以包含信號層、地層或電源層等不同的功能層。

#### 5. 墊片（Padstacks） 

描述孔的結構，這些孔用於放置連接元件引腳的通孔或埋孔。每個墊片可以包含有關孔徑、形狀、用於連接的層等信息。

#### 6. 引腳（Pins） 

元件引腳的資料，通常是與特定的墊片相關聯，用於建立元件與PCB上其他元件或網絡的物理和電氣連接。

#### 7. 元件（Components） 

涉及的所有電子元件資訊，如晶片、電阻、電容等，包括它們的規格、位置和方向。

#### 8. 激勵（Excitations） 

用於模擬中的電源激勵設置，指定哪些信號或功率將進入電路系統，用於性能分析。

#### 9. 端口（Ports） 

用於模擬的界面，允許模擬中的信號進出，這些通常用於高頻信號傳輸特性分析。

#### 10. 探針（Probes） 

用於測量和分析電路中特定點的電氣特性的虛擬設備。

#### 11. 設定（Setups） 

包含模擬設定，如頻率範圍、解析度和其他參數，這些設定確定了模擬執行的具體條件。

### Q. 如何查詢資料庫？
要查詢EDB資料庫中的資料，可以使用PyEDB API來訪問和操作這些數據。下面代碼段顯示了如何使用edb物件來訪問materials屬性並列印所有材料。這是一種基本的查詢操作。edb.materials.materials 返回了一個字典，其中鍵是材料的名稱，值是對應的材料物件。這樣的物件通常包含更多關於材料的詳細資訊，如其物理和化學屬性。
```python
print(edb.materials.materials)
```
輸出
```python
{'AIR': <pyedb.dotnet.edb_core.materials.Material at 0x26d83380880>,
 'BOTTOM_FILL': <pyedb.dotnet.edb_core.materials.Material at 0x26d83380a90>,
 'COPPER': <pyedb.dotnet.edb_core.materials.Material at 0x26d83380910>,
 'FR-4': <pyedb.dotnet.edb_core.materials.Material at 0x26d83380970>,
 'FR-4_1': <pyedb.dotnet.edb_core.materials.Material at 0x26d83380b50>,
 'FR-4_2': <pyedb.dotnet.edb_core.materials.Material at 0x26d83380b80>,
 'FR4_epoxy': <pyedb.dotnet.edb_core.materials.Material at 0x26d83380be0>,
 'GND_FILL': <pyedb.dotnet.edb_core.materials.Material at 0x26d833809a0>,
 'LYR_1_FILL': <pyedb.dotnet.edb_core.materials.Material at 0x26d83380a60>,
 'LYR_2_FILL': <pyedb.dotnet.edb_core.materials.Material at 0x26d83380730>,
 'PWR_FILL': <pyedb.dotnet.edb_core.materials.Material at 0x26d833807c0>,
 'TOP_FILL': <pyedb.dotnet.edb_core.materials.Material at 0x26d83380820>}
```
> :memo: 探討
對於 `edb.materials.materials` 的寫法，在初看時可能會令人感到混淆，然而這種命名慣例在程式設計中是相當常見的。具體來說，第一個 `materials` 代表一個功能組別的名稱，專門用於存放與材料相關的操作，如添加新材料。而第二個 `materials` 則是該功能組內的一個字典容器，存放著各個材料實例。每個實例代表一種具體的材料，並包含該材料的詳細資訊與屬性。

### Q. 如何讀取材料屬性值
讀取EDB資料庫中材料的屬性值非常直接。首先，你使用了 `dir()` 函數來列出了特定材料對象（在這個例子中是 'FR-4'）的所有屬性和方法。然後，你直接通過屬性名訪問了特定的屬性值。這裡逐步解釋如何進行這個過程：
#### 步驟1: 列出所有屬性和方法 
使用 `dir()` 函數可以查看某個物件的所有屬性和方法，這是探索不熟悉物件的一種很好的方式。例如：

```python
# 列出 FR-4 材料的所有屬性和方法
print(dir(edb.materials.materials['FR-4']))
```

#### 步驟2: 選擇並讀取特定屬性 

一旦你知道了材料物件有哪些可用的屬性，你可以直接通過屬性名來訪問它們。如你所展示，讀取介電常數（permittivity）的值：


```python
# 讀取 FR-4 材料的介電常數
permittivity_value = edb.materials.materials['FR-4'].permittivity
print(permittivity_value)  # 輸出為 3.86
```

> :memo: 常見材料屬性解釋 
在EDB系統中，材料物件可能包括以下一些常見的物理和化學屬性： 
    - **permittivity** （介電常數）: 描述材料對電場的反應能力，影響信號的傳播速度。
    - **conductivity** （導電性）: 表示材料允許電流流動的能力。
    - **loss_tangent** （損耗角正切）: 表示材料在電磁場中能量損耗的指標。
    - **thermal_conductivity** （熱導率）: 材料導熱能力的度量。
    - **mass_density** （質量密度）: 單位體積的材料質量。

### Q. 如何修改材料屬性？
修改EDB資料庫中的材料屬性，如介電常數（permittivity），通常是直接對物件的屬性進行賦值操作。你已經正確展示了如何修改 'FR-4' 材料的介電常數。這裡是該操作的一個更詳細的步驟說明，以及一些注意事項：

#### 步驟1: 定位並修改屬性 

你可以直接修改物件的屬性，如下所示：

```python
# 修改 FR-4 材料的介電常數
edb.materials.materials['FR-4'].permittivity = 4.31
```

這行代碼將 'FR-4' 材料的介電常數設置為4.31。

#### 步驟2: 驗證修改 

修改後，建議檢查修改是否成功：

```python
# 檢查修改後的值
print(edb.materials.materials['FR-4'].permittivity)
```

### Q. 如何保存對EDB文件的修改？
當你想要保存對EDB (Electronic Design Database) 文件的修改或將其另存為新的文件時，使用如 `save_edb_as()` 方法這樣的函數是一種常見的做法。根據你提供的代碼，這裡有一個如何使用該方法來保存文件的步驟說明：在你的 `edb` 物件上調用 `save_edb_as()` 方法，並傳入新文件的路徑作為參數。

```python
edb.save_edb_as('d:/demo4/test.aedb')
```
 
