建立多個cells
---

```python
from pyedb import Edb
edb_path = 'd:/demo/a254.aedb'
edb = Edb(edbpath = edb_path,
          edbversion='2024.1',
          cellname='x1')

edb.core_stackup.load(r"D:\demo\layers.xml")
edb.edb_api.cell.create(edb.db, edb._edb.Cell.CellType.CircuitCell, 'x2')
edb.save_edb()
edb.close_edb()


edb = Edb(edbpath = edb_path,
          edbversion='2024.1',
          cellname='x2')
edb.core_stackup.load(r"D:\demo\layers.xml")
edb.save_edb()
edb.close_edb()

```

![2024-09-18_22-40-41](/assets/2024-09-18_22-40-41.png)