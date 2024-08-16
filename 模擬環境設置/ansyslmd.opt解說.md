ansyslmd.opt解說
---

ansyslmd.opt 是 ANSYS 授權伺服器中用於管理授權選項的檔案。您可以在這個檔案中設定特定的授權規則，使系統管理員能夠針對特定用戶或群組設定授權使用規則，如預約、排除或限制授權的使用。您可以定義使用者和機器，以便有效管理授權的使用和分配。

ansyslmd.opt 在檔案伺服器上的典型路徑為 "C:\Program Files\ANSYS Inc\Shared Files\licensing\license_files"。這個位置是 ANSYS 軟件安裝時所建立的。使用者可以自行在該目錄下創建ansyslmd.opt。

舉例來說，如果您想為特定的使用者 `user1` 預留授權，可以在ansyslmd.opt檔案使用以下語法：

```sql
RESERVE 1 elec_solve_hfss USER user1
```
這表示為使用者 `user1` 預留一個 `elec_solve_hfss` 的授權。

#### 群組定義 (GROUP / HOST_GROUP)
您也可以創建群組，將多個使用者或機器分類管理。例如，創建一個包含三個使用者的群組 `gr1`：

```sql
GROUP gr1 user1 user2 user3
```
如果是要按機器來定群組，可以如下所示定義名為 `gr3` 的機器群組：

```Copy code
HOST_GROUP gr3 host1 host2 host3
```

這樣的設定允許系統管理員更有效地管理授權使用，特別是在大型組織中，或者當授權數量有限時，這樣可以確保重要的任務或用戶能夠獲得所需的資源。

您可以通過指定 INCLUDE、EXCLUDE、RESERVE 和 MAX 規則來管理授權的使用。以下提供繁體中文版本的說明和範例：

#### 許可（INCLUDE）的指定 

許可規則允許您為特定群組定義可以使用某個授權功能的許可。
 
- **範例** ：

```sql
INCLUDE elec_solve_hfss GROUP gr1
```
這表示只有 `gr1` 群組的成員可以使用 `elec_solve_hfss` 的功能。

#### 拒絕（EXCLUDE）的指定 

拒絕規則允許您為特定群組定義禁止使用某個授權功能的設定。
 
- **範例** ：

```sql
EXCLUDE elec_solve_hfss GROUP gr1
```
這表示 `gr1` 群組的成員不能使用 `elec_solve_hfss` 的功能。

#### 預約（RESERVE）的指定 

預約規則允許您為特定群組預留一定數量的授權功能。
 
- **範例** ：

```sql
RESERVE 1 elec_solve_hfss GROUP gr1
```
這表示為 `gr1` 群組預留了一個 `elec_solve_hfss` 的功能。

#### 上限數（MAX）的指定 

上限數規則允許您為特定群組設定授權功能的使用上限。
 
- **範例** ：

```sql
MAX 1 elec_solve_hfss GROUP gr1
```
這表示 `gr1` 群組中的成員共同使用 `elec_solve_hfss` 的功能時，最多只能有一個實例在使用。

這些規則的設定可以幫助系統管理員更有效地分配和管理授權資源，確保重要任務或特定用戶群組可以獲得所需的授權。

### 舉例
以下是如何定義群組並為各個群組預約特定功能的詳細範例說明：

#### 群組定義 

首先，定義兩個使用者群組：
 
- **群組 gr1**  包括使用者 `user1`、`user2` 和 `user3`。
 
- **群組 gr2**  包括使用者 `usera`、`userb` 和 `userc`。

#### 功能預約 

接著，為這些群組預留特定的功能：
 
- 為群組 `gr1` 預約 `elec_solve_hfss` 的 1 個授權。
 
- 為群組 `gr2` 預約 `elec_solve_hfss` 的 2 個授權。

#### 配置範例 

ansyslmd.opt 配置文件中相對應的記述會如下所示：


```plaintext
GROUP gr1 user1 user2 user3
GROUP gr2 usera userb userc
RESERVE 1 elec_solve_hfss GROUP gr1
RESERVE 2 elec_solve_hfss GROUP gr2
```

#### 效果說明 
 
- **群組 gr1**  的成員（`user1`、`user2`、`user3`）共享 1 個 `elec_solve_hfss` 的授權，這意味著在同一時間內只有一個成員可以使用這個授權。
 
- **群組 gr2**  的成員（`usera`、`userb`、`userc`）則可以同時有兩個人使用 `elec_solve_hfss` 的授權。

透過這樣的設定，系統管理員可以根據各群組的需求和重要性來合理分配授權資源，確保關鍵任務或特定用戶群體能夠得到所需的授權。这种管理方式对于控制和优化授权使用尤其有效，特别是在资源有限的情况下。


### TIMEOUT參數
`TIMEOUT` 是一個選項檔案（如 `ansyslmd.opt`）中可以設定的參數，用來指定在多久時間內未使用的特定授權功能將被自動釋放回授權池。這對於管理不活躍的授權非常有用，特別是在多用戶環境中，可以幫助確保授權的有效利用。使用 `TIMEOUT` 的目的：`TIMEOUT` 的主要目的是自動釋放長時間未被使用的授權，從而允許其他用戶或過程訪問這些授權。這尤其重要於需要高度動態共享授權的環境中。如何設置 `TIMEOUT`：`TIMEOUT` 的設置通常寫在選項檔案中，格式如下：

```plaintext
TIMEOUT feature_name timeout_seconds
```
 
- `feature_name`：是指需要設置超時的授權功能名稱。
 
- `timeout_seconds`：是指在多少秒後，如果授權未被使用，則自動釋放。

### 範例： 
假設您想為 `elec_solve_hfss` 功能設置一個超時時間，使其在 7200 秒（2小時）內未被使用就自動釋放，您可以在選項檔案中寫入：

```plaintext
TIMEOUT elec_solve_hfss 7200
```
這樣，如果 `elec_solve_hfss` 功能在兩小時內沒有被任何用戶使用，它就會被自動釋放，其他用戶就可以訪問這個授權了。
### 注意事項： 
 
- 設置 `TIMEOUT` 需要謹慎，因為過短的超時時間可能會導致用戶在使用中被中斷。

- 某些功能或特定情況下，可能不適合使用超時設置，如長時間運行的模擬。
通過合理配置 `TIMEOUT`，系統管理員可以更靈活地管理授權資源，提高授權使用的效率和公平性。