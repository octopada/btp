from camp_xc import calc_delay

fields = ['source','destination','action','time']

raw = calc_delay()
fout = open('init.sql', 'w')

def compare(data,count):
	populate_table(data,count)

def create_database():
	fout.write('DROP DATABASE IF EXISTS BTP2;\nCREATE DATABASE BTP2;\nUSE BTP2;\n')

def create_table():
	fout.write("CREATE TABLE packets(id integer,")
	for i in range(len(fields)):
		fout.write("%s VARCHAR(100)," % fields[i])
	fout.write("PRIMARY KEY(id) );\n")

def populate_table(data,tcount):
	i = 0
	fout.write("INSERT INTO packets(id,")
	for key in fields :
		if i == len(data)-1:
			fout.write("%s ) " % key )
		else:
			fout.write("%s ," % key)
		i = i + 1
	i = 0

	fout.write("VALUES(%s," % tcount )
	for entry in data:
		if i == len(data)-1:
			fout.write("'%s' );\n" % entry )
		else:
			fout.write("'%s' ," % entry)
		i = i + 1


create_database()
create_table()
count = 0

for line in raw:

	compare(line,count)
	count = count + 1
	
fout.close()
