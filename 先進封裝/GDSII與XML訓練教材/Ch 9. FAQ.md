常見問題解答
---

#### Q: 在將GDS檔案匯入AEDT 3D Layout時，如果沒有提供控制檔案，會發生什麼情況？

A: 如果在將GDS匯入AEDT 3D Layout時沒有提供控制檔案，系統會將GDS檔中的所有資料匯入。然而，需要注意的是，在AEDT的3D Layout中，來自GDS檔屬於同一個Layer（層）的不同DataType（資料類型），在AEDT中也會被合併到同一個Layer。


#### Q: 在控制檔案中，除了描述材料屬性外，XML如何描述金屬層之間的連接關係？

A: 在Control檔案中，XML用來描述金屬層之間連接關係的方式主要涉及到層（Layer）的定義和via層（垂直連接層）的配置。透過特定的XML標籤和屬性，可以細致地控制金屬層間的連結方式和特性。以下是兩個主要方面的詳細說明： 
1. **金屬層定義：**  金屬層通常在XML中以`<Layer>`標籤表示，其中包含了描述該層特性的多個屬性： 
- `Name`: 唯一標識該層的名稱。 
- `Material`: 指定層的材料名稱，用於定義其電氣或物理屬性。 
- `GDSDataType`: 與GDS檔案中的DataType對應，用於匹配特定的圖層數據。 
- `TargetLayer`: 指定目標層名稱，有時用於關聯特定的處理或屬性。 
- `Type`: 定義層的類型，如導體（conductor）。 
- `Thickness`和`Elevation`: 分別指定層的厚度和高度位置。 
- `ConvertPolygonToCircle`: 指定是否將多邊形轉換為圓形，用於特定的模型簡化或處理。 
- `ConvertPolygonToCircleRatio`: 轉換多邊形時用於決定圓形大小的比例因子。 
2. **Via層配置：**  Via層用於連接不同的金屬層，通過`<Layer>`標籤內嵌套特定的元素來配置： 
- `StartLayer`和`StopLayer`: 定義via連接的起始層和終止層，指明了via的垂直範圍。 
- `<CreateViaGroups>`: 用於生成via群組，其中`Method`屬性（如`proximity`）定義了群組創建的方式，`Tolerance`設定了相應的容忍範圍或參數。 
- `<SnapViaGroups>`: 處理和優化via群組的配置，如`Method`可設定為`areaFactor`以根據面積因子來調整via群組，`Tolerance`和`RemoveUnconnected`參數幫助細化via的配置和移除未連接的via。

![2024-04-11_15-30-43](/assets/2024-04-11_15-30-43.png)

透過這樣的XML配置，控制檔案可以精確地定義金屬層之間的連結關係和特性，進而在AEDT中實現精確的模型建立和仿真分析。

#### Q: GDSII文件中是否包含介電材料的層？

A: GDSII文件主要用於定義製程中的圖形和層結構，它通常不直接包含介電材料的層。GDSII文件著重於表達電路或互連結構的幾何圖案和層次結構，主要關注於導體（如金屬或多晶矽）的布局。

在AEDT設計流程中，介電材料層的資訊通常由外部的XML檔案描述。在XML檔案中，介電層是作為一系列層（laminate）逐一堆疊起來描述的，假設從Z=0位置開始疊加。

XML中層的排列順序反映了實際的物理結構，每個`<Layer>`元素通常包含如下信息： 
- `Name`: 層的名稱，標識不同的介電材料或其他層。 
- `Material`: 指定層使用的材料名稱。 
- `Thickness`: 指定該層的厚度。

例如，`<Layer Name="Bond_oxide_9" Material="Bond_oxide_9" Thickness="0.201300"/>` 表示一層名為`Bond_oxide_9`的介電材料，其厚度為0.201300單位。

在這種配置中，不需要`Elevation`屬性，因為層的堆疊順序就隱含了它們在垂直方向上的位置。

#### Q: GDS文件中的net如何處理？

A: 在interposer（中介層）設計中，信號網絡（signal net）必須連接到最頂層或最底層的接觸點。在XML檔案中，透過指定net名稱、相關層數和座標點來描述這些連接。例如，`WL1_MRMHT_GND@metal6 985.441 198.406` 表明一個名為`WL1_MRMHT_GND`的net位於`metal6`層，其座標為`(985.441, 198.406)`。AEDT會自動識別這些參數，將相應的金屬互連配置為指定的net。需要注意的是，net名稱不能重複；如果有重複，系統會選擇其中一個來顯示在Nets標籤中。

![2024-04-11_16-17-57](/assets/2024-04-11_16-17-57.png)


