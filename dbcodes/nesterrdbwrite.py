
import MySQLdb as db

conninit=db.connect(host="localhost" ,port=3306,user='root',passwd='Resnova123!',db='NEST_STATION_1')

cursor=conninit.cursor()
count =0
class NestDbQuery:
	def __init__(self):
		global count
		count=count+1
		sqlquery=' select * from barcode_status where barcodes="ERROR\R\N"'
		try:
	
			cursor.execute(sqlquery)
			val=cursor.fetchall()
			try:
				
			    errordbwrite='insert into error_status (id,totalerror) values ("%d","%s")' %(count,str(len(val)))
			    cursor.execute(errordbwrite)
			except:
				pass 

			conninit.commit()
		except:
			print "no error to write"

