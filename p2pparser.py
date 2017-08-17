def p2p_list_of_dict():
  rawdata = open("p2p.tr", "r");

  index = 0
  tracedata = []

  for line in rawdata:
    line = line.replace(')', '(')
    tokens = line.split('(')
    
    moretokens = tokens[0]
    moretokensList = moretokens.split()

    tracedata.append({})
    tracedata[index]['tracetype'] = moretokensList[0];
    tracedata[index]['time'] = moretokensList[1];
    tracedata[index]['link_layer_header'] = moretokensList[3];
    
    nodedata = moretokensList[2]
    tempList = nodedata.split('/')
    nodeNo = tempList[2]
    
    tracedata[index]['node_number'] = nodeNo;
    
    networkheader = tokens[4]
    
    tracedata[index]['network_layer_header'] = networkheader
      
    networkheaderFlags = tokens[7]
    networkheaderList = networkheaderFlags.split()
    
    tracedata[index]['ipv4_length'] = networkheaderList[4]
    tracedata[index]['network_layer_source'] = networkheaderList[5]
    tracedata[index]['network_layer_destination'] = networkheaderList[7]
    
    transportheader = tokens[8]
    transportheaderFlags = tokens[9]
    transportheaderList = transportheaderFlags.split()
    
    tracedata[index]['transport_layer_header'] = transportheader
    tracedata[index]['source_port'] = transportheaderList[0]
    tracedata[index]['destination_port'] = transportheaderList[2]
    
    payloadFlags = tokens[14]
    payloadList = payloadFlags.split()
    
    try:
      if payloadList[0] == 'Payload':
        tracedata[index]['data_payload'] = 'yes'
        
      else:
        tracedata[index]['data_payload'] = 'no'
    
    except IndexError:
      tracedata[index]['data_payload'] = 'no'

    index = index+1
  return tracedata
