def wifi_list_of_dict():
  rawdata = open("wifi.tr", "r");

  index = 0
  tracedata = []

  for line in rawdata:
    line = line.replace(')', '(')
    tokens = line.split('(')

    moretokens = tokens[0]
    moretokensList = moretokens.split()

    tracedata.append({})
    tracedata[index]['tracetype'] = moretokensList[0]
    tracedata[index]['time'] = moretokensList[1]
    tracedata[index]['link_layer_header'] = moretokensList[3]
    
    nodedata = moretokensList[2]
    tempList = nodedata.split('/')
    nodeNo = tempList[2]
    
    tracedata[index]['node_number'] = nodeNo

    linkheaderFlags = tokens[1];
    linkheaderList = linkheaderFlags.split()
    linkheaderType = linkheaderList[0]
    
    if linkheaderType != 'CTL_ACK':
      tempSource = linkheaderList[7]
      tempDestination = linkheaderList[8]
      
      tempList = tempSource.split('=')
      linkheaderSource = tempList[1]
      
      tempList = tempDestination.split('=')
      linkheaderDestination = tempList[1]

      tracedata[index]['link_layer_source'] = linkheaderSource
      tracedata[index]['link_layer_destination'] = linkheaderDestination

    tracedata[index]['link_layer_header_type'] = linkheaderType; 

    if linkheaderType == 'DATA':
      networkheaderType = tokens[4]
      
      tracedata[index]['network_layer_header'] = networkheaderType
      
      if networkheaderType == ' ns3::ArpHeader ':
        arpheaderFlags = tokens[5]
        arpheaderList = arpheaderFlags.split()
        arpheaderType = arpheaderList[0]

        tracedata[index]['arp_header_type'] = arpheaderType
        tracedata[index]['network_layer_source'] = arpheaderList[6]

        if arpheaderType == 'request':
          tracedata[index]['network_layer_destination'] = arpheaderList[9]
        elif arpheaderType == 'reply':
          tracedata[index]['network_layer_destination'] = arpheaderList[12]
            
      elif networkheaderType == ' ns3::Ipv4Header ':
        ipv4headerFlags = tokens[7]
        ipv4headerList = ipv4headerFlags.split()
        
        tracedata[index]['ipv4_length'] = ipv4headerList[4]
        tracedata[index]['network_layer_source'] = ipv4headerList[5]
        tracedata[index]['network_layer_destination'] = ipv4headerList[7]
        
        transportheaderType = tokens[8]
        transportheaderFlags = tokens[9]
        transportheaderList = transportheaderFlags.split()      
        
        tracedata[index]['transport_layer_header'] = transportheaderType
        tracedata[index]['source_port'] = transportheaderList[0]
        tracedata[index]['destination_port'] = transportheaderList[2]
        
        payloadFlags = tokens[14]
        payloadList = payloadFlags.split()
        
        if payloadList[0] == 'Payload':
          tracedata[index]['data_payload'] = 'yes'
          
        else:
          tracedata[index]['data_payload'] = 'no'

    index = index+1
  return tracedata

  #print tracedata

#wifi_list_of_dict()
