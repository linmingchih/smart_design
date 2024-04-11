Lab 2. XML 控制檔案介紹
---





#### V. 附註
生成lab2.gds的python程式碼：

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

# 將設計保存到GDSII文件
gds_filename = 'd:/demo/lab2.gds'
lib.write_gds(gds_filename)

```