Q2D輸出S參數
---
UDO的應用，使用者可以在Q2D畫面當中檢視特定長度S參數。限制是當要檢視不同參數對應的曲線時，只能調整設計左下角的屬性欄位來更新。引此也無法將不同參數時S曲線的差異放在同一張圖比較。

![2024-08-27_09-04-59](/assets/2024-08-27_09-04-59_2juqkff3p.png)

![2024-08-27_09-00-47](/assets/2024-08-27_09-00-47_cu415iawg.png)

>範例下載
[aedtz下載](/assets/Q2DS_test_bench.aedtz)

```python
from Ansys.Ansoft.ModulePluginDotNet.Common.API import *
from Ansys.Ansoft.ModulePluginDotNet.Common.API.Interfaces import *
from Ansys.Ansoft.ModulePluginDotNet.UDO.API.Interfaces import * 
from Ansys.Ansoft.ModulePluginDotNet.UDO.API.Data import *

import clr
clr.AddReference("System.Collections")

import os, time
import math
import logging
logging.basicConfig(filename='Q2DS.log', level=logging.DEBUG, filemode='w')
logging.debug('start')

txt_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp.txt')

class Sp:
    def __init__(self, path):
        with open(path) as f:
            text = f.readlines()

        self.n = int(math.sqrt((len(text[0].split())-1)/2))
        
        values = []
        for line in text[1:]:
            values.append([float(i) for i in line.split()])
        
        self.freqs = list(zip(*values))[0]
        matrix = list(zip(*values))[1:]
        
        self.network = {}
        for i in range(self.n):
            for j in range(self.n):
                _u = matrix.pop(0)
                _v = matrix.pop(0)
                self.network['S({},{})'.format(i+1,j+1)] = [complex(u, v) for u, v in zip(_u, _v)]

class UDOExtension(IUDOPluginExtension):
    def __init__(self):
        logging.info(dir(self))
        oDesign = self.GetUDSCommandContext()
        oModule = oDesign.GetModule('AnalysisSetup')

        setup = oDesign.GetChildObject('Analysis').GetChildObject('Setup1')
        f0 = float(setup.GetPropSIValue('Adaptive Freq'))
        
        oDesign.ExportNetworkData("", "Setup1 : Sweep1", txt_path, "Original", 50, [f0], "RealImag", "1meter", 0)
        self.n = Sp(txt_path).n
        logging.debug(self.n)
        
    def GetUDSName(self):
        logging.debug('GetUDSName')
        return "Q2DS"
    
    def GetUDSDescription(self):
        logging.debug('GetUDSDescription')
        return "User Defined Solution: S"

    def GetInputUDSParams(self, udsParams, propertyList, userSelectedDynamicProbes):
        logging.debug('GetInputUDSParams')   
        

        p1 = UDSProbeParams('freq_probe', '', Constants.kDoubleParamStr, '', 'Freq')
        udsParams.Add(p1)
        
        prop = propertyList.AddTextProperty('Length', '1meter')
        prop.Description = 'Length'
        
        return True

    def GetDynamicProbes(self, probes):
        logging.debug('GetDynamicProbes')

    def GetCategoryNames(self):  
        logging.debug('GetCategoryNames')
        return ['S Parameter']
    
    def GetQuantityNames(self, category):
        quantities = []
        for i in range(self.n):
            for j in range(self.n):
                quantities.append('S({},{})'.format(i+1, j+1))
            
        
        logging.debug('GetQuantityNames')
        return quantities

    def GetQuantityInfo(self, qtyName):
        return QuantityInfo(Constants.kComplexParamStr)


    def GetUDSSweepNames(self):
        logging.debug('GetUDSSweepNames')        
        return ["Freq"]


    def Compute(self, inData, outData, params, progressMonitor):
        oDesign = self.GetUDSCommandContext()
        logging.info(dir(oDesign))
        
        logging.debug('Compute')
        
        freqs = list(inData.GetSweepsDataForProbe('freq_probe', 'Freq'))
        logging.debug(freqs)
        length = params.GetTextProperty('Length').Text
        logging.debug(length)

        theDict = dict(inData.GetVariableValues())
        logging.debug(theDict)

        for name in theDict:
            logging.info((name, theDict[name]))

        

        try:
            oDesign.ExportNetworkData("", "Setup1 : Sweep1", txt_path, "Original", 50, freqs, "RealImag", length, 0)
        except:
            return False
        sp = Sp(txt_path)
        logging.debug(sp.network)
        
        outData.SetSweepsData("Freq", freqs)
        
        for i in range(self.n):
            for j in range(self.n):
                doubleFromComplexList = []
                for aComplex in sp.network['S({},{})'.format(i+1, j+1)]:
                    doubleFromComplexList.append(aComplex.real)
                    doubleFromComplexList.append(aComplex.imag)
                    
                outData.SetComplexQuantityData('S({},{})'.format(i+1, j+1), doubleFromComplexList)
                logging.debug(doubleFromComplexList)

        return True





```
