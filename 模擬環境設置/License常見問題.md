License常見問題
---

### 問題
**在執行長時間模擬時，經常跳出 "Cannot connect to license server" 的錯誤視窗。每次錯誤跳出後需要手動重新連接 license manager，否則程式會自動關閉。這個錯誤不僅影響模擬的穩定性，也可能延長模擬時間。是否有解決方法？**

#### 解答 

這類問題通常可能是由於網路連線不穩或 license server 配置不當導致。可以嘗試以下步驟來解決：
 
1. **設定 `ansyslmd.ini` 檔案** 
在 `C:\Program Files\AnsysEM\Shared Files\Licensing\ansyslmd.ini` 檔案中，將 license server 的名稱和 IP 地址分別設定，並使用不帶分號的方式來增加多個伺服器設定。例如：

```plaintext
SERVER=1055@AAPJCBUFCOMRR
SERVER=1055@172.16.99.190
ANSYSLI_SERVERS=2355@AAPJCBUFCOMRR
ANSYSLI_SERVERS=2325@172.16.99.190
```

這樣的配置可以增加容錯性，若一個 license server 無法連接，ANSYS 會嘗試連接其他的伺服器。
 
2. **檢查網路穩定性** 
由於長時間模擬過程中可能會有臨時的網路斷線或波動，確保工作站與 license server 之間的網路連線穩定。
 
3. **升級或檢查 License Server** 
確認 License Server 的軟體版本符合需求。可能的話，可以嘗試升級到最新的 License Server 版本，這樣有助於避免兼容性問題。

