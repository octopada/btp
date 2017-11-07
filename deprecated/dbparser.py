from wifiparser import wifi_list_of_dict
from csmaparser import csma_list_of_dict
from p2pparser import p2p_list_of_dict

fields = []
ll_headers = []
nl_headers = []
tables = []
table_count = []


fout = open('init.sql', 'w')

def compare(data,base):

	name = base

        if base=="CSMA":
                nl_header = data['network_layer_header']

        ll_header = ''
        if base=="WIFI":
                ll_header = data['link_layer_header_type']
                if ll_header == 'DATA':
                        nl_header = data['network_layer_header']
                else:
                        nl_header = ' '

                if ll_header == 'MGT_BEACON' or ll_header == 'MGT_ASSOCIATION_REQUEST' or ll_header == 'MGT_ASSOCIATION_RESPONSE':
                        name += '_MGT'

                if ll_header == 'CTL_ACK':
                        name += '_CTL_ACK'

        if (ll_header == 'DATA' and base=="WIFI") or base=="CSMA":
                if nl_header == ' ns3::ArpHeader ':
                        name += '_DATA_ArpHeader '
                if nl_header == ' ns3::Ipv4Header ':
                        name += '_DATA_Ipv4Header '
        if base=="P2P":
                name += '_DATA_Ipv4Header '
                                

	flag = 0
        
	for i in range(len(tables)):
		if  tables[i] == name:
			populate_table(data,name)
			table_count[i] = table_count[i] + 1
			flag = 1

	if flag == 0:
                create_table(data.keys(),name)
		table_count.append(0)
		tables.append(name)

#	flag = 0
#	for i in range(len(ll_headers)):
#		if  ll_headers[i] == ll_header and nl_headers[i] == nl_header:
#			populate_table(data,ll_header+nl_header)
#			flag = 1
#
#	if flag == 0:
#		create_table(data.keys(),ll_header+nl_header)
#		ll_headers.append(ll_header)
#		nl_headers.append(nl_header)

#	fout.write("%s " % len(data))
#	fout.write(" %s " % ll_header+nl_header)

#def create_database(base):
#	fout.write('DROP DATABASE IF EXISTS BTP2;\nCREATE DATABASE BTP2;\nUSE BTP2;\n')

def create_table(fields,name):
	fout.write("CREATE TABLE %s(id integer," % name)
	for i in range(len(fields)):
		fout.write("%s VARCHAR(100)," % fields[i])
	fout.write("PRIMARY KEY(id) );\n")

def populate_table(data,name):
	i = 0
	fout.write("INSERT INTO %s(id," % name)
	for key in data :
		if i == len(data)-1:
			fout.write("%s ) " % key )
		else:
			fout.write("%s ," % key)
		i = i + 1
	i = 0
	tcount = 0
	for j in range(len(tables)):
		if tables[j] == name:
			tcount = table_count[j]

	fout.write("VALUES(%s," % tcount )
	for key, entry in data.iteritems():
		if i == len(data)-1:
			fout.write("'%s' );\n" % entry )
		else:
			fout.write("'%s' ," % entry)
		i = i + 1


def for_each(base, arw):
        global tables
        global table_count
        tables = []
        table_count = []       
        for line in arw:
                fields = line.keys()
                compare(line, base)
                
raw =  wifi_list_of_dict()
raw_csma=csma_list_of_dict()
raw_p2p=p2p_list_of_dict()        

def a2l():
	fout.write('DROP DATABASE IF EXISTS BTP2;\nCREATE DATABASE BTP2;\nUSE BTP2;\n')
        for_each("WIFI",raw)
        for_each("CSMA",raw_csma)
        for_each("P2P",raw_p2p)


a2l()


#	create_table(fields,'kely')
#	populate_table(line,'kely')


#	for item in data:
#		item = item.split(': ')
#		if len(item) == 1:
#			item = ""
#		fout.write("%s\n" % item)
#		temp_fields.append(item[1])
#
#	if not compare(temp_fields,fields):
#		fields = temp_fields
#		fout.write("CHANGING>>>>>>\n")
#	fout.write("%s\n" % line )
fout.close()
