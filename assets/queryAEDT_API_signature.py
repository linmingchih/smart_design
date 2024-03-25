import os, sys
import webbrowser

version_name = oDesktop.GetVersion()
folder = os.path.dirname(os.path.abspath(__file__))

#%%

html='''<!DOCTYPE html>
<html>
<head>
    <style>
    table.fixed {{
        table-layout:fixed; 
        }}
    table.fixed td {{
        overflow: hidden; 
        }}
    </style>
</head>
<body>{}</body>
'''
class ListStream:
    def __init__(self):
        self.data = []
    def write(self, s):
        self.data.append(s)

def dir(x):
    sys.stdout = y = ListStream()
    dir_sig(x)
    sys.stdout = sys.__stdout__
    return [i for i in sorted(y.data) if i.strip()]
    
def returnTable(li,N):
    x=''
    n=0
    for i in li:
        if n==0:
            x+='<tr>'
        x+='<td>{}</td>'.format(i)
        n+=1
        if n==N:
            x+='</tr>\n'
            n=0
    return '<table class="fixed">{}</table>'.format(x)

def generateHtml(funcs, html_name, color='red'):
    html_path=os.path.join(folder, html_name)

    x='<h1 style="color:{}";>{}</h1>'.format(color, html_name)
    for i in funcs:
        f_list = [j for j in funcs[i] if not j.startswith('_')] 
        x+='<h2 style="color:{}";>{}({})</h2>'.format(color, i, len(f_list))
        x+=returnTable(f_list,1)

       
    with open(html_path,'w') as sf:
        sf.writelines(html.format(x))        
    webbrowser.open('file://' + os.path.realpath(html_path))
    
#--------------------------------------------------------------------     
   
from collections import OrderedDict

oProject = oDesktop.NewProject()
oDefinitionManager = oProject.GetDefinitionManager()


def exportFunctions(oDesign, oEditor):
    data=OrderedDict()
    data['oDesktop']=dir(oDesktop)
    data['oProject']=dir(oProject)
    data['oDefinitionManager']=dir(oDefinitionManager)
    data['oDesign']=dir(oDesign)
    data['oEditor']=dir(oEditor)

    for m in ['Point', 'Polygon']:
        try:
            data ['oEditor-'+ m] = dir(getattr(oEditor, m)())
        except:
            pass

    for m in ["NdExplorer","ImportExport"]:
        try:
            data['oTool-'+m]= dir(oDesktop.GetTool(m))
        except:
            pass
    
    
    for m in ["DataBlock","BoundarySetup","MeshSetup","AnalysisSetup","SimSetup","Optimetrics","Solutions","SolveSetups","ModelSetup","FieldsReporter","RadField", "RadiationSetupMgr", "ReduceMatrix","ReportSetup","OutputVariable","UserDefinedSolutionModule","DV","Excitations","Padstack", "Cavities"]:
        try:
            data['oModule-' + m]= dir(oDesign.GetModule(m))
        except:
            pass
  
    for m in ["NdExplorer", "Component", "Material", "Model", "Symbol", "Footprint", "Padstack"]:
        try:
            data['oManager-' + m]= dir(oDefinitionManager.GetManager(m))
        except:
            pass
            
    for i in data:
        data[i] = [j for j in data[i] if not j.startswith('__')]        
  
    return data


#HFSS
oDesign = oProject.InsertDesign("HFSS", "HFSSDesign1", "DrivenModal", "")
oEditor = oDesign.SetActiveEditor("3D Modeler")
data=exportFunctions(oDesign, oEditor)
generateHtml(data, '{}_HFSS_signature.html'.format(version_name), 'OrangeRed')

#3D Layout
oDesign = oProject.InsertDesign("HFSS 3D Layout Design", "EMDesign1", "", "")
oEditor = oDesign.SetActiveEditor("Layout")
data=exportFunctions(oDesign, oEditor)
generateHtml(data, '{}_3D Layout_signature.html'.format(version_name),'RoyalBlue')

#Circuit
oDesign = oProject.InsertDesign("Circuit Design", "Circuit1", "", "")
oEditor = oDesign.SetActiveEditor("SchematicEditor")
data=exportFunctions(oDesign, oEditor)
generateHtml(data, '{}_Circuit_signature.html'.format(version_name),'SeaGreen')

#Q3D
oDesign=oProject.InsertDesign("Q3D Extractor", "Q3DDesign1", "", "")
oEditor = oDesign.SetActiveEditor("3D Modeler")
data=exportFunctions(oDesign, oEditor)
generateHtml(data, '{}_Q3D_signature.html'.format(version_name),'Magenta')

#Maxwell
oDesign=oProject.InsertDesign("Maxwell 3D", "Maxwell3DDesign1", "Magnetostatic", "")
oEditor = oDesign.SetActiveEditor("3D Modeler")
data=exportFunctions(oDesign, oEditor)
generateHtml(data, '{}_Maxwell_signature.html'.format(version_name),'DarkSalmon')

#Icepak
oDesign=oProject.InsertDesign("Icepak", "IcepakDesign2", "TemperatureAndFlow", "")
oEditor = oDesign.SetActiveEditor("3D Modeler")
data=exportFunctions(oDesign, oEditor)
generateHtml(data, '{}_Icepak_signature.html'.format(version_name),'GoldenRod')

#Mechanocal
oDesign=oProject.InsertDesign("Mechanical", "MechanicalDesign1", "", "")
oEditor = oDesign.SetActiveEditor("3D Modeler")
data=exportFunctions(oDesign, oEditor)
generateHtml(data, '{}_Mechanical_signature.html'.format(version_name),'MediumPurple')

#Simplorer
oDesign=oProject.InsertDesign("Twin Builder", "Simplorer1", "", "")
oEditor = oDesign.SetActiveEditor("SchematicEditor")
data=exportFunctions(oDesign, oEditor)
generateHtml(data, '{}_Simplorer_signature.html'.format(version_name),'Sienna')

