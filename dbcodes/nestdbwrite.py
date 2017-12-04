
import MySQLdb as db

conninit=db.connect(host="localhost" ,port=3306,user='root',passwd='Resnova123!',db='NEST')

cursor=conninit.cursor()

class NestDbInsert:
	def __init__(self,id,barcode):
		sqlquery='insert into barcode_status(id,barcodes) values ("%d","%s")' %(id,barcode)
		try:
	
			cursor.execute(sqlquery)
			conninit.commit()
		except:
			print "error_db"

