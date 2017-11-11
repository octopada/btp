import pcap_parser as cap
import matplotlib.pyplot as plt

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

                send[sotod].append({"timestamp":float(item["timestamp"]), "seq_no":item["sequence-no"], "length":item["length"]})
                stemp[sotod]+=1
                if item["sequence-no"] not in guide_send[sotod]:
                    guide_send[sotod][item["sequence-no"]] = []
                    
                guide_send[sotod][item["sequence-no"]].append(stemp[sotod])

            elif i == item["destination"]:

                recv[sotod].append({"timestamp":float(item["timestamp"]), "seq_no":item["sequence-no"], "length":item["length"]})
                rtemp[sotod]+=1
                if item["sequence-no"] not in guide_recv[sotod]:
                    guide_recv[sotod][item["sequence-no"]] = []
                    
                guide_recv[sotod][item["sequence-no"]].append(rtemp[sotod])

    # need to sort the drop data as per time stamp
    
    return (send, recv, guide_send, guide_recv)


def plot(ls, title):
    plt.subplot(111)
    plt.plot(ls[0], ls[1], marker = "o")
    plt.xscale('linear')
    plt.yscale('linear')
    plt.xlabel(ls[2])
    plt.ylabel(ls[3])
    plt.title(title)
    plt.grid(True)
    plt.show()

def plot_transfer_rate(data, ip_choices):
    title = "packet-transfer-rate vs time"
    len_of_packet = -1
    arr1 = [[], [], "time (in s)", "packet-transfer-rate (in bits/s)"]
    if len(ip_choices) == 0:
        for i in data:
            if i[-4] == "Delay":
                diff = i[-3]
                len_of_packet = i[-1]
                thruput = float(len_of_packet)*8
                thruput /= diff

                arr1[0].append(i[0]+diff)
                arr1[1].append(thruput)

    elif len(ip_choices) == 2:
        for i in data:
            if i[-4] == "Delay" and i[1] == ip_choices[0] and i[2] == ip_choices[1]:
                diff = i[-3]
                len_of_packet = i[-1]
                thruput = float(len_of_packet)*8
                thruput /= diff

                arr1[0].append(i[0]+diff)
                arr1[1].append(thruput)        

    plot(arr1, title)


def plot_multi_e2e(data, ip_choices):

    title = "end-to-end delay vs time (per packet)"
    arr1 = [[], [], "time (in s)", "end-to-end delay (in s)"]
    if len(ip_choices) == 0:
        for i in data:
            if i[-4] == "Delay":
                diff = i[-3]
                arr1[0].append(i[0]+diff)
                arr1[1].append(diff)

    elif len(ip_choices) ==2:
        for i in data:
            if i[-4] == "Delay" and i[1] == ip_choices[0] and i[2] == ip_choices[1]:
                diff = i[-3]
                arr1[0].append(i[0]+diff)
                arr1[1].append(diff)


    plot(arr1, title)


def plot_cumulative_drop(data, ip_choices):
    title = "cumulative drop vs time"
    
    arr1 = [[], [], "time (in s)", "no of packets dropped"]
    count_drop = 0
    if len(ip_choices) == 0:
        for i in data:
            if i[-4] == "Delay":
                diff = i[-3]
                arr1[0].append(i[0]+diff)
                arr1[1].append(count_drop)

            else:
                count_drop += 1
                arr1[0].append(i[0])
                arr1[1].append(count_drop)

    elif len(ip_choices) ==2:
        for i in data:
            if i[-4] == "Delay" and i[1] == ip_choices[0] and i[2] == ip_choices[1]:
                diff = i[-3]
                arr1[0].append(i[0]+diff)
                arr1[1].append(count_drop)

            elif i[1] == ip_choices[0] and i[2] == ip_choices[1]:
                count_drop += 1
                arr1[0].append(i[0])
                arr1[1].append(count_drop)        

    plot(arr1, title)

