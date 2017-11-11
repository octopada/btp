import os

def remove_port_number(address):
#    print('working with address: ' + address)
    l = address.split('.')
    modified_address = l[0]
    for n in range(3):
        modified_address = modified_address + '.' + l[n+1];
    return modified_address

def generate_trace_dict_of_list_of_dicts():

    files = os.listdir(os.getcwd() + '/traces')

    #p2p_pcaps = []
    #csma_pcaps = []
    #wifi_pcaps = []

    pcaps = []

    for filename in files:
        if '.pcap' in filename:
            pcaps.append(filename)
            
#        if 'p2p' in filename:
#            pcaps.append(filename);
#    #        p2p_pcaps.append(filename);
#        if 'csma' in filename:
#            pcaps.append(filename);
#    #        csma_pcaps.append(filename);
#        if 'wifi' in filename:
#            pcaps.append(filename);
#    #        wifi_pcaps.append(filename);
            
    #print(p2p_pcaps)
    #print(csma_pcaps)
    #print(wifi_pcaps)

    tracedata = {}
    node_addresses = {}

    f = open('node_addresses.txt')
    for line in f:
        l = line.split('\n')
        l = l[0].split(':')
        node_addresses[l[0]+'.pcap'] = l[1]

    for pcap in pcaps:
        command = "tcpdump -nn -tt -r traces/" + pcap + " | grep \'IP\' | grep \'seq\'"
        output = os.popen(command).read()
        tracelist = output.split('\n')
        tracelist = tracelist[:-1]
        
        trace_list_of_dicts = []
        
#        skip = True # for first line which is not a record
        for trace in tracelist:
#            if skip:
#                skip = False
#                continue

            trace_dict = {}
            colon_split = trace.split(':')
            space_split = colon_split[0].split()
            comma_split = trace.split(',')
            
        #        print('sending address: ' + space_split[2])
            source = remove_port_number(space_split[2])
            destination = remove_port_number(space_split[4])
            seq_no = comma_split[1].split()[1]
            
            for entry in comma_split:
                if 'length' in entry:
                    length = entry.split()[1]
            
            if seq_no == '0':
                continue
            
            trace_dict['timestamp'] = space_split[0];
            trace_dict['source'] = source
            trace_dict['destination'] = destination
            trace_dict['sequence-no'] = seq_no
            trace_dict['length'] = length

            trace_list_of_dicts.append(trace_dict)
            
        tracedata[node_addresses[pcap]] = trace_list_of_dicts
        
    return tracedata
