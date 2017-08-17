
Aim: To learn network simulation, and create a way to interpret the trace files
produced in an efficient way to ease the study of existing network (such as pinpointing
the locations of problems/drops produced if any)

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
