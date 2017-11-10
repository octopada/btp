import pcap_parser as cap
import matplotlib.pyplot as plt

def create_newdic(dic):
    send = {}
    guide_send = {}
    recv = {}
    guide_recv = {}
    stemp = {}
    rtemp = {}
    first_sent_time = 10000000000000
    last_recv_time = -1

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
                if float(item["timestamp"]) < first_sent_time:
                    first_sent_time = float(item["timestamp"])
                send[sotod].append({"timestamp":float(item["timestamp"]), "seq_no":item["sequence-no"]})
                stemp[sotod]+=1
                if item["sequence-no"] not in guide_send[sotod]:
                    guide_send[sotod][item["sequence-no"]] = []
                    
                guide_send[sotod][item["sequence-no"]].append(stemp[sotod])

            elif i == item["destination"]:
                if float(item["timestamp"]) > last_recv_time:
                    last_recv_time = float(item["timestamp"])
                recv[sotod].append({"timestamp":float(item["timestamp"]), "seq_no":item["sequence-no"]})
                rtemp[sotod]+=1
                if item["sequence-no"] not in guide_recv[sotod]:
                    guide_recv[sotod][item["sequence-no"]] = []
                    
                guide_recv[sotod][item["sequence-no"]].append(rtemp[sotod])

    # need to sort the drop data as per time stamp
    
    return (send, recv, guide_send, guide_recv, first_sent_time, last_recv_time)


def plot(ls):

    # linear
    plt.subplot(111)
    plt.plot(ls[0], ls[1])
    plt.xscale('linear')
    plt.yscale('linear')
    plt.xlabel(ls[2])
    plt.ylabel(ls[3])
    plt.title('title_here')
    plt.grid(True)
    plt.show()


#return format is going to be a list of below
#init_time, source, destination, ("Drop" or "Delay") ,difference_time, sequence number
def calc_delay():
    dic = cap.generate_trace_dict_of_list_of_dicts()
    
    send = {}
    guide_send = {}
    recv = {}
    guide_recv = {}
    first_sent_time = 10000000000000
    last_recv_time = -1
    
    (send, recv, guide_send, guide_recv, first_sent_time, last_recv_time) = create_newdic(dic)

    len_of_packet = 20
    thruput = 0
    count_success = 0
    total_time_sent = 0
    
    avg_end_to_end = 0
    
    jitter = 0
    temp_jitter_diff = -1
    #[[xValues], [yVales], "xName", "yName"]
    arr1 = [[], [], "no. of packets", "Jitter"]

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
                            
                            count_success += 1
                            thruput += len_of_packet*8
                            avg_end_to_end += diff
                            
                            if temp_jitter_diff != -1:
                                jitter += abs(diff - temp_jitter_diff)
                                arr1[0].append(count_success)
                                arr1[1].append(jitter)
                                
                            temp_jitter_diff = diff
                            
                            s_it += 1
                            r_it += 1

                else:
                    while (s_it < len(guide_send[i][key])):
                        record  = [ send[i][guide_send[i][key][s_it]]["timestamp"], i[:i.find(' >')], i[i.find('>')+2:], "Drop", "-", key]
                        final.append(record)
                        s_it += 1
                                        
                
    final = sorted(final)

    avg_end_to_end /= count_success
    jitter /= count_success
    thruput/=(last_recv_time - first_sent_time)

    #for key in send:
    #print "S ",send[key],"\nR ",recv[key],"\n\n\n"
    
    #for i in final:
        #print i

    plot(arr1)
    return final, dic


calc_delay()
