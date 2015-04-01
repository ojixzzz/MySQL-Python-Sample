import falcon
import MySQLdb
import json
from settings import db_host, db_user, db_password, db_name

class TesResource:
	def on_get(self, req, resp):
		try:
			con = MySQLdb.connect(host=db_host, user=db_user,
									passwd=db_password, db=db_name)
			cursor = con.cursor(MySQLdb.cursors.DictCursor)
			
			query = ("SELECT field1,field2 FROM tes")
			cursor.execute(query)
			rows = cursor.fetchall()
			
			output = []
			for row in rows:
				data = {
						"field1": row['field1'],
						"field2": row['field2']
					   }
				output.append(data)
			
			resp.status = falcon.HTTP_200
			resp.body = json.dumps(output, encoding='utf-8')
			cursor.close()
			con.close()
		except Exception as e:
			return json.dumps({'error':str(e)}, encoding='utf-8')
