import os

command = "rm *.tr; rm init.sql"
os.system(command);

ns3_dir = raw_input("Enter NS-3 directory-> ");
sim_file = raw_input("Enter simulator filename (without extension)-> ");

command = "cd " + str(ns3_dir) + "; ./waf --run scratch/" + str(sim_file)
os.system(command);

command = "mv " + str(ns3_dir) + "/*.tr .";
os.system(command);

command = "python dbparser.py"
os.system(command);

command = "mysql -u root -p < init.sql";
os.system(command);
