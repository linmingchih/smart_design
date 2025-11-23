Pyedb Explorer使用說明
---

Pyedb是一個用於編輯EDB檔案的Python API函式庫，可以載入.aedb檔案並進行查詢及修改、設定端口、執行HFSS 3D Layout模擬等操作。功能包括：
- 載入.aedb檔案並顯示其結構。
- 查詢和修改元件屬性。
- 設定端口和連接。
- 建立HFSS模擬或SIwave模擬。


雖然Pyedb提供了強大的功能，但當中複雜的物件連結與豐富的API方法屬性使得使用門檻較高。開發者需要透過dir()和help()等方法來探索及查詢API，對於初學者來說可能較為困難。

為了降低使用門檻並提升用戶體驗，我們開發了Pyedb Explorer，一個基於PyWebView的圖形化使用介面，讓用戶能夠更直觀地探索edb物件及其屬性，並提供便捷的操作功能，讓使用者能夠輕鬆地進行查詢pyedb物件的關係與說明，大幅提升模擬自動化程式開發效率與體驗。

### Pyedb Explorer 功能介紹

![Pyedb Explorer介面截圖](/assets/2025-11-23_19-23-55.png)

當Pyedb Explorer啟動後，會載入內建的範例.aedb檔案，並顯示其最上層物件edb，

```
from pyedb import Edb
edb = Edb('pcb.aedb')
```
點擊edb物件，上方Target視窗會顯示該物件的完整路徑，中間視窗顯示該物件，物件型別及數值。其下為說明Docstring，最右邊視窗則顯示該物件的屬性及方法列表。

- M: 物件方法
- P: 屬性名稱與屬性型別
- C: 集合型別，像是list或dict

使用者可以點擊屬性名稱，查看該屬性的值及說明，若該屬性本身也是一個物件，則可以繼續點擊進入該物件，探索其屬性與方法。這樣的操作方式讓使用者能夠直觀地了解edb物件的結構與關係。

此外，Pyedb Explorer還提供搜尋功能Regex Filter，使用者可以輸入關鍵字來搜尋物件的屬性或方法，快速定位所需資訊。這對於大型edb檔案中特定物件的查詢非常有幫助。

舉例來說，點選stackup屬性，可以看到它是一個Stackup型別的物件，並且可以查看其屬性與方法說明。target視窗會顯示完整路徑edb.stackup，而中間視窗則顯示stackup物件的詳細資訊與說明。右邊視窗則顯示stackup物件的屬性及方法列表。以此類推，使用者可以深入探索edb物件的結構與關係。

點選signal_layers屬性，可以看到它是一個OrderedDict，右邊視窗除了顯示signal_layers的屬性與方法外，Collection Items標題下方還會列出該OrderedDict中的所有鍵，點選鍵'1_Top'，則中間視窗會顯示對應的Layer物件資訊與說明，而右邊視窗則顯示StackupLayerEdbClass物件的屬性與方法列表。這樣的操作方式讓使用者能夠方便地瀏覽集合型別的物件內容。

target右方星號可以將目前瀏覽的物件加入左方最愛欄位(FAVORITES)，方便日後快速存取。

target右方的Undo/Redo按鈕，可以讓使用者回到上一個瀏覽的物件位置，方便在不同物件間切換與比較。

底下PYTHON CONSOLE視窗，則提供一個互動式的Python命令列介面，使用者可以直接在此輸入Python指令來操作edb物件，並即時查看結果。這對於進行快速測試與驗證非常有幫助。

例如edb.create_hfss_setup的說明為
```
Create an HFSS simulation setup from a template.

Parameters
name : str, optional
    Setup name.

Returns
:class:`legacy.database.edb_data.hfss_simulation_setup_data.HfssSimulationSetup`

Examples
>>> from pyedb import Edb
>>> edbapp = Edb()
>>> setup1 = edbapp.create_hfss_setup("setup1")
>>> setup1.hfss_port_settings.max_delta_z0 = 0.5
```
但是回傳的setup1物件到底有哪些屬性與方法呢？這時候就可以利用Python Console來查詢，例如在Python Console中輸入  
```
setup1 = edbapp.create_hfss_setup("setup1")
```
這時候setup1物件就會被建立，並放在左側GlOBAL Variables清單中，點選setup1物件，Target便會顯示setup1物件，中間視窗顯示setup1物件的說明，而最右邊視窗則會列出setup1物件的屬性與方法列表。這樣使用者就能夠清楚地了解setup1物件的結構與功能，並進一步操作與測試。

如果不需要setup1物件，可以在Python Console中輸入  
```
del(setup1)
```

如果不需要使用Python Console，可以在Options中將其關閉，讓介面更簡潔。


### 進階使用技巧：載入自訂.aedb檔案

由於Pyedb Explorer是基於實體.aedb建立物件，並透過dir()與help()等內建方法來動態查詢物件屬性與方法，因此有些物件可能無法正確取得其屬性與方法說明，一個workaround的方式是使用Pyedb Explorer載客戶設定的.aedb檔案，例如預設的pcb.aedb檔案並沒有DCIR的電壓源元件，因此無法查詢到相關屬性與方法說明。如果客戶提供一個包含DCIR電壓源的.aedb檔案，則可以正確查詢到相關屬性與方法說明。透過Options中的Load Custom .aedb功能，可以載入客戶手動設定的.aedb檔案，這樣就能夠查詢到更多元件的屬性與方法說明，提升使用體驗。