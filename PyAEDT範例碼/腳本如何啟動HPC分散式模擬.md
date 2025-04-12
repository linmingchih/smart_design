腳本如何啟動HPC分散式模擬
---
這個 `analyze()` 方法是用來執行 HFSS/Q3D/Maxwell...中「目前啟用設計（active design）」的模擬分析。它可以根據指定的設定（如 setup 名稱、使用的核心數、是否批次運算等）來啟動模擬，並回傳模擬是否成功的結果（True 或 False）。

如果是多台電腦的分散式處理設定，我們可以事先手動完成設定，並匯出為 `.acf` 檔案。之後在程式碼當中，用參數 `acf_file` 指定該路徑即可，讓模擬時自動套用這些分散運算設定。


```python
analyze(setup=None, 
        cores=4, 
        tasks=1, 
        gpus=1, 
        acf_file=None, 
        use_auto_settings=True, 
        solve_in_batch=False, 
        machine='localhost', 
        run_in_thread=False, 
        revert_to_initial_mesh=False, 
        blocking=True)
```

### 匯出.acf檔案

![2025-04-12_15-01-26](/assets/2025-04-12_15-01-26.png)

### 執行HPC模擬
直接調用acf_file即可：
```python
hfss.analyze(acf_file='D:/rsm.acf')
```

### 補充 analyze() 參數說明

1. **選擇分析目標**：可以指定特定的 setup 名稱，如果不指定則會對所有 setup 進行分析。
2. **設定硬體資源**：可自訂使用的 CPU 核心數（cores）、模擬任務數（tasks）及 GPU 數量（gpus）。
3. **進階設定**：
   - 可以使用自訂的 ACF 設定檔（`acf_file`）來控制 HPC（高效能運算）參數。
   - `use_auto_settings=True` 時，會根據 setup 自動調整運算資源分配。
4. **控制執行方式**：
   - `solve_in_batch=True` 表示以批次模式執行：專案會被儲存、關閉、模擬，再重新打開。
   - `run_in_thread=True` 可以將分析動作作為非同步執行的 thread 處理。
   - `blocking=True` 則會讓程式碼等到模擬完成後再繼續執行。
5. **模擬初始網格設定**：若 `revert_to_initial_mesh=True`，會在模擬前還原回初始網格狀態。


