import os
import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

import System.Drawing
import System.Windows.Forms
from System.Windows.Forms import DialogResult, OpenFileDialog
from System.Drawing import *
from System.Windows.Forms import *

class MainForm(Form):
    def __init__(self):
        self.InitializeComponent()
    
    def InitializeComponent(self):
        self._groupBox1 = System.Windows.Forms.GroupBox()
        self._file_tb = System.Windows.Forms.TextBox()
        self._number_tb = System.Windows.Forms.TextBox()
        self._select_bt = System.Windows.Forms.Button()
        self._create_bt = System.Windows.Forms.Button()
        self._message_tb = System.Windows.Forms.TextBox()
        self._label1 = System.Windows.Forms.Label()
        self._groupBox1.SuspendLayout()
        self.SuspendLayout()
        # 
        # groupBox1
        # 
        self._groupBox1.Controls.Add(self._select_bt)
        self._groupBox1.Controls.Add(self._file_tb)
        self._groupBox1.Dock = System.Windows.Forms.DockStyle.Top
        self._groupBox1.Location = System.Drawing.Point(0, 0)
        self._groupBox1.Name = "groupBox1"
        self._groupBox1.Size = System.Drawing.Size(556, 59)
        self._groupBox1.TabIndex = 1
        self._groupBox1.TabStop = False
        self._groupBox1.Text = "Touchstone Path"
        # 
        # file_tb
        # 
        self._file_tb.Dock = System.Windows.Forms.DockStyle.Left
        self._file_tb.Location = System.Drawing.Point(3, 21)
        self._file_tb.Name = "file_tb"
        self._file_tb.Size = System.Drawing.Size(449, 25)
        self._file_tb.TabIndex = 0
        # 
        # number_tb
        # 
        self._number_tb.Location = System.Drawing.Point(397, 73)
        self._number_tb.Name = "number_tb"
        self._number_tb.Size = System.Drawing.Size(55, 25)
        self._number_tb.TabIndex = 2
        self._number_tb.Text = "1"
        self._number_tb.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
        # 
        # select_bt
        # 
        self._select_bt.Location = System.Drawing.Point(458, 15)
        self._select_bt.Name = "select_bt"
        self._select_bt.Size = System.Drawing.Size(92, 33)
        self._select_bt.TabIndex = 1
        self._select_bt.Text = "Select"
        self._select_bt.UseVisualStyleBackColor = True
        self._select_bt.Click += self.Select_btClick
        # 
        # create_bt
        # 
        self._create_bt.Location = System.Drawing.Point(458, 67)
        self._create_bt.Name = "create_bt"
        self._create_bt.Size = System.Drawing.Size(92, 33)
        self._create_bt.TabIndex = 2
        self._create_bt.Text = "Create"
        self._create_bt.UseVisualStyleBackColor = True
        self._create_bt.Click += self.Create_btClick
        # 
        # message_tb
        # 
        self._message_tb.Dock = System.Windows.Forms.DockStyle.Bottom
        self._message_tb.Location = System.Drawing.Point(0, 114)
        self._message_tb.Name = "message_tb"
        self._message_tb.ReadOnly = True
        self._message_tb.Size = System.Drawing.Size(556, 25)
        self._message_tb.TabIndex = 3
        # 
        # label1
        # 
        self._label1.Location = System.Drawing.Point(332, 76)
        self._label1.Name = "label1"
        self._label1.Size = System.Drawing.Size(59, 22)
        self._label1.TabIndex = 4
        self._label1.Text = "Number:"
        # 
        # MainForm
        # 
        self.ClientSize = System.Drawing.Size(556, 139)
        self.Controls.Add(self._label1)
        self.Controls.Add(self._message_tb)
        self.Controls.Add(self._create_bt)
        self.Controls.Add(self._number_tb)
        self.Controls.Add(self._groupBox1)
        self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle
        self.MaximizeBox = False
        self.MinimizeBox = False
        self.Name = "MainForm"
        self.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
        self.Text = "Touchstone Cascade"
        self.TopMost = True
        self._groupBox1.ResumeLayout(False)
        self._groupBox1.PerformLayout()
        self.ResumeLayout(False)
        self.PerformLayout()



    def Select_btClick(self, sender, e):

        dialog = OpenFileDialog()
        dialog.Multiselect = False
        dialog.Title = "Select Touchstone File"
        dialog.Filter = "text files (*.s*p)|*.s*p"
        
        if dialog.ShowDialog() == DialogResult.OK:
            self._file_tb.Text = dialog.FileName
        else:
            pass

    def Create_btClick(self, sender, e):

        data = {}
        snp_path = self._file_tb.Text
        basename = os.path.basename(snp_path)
        model_name, extension = basename.split('.')
        number = int(self._number_tb.Text)
        spice_path = os.path.join(os.path.dirname(snp_path), model_name + '_{}.cir'.format(number))
        port_count = int(extension[1:-1])
        
        
        
        nets = ['net{}'.format(i) for i in range(int(port_count/2)*(number+1))]
        parts = []
        for i in range(number):
            i0 = int(i*(port_count/2))
            i1 = i0 + port_count
            parts.append('S{} {} FQMODEL="{}"'.format(i, ' '.join(nets[i0:i1]), model_name))
        
        data = {'model_name':model_name,
                'number':number,
                'port_count':port_count,
                'snp_path':snp_path,
                'parts':'\n'.join(parts),
                'io':' '.join(nets[:int(port_count/2)] + nets[-int(port_count/2):])}
        
        
        #%%
        netlist = '''
.subckt {model_name}_{number} {io}
.model {model_name} S TSTONEFILE="{snp_path}"
+ INTERPOLATION=LINEAR INTDATTYP=MA HIGHPASS=10 LOWPASS=10 convolution=0 enforce_passivity=0 enforce_adpe=1 Noisemodel=External

{parts}

.ends'''.format(**data)
        
        with open(spice_path, 'w') as f:
            f.write(netlist)
        
        self._message_tb.Text = '{} is generated!'.format(spice_path)
Application.Run(MainForm())