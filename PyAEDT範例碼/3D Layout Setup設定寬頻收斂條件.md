3D Layout Setup設定寬頻收斂條件
---

**Multi Frequency模式**
MaxPasses的值只能在Single Frequency模式下設定，設定完之後再切換到Multi Frequency模式。

**Broadband模式**
MaxPasses及MaxDelta的值只能在Single Frequency模式下設定，設定完之後再切換到Broadband模式。



```python
from ansys.aedt.core import Hfss3dLayout

hfss = Hfss3dLayout(version='2025.2')

setup = hfss.create_setup()

#%% Single Frequency
setup.props['AdaptiveSettings']['AdaptType']='kSingle'

x = [{'AdaptiveFrequency': '3.4GHz',
      'MaxDelta': '0.013',
      'MaxPasses': 16,
      'Expressions': []}]

setup.props['AdaptiveSettings']['SingleFrequencyDataList']['AdaptiveFrequencyData'] = x


#%% Multi Frequency
setup.props['AdaptiveSettings']['AdaptType']='kMultiFrequencies'

setup.props['AdaptiveSettings']['MultiFrequencyDataList']['AdaptiveFrequencyData']


x = [{'AdaptiveFrequency': '1.11GHz',
      'MaxDelta': '0.013',
      'MaxPasses': 10,
      'Expressions': []},
     {'AdaptiveFrequency': '2.22GHz',
      'MaxDelta': '0.014',
      'MaxPasses': 10,
      'Expressions': []}
]
 

setup.props['AdaptiveSettings']['MultiFrequencyDataList']['AdaptiveFrequencyData'] = x

#%% Broadband Frequency

setup.props['AdaptiveSettings']['AdaptType']='kBroadband'

x = [{'AdaptiveFrequency': '3.4GHz',
      'MaxDelta': '0.02',
      'MaxPasses': 10,
      'Expressions': []},
     {'AdaptiveFrequency': '7.8GHz',
      'MaxDelta': '0.02',
      'MaxPasses': 10,
      'Expressions': []}]

setup.props['AdaptiveSettings']['BroadbandFrequencyDataList']['AdaptiveFrequencyData'] = x

```

![](/assets/2026-04-10_08-53-41.jpg)