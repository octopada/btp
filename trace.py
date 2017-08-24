# main
import os

import MySQLdb

from camp_xc import calc_delay


print "Cleaning files..."
command = "rm *.tr; rm init.sql; rm *.xml"
os.system(command);

ns3_dir = raw_input("Enter NS-3 directory-> ");
sim_file = raw_input("Enter simulator filename (without extension)-> ");

print "Running simulation..."
command = "cd " + str(ns3_dir) + "; ./waf --run scratch/" + str(sim_file)
os.system(command);

print "Getting traces and animation..."
command = "mv " + str(ns3_dir) + "/*.tr .";
os.system(command);
command = "mv " + str(ns3_dir) + "/*.xml .";
os.system(command);

print "Parsing traces..."
command = "python dbparser.py"
os.system(command);

password = raw_input("Enter mysql password: ");
print "Creating tables..."
command = "mysql -u root -p'" + password + "' < init.sql";
os.system(command);

print "Connecting to database..."
username = "root"
db = MySQLdb.connect("localhost", username, password, "BTP2")

delaydrops, dropped_packets, successful_packets = calc_delay(db)

for record in delaydrops:
    if record[3] == 'porD':
        record[3] = 'Dropped packet'
    elif record[3] == 'Delay':
        record[3] = 'Succesful packet'

while(True):
    print "\n\nMenu:\n1. Show all packets\n2. Enter source and destination\n3. Show stats\n4. Netanim\n5. Quit"
    choice = raw_input("Enter choice-> ");
    print "\n"

    if choice == '1':
        print "TIMESTAMP  SOURCE     DESTINATION     OUTCOME           DELAY"
        for record in delaydrops:
            print record
            
    elif choice == '2':
        source = raw_input("Enter source IP: ");
        destination = raw_input("Enter destination IP: ");
        print "TIMESTAMP  SOURCE     DESTINATION     OUTCOME           DELAY"
        for record in delaydrops:
            if record[1] == source and record[2] == destination:
                print record
                
    elif choice == '3':
        print "No. of successful packets: " + str(successful_packets)
        print "No. of dropped packets: " + str(dropped_packets)
        
    elif choice == '4':
        netanim_dir = raw_input("Enter NetAnim directory -> ");
        command = netanim_dir + "/NetAnim";
        os.system(command);
    
    elif choice == '5':
        break
        
    else:
        pass
        

