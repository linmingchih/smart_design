讀取stackup.xml並建立多個cells(Designs)
---
這段程式碼展示了如何使用 PyAEDT 中的 Edb 模組來進行 HFSS 3D Layout 中的設計自動化。首先，程式會建立一個 EDB 專案，並透過迴圈建立多個不同的電路設計。接著，它會從指定的 XML 檔案中載入堆疊層資訊檔案，並創建十個不同的電路設計。

在每個電路設計中，程式將會生成傳輸線 (trace) 和矩形接地平面，並分別在不同的層 (如 TOP, L2GND, L3, L4GND) 上進行設計。每次設計完成後，EDB 檔案將被儲存並關閉。

此範例展示了如何通過程式化方式進行設計重複性操作，從而自動化設計流程，提升設計效率並避免手動設置時的錯誤。該程式適合用於大規模設計與自動化佈局流程。
>xml下載
[layers.xml](/assets/layers.xml)
```python
from pyedb import Edb
from pyaedt import Hfss3dLayout

edb = Edb(edbversion='2024.1', cellname='cell')

for i in range(10):
    edb.core_stackup.load(r"D:\demo\layers.xml")
    edb.edb_api.cell.create(edb.db, edb._edb.Cell.CellType.CircuitCell, f'cell_{i:02}')

edb.save_edb()
edb.close_edb()

for i in range(10):
    edb = Edb(edb.edbpath,
              edbversion='2024.1',
              cellname=f'cell_{i:02}')
    edb.core_stackup.load(r"D:\demo\layers.xml")
    edb.save_edb()
    edb.close_edb()


#%%
edb = Edb(edb.edbpath, cellname='cell_00', edbversion='2024.1')

edb.modeler.create_trace([('0mm','0mm'), ('10mm','0mm')], 'TOP', '0.156mm', 'sp','Flat', 'Flat')
edb.modeler.create_rectangle('L2GND', 'GND', ('-2mm','-3mm'), ('12mm', '3mm'))

edb.save_edb()
edb.close_edb()


#%%
edb = Edb(edb.edbpath, cellname='cell_01', edbversion='2024.1')

edb.modeler.create_trace([('0mm','0mm'), ('10mm','0mm')], 'L3', '0.123mm', 'sp','Flat', 'Flat')
edb.modeler.create_rectangle('L2GND', 'GND', ('-2mm','-3mm'), ('12mm', '3mm'))
edb.modeler.create_rectangle('L4GND', 'GND', ('-2mm','-3mm'), ('12mm', '3mm'))

edb.save_edb()
edb.close_edb()


#%%

edb = Edb(edb.edbpath, cellname='cell_02', edbversion='2024.1')

edb.modeler.create_trace([('0mm','0.1636mm'), ('10mm','0.1636mm')], 'TOP', '0.12mm', 'sp','Flat', 'Flat')
edb.modeler.create_trace([('0mm','-0.1636mm'), ('10mm','-0.1636mm')], 'TOP', '0.12mm', 'sn','Flat', 'Flat')
edb.modeler.create_rectangle('L2GND', 'GND', ('-2mm','-3mm'), ('12mm', '3mm'))

edb.save_edb()
edb.close_edb()

#%%

edb = Edb(edb.edbpath, cellname='cell_03', edbversion='2024.1')

edb.modeler.create_trace([('0mm','0.2806mm'), ('10mm','0.2806mm')], 'L3', '0.12mm', 'sp','Flat', 'Flat')
edb.modeler.create_trace([('0mm','-0.2806mm'), ('10mm','-0.2806mm')], 'L3', '0.12mm', 'sn','Flat', 'Flat')
edb.modeler.create_rectangle('L2GND', 'GND', ('-2mm','-3mm'), ('12mm', '3mm'))
edb.modeler.create_rectangle('L4GND', 'GND', ('-2mm','-3mm'), ('12mm', '3mm'))
edb.save_edb()
edb.close_edb()

#%%

edb = Edb(edb.edbpath, cellname='cell_04', edbversion='2024.1')

edb.modeler.create_trace([('0mm','0mm'), ('4.5mm','0mm')], 'TOP', '0.156mm', 'sp','Flat', 'Flat')
edb.modeler.create_trace([('5.5mm','0mm'), ('10mm','0mm')], 'TOP', '0.156mm', 'sn','Flat', 'Flat')
edb.modeler.create_rectangle('L2GND', 'GND', ('-2mm','-3mm'), ('12mm', '3mm'))

edb.save_edb()
edb.close_edb()

#%%

edb = Edb(edb.edbpath, cellname='cell_05', edbversion='2024.1')

edb.modeler.create_trace([('0mm','0mm'), ('4.5mm','0mm')], 'TOP', '0.156mm', 'sp','Flat', 'Flat')
edb.modeler.create_rectangle('TOP', 'GND', ('5.5mm','-3mm'), ('12mm', '3mm'))
edb.modeler.create_rectangle('L2GND', 'GND', ('-2mm','-3mm'), ('12mm', '3mm'))

edb.padstacks.create('via', pad_shape='Rectangle', holediam='200um', x_size='0.3mm', y_size='0.3mm')

pin2 = edb.padstacks.place_padstack(('7mm','1.5mm'), 'via', is_pin=True, fromlayer='TOP', tolayer='L2GND', net_name='GND')
pin3 = edb.padstacks.place_padstack(('7mm','-1.5mm'), 'via', is_pin=True, fromlayer='TOP', tolayer='L2GND', net_name='GND')
pin4 = edb.padstacks.place_padstack(('10mm','1.5mm'), 'via', is_pin=True, fromlayer='TOP', tolayer='L2GND', net_name='GND')
pin5 = edb.padstacks.place_padstack(('10mm','-1.5mm'), 'via', is_pin=True, fromlayer='TOP', tolayer='L2GND', net_name='GND')

edb.save_edb()
edb.close_edb()


#%%
edb = Edb(edb.edbpath, cellname='cell_06', edbversion='2024.1')

edb.modeler.create_trace([('0mm','0mm'), ('4.5mm','0mm')], 'TOP', '0.156mm', 'sp','Flat', 'Flat')
edb.modeler.create_trace([('5.5mm','0mm'), ('10mm','0mm')], 'TOP', '0.156mm', 'sn','Flat', 'Flat')
edb.modeler.create_rectangle('L2GND', 'GND', ('-2mm','-3mm'), ('12mm', '3mm'))

edb.padstacks.create('pad', pad_shape='Rectangle', holediam=0, x_size='0.3mm', y_size='0.3mm')
pin1 = edb.padstacks.place_padstack(('4.5mm','0mm'), 'pad', is_pin=True, fromlayer='TOP', tolayer='TOP')
pin2 = edb.padstacks.place_padstack(('5.5mm','0mm'), 'pad', is_pin=True, fromlayer='TOP', tolayer='TOP')
edb.components.create([pin1, pin2], 'R1', 'TOP', 'RP1', True)

edb.save_edb()
edb.close_edb()


#%%
edb = Edb(edb.edbpath, cellname='cell_07', edbversion='2024.1')

edb.modeler.create_trace([('0mm','0mm'), ('10mm','0mm')], 'TOP', '0.156mm', 'sp','Flat', 'Flat')
edb.modeler.create_rectangle('L2GND', 'GND', ('-2mm','-3mm'), ('12mm', '3mm'))

edb.padstacks.create('pad', pad_shape='Rectangle', holediam=0, x_size='0.3mm', y_size='0.3mm')
edb.padstacks.create('via', pad_shape='Rectangle', holediam='200um', x_size='0.3mm', y_size='0.3mm')
pin1 = edb.padstacks.place_padstack(('0mm','0mm'), 'pad', is_pin=True, fromlayer='TOP', tolayer='TOP', net_name='sp')
pin2 = edb.padstacks.place_padstack(('0mm','1mm'), 'via', is_pin=True, fromlayer='TOP', tolayer='L2GND', net_name='GND')
pin3 = edb.padstacks.place_padstack(('0mm','-1mm'), 'via', is_pin=True, fromlayer='TOP', tolayer='L2GND', net_name='GND')
pin4 = edb.padstacks.place_padstack(('-1mm','1mm'), 'via', is_pin=True, fromlayer='TOP', tolayer='L2GND', net_name='GND')
pin5 = edb.padstacks.place_padstack(('-1mm','-1mm'), 'via', is_pin=True, fromlayer='TOP', tolayer='L2GND', net_name='GND')
edb.components.create([pin1, pin2, pin3, pin4, pin5], 'U1', 'TOP', 'UP1', False)

pin1 = edb.padstacks.place_padstack(('10mm','0mm'), 'pad', is_pin=True, fromlayer='TOP', tolayer='TOP', net_name='sp')
pin2 = edb.padstacks.place_padstack(('10mm','1mm'), 'via', is_pin=True, fromlayer='TOP', tolayer='L2GND', net_name='GND')
pin3 = edb.padstacks.place_padstack(('10mm','-1mm'), 'via', is_pin=True, fromlayer='TOP', tolayer='L2GND', net_name='GND')
pin4 = edb.padstacks.place_padstack(('11mm','1mm'), 'via', is_pin=True, fromlayer='TOP', tolayer='L2GND', net_name='GND')
pin5 = edb.padstacks.place_padstack(('11mm','-1mm'), 'via', is_pin=True, fromlayer='TOP', tolayer='L2GND', net_name='GND')

edb.components.create([pin1, pin2, pin3, pin4, pin5], 'U2', 'TOP', 'UP2', False)                       

edb.save_edb()
edb.close_edb()
```

