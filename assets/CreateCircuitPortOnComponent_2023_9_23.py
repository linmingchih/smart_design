import re
import clr
import copy
import math

clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

import System.Drawing
import System.Windows.Forms

from System.Drawing import *
from System.Windows.Forms import *

oDesktop.ClearMessages("", "", 2)
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.GetActiveEditor()

unit = oEditor.GetActiveUnits()
AddWarningMessage(str(unit))

scale_map = {'mm':1e-3, 'um':1e-6, 'mil':2.54e-5}
scale = scale_map[unit]
# AddWarningMessage(str(scale))

def getComponents():
    return oEditor.FindObjects('Type', 'component')

def getCompPinInfo():
    data = {}
    for comp in oEditor.FindObjects('Type', 'component'):
        data[comp]=[]
        for i in oEditor.GetComponentPins(comp):
            net = oEditor.GetPropertyValue("BaseElementTab", i, "Net")
            Location = oEditor.GetPropertyValue("BaseElementTab", i, "Location")
            x, y = map(float, Location.split(','))
            start_layer = oEditor.GetPropertyValue("BaseElementTab", i, "Start Layer")
            data[comp].append((i, net, x, y, start_layer))
    return data


class MainForm(Form):
    def __init__(self):
        self.InitializeComponent()
    
    def InitializeComponent(self):
        self._groupBox1 = System.Windows.Forms.GroupBox()
        self._component_filter_tb = System.Windows.Forms.TextBox()
        self._component_cb = System.Windows.Forms.ComboBox()
        self._groupBox2 = System.Windows.Forms.GroupBox()
        self._reference_cb = System.Windows.Forms.ComboBox()
        self._reference_filter_tb = System.Windows.Forms.TextBox()
        self._create_bt = System.Windows.Forms.Button()
        self._label1 = System.Windows.Forms.Label()
        self._label2 = System.Windows.Forms.Label()
        self._label3 = System.Windows.Forms.Label()
        self._label4 = System.Windows.Forms.Label()
        self._groupBox3 = System.Windows.Forms.GroupBox()
        self._label5 = System.Windows.Forms.Label()
        self._pins_filter_tb = System.Windows.Forms.TextBox()
        self._pins_clb = System.Windows.Forms.CheckedListBox()
        self._groupBox1.SuspendLayout()
        self._groupBox2.SuspendLayout()
        self._groupBox3.SuspendLayout()
        self.SuspendLayout()
        # 
        # groupBox1
        # 
        self._groupBox1.Controls.Add(self._label2)
        self._groupBox1.Controls.Add(self._label1)
        self._groupBox1.Controls.Add(self._component_cb)
        self._groupBox1.Controls.Add(self._component_filter_tb)
        self._groupBox1.Location = System.Drawing.Point(12, 12)
        self._groupBox1.Name = "groupBox1"
        self._groupBox1.Size = System.Drawing.Size(341, 100)
        self._groupBox1.TabIndex = 0
        self._groupBox1.TabStop = False
        self._groupBox1.Text = "1> Select Component"
        # 
        # component_filter_tb
        # 
        self._component_filter_tb.Location = System.Drawing.Point(114, 24)
        self._component_filter_tb.Name = "component_filter_tb"
        self._component_filter_tb.Size = System.Drawing.Size(221, 25)
        self._component_filter_tb.TabIndex = 0
        self._component_filter_tb.TextChanged += self.Component_filter_tbTextChanged
        # 
        # component_cb
        # 
        self._component_cb.FormattingEnabled = True
        self._component_cb.Location = System.Drawing.Point(114, 56)
        self._component_cb.Name = "component_cb"
        self._component_cb.Size = System.Drawing.Size(221, 23)
        self._component_cb.TabIndex = 1
        self._component_cb.SelectedIndexChanged += self.Component_cbSelectedIndexChanged
        # 
        # groupBox2
        # 
        self._groupBox2.Controls.Add(self._label4)
        self._groupBox2.Controls.Add(self._label3)
        self._groupBox2.Controls.Add(self._reference_cb)
        self._groupBox2.Controls.Add(self._reference_filter_tb)
        self._groupBox2.Location = System.Drawing.Point(12, 118)
        self._groupBox2.Name = "groupBox2"
        self._groupBox2.Size = System.Drawing.Size(341, 100)
        self._groupBox2.TabIndex = 2
        self._groupBox2.TabStop = False
        self._groupBox2.Text = "2> Select Reference"
        # 
        # reference_cb
        # 
        self._reference_cb.FormattingEnabled = True
        self._reference_cb.Location = System.Drawing.Point(114, 56)
        self._reference_cb.Name = "reference_cb"
        self._reference_cb.Size = System.Drawing.Size(221, 23)
        self._reference_cb.TabIndex = 1
        self._reference_cb.SelectedIndexChanged += self.Reference_cbSelectedIndexChanged
        # 
        # reference_filter_tb
        # 
        self._reference_filter_tb.Location = System.Drawing.Point(114, 24)
        self._reference_filter_tb.Name = "reference_filter_tb"
        self._reference_filter_tb.Size = System.Drawing.Size(221, 25)
        self._reference_filter_tb.TabIndex = 0
        self._reference_filter_tb.TextChanged += self.Reference_filter_tbTextChanged
        # 
        # create_bt
        # 
        self._create_bt.Location = System.Drawing.Point(18, 508)
        self._create_bt.Name = "create_bt"
        self._create_bt.Size = System.Drawing.Size(329, 45)
        self._create_bt.TabIndex = 4
        self._create_bt.Text = "4> Create Ports"
        self._create_bt.UseVisualStyleBackColor = True
        self._create_bt.Click += self.Create_btClick
        # 
        # label1
        # 
        self._label1.Location = System.Drawing.Point(6, 27)
        self._label1.Name = "label1"
        self._label1.Size = System.Drawing.Size(100, 23)
        self._label1.TabIndex = 2
        self._label1.Text = "Filter(Regex)"
        # 
        # label2
        # 
        self._label2.Location = System.Drawing.Point(6, 59)
        self._label2.Name = "label2"
        self._label2.Size = System.Drawing.Size(100, 23)
        self._label2.TabIndex = 3
        self._label2.Text = "Component"
        # 
        # label3
        # 
        self._label3.Location = System.Drawing.Point(6, 27)
        self._label3.Name = "label3"
        self._label3.Size = System.Drawing.Size(100, 23)
        self._label3.TabIndex = 4
        self._label3.Text = "Filter(Regex)"
        # 
        # label4
        # 
        self._label4.Location = System.Drawing.Point(6, 59)
        self._label4.Name = "label4"
        self._label4.Size = System.Drawing.Size(100, 23)
        self._label4.TabIndex = 5
        self._label4.Text = "Reference Net"
        # 
        # groupBox3
        # 
        self._groupBox3.Controls.Add(self._pins_clb)
        self._groupBox3.Controls.Add(self._label5)
        self._groupBox3.Controls.Add(self._pins_filter_tb)
        self._groupBox3.Location = System.Drawing.Point(359, 13)
        self._groupBox3.Name = "groupBox3"
        self._groupBox3.Size = System.Drawing.Size(385, 543)
        self._groupBox3.TabIndex = 5
        self._groupBox3.TabStop = False
        self._groupBox3.Text = "3> Check Pins For Ports"
        # 
        # label5
        # 
        self._label5.Location = System.Drawing.Point(10, 26)
        self._label5.Name = "label5"
        self._label5.Size = System.Drawing.Size(100, 23)
        self._label5.TabIndex = 5
        self._label5.Text = "Filter(Regex)"
        # 
        # pins_filter_tb
        # 
        self._pins_filter_tb.Location = System.Drawing.Point(118, 23)
        self._pins_filter_tb.Name = "pins_filter_tb"
        self._pins_filter_tb.Size = System.Drawing.Size(148, 25)
        self._pins_filter_tb.TabIndex = 4
        self._pins_filter_tb.TextChanged += self.Pins_filter_tbTextChanged
        # 
        # pins_clb
        # 
        self._pins_clb.Dock = System.Windows.Forms.DockStyle.Bottom
        self._pins_clb.FormattingEnabled = True
        self._pins_clb.Location = System.Drawing.Point(3, 56)
        self._pins_clb.Name = "pins_clb"
        self._pins_clb.ScrollAlwaysVisible = True
        self._pins_clb.Size = System.Drawing.Size(379, 484)
        self._pins_clb.TabIndex = 6
        self._pins_clb.SelectedIndexChanged += self.Pins_clbSelectedIndexChanged
        self._pins_clb.MouseUp += self.Pins_clbMouseUp
        # 
        # MainForm
        # 
        self.ClientSize = System.Drawing.Size(756, 565)
        self.Controls.Add(self._groupBox3)
        self.Controls.Add(self._create_bt)
        self.Controls.Add(self._groupBox2)
        self.Controls.Add(self._groupBox1)
        self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle
        self.MaximizeBox = False
        self.MinimizeBox = False
        self.Name = "MainForm"
        self.Text = "Create Circuit Ports on Components"
        self.Load += self.MainFormLoad
        self._groupBox1.ResumeLayout(False)
        self._groupBox1.PerformLayout()
        self._groupBox2.ResumeLayout(False)
        self._groupBox2.PerformLayout()
        self._groupBox3.ResumeLayout(False)
        self._groupBox3.PerformLayout()
        self.ResumeLayout(False)


    def MainFormLoad(self, sender, e):
        self.data = getCompPinInfo()
        self.components = sorted(getComponents())

        sel = oEditor.GetSelections()
        if sel and sel[0] in self.components:
            index = self.components.index(sel[0])
        else:
            index = 0
            
        self.Refresh_component_tb(index)
    
    def Refresh_component_tb(self, index=0):
        pattern = self._component_filter_tb.Text
        filtered = [i for i in self.components if re.search(pattern, i)] 
        
        self._component_cb.Items.Clear()
        for i in filtered:
            self._component_cb.Items.Add(i)
        
        try:
            self._component_cb.SelectedIndex = index
        except:
            self._component_cb.Text = ''
            
            
    def Component_filter_tbTextChanged(self, sender, e):
        self.Refresh_component_tb()

    def Pins_filter_tbTextChanged(self, sender, e):
        self.Reference_cbSelectedIndexChanged(sender, e)

    def Reference_filter_tbTextChanged(self, sender, e):
        self.Component_cbSelectedIndexChanged(sender, e)

    def Reference_cbSelectedIndexChanged(self, sender, e):
        pins = []
        pg = []
        for pin, net, _, _, _ in self.data[self._component_cb.SelectedItem]:
            if net != self._reference_cb.SelectedItem:
                pins.append(pin+':'+net)
        
        for i in oEditor.FindObjects('Type', 'PinGroup'):
            if self._component_cb.SelectedItem in i and self._reference_cb.SelectedItem != i:
                pg.append(i)
        
        if self._reference_cb.SelectedItem in oEditor.FindObjects('Type', 'PinGroup'):
            tobecheck = sorted(pg) + sorted(pins)
        else:
            tobecheck = sorted(pins)                

        filtered = [i for i in tobecheck if re.search(self._pins_filter_tb.Text, i)]
        
        self._pins_clb.Items.Clear()
        for i in filtered:
            self._pins_clb.Items.Add(i)

    def Component_cbSelectedIndexChanged(self, sender, e):
        reference = sorted(oEditor.FindObjects('Type', 'PinGroup'))
        nets = []
        for pin, net, _, _, _ in self.data[self._component_cb.SelectedItem]:
            if net not in nets:
                nets.append(net)
                
        reference += sorted(nets)
        
        pattern = self._reference_filter_tb.Text
        filtered = [i for i in reference if re.search(pattern, i)]
        
        self._reference_cb.Items.Clear()
        for i in filtered:
            self._reference_cb.Items.Add(i)        
        
        try:
            self._reference_cb.SelectedIndex = 0
        except:
            self._reference_cb.Text = ''    

    def Pins_clbSelectedIndexChanged(self, sender, e):
        index = self._pins_clb.SelectedIndex
        if index != -1:
            self._pins_clb.SetItemChecked(index, not self._pins_clb.GetItemChecked(index))


    def Pins_clbMouseUp(self, sender, e):
        if e.Button == MouseButtons.Right:
            checked_cbs = [item.split(':')[0].strip('_') for item in self._pins_clb.CheckedItems]
            if checked_cbs:
                for i in range(len(self._pins_clb.Items)):
                    self._pins_clb.SetItemChecked(i, False)
            else:
                for i in range(len(self._pins_clb.Items)):
                    self._pins_clb.SetItemChecked(i, True)                
            
    def Create_btClick(self, sender, e):
        checked_cbs = [item.split(':')[0].strip('_') for item in self._pins_clb.CheckedItems]
        
        checked_pins=[]
        for i in checked_cbs:
            for j in self.data[self._component_cb.SelectedItem]:
                if j[0] == i:
                    checked_pins.append(j)
                    break
            else:
                checked_pins.append(i)
                    
        #AddWarningMessage(str(checked_pins))
        
        if self._reference_cb.SelectedItem in oEditor.FindObjects('Type', 'PinGroup'):
            for i in checked_pins:
                AddWarningMessage(str(i))
                
                if i in oEditor.FindObjects('Type', 'PinGroup'):
                    self.createPinGroupPort(i, self._reference_cb.SelectedItem)
                    continue
                
                elif i[0].startswith(self._component_cb.SelectedItem) and i[0].endswith(i[1]):
                    port_name = i[0]
                
                
                elif self._component_cb.SelectedItem + '-' in i[0]:
                    port_name = i[0].replace('-','.') + '.' + i[1]
                    
                elif i[1] == '':
                    AddWarningMessage('Ignore {}: No net assignment!'.format(i[0]))
                    continue
                else:
                    port_name = "{}.{}.{}".format(self._component_cb.SelectedItem, i[0], i[1])
                
                AddWarningMessage('port_name:'+port_name)
                
                oEditor.ToggleViaPin(
                    [
                        "NAME:elements", 
                        i[0]
                    ])
                oEditor.AddPinGroupRefPort([port_name], [self._reference_cb.SelectedItem])                
        
        else:
            reference_pins=[i for i in self.data[self._component_cb.SelectedItem] if i[1] == self._reference_cb.SelectedItem]
                   
            for i in checked_pins:
                info=[]
                x0, y0 = i[2], i[3]
                for j in reference_pins:
                    x1, y1 = j[2], j[3]
                    distance = math.sqrt((x1-x0)**2 + (y1-y0)**2)
                    info.append((distance, i, j))
                
                info.sort()
                _, i, j = info[0]
            
                oEditor.CreateCircuitPort(
                    [
                        "NAME:Location",
                        "PosLayer:="		, i[4],
                        "X0:="			, i[2]*scale,
                        "Y0:="			, i[3]*scale,
                        "NegLayer:="		, j[4],
                        "X1:="			, j[2]*scale,
                        "Y1:="			, j[3]*scale
                    ])
                oDesign.ChangeProperty(
                    [
                        "NAME:AllTabs",
                        [
                            "NAME:EM Design",
                            [
                                "NAME:PropServers", 
                                "Excitations:Port1"
                            ],
                            [
                                "NAME:ChangedProps",
                                [
                                    "NAME:Port",
                                    "Value:="		, "{}.{}.{}".format(self._component_cb.SelectedItem, i[0], i[1])
                                ]
                            ]
                        ]
                    ])

Application.Run(MainForm())

