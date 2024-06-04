import os
import pormake as pm

topology_data = {
        ("3c", "2c"): ["srs"],
        ("3c", "3c"): ["bwt", "pyo"],
        ("3c", "square"): ['fjh', 'fmj', 'gee', 'iab'],
        ("3c", "tet"): [ 'ofp'],
        ("3c", "hexagon"): [],
        ("3c", "oct"): ["anh", "ant", "apo", "brk", "cml", "eea", "qom", "rtl", "tsx", "zzz"],
        ("square", "2c"): ["nbo", "lvt", "rhr"],
        ("square", "3c"): ["pto", "tbo"],
        ("square", "square"): ["cdl", "cdm", "cdn", "cds", "cdz", "mot", "muo", "qdl", "qzd", "ssd", "sse", "ssf", "sst"], 
        ("square", "tet"): ["pts"],
        ("square", "hexagon"): [], 
        ("square", "oct"): ["myd", "ybh"],
        ("tet", "2c"): ["dia", "lcs", "qtz", "sod"],
        ("tet", "3c"): ["bor", "ctn"],
        ("tet", "square"): ["fgl", "mog", "pds","pth", "pti", "ptr", "ptt"], 
        ("tet", "tet"): ["bnl", "byl", "cag", "cbt", "coe", "crb", "fel", "icm", "kea", "lon", "pcl", "sca",'tpd',"ucn"],
        ("tet", "hexagon"): [], 
        ("tet", "oct"): [ "alw", "bix", "cor", "spl", "toc"],     
        ("hexagon", "2c"): ["hxg"],
        ("hexagon", "3c"): [],
        ("hexagon", "square"): ["she"], 
        ("hexagon", "tet"): [],
        ("hexagon", "hexagon"): [], 
        ("hexagon", "oct"): [],      
        ("oct", "2c"): ["pcu", "bcs", "crs", "reo"],
        ("oct", "3c"): ["pyr", "spn"],
        ("oct", "square"): ["soc"], 
        ("oct", "tet"): ["gar", "iac", "ibd", "toc"],
        ("oct", "hexagon"): [], 
        ("oct", "oct"): [],      
        ("trp", "2c"): [ "lcy", "acs"],
        ("trp", "3c"): ["dag", "hwx", "moo", "sab", "sit", "ydq"],
        ("trp", "square"): ["stp"], 
        ("trp", "tet"): ["fsi", "hea", "tpt"],
        ("trp", "hexagon"): ["htp"], 
        ("trp", "oct"): ["nia"],     
        ("8c", "2c"): ["bcu"],
        ("8c", "3c"): ["the"],
        ("8c", "square"): ["scu", "csq", "sqc"],
        ("8c", "tet"): [ 'flu'],
        ("8c", "hexagon"): [],
        ("8c", "oct"): ["ocu"],
        ("cuo", "2c"): [ "fcu"],
        ("cuo", "3c"): [],
        ("cuo", "square"): ["ftw"], 
        ("cuo", "tet"): ["edc"],
        ("cuo", "hexagon"): [], 
        ("cuo", "oct"): [],     
        ("ico", "2c"): [ ],
        ("ico", "3c"): [],
        ("ico", "square"): [], 
        ("ico", "tet"): ["ith"],
        ("ico", "hexagon"): [], 
        ("ico", "oct"): [],     
        ("hpr", "2c"): [ ],
        ("hpr", "3c"): ["aea"],
        ("hpr", "square"): ["shp"], 
        ("hpr", "tet"): [],
        ("hpr", "hexagon"): [], 
        ("hpr", "oct"): [],        
        ("tte", "2c"): [ ],
        ("tte", "3c"): ["ttt"],
        ("tte", "square"): [], 
        ("tte", "tet"): [],
        ("tte", "hexagon"): ["mgc"], 
        ("tte", "oct"): [],  
        ("24c", "2c"): [ ],
        ("24c", "3c"): [],
        ("24c", "square"): [], 
        ("24c", "tet"): ["twf"],
        ("24c", "hexagon"): [], 
        ("24c", "oct"): [],  
        }
def topology_list(SBU_1, SBU_2):
    
    try:
        sbu_1 = SBU_1.strip('\n')
        connectnum = sbu_1.split('_')[-1]
        sbu_2 = SBU_2.strip('\n')
        connectnum_2 = sbu_2.split('_')[-1] 

        topology_determin = topology_data[connectnum_2, connectnum]  
        return topology_determin
    
    except Exception:
        pass

def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)

def get_c_info(s):
    parts = s.split("_")
    for part in parts:
        if 'o' in part and has_numbers(part) == True:
            mbb = parts[parts.index(part)-1]
    topo = parts[-1]
    obb  = parts[-2]
    return mbb, obb, topo
    
target_dir = 'run/'
mof_total = []
with open('bb_o.txt', 'r') as bb_o_file, open('bb_m.txt', 'r') as bb_m_file:
    bb_o_list = bb_o_file.readlines()
    bb_m_list = bb_m_file.readlines()
    for bbo in bb_o_list:
        for bbm in bb_m_list:   
            topo_list = topology_list(bbo, bbm)
            
            bbo_clean = bbo.strip('\n')
            bbm_clean = bbm.strip('\n')
            
            if topo_list is not None and topo_list != []:
                for topology in topo_list:
                    dirname = f"{bbm_clean}_{bbo_clean}_{topology}"
                    file_name = "build.py"+str(topology )
                    
                    simulation = open("build.py","r")
                    simulation_content = simulation.readlines()
                    simulation_towrite = open(file_name,"w") 
                    
                    for line in simulation_content:   
                        if "SBU_1 = 'replace'" in line:
                            line = line.replace("replace",bbo_clean)
                        if "SBU_2 = 'replace'" in line:
                            line = line.replace("replace",bbm_clean)
                        if "topo = 'replace'" in line:
                            line = line.replace("replace",topology)
                        simulation_towrite.writelines(line)
                    os.system('mkdir '+ dirname)
                    os.system('mv '+file_name+' '+ dirname+'/build.py')
                    os.system('mv '+dirname+'/ '+target_dir)
                    print('create '+dirname)
    