def csma_list_of_dict():
  rawdata = open("csma.tr", "r");

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
    
    linkheaderFlags = tokens[1];
    linkheaderList = linkheaderFlags.split()
    
    tempSource = linkheaderList[1]
    tempList = tempSource.split('=')
    linkheaderSource = tempList[1]
    
    tempDestination = linkheaderList[2]
    tempList = tempDestination.split('=')
    linkheaderDestination = tempList[1]
    
    tracedata[index]['link_layer_source'] = linkheaderSource
    tracedata[index]['link_layer_destination'] = linkheaderSource
    
    networkheader = tokens[2]
    
    tracedata[index]['network_layer_header'] = networkheader
    
    if networkheader == ' ns3::ArpHeader ':

      networkheaderFlags = tokens[3]
      networkheaderList = networkheaderFlags.split()
      networkheaderType = networkheaderList[0]
      
      if networkheaderType == 'request':
        networkheaderSource = networkheaderList[6]
        networkheaderDestination = networkheaderList[9]

      elif networkheaderType == 'reply':
        networkheaderSource = networkheaderList[6]
        networkheaderDestination = networkheaderList[12]
        
      tracedata[index]['arp_header_type'] = networkheaderType
      tracedata[index]['network_layer_source'] = networkheaderSource
      tracedata[index]['network_layer_destination'] = networkheaderDestination
      
    elif networkheader == ' ns3::Ipv4Header ':
      networkheaderFlags = tokens[5]
      networkheaderList = networkheaderFlags.split()
      
      tracedata[index]['ipv4_length'] = networkheaderList[4]
      tracedata[index]['network_layer_source'] = networkheaderList[5]
      tracedata[index]['network_layer_destination'] = networkheaderList[7]
      
      transportheader = tokens[6]
      transportheaderFlags = tokens[7]
      transportheaderList = transportheaderFlags.split()
      
      tracedata[index]['transport_layer_header'] = transportheader
      tracedata[index]['source_port'] = transportheaderList[0]
      tracedata[index]['destination_port'] = transportheaderList[2]
      
      payloadFlags = tokens[12]
      payloadList = payloadFlags.split()
      
      if payloadList[0] == 'Payload':
        tracedata[index]['data_payload'] = 'yes'
        
      else:
        tracedata[index]['data_payload'] = 'no'

    index = index+1
  return tracedata
  #print tracedata


#csma_list_of_dict()
