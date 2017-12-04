"code for local sqlite  operations"

import sqlite3,logging
logging.basicConfig(filename='/var/log/nest/db.log',level=logging.DEBUG)
errodb = sqlite3.connect('../Db/error.db')
configdb=sqlite3.connect('../Db/config.db')
backarray=sqlite3.connect('../Db/backarray.db')
class SqLiteOperations:

	def InsertConfig(name,pcb_t,pcp_pn,plen,fdata,dlen):
		configdb.execute("INSERT INTO config (name,pcbtotal,pcbperpannel,prefixlength,firstdata,datalength) values \
					('%s' ,'%d' ,'%d','%d','%d','%d') " % ( name ,pcb_t,pcb_pn,plen,fdata,dlen))
		configdb.commit()
		logging.info("config db write complete ...")
	
	def InsertError(errorarray):
		for i in errorarray:
			errordb.execute("INSERT INTO errordb (barcode) value ('%s')" % (errorarray[i]))
			errordb.commit()
			logging.info("error db updated....")
	

