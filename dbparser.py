from delay_drop import calc_delay 
	
def init(fout,raw):
	fout.write("CREATE TABLE pcap(id integer,timestamp float,source VARCHAR(100),destination VARCHAR(100),status VARCHAR(100),difference_time float,sequence_number VARCHAR(100),packet_length integer);\n")
#	fout.write("CREATE TABLE pcap(id integer,timestamp float,source VARCHAR(100),destination VARCHAR(100),status VARCHAR(100),difference_time float,sequence_number VARCHAR(100));\n")
	i = 0
	for line in raw:
		fout.write("INSERT INTO pcap(id,timestamp,source,destination,status,difference_time,sequence_number,packet_length) VALUES (%d," %i)
#		fout.write("INSERT INTO pcap(id,timestamp,source,destination,status,difference_time,sequence_number) VALUES (%d," %i)
		fout.write("%.5f," %line[0]) 
		fout.write("'%s'," %line[1])
		fout.write("'%s'," %line[2])
		fout.write("'%s'," %line[3])
		if line[4] == '-':
			fout.write("NULL,")
		else:
			fout.write("%.5f," %line[4])
		fout.write("'%s'," %line[5])
		if line[6] == '-':
			fout.write("NULL);\n")
		else:
			fout.write("%d);\n" %int(line[6]))
		i = i + 1
		
def init2(fout,raw2):
	count = 0
	fout.write("CREATE TABLE pcap_all(id integer,traced_at VARCHAR(100),timestamp float,source VARCHAR(100),destination VARCHAR(100),sequence_number VARCHAR(100),packet_length VARCHAR(100));\n")
	for packet in raw2:
		for line in raw2[packet]:
			fout.write("INSERT INTO pcap_all(id,traced_at,timestamp,source,destination,sequence_number,packet_length) VALUES (%d," %count)
			fout.write("'%s'," %packet)
			fout.write("%.5f," %float(line['timestamp'])) 
			fout.write("'%s'," %line['source'])
			fout.write("'%s'," %line['destination'])
			fout.write("'%s'," %line['sequence-no'])
			fout.write("'%s');\n" %line['length']) 
			count = count + 1
		
def enter_data():
	fout = open('init.sql', 'w')
	raw, raw2 = calc_delay()
	fout.write('DROP DATABASE IF EXISTS BTP2;\nCREATE DATABASE BTP2;\nUSE BTP2;\n')
	init(fout,raw)
	init2(fout,raw2)
	fout.close()
	return raw, raw2

#enter_data()