def plot_jitter(data, ip_choices):
    title = "jitter vs time"
    
    jitter = 0
    temp_jitter_diff = -1
    #[[xValues], [yVales], "xName", "yName"]
    arr1 = [[], [], "time (in s)", "jitter (in s)"]

    if len(ip_choices) ==0:
        for i in data:
            if i[-4] == "Delay":
                diff = i[-3]
                if temp_jitter_diff != -1:
                    jitter = diff - temp_jitter_diff
                    arr1[0].append(i[0]+diff)
                    arr1[1].append(jitter)
                                
                temp_jitter_diff = diff

    elif len(ip_choices) ==2:
        for i in data:
            if i[-4] == "Delay" and i[1] == ip_choices[0] and i[2] == ip_choices[1]:
                diff = i[-3]
                if temp_jitter_diff != -1:
                    jitter = diff - temp_jitter_diff
                    arr1[0].append(i[0]+diff)
                    arr1[1].append(jitter)
                                
                temp_jitter_diff = diff
        

    plot(arr1, title)
    
def get_stats(data):

    first_time = 10000000000000
    last_time = -1

    len_of_packet = -1
    thruput = 0
    count_success = 0
    total_time_sent = 0
    
    avg_end_to_end = 0
    avg_jitter = 0
    
    temp_jitter_diff = -1
    
    for i in data:
        if i[0] < first_time:
            first_time = float(i[0])

        if i[-4] == "Delay" and i[-3] + i[0] > last_time:
            last_time = float(i[-3] + i[0])
        if i[-4] == "Drop" and i[0] > last_time:
            last_time = float(i[0])

        if i[-4] == "Delay":
            diff = i[-3]
            len_of_packet = i[-1]
            count_success += 1
            thruput = thruput + float(len_of_packet)*8
            avg_end_to_end += diff
                                
            if temp_jitter_diff != -1:
                avg_jitter += abs(diff - temp_jitter_diff)
                                
            temp_jitter_diff = diff


    avg_end_to_end /= count_success
    avg_jitter /= count_success
    thruput/=(last_time - first_time)
    
    print("\navg-end-to-end delay =", avg_end_to_end)
    print("avg-jitter =", avg_jitter)
    print("throughput =", thruput)
    print("no. of successful packets =",count_success)
    print("no. of dropped packets =",len(data) - count_success,"\n")
    


#return format is going to be a list of below
#init_time, source, destination, ("Drop" or "Delay") ,difference_time, sequence number, length
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
                record = [ j["timestamp"], i[:i.find(' >')], i[i.find('>')+2:], "Drop", "-", j["seq_no"], "-"]
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
                            record  = [ send[i][guide_send[i][key][s_it]]["timestamp"], i[:i.find(' >')], i[i.find('>')+2:], "Drop", "-", key, "-"]
                            final.append(record)
                            s_it += 1

                        if (send[i][guide_send[i][key][s_it]]["timestamp"] < recv[i][guide_recv[i][key][r_it]]["timestamp"]):
                            diff = recv[i][guide_recv[i][key][r_it]]["timestamp"] - send[i][guide_send[i][key][s_it]]["timestamp"]
                            record  = [ send[i][guide_send[i][key][s_it]]["timestamp"], i[:i.find(' >')], i[i.find('>')+2:], "Delay", diff, key, send[i][guide_send[i][key][s_it]]["length"]]
                            final.append(record)
                                                        
                            s_it += 1
                            r_it += 1

                else:
                    while (s_it < len(guide_send[i][key])):
                        record  = [ send[i][guide_send[i][key][s_it]]["timestamp"], i[:i.find(' >')], i[i.find('>')+2:], "Drop", "-", key, "-"]
                        final.append(record)
                        s_it += 1
                                        
                
    final = sorted(final)
   
    #for i in final:
        #print i

    #can call below plot functions with [] as parameter 2 if want a general answer
    #plot_multi_e2e(final,["10.1.3.1","10.1.2.4"])   
    #plot_transfer_rate(final,["10.1.3.1","10.1.2.4"])    
    #plot_jitter(final,["10.1.3.1","10.1.2.4"])
    #plot_cumulative_drop(final,["10.1.3.1","10.1.2.4"])
    #get_stats(final)
    
    return final, dic


#calc_delay()
