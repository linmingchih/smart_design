Intel MPI安裝與註冊
---
以下設定流程是針對Intel MPI進行安裝和服務啟動的一個詳細步驟。這些步驟包含了舊版本MPI的移除、新版本MPI服務的啟動以及MPI的註冊過程。下面是這些步驟的具體解釋與建議：

### 1. 移除舊的MPI版本 2019.0.10
這一部分主要是清除舊版本MPI的服務，避免舊版本與新版本產生衝突。使用 `sc` 指令來停止、禁用並刪除舊的服務。

```bash
sc stop “impi_hydra_2019_0_10” & sc config “impi_hydra_2019_0_10" start=disabled & sc delete “impi_hydra_2019_0_10”
sc stop “impi_hydra” & sc config “impi_hydra" start=disabled & sc delete “impi_hydra”
```
 
- `sc stop`: 停止MPI服務。
 
- `sc config ... start=disabled`: 禁用服務的自動啟動。
 
- `sc delete`: 刪除服務，以確保舊版本完全清除。

這一步的目的是徹底移除舊有的MPI服務，避免新舊版本之間的衝突。

### 2. 安裝 2021.8.0 MPI
![2024-11-09_14-23-16](/assets/2024-11-09_14-23-16_8y39ofsqf.png)

### 3. 啟動MPI服務 
，接下來需要啟動新版本的MPI服務。以下指令顯示如何使用 `hydra_service.exe` 控制MPI服務。

```bash
C:\Program Files (x86)\Intel\oneAPI\mpi\2021.8.0\bin\hydra_service.exe -install
C:\Program Files (x86)\Intel\oneAPI\mpi\2021.8.0\bin\hydra_service.exe -stop
C:\Program Files (x86)\Intel\oneAPI\mpi\2021.8.0\bin\hydra_service.exe -start
```
 
- `-install`: 用於安裝MPI服務。
 
- `-stop`: 停止MPI服務，通常用於檢查或重啟。
 
- `-start`: 啟動MPI服務。

這些指令確保MPI的服務啟動與停止過程可以順利執行，並且將服務正確配置到系統中。

### 4. MPI註冊 

最後一步是註冊MPI，這是為了確保MPI正確集成到系統中，並且能夠被MPI程序識別和使用。


```bash
C:\Program Files (x86)\Intel\oneAPI\mpi\2021.8.0\bin\mpiexec.exe -register
```

這一指令的作用是將MPI可執行文件與系統註冊，使得後續使用MPI執行程式時能夠順利執行。

 
 **確認服務狀態** ：
在安裝和註冊完MPI後，建議使用以下指令來確認MPI服務的狀態。

```bash
sc qc impi_hydra
```

這個指令可以顯示服務的配置信息，幫助確認服務是否正確啟動。


### 5. 附註
`sc` 是 Windows 操作系統中的一個命令行工具，用於管理和控制系統服務。它提供了許多功能，幫助用戶查詢、啟動、停止、配置和刪除服務。使用 `sc` 命令，管理員可以進行服務的各種操作，包括設置服務的啟動類型、查看服務狀態、管理服務的依賴關係，以及修改服務的安全設置。
#### 主要功能： 
 
1. **查詢服務狀態 (`sc query`)** ：查看服務的當前狀態，了解它是否正在運行。
 
2. **啟動/停止服務 (`sc start`, `sc stop`)** ：啟動或停止指定的服務。
 
3. **配置服務 (`sc config`)** ：修改服務的啟動類型（如自動啟動、手動啟動等）或其他參數。
 
4. **刪除服務 (`sc delete`)** ：刪除指定服務的註冊信息。
 
5. **查看服務安全設置 (`sc sdshow`)** ：顯示服務的安全描述符。