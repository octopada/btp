import os

files = os.listdir(os.getcwd())

#p2p_pcaps = []
#csma_pcaps = []
#wifi_pcaps = []

pcaps = []

for filename in files:
    if 'p2p' in filename:
        pcaps.append(filename);
#        p2p_pcaps.append(filename);
    if 'csma' in filename:
        pcaps.append(filename);
#        csma_pcaps.append(filename);
    if 'wifi' in filename:
        pcaps.append(filename);
#        wifi_pcaps.append(filename);
        
#print(p2p_pcaps)
#print(csma_pcaps)
#print(wifi_pcaps)


