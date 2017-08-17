import MySQLdb

username="root"
password="kadebore"
database="BTP2"
# change database P2P
print '\n'
db = MySQLdb.connect("localhost",username,password,database)
cursor = db.cursor()

delay = "select * from packets where action=\"Delay\" order by time;"
cursor.execute(delay)
data = cursor.fetchall()
print ["source ip", "dest ip", "Delay/Drop", "Delay time"]
for atom in data:
    ls=list(atom)
    del ls[0]
    print str(ls)
	
print '\n'

delay = "select * from packets where action=\"porD\" order by time;"
cursor.execute(delay)
data = cursor.fetchall()
print ["source ip", "dest ip", "Delay/Drop", "Delay time"]
for atom in data:
    ls=list(atom)
    del ls[0]
    print str(ls)
db.close()
