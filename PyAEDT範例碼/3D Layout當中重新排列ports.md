3D Layout當中重新排列ports
---
**使用者可以利用AI Agents協助進行port的重新排列。將以下程式碼貼到Prompt當中，並根據自己需求重新描述排序邏輯，讓AI Agent重新生成新的程式碼。**

這段程式的排序邏輯可分為三個層級，核心目的是將所有 port 依照「晶片 → 訊號類型 → 編號 → 差分極性」進行有結構的排列。

首先，程式會從 port 名稱中解析出晶片名稱（例如 U1、U2），並將所有 port 依晶片分組。接著透過正則表達式擷取數字，將晶片依編號由小到大排序，例如 U1、U2、U10。

第二層是在每顆晶片內，依訊號類型分類，順序固定為 DQ → DMI → WCK → RDQS。這代表資料線（DQ）優先，其次是遮罩（DMI），再來是時脈（WCK）與讀取 strobe（RDQS）。

第三層是每個訊號類型內的排序規則。對於 DQ 和 DMI，依其數字編號（例如 DQ0、DQ1）由小到大排序；對於 WCK 與 RDQS，除了編號排序外，還會進一步依差分對的極性排序，確保 T（True）在前、C（Complement）在後。

最終結果是形成一個高度結構化且符合訊號邏輯的 port 順序，並透過 ReorderMatrix 套用於矩陣排列。

![](/assets/2026-03-26_16-26-10.png)

```python
import re

oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oModule = oDesign.GetModule("Excitations")

all_ports = oModule.GetAllPortsList()


def get_chip_name(port_name):
    parts = port_name.split("_")
    if len(parts) < 2:
        return None
    return parts[-2]


def get_chip_sort_key(chip_name):
    m = re.match(r"^U(\d+)$", chip_name)
    if m:
        return int(m.group(1))
    return 999999


def get_signal_info(port_name):
    parts = port_name.split("_")
    n_parts = len(parts)

    i = 0
    while i < n_parts:
        token = parts[i]

        m = re.match(r"^DQ(\d+)$", token)
        if m:
            return ("DQ", int(m.group(1)))

        m = re.match(r"^DMI(\d+)$", token)
        if m:
            return ("DMI", int(m.group(1)))

        m = re.match(r"^WCK(\d+)$", token)
        if m and i + 1 < n_parts:
            nxt = parts[i + 1]
            if nxt == "T":
                return ("WCK", int(m.group(1)), 0)
            elif nxt == "C":
                return ("WCK", int(m.group(1)), 1)

        m = re.match(r"^RDQS(\d+)$", token)
        if m and i + 1 < n_parts:
            nxt = parts[i + 1]
            if nxt == "T":
                return ("RDQS", int(m.group(1)), 0)
            elif nxt == "C":
                return ("RDQS", int(m.group(1)), 1)

        i += 1

    return None


# group by chip
chip_dict = {}
for port in all_ports:
    chip = get_chip_name(port)
    if chip is None:
        continue

    if chip not in chip_dict:
        chip_dict[chip] = []

    chip_dict[chip].append(port)


# sort chip order (U1, U2, ...)
chip_names = sorted(chip_dict.keys(), key=get_chip_sort_key)

ordered_ports = []

for chip in chip_names:

    dq_list = []
    dmi_list = []
    wck_list = []
    rdqs_list = []

    for port in chip_dict[chip]:
        info = get_signal_info(port)
        if info is None:
            continue

        sig_type = info[0]

        if sig_type == "DQ":
            dq_list.append((info[1], port))

        elif sig_type == "DMI":
            dmi_list.append((info[1], port))

        elif sig_type == "WCK":
            wck_list.append((info[1], info[2], port))

        elif sig_type == "RDQS":
            rdqs_list.append((info[1], info[2], port))

    dq_list.sort(key=lambda x: x[0])
    dmi_list.sort(key=lambda x: x[0])
    wck_list.sort(key=lambda x: (x[0], x[1]))
    rdqs_list.sort(key=lambda x: (x[0], x[1]))

    ordered_ports.extend([p for _, p in dq_list])
    ordered_ports.extend([p for _, p in dmi_list])
    ordered_ports.extend([p for _, _, p in wck_list])
    ordered_ports.extend([p for _, _, p in rdqs_list])


# print result
print("Sorted ports:")
i = 1
for p in ordered_ports:
    print(str(i) + ": " + p)
    i += 1


# reorder matrix
oModule.ReorderMatrix(ordered_ports)

print("ReorderMatrix done.")

```