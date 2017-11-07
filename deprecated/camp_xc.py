#!/usr/bin/python

import MySQLdb

def create_dic(choice, db ,table_name):
    #choice="drop_p" or "send" or "recv"

    cursor = db.cursor()

    cursor.execute("SHOW columns FROM "+str(table_name)+";")
    column_name= [column[0] for column in cursor.fetchall()]

    col_trace=column_name.index('tracetype')
    col_dest=column_name.index('network_layer_destination')
    col_source=column_name.index('network_layer_source')
    col_time=column_name.index('time')
    col_node= column_name.index('node_number')
    col_pay=column_name.index('data_payload')
    #col_device= column_name.index('device_no')

    dic={}
    
    if choice =="send":
        delay = "select * from "+str(table_name)+" where tracetype=\"t\";"
        cursor.execute(delay)
        data = cursor.fetchall()
        for atom in data:
            sotodes=str(atom[col_source])+" > "+ str(atom[col_dest])
            #may need to add another condition if need be
            
            if atom[col_trace]=='t' and atom[col_pay]=="yes":
                if sotodes in dic.keys():
                    dic[sotodes].append(atom[col_time])
                else:
                    dic[sotodes] = [atom[col_time] ]

    if choice =="drop_p":
        drop_p = "select * from "+str(table_name)+" where tracetype=\"d\";"
        cursor.execute(drop_p)
        data = cursor.fetchall()
        for atom in data:
            sotodes=str(atom[col_source])+" > "+ str(atom[col_dest])

            if atom[col_trace]=='d' and atom[col_pay]=="yes":
                if sotodes in dic.keys():
                    dic[sotodes].append(atom[col_time])
                else:
                    dic[sotodes] = [atom[col_time] ]

    if choice =="recv":
        delay = "select * from "+str(table_name)+" where tracetype=\"r\";"
        cursor.execute(delay)
        data = cursor.fetchall()
        for atom in data:
            sotodes=str(atom[col_source])+" > "+ str(atom[col_dest])

            if atom[col_trace]=='r' and atom[col_dest].split('.')[-1]==atom[col_node] and atom[col_pay]=="yes":
                if sotodes in dic.keys():
                    dic[sotodes].append(atom[col_time])
                else:
                    dic[sotodes] = [atom[col_time] ]    

    return dic


def calc_delay(db):
    
    send=create_dic("send", db, "WIFI_DATA_Ipv4Header")
    recv=create_dic("recv", db, "CSMA_DATA_Ipv4Header")

    table_name = ["WIFI_DATA_Ipv4Header", "CSMA_DATA_Ipv4Header", "P2P_DATA_Ipv4Header"]
    drop_temp = []

    for i in range(len(table_name)):
        drop_temp.append(create_dic("drop_p", db, table_name[i]))

    db.close()

    drop_p = {}
    for i in send.keys():
        for dic in drop_temp:
            if i in dic:
                if i not in drop_p:
                    drop_p[i] = []
                drop_p[i].extend(dic[i])

        if i in drop_p:
            drop_p[i] = sorted(drop_p[i])

    final=[]

    #print len(send['10.1.3.1 > 10.1.2.4']),len(recv['10.1.3.1 > 10.1.2.4']),len(drop_p['10.1.3.1 > 10.1.2.4'])

#    print "############# Drop = porD ##############\n\n"
    sucks=0
    pot=0

    for i in send.keys():
        while( len(send[i])>0):
            
            if len(drop_p)>0 and (i in drop_p.keys()):
                d=(lambda ls: 0 if len(ls)==0 else ls[0])(drop_p[i])
            if len(recv)>0 and (i in recv.keys()):
                r=(lambda ls: 100 if len(ls)==0 else ls[0])(recv[i])
            
            if (i in drop_p.keys()) and float(send[i][0])<= float(d) and float(d) < float(r):
                
                fin_time=float(drop_p[i][0]) - float(send[i][0])
                final.append( [float(send[i][0]), i[:i.find(' >')],i[i.find('>')+2:] , "porD",fin_time])
                del send[i][0]
                del drop_p[i][0]
                pot=pot+1

            else:
                if len(recv[i])>0 and float(send[i][0])<=float(recv[i][0]):
                    fin_time=float(recv[i][0])-float(send[i][0])
                    final.append( [float(send[i][0]), i[:i.find(' >')],i[i.find('>')+2:],"Delay",fin_time])
                    del send[i][0]
                    del recv[i][0]
                    sucks=sucks+1

                #else:
                #    del recv[i][0]
                #print final, len(send), len(recv), len(drop_p)
                

#    for i in final:
#        print i

#    print "\nDropped packets", pot
#    print "Successful packets", sucks
    return final, pot, sucks

