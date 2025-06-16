# ----------------------------------------------
# Script Recorded by ANSYS Electronics Desktop Version 2021.1.0
# 8:17:33  May 09, 2021
# ----------------------------------------------
from math import atan, degrees
import ScriptEnv

ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oDesktop.ClearMessages("", "", 2)

oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.GetActiveEditor()
oModule = oDesign.GetModule('Excitations')


def getPadInfo():
    oDefinitionManager = oProject.GetDefinitionManager()
    oPadstackManager = oDefinitionManager.GetManager("Padstack")
    scale = 0.0000254
    x = oPadstackManager.GetNames()
    result = {}
    for i in x:
        try:
            info = oPadstackManager.GetData(i)
            if info[9][9][1][6][1] == 'Rct':
                x, y = info[9][9][1][6][3]
                result[i] = (float(x[:-3]) / 2 * scale, float(y[:-3]) / 2 * scale)
            if info[9][9][1][6][1] == 'Sq':
                x = info[9][9][1][6][3][0]
                result[i] = (float(x[:-3]) / 2 * scale, float(x[:-3]) / 2 * scale)
        except:
            pass
    return result


padinfo = getPadInfo()

def getLayerID():
    result = {}
    for i in oEditor.GetStackupLayerNames():
        x = oEditor.GetLayerInfo(i)
        result[i] = int(x[10].split(':')[1])
    return result


ID = getLayerID()


def disableModel(cmp_name):
    oEditor.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:BaseElementTab",
                [
                    "NAME:PropServers",
                    cmp_name
                ],
                [
                    "NAME:ChangedProps",
                    [
                        "NAME:Model Info",
                        [
                            "NAME:Model",
                            "RLCProp:=",
                            ["CompPropEnabled:=", False, "Pid:=", -1, "Pmo:=", "0", "CompPropType:=", 0, "PinPairRLC:=",
                             ["RLCModelType:=", 0, "ppr:=", ["p1:=", "1", "p2:=", "2", "rlc:=",
                                                             ["r:=", "240ohm", "re:=", True, "l:=", "0", "le:=", False,
                                                              "c:=", "0", "ce:=", False, "p:=", False, "lyr:=", 1]]]],
                            "CompType:=", 1
                        ]
                    ]
                ]
            ]
        ])


def createPort(sx0, sy0, ex0, ey0, sx1, sy1, ex1, ey1):
    ports_old = oModule.GetAllPortsList()
    oEditor.CreateEdgePort(
        [
            "NAME:Contents",
            "edge:=",
            ["et:=", "pse", "sel:=", "{}-2".format(i), "layer:=", layerid, "sx:=", sx0, "sy:=", sy0, "ex:=", ex0,
             "ey:=", ey0, "h:=", 0, "rad:=", 0],
            "external:=", True,
            "btype:=", 0
        ])
    ports_new = oModule.GetAllPortsList()

    portname = list(set(ports_new) - set(ports_old))
    oEditor.AddRefPort(portname,
                       [
                           "NAME:Contents",
                           "edge:=",
                           ["et:=", "pse", "sel:=", "{}-1".format(i), "layer:=", layerid, "sx:=", sx1, "sy:=", sy1,
                            "ex:=", ex1, "ey:=", ey1, "h:=", 0, "rad:=", 0]
                       ])
    renamePort(portname[0], 'port_{}'.format(i))


def renamePort(old, new):
    oDesign.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:EM Design",
                [
                    "NAME:PropServers",
                    "Excitations:{}".format(old)
                ],
                [
                    "NAME:ChangedProps",
                    [
                        "NAME:Port",
                        "Value:="  , new
                    ]
                ]
            ]
        ])

def getAngle(x, y):
    x = 1e-12 if x == 0 else x
    z = round(degrees(atan(y/x)))
    if x < 0:
        return (z-90)%360-180
    else:
        return (z-90)%360

allcmps = oEditor.FindObjects('type', 'component')
for i in oEditor.GetSelections():
    oEditor.SetCS("")
    if i not in allcmps:        
        continue
    if len(oEditor.GetComponentPins(i)) != 2:
        continue

    try:
        pds = oEditor.GetPropertyValue('BaseElementTab', i +'-1', 'Padstack Definition')
        W, H = padinfo[pds]
    except:
        AddErrorMessage('{} does not belong to "square" or "rectangle"!'.format(i))
        continue

    layername = oEditor.GetPropertyValue('BaseElementTab', i, 'PlacementLayer')
    layerid = ID[layername]

    try:
        disableModel(i)
    except:
        pass

    angle = oEditor.GetPropertyValue('BaseElementTab', i + '-1', 'Angle')
    angle = int(float(angle[:-3]))
    loc1 = oEditor.GetPropertyValue('BaseElementTab', i + '-1', 'Location')
    loc2 = oEditor.GetPropertyValue('BaseElementTab', i + '-2', 'Location')
    x1, y1 = [float(j) for j in loc1.split(',')]
    x2, y2 = [float(j) for j in loc2.split(',')]
    dx, dy = x1 - x2, y1 - y2
    orien = getAngle(dx, dy)

    theta = int(angle - orien)%360
    if theta == 0:
        createPort(W, H, -W, H, W, -H, -W, -H)
    elif theta == 90:
        createPort(W, -H, W, H, -W, -H, -W, H)
    elif theta == 180:
        createPort(W, -H, -W, -H, W, H, -W, H)
    elif theta == 270:
        createPort(-W, -H, -W, H, W, -H, W, H)
    else:
        pass
        
    oEditor.SetCS("")

    AddWarningMessage(str(theta))
    AddWarningMessage('port_{}'.format(i))