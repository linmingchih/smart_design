結構簡化與修正
---

### 3.1 Via Grouping

在晶片製造過程中，常見的做法是使用數以千計的小通孔（vias）在信號層之間建立連接。在Ansys Electronics Desktop Layout Editor中，這些通孔通常以方形原始體（square primitives）來表示。這種表示對於製造來說很重要，但對於模擬時卻可能引入不適宜的網格密度，從而增加了計算的複雜性。

通孔分組（Via Grouping）選項允許將這些方形原始體分組，並用單個原始體來代表整個組，這樣可以大大降低網格的複雜性，同時只會輕微降低精度。精度的保持是通過計算基於原始幾何形狀的等效材料來實現的。

當你有一組方形原始體時，通孔分組工具可以自動檢測出矩形原始體的集群，並相應地創建通孔分組。然後可以根據需要結合或分解這些通孔分組。進行通孔分組的步驟如下：

1. 選擇要分組的方形原始體。
2. 點擊 Via Groups 按鈕，如下圖所示。
3. 然後選擇創建選項之一：
    - **Persistent**：在所選原始體上創建持久性或非持久性通孔分組。
    - **Non-Persistent**：創建時會刪除原始體輸入
    - **Combine**：將選定的通孔分組和/或通孔原始體合併為新的通孔分組。
    - **Dissolve**：將選定的通孔分組還原為組成它的原始體。

![2024-04-12_15-18-58](/assets/2024-04-12_15-18-58.png)

#### 設定

![2024-04-12_14-40-18](/assets/2024-04-12_14-40-18.png)


通孔可以通過兩種方法進行分組：按範圍（Group by Range）和按鄰近性（Group by Proximity）。 
- **按範圍分組** ：這種方法擴展新的分組，只考慮潛在成員是否與現有成員之間隔著不超過設定容差的距離。 
- **按鄰近性分組** ：這種方法則是將空間上相似分布的通孔進行分組，如果通孔之間的距離超過了容差，則不會被分組。

以下兩幅圖示用來說明按鄰近性分組和按範圍分組的差異。這些圖示顯示了不同分組策略下的通孔排列情況。按鄰近性分組的通孔在空間上分佈類似，而按範圍分組的通孔則是基於它們與其他成員之間的距離是否在容差範圍內。

![2024-04-12_15-06-43](/assets/2024-04-12_15-06-43.png)

檢查封裝選項（Check Containment）。這個選項的功能是通過分析通孔原始件（via primitives）的放置情況來檢測電路短路。如果發現短路，該功能會自動將涉及短路的通孔組分開，以此來防止短路的發生。

這意味著當進行電路設計或佈局優化時，這個工具可以自動識別可能導致電氣連接問題的區域，並採取預防措施，保證設計的安全性和可靠性。這對於減少設計錯誤、避免後期修正所需的時間和成本是非常有幫助的。


#### 採用Dielectric Merge
半導體長有多個電性相近的薄薄膜層疊在一起，這些層的介電常數差異很小，導致單獨為每一層切網格會使得網格總數急劇增加，從而增加了計算資源的消耗。為了解決這個問題，HFSS提供了介電質簡化的方法。

在這個過程中，可以選擇一個或多個連續的介電層，然後將每一組合併為一個介電層。合併後的介電層將有一個計算出的相對介電常數 \(\epsilon_{r\_merged}\)。計算 \(\epsilon_{r\_merged}\) 可以使用以下三種方法之一：

1. **加權電容法（Weighted Capacitance）**:
   $$
   \epsilon_{r\_merged} = \frac{\sum_{i=1}^{n} h_i}{\sum_{i=1}^{n} \frac{h_i}{\epsilon_i}}
   $$
   其中 \(h_i\) 是每個薄膜層的厚度，而 \(\epsilon_i\) 是相應層的介電常數。

2. **Kraszewski 方法**:
   $$
   \epsilon_{r\_merged} = \left( \frac{\sum_{i=1}^{n} h_i \sqrt{\epsilon_i}}{\sum_{i=1}^{n} h_i} \right)^2
   $$

3. **加權平均法（Weighted Average）**:
   $$
   \epsilon_{r\_merged} = \frac{\sum_{i=1}^{n} h_i\epsilon_i}{\sum_{i=1}^{n} h_i}
   $$


這些方法將各層的物理厚度和介電常數結合，以計算出合併後層的等效介電常數。這種方法的好處在於，它能通過減少網格元素的數量來縮短計算時間，同時仍保持合理的計算準確性。

對於介電質簡化的實際應用，通過合併具有類似介電特性的薄薄膜層，您能夠大大簡化網格的複雜性，從而提高計算效率。這在半導體設計中尤其重要，因為這些設計通常包含了許多極薄的介電層。通过用户界面或者FDB API，可以根据设计需要和计算精度的要求選擇最合適的方法來進行合併簡化。

![2024-03-23_20-16-16](/assets/2024-03-23_20-16-16.png)


```python
import gdspy
from itertools import product

unit_size = 0.05  
spacing = 2   

lib = gdspy.GdsLibrary()


cell = lib.new_cell('SQUARE_ARRAY')

for i in range(10):
    for j in range(10):
        square = gdspy.Rectangle((0.1*i, 0.1*j), 
                                 (0.1*i+unit_size, 0.1*j+unit_size),
                                 layer=100, 
                                 datatype=0)
        cell.add(square)


dummy = lib.new_cell('Dummy_ARRAY')

for i in range(6):
    for j in range(6):
        square = gdspy.Rectangle((0.1*i, 0.1*j), 
                                 (0.1*i+unit_size, 0.1*j+unit_size),
                                 layer=300, 
                                 datatype=0)
        dummy.add(square)


main_cell = lib.new_cell('MAIN')

# 創建兩個間隔一定距離的方塊陣列cell的實例
for i, j in product(range(6), range(6)):
    dx = i*spacing
    dy = j*spacing
    instance = gdspy.CellReference(cell, (dx, dy))
    main_cell.add(instance)
    
    if i < 5 and j < 5:
        instance = gdspy.CellReference(dummy, (dx+1.2, dy+1.2))
        main_cell.add(instance)

    rectangle = gdspy.Rectangle((-0.05+dx, -0.05+dy), (1+dx, 1+dy), layer=200, datatype=0)
    main_cell.add(rectangle)

    rectangle = gdspy.Rectangle((-0.1, -0.1+dy), (11.05, 1.05+dy), layer=300, datatype=0)
    main_cell.add(rectangle)

    rectangle = gdspy.Rectangle((-0.1+dx, -0.1), (1.05+dx, 11.05), layer=300, datatype=0)
    main_cell.add(rectangle)


# 添加更大的外框以顯示整個設計的邊界

# 將標籤添加到 cell
label = gdspy.Label('s0', (0.5, 0.5), layer=200, texttype=20)
main_cell.add(label)

# 將設計保存到GDSII文件
gds_filename = 'd:/demo5/lab3.gds'
lib.write_gds(gds_filename)

```