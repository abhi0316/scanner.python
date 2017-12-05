"code for local sqlite  operations"

import sqlite3,logging
logging.basicConfig(filename='/var/log/nest/db.log',level=logging.DEBUG)
errodb = sqlite3.connect('/home/nest/NEST/nest_python/Db/error.db')
configdb=sqlite3.connect('/home/nest/NEST/nest_python/Db/config.db')
backarray=sqlite3.connect('/home/nest/NEST/nest_python/Db/backarray.db')
class SqLiteOperations:

	def InsertConfig(self,name,pcb_t,pcb_pn,plen,fdata,dlen):
		configdb.execute("INSERT INTO config (name,pcbtotal,pcbperpannel,prefixlength,firstdata,datalength) values \
					('%s' ,'%d' ,'%d','%d','%d','%d') " % ( name ,int(pcb_t),int(pcb_pn),int(plen),int(fdata),int(dlen)))
		configdb.commit()
		logging.info("config db write complete ...")
	
	def InsertError(errorarray):
		for i in errorarray:
			errordb.execute("INSERT INTO errordb (barcode) value ('%s')" % (errorarray[i]))
			errordb.commit()
			logging.info("error db updated....")
	

