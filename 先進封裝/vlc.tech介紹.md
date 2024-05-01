.vlc.tech 技術檔案
---
AEDT預設支持的是XML格式的技術檔案，從2024R1版本開始支持vlc.tech格式的技術檔案。vlc.tech遵循JSON格式類型，用Python json.load()及jon.dump()便可以讀取/寫入vlc.tech。

[gds_import_example.zip](/assets/gds_import_example.zip)

![2024-05-01_07-07-00](/assets/2024-05-01_07-07-00_ppfwjd7co.png)

以下為一vlc.tech檔格式：

```json
{
    "header": {
        "version": "4.0",
        "corner": "typ"
    },
    "units": {
        "spacing": "um",
        "width": "um",
        "thickness": "um",
        "rpsq": "ohm/sq",
        "rho": "ohm*um",
        "etching": "um",
        "loading_effect": "um",
        "bottom_etching": "um",
        "temperature": "C",
        "tc1": "1/C",
        "tc2": "1/C/C"
    },
    "process": {
        "name": "12nm_process",
        "global_temperature": "25.000000",
        "shrink_factor": 1.0,
        "background_ER": 1.0
    },
    "layers": [
        {
            "type": "conductor",
            "name": "m3",
            "thickness": 5,
            "smin": 0.01,
            "wmin": 0.01,
            "rpsq": 0.00419533478771606,
            "height": 30
        },
        {
            "type": "dielectric",
            "name": "diel2",
            "ER": 4.5,
            "thickness": 30
        },		
		
        {
            "type": "conductor",
            "name": "m2",
            "thickness": 1,
            "smin": 0.01,
            "wmin": 0.01,
            "rpsq": 0.00419533478771606,
            "height": 20
        },
        {
            "type": "dielectric",
            "name": "diel1",
            "ER": 1.1,
            "thickness": 30
        },
        {
            "type": "conductor",
            "name": "m1",
            "thickness": 5,
            "smin": 0.01,
            "wmin": 0.01,
            "rpsq": 0.005593779716954746,
            "height": 10
        }
    ],
    "vias": [
        {
            "name": "via12",
            "from_to": [
                ["m1", "m2"]
            ],
            "rho": 0.01678133915086424
        },
		{
            "name": "via23",
            "from_to": [
                ["m2", "m3"]
            ],
            "rho": 0.01678133915086424
        }
    ]
}
```

### 