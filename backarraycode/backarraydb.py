import sqlite3,logging

backarray=sqlite3.connect("/home/nest/NEST/nest_python/Db/backarray.db")
cursor=backarray.cursor()
logging.basicConfig(filename='/var/log/nest/servers.log',level=logging.DEBUG)
class StartupChecks:
	
	def backarraycheck():
		
		arraycheck=backarray.execute("select * from backarray")
		for barcode in arraycheck:
			backarray[barcode] = barcode

		return backarray

		
	def backarrayInsert(self,barcode):
                global cursor,backarray	
		arrayinsert=cursor.execute("insert into backarray (barcode) values ('%d')" %barcode)
		backarray.commit()
		if arrayinsert:
			logging.info("sussessfully entered to db")
		
	def backarrayTruncate():
		backarray.execute("truncate backarray")
			
		
