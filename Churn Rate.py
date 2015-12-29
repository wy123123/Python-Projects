import MySQLdb as mdb
import datetime
import pandas as pd
import os
pd.options.mode.chained_assignment = None

#set working directory
os.chdir("c:/users/ChurnRate")

#start churn rate
churn_rate=pd.DataFrame(columns=['Date','starting_customer_base','New_Customers','Churned','end_Customer_base'])
#set average days to be considered inactive
N = 91
print "average days to be considered inactive: " + str(N)

#set baseline date "2014-01-01"
base_line_time = datetime.datetime.strptime('2014-01-01', '%Y-%m-%d')

#find starting time
starting_time = base_line_time - datetime.timedelta(days=N)
print "base line date: "+ str(base_line_time.date())
print "starting date: " + str(starting_time.date())

#set baseline data starting 2014-01-01 and count back N days
print "getting base line customers information between "+str(base_line_time.date())+" and "+str(starting_time.date())
print "baseline data starting 2014-01-01 and count back "+str(N)+" days"
db = mdb.connect('url', 'user', 'password', 'db_name');
c = db.cursor()
c.execute("""SELECT
    ps_orders.id_customer as id_customer,
    count(ps_orders.id_customer) as number_of_orders,
    min(date(ps_orders.invoice_date)) as date_of_first_purchase,
    max(date(ps_orders.invoice_date)) as date_of_recent_purchase,
    date(ps_customer.date_add) as date_registered
FROM
    ps_orders
        left JOIN
    ps_customer ON ps_customer.id_customer = ps_orders.id_customer
WHERE
    ps_customer.active = 1
        and valid =1
        and invoice_date between \'"""+str(starting_time.date())+""" 00:00:00\' and '"""+str(base_line_time.date())+""" 23:59:59'
group by ps_orders.id_customer;
""")
df_base = pd.DataFrame(data=list(c.fetchall()),columns=['id_customer','no_of_orders','1st_purchase',"recent_purchase","date_registered"])


#find average of N days:
N_DAYS = 600
for i in range(N_DAYS):
    print "current customer base: "+str(df_base.shape[0])
    print "connecting to db... ..."
    db = mdb.connect('url', 'user', 'password', 'db_name');
    c = db.cursor()
    print "connected to db... ..."
    FINAL_INFOR = []
    current_date = base_line_time + datetime.timedelta(days=1)
    print "calculating churn rate for date: "+str(current_date.date())
    churn_threshole_date = base_line_time - datetime.timedelta(days=N)
    base_line_time = current_date
    print "churn rate threshole date: "+str(churn_threshole_date.date())

    #find current day sales data
    c.execute("""SELECT ps_orders.id_customer FROM ps_orders left JOIN ps_customer ON ps_customer.id_customer = ps_orders.id_customer WHERE ps_customer.active = 1 and valid =1
    and invoice_date between '"""+str(current_date.date())+""" 00:00:00' and '"""+str(current_date.date())+""" 23:59:59'
group by ps_orders.id_customer;
""")
    query_data = c.fetchall()
    FINAL_INFOR.append(current_date)
    FINAL_INFOR.append(df_base.shape[0])
    #print FINAL_INFOR
    
    #get customers who purchased on that day
    purchased_customers = []
    for i in query_data:
        purchased_customers.append(i[0])
    #print len(purchased_customers)!=len(set(purchased_customers))

    print str(len(purchased_customers)) +" customers made at least one purchase on " + str(current_date.date())
    
    #update recent purchase date
    print "updating recent purchase date... ..."
    for i in df_base['id_customer']:
        if i in purchased_customers:
            df_base["recent_purchase"][df_base['id_customer']==i] = current_date.date()
            #print df_base[df_base["id_customer"]==int(i)]
    #add in new customers
    print "Adding in new customers"
    df_base_added = df_base
    for i in purchased_customers:
        if int(i) not in list(df_base['id_customer']):
            rows_list = []
            dict1 = {}
            columns=['id_customer','no_of_orders','1st_purchase',"recent_purchase","date_registered"]
            l = [i,None,None,current_date.date(),None]
            for s in range(len(l)):
                dict1[columns[s]]=l[s]
            rows_list.append(dict1)
            df = pd.DataFrame(rows_list,columns=columns)  
            df_base_added = df_base_added.append(df)
            #print df_base_added[df_base_added["id_customer"]==int(i)]
            #print "1 customer added: "+str(i)
    FINAL_INFOR.append(df_base_added.shape[0]-df_base.shape[0])
    #print FINAL_INFOR
    #print df_base_added.shape[0]
    
    #find customer's latest date of purchase is the churn_threshole_date
    print "churning inactive customers..."
    FINAL_INFOR.append(df_base_added[df_base_added['recent_purchase'] <= churn_threshole_date.date()].shape[0])
    df_base_churned = df_base_added[df_base_added['recent_purchase'] > churn_threshole_date.date()]
    FINAL_INFOR.append(df_base_churned.shape[0])
    
    print "remaining customers: "+str(df_base_churned.shape[0])
    
    df_base = df_base_churned
    
    rows_list = []
    dict1 = {}
    columns=['Date','starting_customer_base','New_Customers','Churned','end_Customer_base']
    for i in range(len(FINAL_INFOR)):
        dict1[columns[i]]=FINAL_INFOR[i]
    rows_list.append(dict1)
    df = pd.DataFrame(rows_list,columns=columns)  
    churn_rate = churn_rate.append(df) 
    
    print "------------------------------" 
print "###############################"

churn_rate.to_excel("churn_rate.xlsx",sheet_name="report"+str(current_date.date()))
print "Report Created: churn_rate.xlsx"
df_base.to_excel("current_customer_base.xlsx",sheet_name=str(current_date.date()))
