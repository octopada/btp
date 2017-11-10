
Aim: To learn network simulation, and create a way to interpret the trace files
produced in an efficient way to ease the study of existing network

Network.cc is used to create the network we are working with in ns3.
This network consists of CSMA and WiFi networks connected by a point-to-point link.
Network.cc can be run (with ns3 installed) using the command

-waf --run ./scratch/network

This produces ascii trace files csma.tr, wifi.tr and p2p.tr
Which is parsed and processed to make the relevant information
easily understandable  and queryable using mysql 

******** Next few steps:  *******

   1) Run dbparser.py (generates init.sql)
   2) mysql -u root -p < init.sql
   3) Change username and pass in camp_xc.py file and run it.
   4) Run tableparser.py (generates init.sql)
   5) mysql -u root -p < init.sql
   6) Query the table "packets" in database "BTP2" as required
   7) Example: run final_table.py

******* Details of Parsing and processing: ********

dbparser.py imports three different parsing functions for each trace file
and generates init.sql file.
This file is fed into the mysql database.
Username and password for mysql should be correctly specified in camp_xc.py file.
The camp_xc.py sorts and orders out the relevant information and calculates 
the delay for all data packet transfers happening from wifi to csma in network; 
output of which is used by final_table.py.

Run final_table.py. 
This will display a list of [ip_source, ip_destination, "Delay"/"Drop", Delay if any] 
and further produce an init.sql, this relevant information is fed into database system
for the final queryable result.

** NETANIM **

The netanim.xml file can be opened in Network Animator to visualise the network.
--------------------------------------------------------------------------------
NS3 Directory: /home/gogol/Documents/threetwo/btp/ns3/ns-allinone-3.26/ns-3.26

problem: csma each node except one connected to p2p link traces only packets 
sent/received to/by it. wifi all nodes trace all packets, but times are diff.
in a general network how to know, in case of wifi, or ethernet p2p link nodes,
which packets are sent/received to/by it? cannot get address from trace.

solution: create a node-device to ip address list separately and feed it to the trace
program. |format| <network type>-<node number>-<device number>:<ip address>
        |example| p2p-0-0:10.1.1.1
put this list in a file called node_addresses.txt. pcap_parser will pick it up.
