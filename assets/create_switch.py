import clr
import os
import re

clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import SaveFileDialog, DialogResult, MessageBox

def generate_netlist(n):
    if n < 0:
        n = 0

    outputs = ["o" + str(i) for i in range(1, n + 1)]
    outputs_str = " ".join(outputs)
    
    lines = []
    lines.append(".subckt switch in {} on=1 Zt=50".format(outputs_str))
    
    # Condition for state 0: all pins connected to Zt
    lines.append(".if(on==0)")
    for i in range(1, n + 1):
        lines.append("r{} o{} 0 Zt".format(i, i))
        
    # Conditions for active switch states (on == 1 to N)
    for k in range(1, n + 1):
        lines.append(".elseif(on=={})".format(k))
        for i in range(1, n + 1):
            if i == k:
                lines.append("r{} o{} in 0".format(i, i))
            else:
                lines.append("r{} o{} 0 Zt".format(i, i))
                
    # Fallback (.else): Handles any other undefined states
    lines.append(".else")
    for i in range(1, n + 1):
        lines.append("r{} o{} 0 Zt".format(i, i))
        
    lines.append(".endif")
    lines.append(".ends")
    return "\r\n".join(lines)

def main():
    default_n = 8
    
    sfd = SaveFileDialog()
    sfd.Filter = "CIR files (*.cir)|*.cir|All files (*.*)|*.*"
    sfd.FilterIndex = 1
    sfd.FileName = "switch{}.cir".format(default_n)
    sfd.Title = "Save Switch Netlist File"

    if sfd.ShowDialog() == DialogResult.OK:
        try:
            filename = os.path.basename(sfd.FileName)
            match = re.search(r'switch(\d+)', filename, re.IGNORECASE)
            
            if match:
                n = int(match.group(1))
            else:
                n = default_n

            netlist_content = generate_netlist(n)
            
            with open(sfd.FileName, 'w') as f:
                f.write(netlist_content)
                
            MessageBox.Show("Successfully generated N={} netlist.\nSaved to: {}".format(n, sfd.FileName), "Success")
        except Exception, e:
            MessageBox.Show("Failed to save file:\n" + str(e), "Error")

if __name__ == "__main__":
    main()