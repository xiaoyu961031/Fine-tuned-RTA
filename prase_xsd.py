import os
import glob

cif_directory = 'cif_file'
cif_files = glob.glob(os.path.join(cif_directory, "*.cif"))
xsd_directory = 'xsd_file'
pac_directory = 'cif_file_pacmof'
xsd_new_directory = 'xsd_file_prased'

for root, dirs, files in os.walk(cif_directory):
    for file in files:
        if file.endswith('.cif'):
            mofname = file.split('.cif')[0]           
            cif_file = open(pac_directory+'/'+mofname+'_charged.cif','r')
            cif_content = cif_file.readlines()
            start_line = 25
            atom_lines = cif_content[start_line:]
            atom_len = len(atom_lines)
            
            xsd_file = open(xsd_directory+'/'+mofname+'.xsd','r')
            xsd_content = xsd_file.readlines()

            xsd_atom_lines_new = []

            end_xsd = 71 + atom_len
            xsd_atom_lines = xsd_content[71:end_xsd]
            for i in range(atom_len):     
                cif_line = atom_lines[i]
                charge = cif_line.split()[-1]
                xsd_atom_line_new = xsd_atom_lines[i].strip('/>\n') + ' Charge="'+str(charge)+"\""+" />\n"
                xsd_atom_lines_new.append(xsd_atom_line_new)
                
            xsd_content[71:end_xsd] = xsd_atom_lines_new
                
            xsd_file_new = open(xsd_new_directory+'/'+mofname+'.xsd','w')
            for line in xsd_content:
                xsd_file_new.writelines(line) 

#don't know why the last MOF is not properly looped thus do this for this
last_MOF = files[-1]
mofname = last_MOF.split('.cif')[0]           
cif_file = open(pac_directory+'/'+mofname+'_charged.cif','r')
cif_content = cif_file.readlines()
start_line = 25
atom_lines = cif_content[start_line:]
atom_len = len(atom_lines)
            
xsd_file = open(xsd_directory+'/'+mofname+'.xsd','r')
xsd_content = xsd_file.readlines()
xsd_atom_lines_new = []
end_xsd = 71 + atom_len
xsd_atom_lines = xsd_content[71:end_xsd]
for i in range(atom_len):     
    cif_line = atom_lines[i]
    charge = cif_line.split()[-1]
    xsd_atom_line_new = xsd_atom_lines[i].strip('/>\n') + ' Charge="'+str(charge)+"\""+" />\n"
    xsd_atom_lines_new.append(xsd_atom_line_new)
                
xsd_content[71:end_xsd] = xsd_atom_lines_new
                
xsd_file_new = open(xsd_new_directory+'/'+mofname+'.xsd','w')
for line in xsd_content:
    xsd_file_new.writelines(line) 