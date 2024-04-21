.vlc.tech 技術檔案
---
AEDT預設支持的是XML格式的技術檔案，從2024R1版本開始支持vlc.tech格式的技術檔案。vlc.tech遵循JSON格式類型，用Python json.load()及jon.dump()便可以讀取/寫入vlc.tech。以下為一vlc.tech檔格式：

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
            "type": "dielectric",
            "name": "diel_bottomAir",
            "ER": 1.1,
            "thickness": 4.95
        },
        {
            "type": "conductor",
            "name": "metal1",
            "thickness": 5.1,
            "smin": 0.01,
            "wmin": 0.01,
            "rpsq": 0.003356267830172848,
            "height": 4.95
        },
        {
            "type": "dielectric",
            "name": "diel2",
            "ER": 4.5,
            "thickness": 11.0
        },
        {
            "type": "conductor",
            "name": "VSS",
            "thickness": 4.1,
            "smin": 0.01,
            "wmin": 0.01,
            "rpsq": 0.00419533478771606,
            "height": 9.95
        },
        {
            "type": "conductor",
            "name": "metal2",
            "thickness": 4.1,
            "smin": 0.01,
            "wmin": 0.01,
            "rpsq": 0.00419533478771606,
            "height": 13.95
        },
        {
            "type": "dielectric",
            "name": "diel3",
            "ER": 1.1,
            "thickness": 22.0
        },
        {
            "type": "conductor",
            "name": "metal3",
            "thickness": 3.1,
            "smin": 0.01,
            "wmin": 0.01,
            "rpsq": 0.005593779716954746,
            "height": 17.95
        },
        {
            "type": "conductor",
            "name": "metal5",
            "thickness": 2.1,
            "smin": 0.01,
            "wmin": 0.01,
            "rpsq": 0.00839066957543212,
            "height": 35.95
        }
    ],
    "vias": [
        {
            "name": "via_die",
            "from_to": [
                ["metal3", "metal5"]
            ],
            "rho": 0.01678133915086424
        }
    ]
}
```

### 