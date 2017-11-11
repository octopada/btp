# main
import os

import delay_drop
from dbparser import enter_data

# /home/gogol/Documents/threetwo/btp/ns3/ns-allinone-3.26/ns-3.26
# /home/gogol/Documents/threetwo/btp/ns3/ns-allinone-3.26/netanim-3.107

#import MySQLdb

#from camp_xc import calc_delay

print("Cleaning files...")
command = "rm init.sql; rm -r *.xml; rm -r *.pcap"
os.system(command);

ns3_dir = input("Enter NS-3 directory-> ");
sim_file = input("Enter simulator filename (without extension)-> ");

print("Running simulation...")
command = "cd " + str(ns3_dir) + "; ./waf --run scratch/" + str(sim_file)
os.system(command);

#os.system("ls");

print("Getting pcap traces and animation...")
command = "mv " + str(ns3_dir) + "/*.pcap ./traces";
os.system(command);
command = "mv " + str(ns3_dir) + "/*.xml ./traces";
os.system(command);

print("Parsing pcap traces into database...")
raw, raw2 = enter_data()
#command = "python dbparser.py"
#os.system(command)

password = input("Enter mysql password: ");
print("Creating tables...")
command = "mysql -u root -p'" + password + "' < init.sql";
os.system(command);

while True:
    print("\nMenu:\n1. Show stats\n2. Graphs\n3. Netanim\n4. Quit")
    choice = input("Enter choice-> ");
    
    if choice == '1':
        delay_drop.get_stats(raw)
    elif choice == '2':
        print("\nGraph Menu:\n1. General graphs\n2. Specific src-dest pairs\n3. Back")
        choice = input("Enter choice-> ");
            
        if choice == '1':
            print("\nGeneral Graphs:\n1. end-to-end delay\n2. transfer rate\n3. jitter\n4. dropped packets\n5. Back")
            choice = input("Enter choice-> ");
            
            if choice == '1':
                delay_drop.plot_multi_e2e(raw, [])
                continue
            elif choice == '2':
                delay_drop.plot_transfer_rate(raw, [])
                continue
            elif choice == '3':
                delay_drop.plot_jitter(raw, [])
                continue
            elif choice == '4':
                delay_drop.plot_cumulative_drop(raw, [])
                continue
            else:
                pass
        elif choice == '2':
            src = input("Enter source IP-> ");
            dest = input("Enter destination IP-> ");
            print("\nSpecific Graphs:\n1. end-to-end delay\n2. transfer rate\n3. jitter\n4. dropped packets\n5. Back")
            choice = input("Enter choice-> ");
            
            if choice == '1':
                delay_drop.plot_multi_e2e(raw, [src, dest])
                continue
            elif choice == '2':
                delay_drop.plot_transfer_rate(raw, [src, dest])
                continue
            elif choice == '3':
                delay_drop.plot_jitter(raw, [src, dest])
                continue
            elif choice == '4':
                delay_drop.plot_cumulative_drop(raw, [src, dest])
                continue
            else:
                pass
        elif choice == '3':
            continue
        else:
            pass
    elif choice == '3':
        netanim_dir = input("Enter NetAnim directory -> ");
        command = netanim_dir + "/NetAnim";
        os.system(command);
    elif choice == '4':
        break
    else:
        pass

#    delay_drop.plot_multi_e2e(raw, [])
#    delay_drop.plot_transfer_rate(raw, [])
#    delay_drop.plot_jitter(raw, [])
#    delay_drop.plot_cumulative_drop(raw, [])
#    delay_drop.get_stats(raw)

#print "Connecting to database..."
#username = "root"
#password = "ilikeshinydratini"
#db = MySQLdb.connect("localhost", username, password, "BTP2")

#delaydrops, dropped_packets, successful_packets = calc_delay(db)

#for record in delaydrops:
#    if record[3] == 'porD':
#        record[3] = 'Dropped packet'
#    elif record[3] == 'Delay':
#        record[3] = 'Succesful packet'

#while(True):
#    print "\n\nMenu:\n1. Show all packets\n2. Enter source and destination\n3. Show stats\n4. Netanim\n5. Quit"
#    choice = raw_input("Enter choice-> ");
#    print "\n"

#    if choice == '1':
#        print "TIMESTAMP  SOURCE     DESTINATION     OUTCOME           DELAY"
#        for record in delaydrops:
#            print record
#            
#    elif choice == '2':
#        source = raw_input("Enter source IP: ");
#        destination = raw_input("Enter destination IP: ");
#        print "TIMESTAMP  SOURCE     DESTINATION     OUTCOME           DELAY"
#        for record in delaydrops:
#            if record[1] == source and record[2] == destination:
#                print record
#                
#    elif choice == '3':
#        print "No. of successful packets: " + str(successful_packets)
#        print "No. of dropped packets: " + str(dropped_packets)
#        
#    elif choice == '4':
#        netanim_dir = raw_input("Enter NetAnim directory -> ");
#        command = netanim_dir + "/NetAnim";
#        os.system(command);
#    
#    elif choice == '5':
#        break
#        
#    else:
#        pass
#        

