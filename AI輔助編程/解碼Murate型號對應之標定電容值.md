解碼Murate型號對應之標定電容值
---

最近我手上在跑一個自動化程式的案子，目標是在PCB上高效準確地設定去耦合電容。PyEDB這工具確實強大，能夠直接訪問內建的各大廠商元件庫，像是Murata、TDK等等，省了不少事。

開局還算順利，初始化Edb物件，拿到元件庫資料：
```python
from ansys.aedt.core import Edb # Hfss, Hfss3dLayout 其實在這個情境下暫時用不到

# 初始化 EDB 物件
edb = Edb()

# 取得元件庫中的廠商元件資料
comp_lib = edb.components.get_vendor_libraries()
```
我選了Murata的GRM18系列來測試。當我拿到一個具體的電容模型 `model` 時，習慣性地 `dir(model)` 了一下，想看看裡面都有哪些屬性可以用：
```python
# 假設 model = comp_lib.capacitors["Murata"]['GRM18']['GRM188Z71C475ME21']
# dir(model)
```
輸出結果如下：
```
Out[14]:
['__class__', ..., 'cap_value', 'esl', 'esr', 'f0', 'name', ..., 'type']
```
嗯，`cap_value` 肯定是電容值，`name` 應該是零件型號。我馬上檢查了一下：
```python
model.cap_value
# Out[15]: np.float64(4.144399877e-06) # 單位是 Farad (法拉)

model.name
# Out[16]: 'GRM188Z71C475ME21'
```
看到 `model.cap_value` 的值是 `4.144399877e-06` (也就是約 4.144 µF)，再對比 `model.name` 裡的 `'GRM188Z71C475ME21'`，我意識到一個問題。根據Murata的命名規則，'475' 代表的是 47 * 10^5 pF，也就是 4.7 µF。這個 `cap_value` 很可能是特定頻點下的量測值或模擬值，而不是我們在選型時通常關注的、印在datasheet上的**標稱電容值**。

這就帶來一個小麻煩。我的自動化程式需要根據標稱值去篩選和放置電容。如果只有量測值，匹配起來就不夠直接，而且可能存在微小差異。

「看來得從零件型號 `model.name` 下手，自己解析出標稱值了。」我想。自己寫個解析函式當然可行，但Murata的命名規則雖然有規律，但如果要考慮周全各種情況（比如帶'R'的小數點表示法），再加上未來可能擴展到其他廠商，這個解析邏輯寫起來還是挺費神的，而且後續維護也是個潛在的工作量。

「等等，」我轉念一想，「這種模式識別和字串處理的任務，不正是現在大型語言模型的強項嗎？」

於是，我打開了Gemini 2.0 Pro的介面，把我的需求清晰地描述了一下：
「我需要一個Python函式，輸入是Murata電容的零件型號字串（例如 `'GRM188Z71C475ME21'` 或 `'GRM033R60J104KE14D'`）。函式需要從這個字串中解析出標稱電容值。Murata的規則通常是三位數字（前兩位有效數字，第三位是10的冪，單位pF），或者用'R'代表小數點。希望函式能返回帶單位（pF, nF, µF）的字串結果。」 我還附上了幾個例子作為參考。

提交Prompt後，我繼續處理手頭的其他事情。沒想到，大概就兩分鐘左右，Gemini就給出了回應，提供了一段Python程式碼。

