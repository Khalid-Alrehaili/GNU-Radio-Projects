# this module will be imported in the into your flowgraph
point1 = 0

def detect(probe_lvl):
    global point1
    if probe_lvl > point1:
        point1 = probe_lvl
        return 1
    elif probe_lvl < point1:
        point1 = probe_lvl
        return -1
    else:
        return 0
        
    
    
