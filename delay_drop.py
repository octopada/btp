import pcap_parser as cap

def create_newdic(dic):
    send = {}
    guide_send = {}
    recv = {}
    guide_recv = {}
    stemp = {}
    rtemp = {}

    for i in dic.keys():

        for j in range(len(dic[i])):

            item = dic[i][j]
            #sotod =====> source > destination
            sotod = item["source"] +" > "+ item["destination"]
            
            if sotod not in send:
                send[sotod] = []
                guide_send[sotod] = {}
                stemp[sotod] = -1

            if sotod not in recv:
                recv[sotod] = []
                guide_recv[sotod] = {}
                rtemp[sotod] = -1


            if i == item["source"]:
                send[sotod].append({"timestamp":float(item["timestamp"]), "seq_no":item["sequence-no"]})
                stemp[sotod]+=1
                if item["sequence-no"] not in guide_send[sotod]:
                    guide_send[sotod][item["sequence-no"]] = []
                    
                guide_send[sotod][item["sequence-no"]].append(stemp[sotod])

            elif i == item["destination"]:
                recv[sotod].append({"timestamp":float(item["timestamp"]), "seq_no":item["sequence-no"]})
                rtemp[sotod]+=1
                if item["sequence-no"] not in guide_recv[sotod]:
                    guide_recv[sotod][item["sequence-no"]] = []
                    
                guide_recv[sotod][item["sequence-no"]].append(rtemp[sotod])

    # need to sort the drop data as per time stamp
    
    return (send, recv, guide_send, guide_recv)
                

#return format is going to be a list of below
#init_time, source, destination, ("Drop" or "Delay") ,difference_time, sequence number
def calc_delay():
    dic = cap.generate_trace_dict_of_list_of_dicts()
    send = {}
    guide_send = {}
    recv = {}
    guide_recv = {}
    
    (send, recv, guide_send, guide_recv) = create_newdic(dic)
    

    final = []
    record = ""
    for i in send.keys():
        
        #d_it = 0
        if i not in recv:
            for j in send[i]:
                record = [ j["timestamp"], i[:i.find(' >')], i[i.find('>')+2:], "Drop", "-"]
                #get_drop()
                final.append(record)

        else:

            #record  = [ send[i][s_it]["timestamp"], i[:i.find(' >')], i[i.find('>')+2:], "Delay", time_diff]
            #guide_send[i][key]
            for key in guide_send[i].keys():
                s_it = 0
                r_it = 0

                if key in guide_recv[i]:
                    while (s_it < len(guide_send[i][key])) and (r_it < len(guide_recv[i][key])):

                        #print guide_send[i][key][s_it], "  &  ",guide_recv[i][key][r_it], 
                        #print "# ",send[i][guide_send[i][key][s_it]], recv[i][guide_recv[i][key][r_it]], "\n\n"
                        
                        while (s_it < len(guide_send[i][key]) - 1) and (send[i][guide_send[i][key][s_it + 1]]["timestamp"] < recv[i][guide_recv[i][key][r_it]]["timestamp"]):
                            record  = [ send[i][guide_send[i][key][s_it]]["timestamp"], i[:i.find(' >')], i[i.find('>')+2:], "Drop", "-", key]
                            final.append(record)
                            s_it += 1

                        if (send[i][guide_send[i][key][s_it]]["timestamp"] < recv[i][guide_recv[i][key][r_it]]["timestamp"]):
                            diff = recv[i][guide_recv[i][key][r_it]]["timestamp"] - send[i][guide_send[i][key][s_it]]["timestamp"]
                            record  = [ send[i][guide_send[i][key][s_it]]["timestamp"], i[:i.find(' >')], i[i.find('>')+2:], "Delay", diff, key]
                            final.append(record)
                            s_it += 1
                            r_it += 1

                else:
                    while (s_it < len(guide_send[i][key])):
                        record  = [ send[i][guide_send[i][key][s_it]]["timestamp"], i[:i.find(' >')], i[i.find('>')+2:], "Drop", "-", key]
                        final.append(record)
                        s_it += 1
                                        
                
    final = sorted(final)

    #for key in send:
    #print "S ",send[key],"\nR ",recv[key],"\n\n\n"
    
#    for i in final:
#        print i
        
    return final, dic