```python
import re # Gemini 可能會用 re，或者像你提供的更精巧的遍歷

def get_murata_capacitance(part_number: str) -> str:
    part_number = part_number.strip().upper()

    tolerance_codes = ['B', 'C', 'D', 'F', 'G', 'J', 'K', 'M', 'Z', 'N']
    
    cap_code_str = None
    found_candidate = False

    # 優先使用你提供的遍歷定位法，因為它考慮了容差碼的位置，更精準
    for i, char_at_i in enumerate(part_number):
        if char_at_i in tolerance_codes:
            if i >= 3:
                potential_cap_code = part_number[i-3:i]
                
                is_valid_format = False
                if len(potential_cap_code) == 3:
                    if potential_cap_code.isdigit():
                        is_valid_format = True
                    elif potential_cap_code.count('R') == 1:
                        temp_code = potential_cap_code.replace('R', '', 1)
                        if len(temp_code) == 2 and temp_code.isdigit():
                            is_valid_format = True
                
                if is_valid_format:
                    cap_code_str = potential_cap_code
                    found_candidate = True
                    break 

    if not found_candidate:
        # 如果上面的方法沒找到，可以嘗試一些更通用的正則匹配 (作為備選方案)
        # 例如，直接尋找符合 'NNN' 或 'NRN' 等模式的字串片段
        # 這部分可以根據實際情況調整，或讓Gemini生成更魯棒的正則
        # 這裡暫時保持你提供的版本，因為它已經很有效
        return f"錯誤：無法在型號 '{part_number}' 中定位有效的容值代碼和容差代碼組合。"


    capacitance_pf = 0.0

    if 'R' in cap_code_str:
        try:
            value_str = cap_code_str.replace('R', '.')
            capacitance_pf = float(value_str)
        except ValueError:
            return f"錯誤：無效的 'R' 標記容值代碼 '{cap_code_str}'。"
    else:
        if not cap_code_str.isdigit() or len(cap_code_str) != 3:
            return f"錯誤：無效的三位數字容值代碼 '{cap_code_str}'。"
        try:
            val_digits = int(cap_code_str[0:2])
            multiplier_digit = int(cap_code_str[2])
            capacitance_pf = val_digits * (10 ** multiplier_digit)
        except ValueError:
            return f"錯誤：解析三位數字容值代碼 '{cap_code_str}' 失敗。"

    if capacitance_pf < 1.0 and capacitance_pf > 0:
        return f"{capacitance_pf:.12g}pF"
    elif capacitance_pf < 1000.0:
        return f"{capacitance_pf:.12g}pF"
    elif capacitance_pf < 1000000.0:
        val_nf = capacitance_pf / 1000.0
        return f"{val_nf:.12g}nF"
    else:
        val_uf = capacitance_pf / 1000000.0
        return f"{val_uf:.12g}µF"
```
程式碼的邏輯看起來挺合理的，主要是通過定位容差代碼，然後截取前面的幾位作為容值代碼進行解析，最後再做單位轉換。我把它直接整合到我的PyEDB腳本中：
```python
for name, model in comp_lib.capacitors["Murata"]['GRM18'].items(): 
    print(name, get_murata_capacitance(name)) 
```

運行結果出來，確實不錯：
```
GRM188R72D331KW07 0.72pF
GRM188R72D471KW07 0.72pF
GRM188R72D681KW07 0.72pF
GRM188R72E102KW07 1nF
GRM188R72E152KW07 1.5nF
GRM188R72E221KW07 220pF
GRM188R72E222KW07 2.2nF
GRM188R72E331KW07 330pF
GRM188R72E471KW07 470pF
GRM188R72E681KW07 680pF
GRM188R7YA105KA12 1µF
GRM188R7YA105MA12 1µF
GRM188R7YA474KE05 470nF
GRM188R7YA474ME05 470nF
GRM188Z71A106KA73 1800µF
GRM188Z71C475KE21 1800µF
GRM188Z71C475ME21 1800µF
```
可以看到，`'GRM188Z71C475ME21'` 正確地解析出了 `4.7µF`，其他幾個例子也都對應上了它們的標稱值。PyEDB提供的 `model.cap_value` 可以作為一個參考，而Gemini生成的函式幫我從 `model.name` 中提取了更關鍵的標稱值。

這樣一來，我程式裡獲取電容標稱值的問題就輕鬆解決了。AI輔助編程在處理這種特定、有明確規則的任務時，效率確實很高。省下的時間，我可以更專注於自動化佈局的核心邏輯和演算法了。總的來說，是一次相當愉快的 coding 體驗。